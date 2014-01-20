import xdrlib
import struct
from collections import namedtuple


class TypeBase(object):
    def pack(self, stream, value):
        raise NotImplementedError()

    def unpack(self, stream):
        raise NotImplementedError()


class Type(TypeBase):
    def __init__(self, packer, unpacker):
        self.pack = packer
        self.unpack = unpacker


class TypeFactoryMeta(type):
    pass


class TypeFactory(TypeBase):
    __metaclass__ = TypeFactoryMeta


class CustomSimpleType(TypeBase):
    def __init__(self, fmt):
        self.fmt = fmt
        self.length = struct.calcsize(fmt)

    def pack(self, stream, value):
        stream.get_buffer().write(struct.pack(self.fmt, value))

    def unpack(self, stream):
        i = stream.get_position()
        j = i + self.length
        stream.set_position(j)
        data = stream.get_buffer()[i:j]
        if len(data) < self.length:
            raise EOFError
        return struct.unpack(self.fmt, data)[0]


def make_xdr_type(name):
    packer = getattr(xdrlib.Packer, 'pack_{}'.format(name))
    unpacker = getattr(xdrlib.Unpacker, 'unpack_{}'.format(name))
    return Type(packer, unpacker)


class FixedLengthString(TypeFactory):
    def __init__(self, length):
        self.length = length

    def pack(self, stream, s):
        stream.pack_fstring(self.length, s)

    def unpack(self, stream):
        return stream.unpack_fstring(self.length)


class FixedLengthData(TypeFactory):
    def __init__(self, length):
        self.length = length

    def pack(self, stream, s):
        stream.pack_fopaque(self.length, s)

    def unpack(self, stream):
        return stream.unpack_fopaque(self.length)


class ComplexType(TypeFactory):
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
        self.model = namedtuple(name, [f[0] for f in fields])

    def __repr__(self):
        return '{}({})'.format(self.name, ', '.join(f[0] for f in self.fields))

    def __str__(self):
        return self.name

    def unpack(self, stream):
        values = (type.unpack(stream) for _, type in self.fields)
        return self.model(*values)

    def pack(self, stream, value):
        for name, type in self.fields:
            type.pack(stream, getattr(value, name))


class FixedLengthArray(TypeFactory):
    def __init__(self, items_type, length):
        self.items_type = items_type
        self.length = length

    def pack(self, stream, items):
        packer = lambda item: self.items_type.pack(stream, item)
        stream.pack_farray(self.length, items, packer)

    def unpack(self, stream):
        unpacker = lambda: self.items_type.unpack(stream)
        return stream.unpack_farray(self.length, unpacker)


class VariableLengthArray(TypeFactory):
    def __init__(self, items_type, maxlength):
        self.maxlength = maxlength
        self.items_type = items_type

    def pack(self, stream, items):
        packer = lambda item: self.items_type.pack(stream, item)
        stream.pack_array(items, packer)

    def unpack(self, stream):
        unpacker = lambda: self.items_type.unpack(stream)
        return stream.unpack_array(unpacker)


class Optional(TypeFactory):
    def __init__(self, type):
        self.type = type

    def pack(self, stream, v):
        if v:
            stream.pack_bool(True)
            self.type.pack(stream, v)
        else:
            stream.pack_bool(False)

    def unpack(self, stream):
        if stream.unpack_bool():
            return self.type.unpack(stream)
        else:
            return None


class Enum(TypeFactory):
    def __init__(self, name, values):
        self.name = name
        self.values = values
        self.ids = set([v[1] for v in values])
        self.keys = set([v[0] for v in values])
        for k, v in self.values:
            setattr(self, k, v)
        self._id_to_key = {v: k for k, v in values}
        self._key_to_id = {k: v for k, v in values}

    def __str__(self):
        return self.name

    def key(self, id):
        return self._id_to_key[id]

    def id(self, key):
        return self._key_to_id[key]

    def pack(self, stream, v):
        if isinstance(v, int):
            assert v in self.ids
        else:
            v = self.id(v)
        return stream.pack_enum(v)

    def unpack(self, stream):
        v = stream.unpack_enum()
        assert v in self.ids
        return v

    def __iter__(self):
        return iter(self.values)


int = make_xdr_type('int')
uint = make_xdr_type('uint')
hyper = make_xdr_type('hyper')
uhyper = make_xdr_type('uhyper')
char = CustomSimpleType('>b')
uchar = CustomSimpleType('>B')
short = CustomSimpleType('>h')
ushort = CustomSimpleType('>H')
string = make_xdr_type('string')
opaque = make_xdr_type('opaque')

fstring = FixedLengthString
fopaque = FixedLengthData
farray = FixedLengthArray
array = VariableLengthArray
not_implemented = TypeBase
compound = ComplexType
enum = Enum
optional = Optional

def istype(k, v):
    return k.islower() and isinstance(v, (TypeBase, TypeFactoryMeta))


__all__ = [k for k, v in locals().items() if istype(k, v)]

TYPES = {k: v for k, v in locals().items() if istype(k, v)}
