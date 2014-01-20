from twisted.internet import endpoints, defer
from ipd.libvirt.remote import auth_type
from ipd.libvirt import LibvirtFactory


class TCP4LibvirtEndpoint(endpoints.TCP4ClientEndpoint):
    def __init__(self, reactor, host, port, driver, mode='system', timeout=30,
                 bindAddress=None):
        super(TCP4LibvirtEndpoint, self).__init__(reactor, host, port, timeout,
                                                  bindAddress)
        self.driver = driver
        self.mode = mode

    @defer.inlineCallbacks
    def connect(self, protocolFactory=None):
        if protocolFactory is None:
            protocolFactory = LibvirtFactory()
        proto = yield super(TCP4LibvirtEndpoint, self).connect(protocolFactory)
        res = yield proto.auth_list()
        assert auth_type.REMOTE_AUTH_NONE in res.types
        yield proto.connect_open('{}:///{}'.format(self.driver, self.mode), 0)
        defer.returnValue(proto)
