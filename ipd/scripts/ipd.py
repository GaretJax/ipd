from __future__ import absolute_import
import argparse
import signal

from ipd import logging

from twisted.internet import reactor, defer
from structlog import get_logger

logger = get_logger()


def setup_async():
    """
    Sets up a signal handler which catches the KeyboardInterrupt raised by the
    signal handler installed by async.

    Must be called after the reactor is started.
    """
    import async
    async  # Silence pyflakes

    prev = signal.getsignal(signal.SIGINT)

    def catch_exc(signum, frame):
        if callable(prev):
            try:
                prev(signum, frame)
            except KeyboardInterrupt:
                pass

    signal.signal(signal.SIGINT, catch_exc)


def get_parser():
    parser = argparse.ArgumentParser()
    return parser


def main():
    #parser = get_parser()
    #args = parser.parse_args()

    logging.setup_logging()

    reactor.callWhenRunning(setup_async)
    reactor.callWhenRunning(_create_domain)
    reactor.run()

    #project = Project(
    #    repository=repository.GitRepository(),
    #    workdir='',
    #    base_image=Image(),
    #)



@defer.inlineCallbacks
def _redis():
    from twisted.internet import reactor
    from twisted.internet import protocol
    from txredis.client import RedisClient

    HOST = 'localhost'
    PORT = 6379

    clientCreator = protocol.ClientCreator(reactor, RedisClient)
    redis = yield clientCreator.connectTCP(HOST, PORT)

    res = yield redis.ping()
    print res

    info = yield redis.info()
    print info

    res = yield redis.set('test', 42)
    print res

    test = yield redis.get('test')
    print repr(test)

    reactor.stop()


from twisted.conch.ssh.keys import Key

IPD_MANAGER_KEY = Key.fromFile('workdir/ipd-test-key.rsa')


def _jsonserver():
    from twisted.web import server, resource
    from twisted.internet import endpoints
    from twisted.application import service, internet, app
    from ipd.metadata.resource import DelayedRendererMixin, RecursiveResource
    from twisted.python.reflect import prefixedMethodNames
    import json
    from ipd import projects

    class JSONResource(DelayedRendererMixin, RecursiveResource):
        """
        An example object to be published.
        """

        def finish_write(self, res, request):
            if res:
                request.write(res)
            request.finish()

        def finish_err(self, failure, request):
            request.setResponseCode(500)
            request.write('500: Internal server error')
            request.finish()
            return failure

        def render(self, request):
            d = self._delayed_renderer(request)
            d.addCallback(self.finish_write, request)
            d.addErrback(self.finish_err, request)
            return server.NOT_DONE_YET

        def _delayed_renderer(self, request):
            m = getattr(self, 'handle_' + request.method, None)
            if not m:
                from twisted.web.error import UnsupportedMethod
                allowed = prefixedMethodNames(self.__class__, 'handle_')
                raise UnsupportedMethod(allowed)
            request.setHeader('content-type', 'text/json')
            d = defer.maybeDeferred(m, request)
            d.addCallback(lambda r: json.dumps(r) if r is not None else None)
            return d

    class ProjectsListResource(JSONResource):
        def __init__(self, manager):
            super(ProjectsListResource, self).__init__()
            self.manager = manager

        def getChild(self, name, request):
            if name == '':
                return self
            else:
                return ProjectResource(name, self.manager)

        def handle_GET(self, request):
            d = self.manager.get_projects()
            d.addCallback(list)
            return d

    class ProjectResource(JSONResource):
        def __init__(self, key, manager):
            super(ProjectResource, self).__init__()
            self.key = key
            self.manager = manager

        @defer.inlineCallbacks
        def handle_GET(self, request):
            try:
                prj = yield self.manager.get_project(self.key)
            except projects.ProjectNotFound:
                request.setResponseCode(404)
                defer.returnValue({
                    'error': 'project-does-not-exist',
                    'key': self.key,
                })
            else:
                defer.returnValue(prj)

        @defer.inlineCallbacks
        def handle_PUT(self, request):
            repo = request.args['repo'][0]
            try:
                yield self.manager.register_project(self.key, repo)
            except projects.ProjectAlreadyExists:
                request.setResponseCode(403)
                defer.returnValue({
                    'error': 'project-already-exists',
                    'key': self.key,
                })

        @defer.inlineCallbacks
        def handle_DELETE(self, request):
            yield self.manager.unregister_project(self.key)


    class BuildsListResource(JSONResource):
        def __init__(self,  builder):
            super(BuildsListResource, self).__init__()
            self.builder = builder

        def getChild(self, name, request):
            if name == '':
                return self
            else:
                return BuildResource(name, self.builder)

        def handle_GET(self, request):
            d = self.builder.get_builds()
            d.addCallback(list)
            return d

        @defer.inlineCallbacks
        def handle_POST(self, request):
            project_key = request.args['project_key'][0]
            commit_id = request.args['commit_id'][0]

            try:
                build_id = yield self.builder.schedule_build(project_key,
                                                             commit_id)
            except projects.BuildspecNotFound:
                request.setResponseCode(403)
                defer.returnValue({
                    'error': 'buildspec-not-found',
                    'project_key': project_key,
                    'commit_id': commit_id,
                })
            else:
                defer.returnValue(build_id)


    class BuildResource(JSONResource):
        def __init__(self, id, builder):
            super(BuildResource, self).__init__()
            self.id = id
            self.builder = builder

        @defer.inlineCallbacks
        def handle_PUT(self, request):
            project_key, commit_id = self.id.split(':')
            try:
                yield self.manager.register_project(self.key, repo)
            except projects.BuildAlreadyExists:
                request.setResponseCode(403)
                defer.returnValue({
                    'error': 'project-already-exists',
                    'key': self.key,
                })

        @defer.inlineCallbacks
        def handle_DELETE(self, request):
            yield self.manager.unregister_project(self.key)




    from twisted.internet import reactor
    from twisted.python.filepath import FilePath
    import functools
    from txredis.client import RedisClient
    from ipd.libvirt.endpoints import TCP4LibvirtEndpoint
    from ipd.utils import ProtocolConnector

    # Configuration
    libvirt = functools.partial(TCP4LibvirtEndpoint, reactor=reactor,
                                port=16509, driver='qemu', mode='system')

    hosts = ('ipd{}.tic.hefr.ch'.format(i) for i in range(1, 2))
    hosts = {h: libvirt(host=h) for h in hosts}

    workdir = FilePath('workdir/manager')

    redis = ProtocolConnector(reactor, 'localhost', 6379, RedisClient)

    # Business logic setup
    manager = projects.ProjectsManager(workdir, redis, IPD_MANAGER_KEY)
    builder = projects.Builder(manager, hosts, redis)

    # API resources
    api_root = RecursiveResource()
    prjs = ProjectsListResource(manager)
    builds = BuildsListResource(builder)

    # Create tree
    api_root.putChild('projects', prjs)
    api_root.putChild('builds', builds)

    site = server.Site(api_root)
    api_service = internet.TCPServer(8000, site)

    # Application setup
    application = service.Application('projects-manager')
    api_service.setServiceParent(application)
    manager.setServiceParent(application)
    builder.setServiceParent(application)

    # Start application
    service.IService(application).privilegedStartService()
    app.startApplication(application, False)













