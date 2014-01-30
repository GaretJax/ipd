from twisted.web.client import getPage
import yaml
import time
from lxml import etree
from urlparse import urlparse, urlunparse
from twisted.internet import defer, reactor
from twisted.application import service
from twisted.python.filepath import FilePath
from ipd.utils import generate_password
from structlog import get_logger
from ipd.libvirt import error
from ipd import ssh

logger = get_logger()


class BuildspecNotFound(Exception):
    pass


class StopBuildingSentinel(object):
    pass


class DomainNotFound(Exception):
    pass


class Builder(service.Service, object):
    def __init__(self, manager, hosts, redis_connector):
        self._hosts = hosts
        self._manager = manager
        self._redis = redis_connector

        self._hosts_queue = defer.DeferredQueue()
        for h in hosts:
            self._hosts_queue.put(h)

        self._stop_building = defer.Deferred()
        self._builds = defer.DeferredQueue()

    def startService(self):
        logger.msg('builder.starting_service')
        super(Builder, self).startService()
        self.start_building()

    @defer.inlineCallbacks
    def stopService(self):
        logger.msg('builder.stopping_service')
        yield self.stop_building()
        yield super(Builder, self).stopService()

    @defer.inlineCallbacks
    def start_build(self, build_id, host_key):
        redis = yield self._redis()
        build = yield redis.hgetall('build:{}'.format(build_id))

        logger.msg(
            'builder.build_started',
            build_id=build_id,
            host=host_key,
            project=build['project_key'],
            commit=build['commit_id']
        )

        start = time.time()

        buildspec = yaml.load(build['buildspec'])

        base_domain = buildspec['base_domain']

        domain = FilePath('workdir/domains')
        domain = domain.child('{}.xml'.format(base_domain))

        volume = FilePath('workdir/volumes')
        volume = volume.child('{}.xml'.format(base_domain))

        if not domain.exists() or not volume.exists:
            raise DomainNotFound(base_domain)

        with domain.open() as fh:
            tree = etree.parse(fh)

        name = '{}-{}'.format(build['project_key'], build_id)
        vnc_pass = generate_password(32)
        tree.find('name').text = name
        tree.find('devices/disk/source').attrib['volume'] = name
        tree.find('devices/graphics').attrib['passwd'] = vnc_pass
        domxml = etree.tostring(tree)

        with volume.open() as fh:
            tree = etree.parse(fh)

        tree.find('name').text = name
        volxml = etree.tostring(tree)

        virt = yield self._hosts[host_key]()

        # Create storage pool
        try:
            res = yield virt.storage_pool_lookup_by_name('ipd-images')
        except error.RemoteError:
            with open('workdir/base-vm/pool.xml') as fh:
                poolxml = fh.read()
            res = yield virt.storage_pool_create_xml(poolxml, 0)
        pool = res.pool

        # Create base image
        yield virt.storage_vol_create_xml(pool, volxml, 0)

        # Create domain
        res = yield virt.domain_create_xml(domxml, 0)

        # Get information
        res = yield virt.domain_get_xml_desc(res.dom, 0)
        domxml = etree.fromstring(res.xml)

        uuid = domxml.find('uuid').text
        instancedata = {
            'hypervisor': host_key,
            'mac_address': domxml.find('devices/interface/mac').attrib['address'],
            'vncport': domxml.find('devices/graphics').attrib['port'],
            'vncpasswd': vnc_pass,
        }

        redis = yield self._redis()
        key = 'instancedata:{}'.format(uuid)
        redis.hmset(key, instancedata)

        while True:
            status = yield redis.hget(key, 'status')
            if status and status['status'] == 'running':
                break
            d = defer.Deferred()
            reactor.callLater(1, d.callback, None)
            yield d

        instance_data = yield redis.hgetall(key)

        duration = time.time() - start
        print 'Startup duration: {:.1f} seconds'.format(duration)

        ##########

        # Connect ssh
        known_hosts = ssh.KnownHostsLists([
            (instance_data['ip_address'], ssh.Key.fromString(instance_data['pub_key_rsa']))
        ])
        point = ssh.MultipleCommandsClientEndpoint.newConnection(
            reactor, 'ubuntu', instance_data['ip_address'],
            keys=[self._manager._key], knownHosts=known_hosts)

        factory = ssh.MultipleCommandsFactory()
        proto = yield point.connect(factory)

        out = yield proto.exec_command('uname -a')
        print out

        print 'Instance {} is ready'.format(name)
        print ' - IP address: {}'.format(instance_data['ip_address'])
        print ' - VNC host: {}'.format(instance_data['hypervisor'])
        print ' - VNC port: {}'.format(instance_data['vncport'])
        print ' - VNC pass: {}'.format(instance_data['vncpasswd'])

        duration = time.time() - start
        print 'Connect duration: {:.1f} seconds'.format(duration)

        yield proto.exec_command('mkdir -p /srv')

        duration = time.time() - start
        print 'Build duration: {:.1f} seconds'.format(duration)
        yield proto.disconnect()
        # Basic setup
        # - Dir creation
        # - Git checkout
        # - Directory change

        # Exec install
        # Exec start
        # Start routing

    @defer.inlineCallbacks
    def start_building(self):
        def free_item(res, queue, item):
            queue.put(item)
            return res

        while True:
            # Wait for the next free host
            host_key = yield self._hosts_queue.get()
            if isinstance(host_key, StopBuildingSentinel):
                break

            # Wait for a build
            build_id = yield self._builds.get()
            if isinstance(build_id, StopBuildingSentinel):
                break

            d = self.start_build(build_id, host_key)
            d.addBoth(free_item, self._hosts_queue, host_key)

        self._stop_building.callback(None)

    def stop_building(self):
        self._hosts_queue.put(StopBuildingSentinel())
        self._builds.put(StopBuildingSentinel())
        return self._stop_building

    def get_builds(self):
        return defer.succeed([])

    @defer.inlineCallbacks
    def schedule_build(self, project_key, commit_id):
        prj = yield self._manager.get_project(project_key)
        redis = yield self._redis()
        build_id = yield redis.incr('builds')

        buildspec = yield self._get_buildspec(prj['repo'], commit_id)

        yield redis.hmset('build:{}'.format(build_id), {
            'status': 'waiting',
            'buildspec': yaml.dump(buildspec),
            'project_key': project_key,
            'commit_id': commit_id,
        })

        self._builds.put(build_id)
        defer.returnValue('{}-{}'.format(project_key, build_id))

    @defer.inlineCallbacks
    def _get_buildspec(self, repo, commit_id):
        # Just support github repositories right now
        # https://raw.<github repo url>/<commit-id>/<filepath>
        SPEC_PATH = 'Buildspec'
        urlt = urlparse(repo)
        urll = list(urlt)
        urll[1] = urll[1].replace(urlt.hostname, 'raw.github.com')
        urll[2] = urll[2].rstrip('/') + '/' + commit_id + '/' + SPEC_PATH
        url = urlunparse(urll)
        try:
            buildspec = yield getPage(url)
            buildspec = yaml.load(buildspec)
        except Exception:
            raise BuildspecNotFound()
        defer.returnValue(buildspec)
