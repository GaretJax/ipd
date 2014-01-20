from __future__ import absolute_import

import argparse
import sys
from urlparse import urlparse

from twisted.web import server
from twisted.internet import reactor
from structlog import get_logger

from ipd import logging
from ipd.libvirt.endpoints import TCP4LibvirtEndpoint
from ipd.metadata.utils import DomainResolver
from ipd.metadata.revproxy import LibvirtMetaReverseProxyResource


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=80)
    parser.add_argument('upstream')
    parser.add_argument('libvirtd', type=urlparse)
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    logging.setup_logging()
    logger = get_logger()
    logger.msg('metaproxy.starting')

    upstream = args.upstream.split(':')
    if len(upstream) == 1:
        host, port = upstream[0], 80
    else:
        host, port = upstream[0], int(upstream[1])

    if port is None:
        port = 80

    driver, transport = args.libvirtd.scheme.split('+')
    mode = args.libvirtd.path.lstrip('/')
    virt_host = args.libvirtd.hostname
    virt_port = args.libvirtd.port or 16509

    logger.msg('metaproxy.hypervisor', host=virt_host, port=virt_port,
               driver=driver, mode=mode, transport=transport)

    if transport == 'tcp':
        libvirt = TCP4LibvirtEndpoint(reactor, virt_host, virt_port, driver,
                                      mode)
    else:
        print('Transport {!r} not supported'.format(transport))
        sys.exit(1)

    resolver = DomainResolver(libvirt)

    logger.msg('metaproxy.upstream', host=host, port=port)
    res = LibvirtMetaReverseProxyResource(resolver, host, port, '')
    site = server.Site(res)
    reactor.listenTCP(args.port, site)
    reactor.run()