@defer.inlineCallbacks
def _create_domain():
    from twisted.internet.endpoints import TCP4ClientEndpoint
    from ipd.libvirt import LibvirtFactory, remote, error
    from lxml import etree
    from twisted.python.filepath import FilePath

    point = TCP4ClientEndpoint(reactor, 'ipd1.tic.hefr.ch', 16509)
    proto = yield point.connect(LibvirtFactory())

    res = yield proto.auth_list()
    assert remote.auth_type.REMOTE_AUTH_NONE in res.types

    res = yield proto.connect_supports_feature(10)
    assert res.supported

    yield proto.connect_open('qemu:///system', 0)

    name = 'wintest'
    base_domain = 'windows'
    vnc_pass = ''

    # Create storage pool
    try:
        res = yield proto.storage_pool_lookup_by_name('ipd-images')
    except error.RemoteError:
        with open('workdir/base-vm/pool.xml') as fh:
            poolxml = fh.read()
        res = yield proto.storage_pool_create_xml(poolxml, 0)
    pool = res.pool

    # Create base image
    try:
        res = yield proto.storage_vol_lookup_by_name(pool, name)
    except error.RemoteError:
        print('Volume not found')
    else:
        res = yield proto.storage_vol_delete(res.vol, 0)

    volume = FilePath('workdir/volumes')
    volume = volume.child('{}.xml'.format(base_domain))

    if volume.exists():
        with volume.open() as fh:
            tree = etree.parse(fh)

        tree.find('name').text = name
        volxml = etree.tostring(tree)

        print volxml

        res = yield proto.storage_vol_create_xml(pool, volxml, 0)

    # Create domain
    try:
        res = yield proto.domain_lookup_by_name(name)
    except error.RemoteError:
        print('Domain not found')
    else:
        try:
            yield proto.domain_destroy(res.dom)
        except error.RemoteError:
            pass
        d = defer.Deferred()
        reactor.callLater(2, d.callback, None)
        yield d
        try:
            yield proto.domain_undefine(res.dom)
        except error.RemoteError:
            pass
        try:
            res = yield proto.domain_lookup_by_name('base3')
        except error.RemoteError:
            print('Domain deleted')
        else:
            raise RuntimeError()

    domain = FilePath('workdir/domains')
    domain = domain.child('{}.xml'.format(base_domain))

    with domain.open() as fh:
        tree = etree.parse(fh)

    tree.find('name').text = name

    if volume.exists():
        tree.find('devices/disk/source').attrib['volume'] = name

    if vnc_pass:
        tree.find('devices/graphics').attrib['passwd'] = vnc_pass

    domxml = etree.tostring(tree)

    print domxml

    res = yield proto.domain_create_xml(domxml, 0)
    print(res)

    res = yield proto.domain_get_xml_desc(res.dom, 0)
    print res.xml

    # Cleanup
    yield proto.connect_close()

    reactor.stop()


