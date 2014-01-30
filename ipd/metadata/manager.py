from uuid import UUID

from twisted.internet import defer


USER_DATA = """#cloud-config

hostname: {hostname}
fqdn: {hostname}.vm.ipd
manage_etc_hosts: true

phone_home:
 url: http://169.254.169.254/instancedata
 tries: 2
"""

KEY_NAME = 'ipd'


class MetadataManager(object):

    def __init__(self, redis_connector, ssh_key):
        self._libvirt_hosts = {}
        self._ssh_key = ssh_key
        self._redis = redis_connector

    def register_host(self, hostname, endpoint):
        self._libvirt_hosts[hostname] = endpoint

    @defer.inlineCallbacks
    def _get_domain_by_uuid(self, host, domain_uuid):
        client = yield self._libvirt_hosts[host].connect()
        res = yield client.domain_lookup_by_uuid(domain_uuid.bytes)
        yield client.connect_close()
        defer.returnValue(res.dom)

    @defer.inlineCallbacks
    def get_metadata_for_uuid(self, host, domain_uuid):
        domain = yield self._get_domain_by_uuid(host, domain_uuid)
        defer.returnValue({
            'uuid': UUID(bytes=domain.uuid),
            'name': domain.name,
            'public_keys': [
                (KEY_NAME, self._ssh_key),
            ],
            'hostname': domain.name,
        })

    @defer.inlineCallbacks
    def get_userdata_for_uuid(self, host, domain_uuid):
        domain = yield self._get_domain_by_uuid(host, domain_uuid)
        userdata = USER_DATA.format(hostname=domain.name)
        defer.returnValue(userdata)

    @defer.inlineCallbacks
    def get_instancedata_for_uuid(self, domain_uuid):
        key = 'instancedata:{}'.format(domain_uuid)
        redis = yield self._redis()
        data = yield redis.hgetall(key)
        defer.returnValue(data)

    @defer.inlineCallbacks
    def add_instancedata_for_uuid(self, domain_uuid, data):
        key = 'instancedata:{}'.format(domain_uuid)
        redis = yield self._redis()
        yield redis.hmset(key, data)
