from twisted.internet import defer
from ipd.metadata.utils import get_mac_by_ip
from ipd.libvirt import LibvirtFactory, remote
from lxml import etree
import uuid


class MetadataServer(object):

    def __init__(self, ssh_key):
        self._libvirt_hosts = {}
        self._ssh_key = ssh_key

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
            'uuid': uuid.UUID(bytes=domain.uuid),
            'name': domain.name,
            'public_keys': [
                ('ipd', self._ssh_key),
            ],
            'hostname': '{}.vms.ipd'.format(domain.name),
        })

    @defer.inlineCallbacks
    def get_userdata_for_uuid(self, host, domain_uuid):
        domain = yield self._get_domain_by_uuid(host, domain_uuid)
        defer.returnValue(
            '#!/bin/bash\n'
            'echo "root:root" | chpasswd\n'
        )
