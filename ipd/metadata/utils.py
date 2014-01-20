import re
from collections import namedtuple

from lxml import etree
from twisted.internet import defer

import structlog
logger = structlog.get_logger()


ARPEntry = namedtuple('ARPEntry',
                      ['ip', 'type', 'flags', 'mac', 'mask', 'device'])


def load_arp_table():
    with open('/proc/net/arp', 'r') as fh:
        entries = fh.read().strip().split('\n')[1:]
        entries = (re.split('\s+', e) for e in entries)
        entries = [ARPEntry(*e) for e in entries]
    return entries


def get_mac_by_ip(ip_address):
    for entry in load_arp_table():
        if entry.ip == ip_address:
            return entry.mac


class DomainResolver(object):
    class DomainNotFound(Exception):
        pass

    def __init__(self, libvirt_endpoint):
        self._libvirt_endpoint = libvirt_endpoint

    @defer.inlineCallbacks
    def _load_mac_addresses(self):
        addresses = {}

        def extract_macs(response, domain):
            xml = etree.fromstring(response.xml)
            macs = xml.iterfind("devices/interface/mac")
            macs = [e.get('address') for e in macs]
            for addr in macs:
                addresses[addr] = domain

        virt = yield self._libvirt_endpoint.connect()
        res = yield virt.connect_list_all_domains(1, 0)
        dl = []

        for domain in res.domains:
            d = virt.domain_get_xml_desc(domain, 0)
            d.addCallback(extract_macs, domain)
            dl.append(d)

        yield defer.DeferredList(dl)
        self._mac_to_uuid = addresses

    @defer.inlineCallbacks
    def get_domain_by_ip(self, ip_address):
        yield self._load_mac_addresses()
        mac_address = get_mac_by_ip(ip_address)
        try:
            domain = self._mac_to_uuid[mac_address]
        except KeyError:
            logger.msg('domainresolver.notfound', mac=mac_address,
                       ip=ip_address)
            raise DomainResolver.DomainNotFound()
        defer.returnValue(domain)
