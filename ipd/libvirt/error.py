

class LibvirtError(Exception):
    pass


class ProgramNotFound(LibvirtError):
    pass


class VersionNotSupported(LibvirtError):
    pass


class FeatureNotSupported(LibvirtError, NotImplementedError):
    pass


class UnknownPacketType(LibvirtError):
    pass


class ProcedureNotFound(LibvirtError):
    pass


class RemoteError(LibvirtError):
    def __init__(self, error):
        self.__dict__.update(error._asdict())

    def __str__(self):
        return 'Error {}: {}'.format(self.code, self.message)
