from twisted.internet import defer
from ipd.metadata.utils import get_mac_by_ip
from ipd.libvirt import LibvirtFactory, remote
from lxml import etree
import uuid

{
    "availability_zone": "nova",
    "hostname": "test.novalocal",
    "launch_index": 0,
    "meta": {
        "priority": "low",
        "role": "webserver"
    },
}


class MetadataServer(object):

    def __init__(self, ssh_key, libvirt_endpoint):
        self._libvirt_endpoint = libvirt_endpoint
        self._ssh_key = ssh_key

    @defer.inlineCallbacks
    def get_metadata_for_ip(self, ip_address):
        domain = yield self._get_domain_by_ip(ip_address)

        defer.returnValue({
            'uuid': uuid.UUID(bytes=domain.uuid),
            'name': domain.name,
            'public_keys': {
                'ipd': self._ssh_key.toString('OPENSSH', 'admin@ipd'),
            },
            'hostname': '{}.vms.ipd'.format(domain.name),
        })

    @defer.inlineCallbacks
    def get_userdata_for_ip(self, ip_address):
        domain = yield self._get_domain_by_ip(ip_address)
        defer.returnValue('')
