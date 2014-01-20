from __future__ import absolute_import, print_function
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
    reactor.callWhenRunning(_list_domain)
    reactor.run()

    #project = Project(
    #    repository=repository.GitRepository(),
    #    workdir='',
    #    base_image=Image(),
    #)

from twisted.conch.ssh.keys import Key

IPD_MANAGER_KEY = Key.fromFile('workdir/ipd-test-key.rsa')

@defer.inlineCallbacks
def _create_domain():
    from twisted.internet.endpoints import TCP4ClientEndpoint
    from ipd.libvirt import LibvirtFactory, remote, error
    import binascii

    point = TCP4ClientEndpoint(reactor, 'ipd1.tic.hefr.ch', 16509)
    proto = yield point.connect(LibvirtFactory())

    res = yield proto.auth_list()
    assert remote.auth_type.REMOTE_AUTH_NONE in res.types

    res = yield proto.connect_supports_feature(10)
    assert res.supported

    yield proto.connect_open('qemu:///system', 0)

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
        res = yield proto.storage_vol_lookup_by_name(pool, 'base')
    except error.RemoteError:
        with open('workdir/base-vm/volume.xml') as fh:
            volxml = fh.read()
        res = yield proto.storage_vol_create_xml(pool, volxml, 0)

    # Create domain
    try:
        res = yield proto.domain_lookup_by_name('base3')
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

    with open('workdir/base-vm/domain.xml') as fh:
        domxml = fh.read()

    res = yield proto.domain_create_xml(domxml, 0)
    print(res)

    # Cleanup
    yield proto.connect_close()

    reactor.stop()



@defer.inlineCallbacks
def _runmetaserver():
    from twisted.internet.endpoints import TCP4ClientEndpoint

    point = TCP4ClientEndpoint(reactor, "192.168.56.1", 9009)

    #router = MetadataServer()
    from twisted.web import server
    from twisted.internet import endpoints
    from ipd.metadata import MetadataIndex, MetadataServer

    srv = MetadataServer(
        IPD_MANAGER_KEY.public(),
        point
    )
    metadata_resource = MetadataIndex(srv)

    site = server.Site(metadata_resource)

    endpoint = endpoints.TCP4ServerEndpoint(reactor, 80)
    endpoint.listen(site)

    yield defer.Deferred()

@defer.inlineCallbacks
def _exec_command():
    from twisted.internet import protocol
    from twisted.conch.client.knownhosts import KnownHostsFile
    from twisted.conch.endpoints import SSHCommandClientEndpoint
    from twisted.python.filepath import FilePath

    command = '/bin/cat'
    username = 'ipd-admin'
    host = '192.168.56.102'

    keys = [
        IPD_MANAGER_KEY,
    ]
    known_hosts = KnownHostsFile.fromPath(FilePath('workdir/known_hosts'))

    endpoint = SSHCommandClientEndpoint.newConnection(
        reactor, command, username, host, keys=keys, knownHosts=known_hosts)

    class CommandsProtocol(protocol.Protocol):
        def connectionMade(self):
            self.disconnected = None

        def exec_command(self, command):
            conn = self.transport.conn
            factory = protocol.Factory()
            factory.protocol = SingleCommandProtocol

            e = SSHCommandClientEndpoint.existingConnection(
                conn, b"/bin/echo %d" % (i,))
            d = e.connect(factory)
            d.addCallback(lambda p: p.finished)
            return d

        def disconnect(self):
            d = self.disconnected = defer.Deferred()
            self.transport.loseConnection()
            return d

        def connectionLost(self, reason):
            if self.disconnected:
                self.disconnected.callback(None)

    class SingleCommandProtocol(protocol.Protocol):
        def connectionMade(self):
            self.data = []
            self.finished = defer.Deferred()

        def dataReceived(self, data):
            self.data.append(data)

        def connectionLost(self, reason):
            self.finished.callback(''.join(self.data))

    factory = protocol.Factory()
    factory.protocol = CommandsProtocol

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


@defer.inlineCallbacks
def _poll_repo():
    from ipd import repository

    try:
        #repo = yield repository.GitRepository.clone(
        #    'https://github.com/GaretJax/poller-test', 'workdir/poller-test')
        yield defer.succeed(None)
        repo = repository.GitRepository('workdir/poller-test')
        poller = repository.RepositoryPoller(repo)
        def t(repo, branch, new, old):
            logger.msg('up', repo=repo, branch=branch, new=new, old=old)
        poller.subscribe(t)
        poller.start_polling()
    finally:
        pass
        #reactor.stop()
