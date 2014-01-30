import string
import random

from twisted.internet.protocol import Factory
from twisted.internet import defer, endpoints


PASSWORD_CHARS = string.ascii_letters + string.digits + string.punctuation


def generate_password(length):
    return ''.join((random.choice(PASSWORD_CHARS) for _ in xrange(length)))


class ProtocolConnector(object):
    def __init__(self, reactor, host, port, protocol):
        self._endpoint = endpoints.TCP4ClientEndpoint(reactor, host, port)
        self._factory = Factory()
        self._factory.protocol = protocol
        self._port = None

    @defer.inlineCallbacks
    def get_connection(self):
        if self._port is None:
            self._port = yield self._endpoint.connect(self._factory)
        defer.returnValue(self._port)

    def __call__(self):
        return self.get_connection()
