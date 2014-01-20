import struct
import xdrlib

from twisted.protocols import basic
from twisted.internet import protocol

from ipd.libvirt import error, program, remote, constants

from structlog import get_logger
logger = get_logger()


class Packer(xdrlib.Packer):
    def __init__(self, initial=''):
        self._initial = initial
        xdrlib.Packer.__init__(self)

    def reset(self):
        xdrlib.Packer.reset(self)
        # This only works because this class has the same name as its base
        self.__buf.write(self._initial)


class PrefixIntNStringReceiver(basic.IntNStringReceiver):
    def dataReceived(self, data):
        alldata = self._unprocessed + data
        currentOffset = 0
        prefixLength = self.prefixLength
        fmt = self.structFormat
        self._unprocessed = alldata

        while len(alldata) >= (currentOffset + prefixLength) and not self.paused:
            messageStart = currentOffset + prefixLength
            length, = struct.unpack(fmt, alldata[currentOffset:messageStart])
            if length > self.MAX_LENGTH:
                self._unprocessed = alldata
                self._compatibilityOffset = currentOffset
                self.lengthLimitExceeded(length)
                return
            messageEnd = currentOffset + length
            if len(alldata) < messageEnd:
                break

            # Here we have to slice the working buffer so we can send just the
            # netstring into the stringReceived callback.
            packet = alldata[messageStart:messageEnd]
            currentOffset = messageEnd
            self._compatibilityOffset = currentOffset
            self.stringReceived(packet)

            # Check to see if the backwards compat "recvd" attribute got written
            # to by application code.  If so, drop the current data buffer and
            # switch to the new buffer given by that attribute's value.
            if 'recvd' in self.__dict__:
                alldata = self.__dict__.pop('recvd')
                self._unprocessed = alldata
                self._compatibilityOffset = currentOffset = 0
                if alldata:
                    continue
                return

        # Slice off all the data that has been processed, avoiding holding onto
        # memory to store it, and update the compatibility attributes to reflect
        # that change.
        self._unprocessed = alldata[currentOffset:]
        self._compatibilityOffset = 0

    def sendString(self, string):
        if len(string) >= 2 ** (8 * self.prefixLength):
            raise basic.StringTooLongError(
                'Try to send %s bytes whereas maximum is %s' % (
                len(string), 2 ** (8 * self.prefixLength)))
        self.transport.write(
            struct.pack(self.structFormat, len(string) + self.prefixLength) + string)


class PrefixInt32StringReceiver(PrefixIntNStringReceiver,
                                basic.Int32StringReceiver):
    pass


class LibvirtProtocol(PrefixInt32StringReceiver):
    header_format = '>IIiiIi'
    header_length = struct.calcsize(header_format)

    def __init__(self):
        self._log = logger.new()
        self._current_serial = 0
        self._waiting = {}
        self._programs = {}

    def register_program(self, program_factory):
        prog = program_factory(self)
        self._programs[prog.id] = prog
        return prog

    def next_serial(self):
        serial = self._current_serial
        self._current_serial += 1
        return serial

    def connectionMade(self):
        self._log.msg('libvirt.connected')
        self._remote = self.register_program(program.RemoteProgram)
        self._keepalive = self.register_program(program.KeepaliveProgram)

    def stringReceived(self, string):
        header, payload = self._unpack_packet(string)
        try:
            program = self._programs[header[0]]
        except KeyError:
            raise error.ProgramNotFound(header[0])
        program.packet_received(self, header[1:], payload)

    def _unpack_packet(self, data):
        header = struct.unpack(self.header_format, data[:self.header_length])
        payload = xdrlib.Unpacker(data[self.header_length:])
        return header, payload

    def make_packet(self, program, version, procedure, type, serial=0,
                    status=constants.status.OK):
        header = struct.pack('>IIiiIi', program, version, procedure, type,
                             serial, status)
        packet = Packer(header)
        return packet

    def send_packet(self, packet):
        self.sendString(packet.get_buffer())


class MagicLibvirtProtocol(LibvirtProtocol):
    def __getattr__(self, name):
        try:
            procedure = remote.PROCEDURE_BY_NAME[name]
        except KeyError:
            raise
        else:
            return procedure(self._remote)


class LibvirtFactory(protocol.Factory):
    protocol = MagicLibvirtProtocol
