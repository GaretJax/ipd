from twisted.internet import defer
from ipd.libvirt import error, constants

from structlog import get_logger
logger = get_logger()


class ProcedureBase(object):
    id = None
    name = None
    args = None
    ret = None

    def __init__(self, program):
        self._program = program
        self._pending = defer.Deferred()
        self._log = program._log.bind(procedure=self.name)

    def __call__(self, *args, **kwargs):
        return self._program.call(self, args, kwargs)

    def handle_CALL(self, status, payload):
        self._log.msg('libvirt.recv.call')
        raise error.FeatureNotSupported(
                'Remote procedure calls are not supported.')

    def handle_REPLY(self, status, payload):
        self._log.msg('libvirt.recv.reply', status=constants.status[status])
        if status == constants.status.OK:
            response = self.unpack_ret(payload)
            self._pending.callback(response)
        else:
            response = self.unpack_err(payload)
            self._pending.errback(response)

    def handle_EVENT(self, status, payload):
        self._log.msg('libvirt.recv.event')
        raise error.FeatureNotSupported('Remote events are not supported.')

    def handle_STREAM(self, status, payload):
        self._log.msg('libvirt.recv.stream', status=constants.status[status])
        raise error.FeatureNotSupported('Remote streaming is not supported.')

    @classmethod
    def pack_args(cls, stream, args, kwargs):
        if cls.args is not None:
            value = cls.args.model(*args, **kwargs)
            cls.args.pack(stream, value)

    @classmethod
    def unpack_ret(cls, stream):
        if cls.ret is not None:
            return cls.ret.unpack(stream)

    @classmethod
    def unpack_err(cls, stream):
        from ipd.libvirt import remote
        return error.RemoteError(remote.error.unpack(stream))
