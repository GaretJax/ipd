LIBVIRT_CONST = {
    'VIR_SECURITY_MODEL_BUFLEN': 257,
    'VIR_SECURITY_LABEL_BUFLEN': 4097,
    'VIR_SECURITY_DOI_BUFLEN': 257,
    'VIR_UUID_BUFLEN': 16,
}


class Enum(object):
    def __init__(self, *keys):
        self._keys = keys
        for i, k in enumerate(keys):
            setattr(self, k, i)

    def __getitem__(self, key):
        return self._keys[key]

    def __contains__(self, key):
        return key < len(self._keys)


packet_type = Enum('CALL', 'REPLY', 'EVENT', 'STREAM')
status = Enum('OK', 'ERROR', 'CONTINUE')
