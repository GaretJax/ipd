from __future__ import absolute_import

import argparse

from twisted.web import server
from twisted.internet import reactor, endpoints
from twisted.conch.ssh.keys import Key

from txredis.client import RedisClient

from structlog import get_logger

from ipd import logging
from ipd.libvirt.endpoints import TCP4LibvirtEndpoint
from ipd.metadata import MetadataRootResource, MetadataManager
from ipd.utils import ProtocolConnector


IPD_MANAGER_KEY = Key.fromFile('workdir/ipd-test-key.rsa')


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=80)
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    logging.setup_logging()
    logger = get_logger()
    logger.msg('metaserver.starting')

    redis = ProtocolConnector(reactor, 'localhost', 6379, RedisClient)

    srv = MetadataManager(redis, IPD_MANAGER_KEY.public())
    srv.register_host(
        'ipd1.tic.hefr.ch',
        TCP4LibvirtEndpoint(reactor, 'ipd1.tic.hefr.ch', 16509, 'qemu', 'system'),
    )

    site = server.Site(MetadataRootResource(srv))

    endpoint = endpoints.TCP4ServerEndpoint(reactor, args.port)
    endpoint.listen(site)
    reactor.run()
