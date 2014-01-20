from ipd.libvirt import error, constants, remote

from structlog import get_logger
logger = get_logger()


class Program(object):
    id = None
    version = None

    def __init__(self, protocol):
        self._pending_calls = {}
        self._protocol = protocol
        self._log = logger.new(program=self.__class__.__name__)

    def version_supported(self, version):
        return version == self.version

    def get_procedure_class(self, procedure_id):
        raise NotImplementedError()

    def get_procedure(self, procedure_id, packet_type, serial):
        if packet_type == constants.packet_type.REPLY:
            try:
                procedure = self._pending_calls.pop((procedure_id, serial))
            except KeyError:
                raise error.NoPendingCall(procedure, serial)
        else:
            klass = self.get_procedure_class(procedure_id)
            procedure = klass(self)

        return procedure

    def packet_received(self, protocol, header, payload):
        ver, procedure, packet_type, serial, status = header

        if not self.version_supported(ver):
            raise error.VersionNotSupported(self.id, ver)

        if packet_type not in constants.packet_type:
            raise error.UnknownPacketType(packet_type)

        procedure = self.get_procedure(procedure, packet_type, serial)

        packet_type_name = constants.packet_type[packet_type]
        func = getattr(procedure, 'handle_' + packet_type_name)
        func(status, payload)

    def call(self, procedure, args=None, kwargs=None):
        self._log.msg('libvirt.call', procedure=procedure.name)
        serial = self._protocol.next_serial()
        packet = self._protocol.make_packet(
            self.id, self.version, procedure.id,
            constants.packet_type.CALL, serial, constants.status.OK
        )
        procedure.pack_args(packet, args, kwargs)
        self._protocol.send_packet(packet)
        self._pending_calls[procedure.id, serial] = procedure
        return procedure._pending


class RemoteProgram(Program):
    id = remote.PROGRAM
    version = remote.PROTOCOL_VERSION

    def get_procedure_class(self, procedure_id):
        try:
            return remote.PROCEDURE_BY_ID[procedure_id]
        except KeyError:
            raise error.ProcedureNotFound(self.id, procedure_id)


class KeepaliveProgram(Program):
    id = 0x6b656570
    version = 1

    def packet_received(self, protocol, header, payload):
        ver, procedure, packet_type, serial, status = header

        if not self.version_supported(ver):
            raise error.VersionNotSupported(self.id, ver)

        if packet_type != constants.packet_type.EVENT:
            raise error.UnknownPacketType(packet_type)

        if procedure != 1:
            raise error.ProcedureNotFound(procedure)

        self._log.msg('libvirt.keepalive.ping')
        header = self._protocol.make_packet(
            self.id, self.version, 2, constants.packet_type.EVENT)
        self._protocol.send_packet(header)