@defer.inlineCallbacks
def _exec_command():
    from twisted.conch.client.knownhosts import KnownHostsFile
    from twisted.python.filepath import FilePath
    from ipd import ssh

    username = 'ubuntu'
    host = '160.98.61.245'

    keys = [
        IPD_MANAGER_KEY,
    ]
    known_hosts = KnownHostsFile.fromPath(FilePath('workdir/known_hosts'))

    endpoint = ssh.MultipleCommandsClientEndpoint.newConnection(
        reactor, username, host, keys=keys, knownHosts=known_hosts)

    factory = ssh.MultipleCommandsFactory()

    proto = yield endpoint.connect(factory)

    for i in range(10):
        out = yield proto.exec_command(b"/bin/echo %d" % (i,))
        print('server said:', out)

    yield proto.disconnect()

    reactor.stop()


@defer.inlineCallbacks
def _list_domain():
    from twisted.internet.endpoints import SSL4ClientEndpoint, clientFromString
    from twisted.internet.ssl import DefaultOpenSSLContextFactory, CertificateOptions, Certificate, PrivateCertificate
    from ipd.libvirt import LibvirtFactory, remote
    from ipd.libvirt.endpoints import TCP4LibvirtEndpoint
    from OpenSSL import crypto
    import binascii

    context = DefaultOpenSSLContextFactory('workdir/pki/client.key.pem',
                                           'workdir/pki/client.crt.pem')


    with open('workdir/pki/ca.crt.pem') as fh:
        cacert = crypto.load_certificate(crypto.FILETYPE_PEM, fh.read())

    with open('workdir/pki/client.key.pem') as fh:
        private_key = crypto.load_privatekey(crypto.FILETYPE_PEM, fh.read())

    with open('workdir/pki/client.crt.pem') as fh:
        cert = crypto.load_certificate(crypto.FILETYPE_PEM, fh.read())

    class CertOpt(CertificateOptions):
        def getContext(self):
            ctx = super(CertOpt, self).getContext()
            ctx.set_info_callback(self.cb)
            return ctx

        def cb(self, conn, where, status):
            from OpenSSL import SSL
            print(where, status)
            if where & SSL.SSL_CB_HANDSHAKE_START:
                print("Handshake started")
            if where & SSL.SSL_CB_HANDSHAKE_DONE:
                print("Handshake done")

    #(self, privateKey=None, certificate=None, method=None, verify=False, caCerts=None,
    #verifyDepth=9, requireCertificate=True, verifyOnce=True, enableSingleUseKeys=True,
    #enableSessions=True, fixBrokenPeers=False, enableSessionTickets=False, extraCertChain=None):

    context = CertOpt(verify=False, requireCertificate=False,
                      caCerts=[cacert], privateKey=private_key, certificate=cert)

    point = SSL4ClientEndpoint(reactor, 'ipd1.tic.hefr.ch', 16514, context)
    #point = clientFromString(reactor, 'ssl:ipd1.tic.hefr.ch:privateKey=workdir/pki/client.key.pem:certKey=workdir/pki/client.crt.pem')
    point = TCP4LibvirtEndpoint(reactor, 'ipd1.tic.hefr.ch', 16509, 'qemu')
    proto = yield point.connect()

    res = yield proto.connect_list_all_domains(1, 0)

    for domain in res.domains:
        print('{:3} {} {}'.format(domain.id, binascii.b2a_hex(domain.uuid),
                                  domain.name))

    #res = yield proto.domain_create(res.domains[-1])
    #print(res)
