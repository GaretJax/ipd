from __future__ import absolute_import, print_function
import argparse
import os
import datetime
from pipes import quote
from collections import namedtuple, OrderedDict

import parsley
from ipd import logging, libvirt
from ipd.libvirt import types as xdrtypes

from structlog import get_logger
logger = get_logger()


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('dest')
    return parser


class SimpleValue(namedtuple('simple', ['value'])):
    def get_actual_value(self, constants):
        return self.value

class Integer(SimpleValue):
    pass

class Optional(namedtuple('optional', ['type'])):
    def get_actual_type(self, types, constants):
        type = self.type.get_actual_type(types, constants)
        if type == 'string':
            return 'optional(string)'
        else:
            return 'optional({})'.format(type)

class FixedLengthArray(namedtuple('fixed_array', ['type', 'len'])):
    def get_actual_type(self, types, constants):
        type = self.type.get_actual_type(types, constants)
        length = self.len.get_actual_value(constants)
        if type == '__string__':
            return 'fstring({})'.format(length)
        elif type == '__opaque__':
            return 'fopaque({})'.format(length)
        else:
            return 'farray({}, {})'.format(type, length)

class VariableLengthArray(namedtuple('variable_array', ['type', 'maxlen'])):
    def get_actual_type(self, types, constants):
        type = self.type.get_actual_type(types, constants)
        maxlen = self.maxlen.get_actual_value(constants)
        if type == '__string__':
            return 'string'
        elif type == '__opaque__':
            return 'opaque'
        else:
            return 'array({}, {})'.format(type, maxlen)

class Enumeration(namedtuple('enum', ['id', 'values'])):
    def process_context(self, types, constants):
        name = self.id
        if name.startswith('remote_'):
            name = name[len('remote_'):]
        values = [(k, v.get_actual_value(constants)) for k, v in self.values]
        types[self.id] = xdrtypes.Enum(name, values)

class Structure(namedtuple('struct', ['id', 'fields'])):
    def process_context(self, types, constants):
        fields = [f.process_context(types, constants) for f in self.fields]
        name = self.id
        if name.startswith('remote_'):
            name = name[len('remote_'):]
        types[self.id] = xdrtypes.ComplexType(name, fields)

class Constant(namedtuple('const', ['id', 'value'])):
    def process_context(self, types, constants):
        constants[self.id] = self.value.get_actual_value(constants)

class Type(namedtuple('type', ['name', 'modifiers'])):
    def get_actual_type(self, types, constants):
        name = self.name
        if 'unsigned' in self.modifiers:
            name = 'u' + name
        return types[name]

class TypeDefinition(namedtuple('typedef', ['alias', 'ref'])):
    def process_context(self, types, constants):
        types[self.alias] = self.ref.get_actual_type(types, constants)

class Union(namedtuple('union', ['id', 'content'])):
    def process_context(self, types, constants):
        types[self.id] = 'not_implemented'

class Reference(namedtuple('ref', ['id'])):
    def get_actual_value(self, constants):
        return constants[self.id]

class Declaration(namedtuple('declaration', ['id', 'type'])):
    def process_context(self, types, constants):
        type = self.type.get_actual_type(types, constants)
        id = self.id
        if id in ['from',]:
            id += '_'
        return (id, type)


def main():
    parser = get_parser()
    args = parser.parse_args()

    logging.setup_logging()

    grammar_file = os.path.join(os.path.dirname(
        libvirt.__file__), 'idl.grammar')

    with open(grammar_file, 'rb') as fh:
        grammar = parsley.makeGrammar(fh.read(), {
            'struct': Structure,
            'enum': Enumeration,
            'const': Constant,
            'typedef': TypeDefinition,
            'ref': Reference,
            'union': Union,
            'optional': Optional,
            'integer': Integer,
            'type': Type,
            'fixed_array': FixedLengthArray,
            'variable_array': VariableLengthArray,
            'declaration': Declaration,
        })

    with open(args.source) as fh:
        source = fh.read()

    tokens = grammar(source).tokens()

    constants = OrderedDict({
        'VIR_SECURITY_MODEL_BUFLEN': 257,
        'VIR_SECURITY_LABEL_BUFLEN': 4097,
        'VIR_SECURITY_DOI_BUFLEN': 257,
        'VIR_UUID_BUFLEN': 16,
    })

    types = OrderedDict({k:k for k in xdrtypes.TYPES})
    types['string'] = '__string__'
    types['opaque'] = '__opaque__'

    try:
        for token in tokens:
            token.process_context(types, constants)
    except:
        for k, v in constants.iteritems():
            print('{:<45} {}'.format(k, v))

        print('-------------')

        for k, v in types.iteritems():
            print('{:<45} {}'.format(k, v))

        raise

    import re, sys
    def to_camelcase(s):
        s = s.capitalize()
        return re.sub(r'(?!^)_([a-zA-Z])', lambda m: m.group(1).upper(), s)

    cmdline = ' '.join(quote(a) for a in sys.argv[1:])
    with open(args.dest, 'w') as fh:
        fh.write(
            '"""\n'
            'Automatically generated Libvirt protocol specification.\n\n'
            'Do not modify this file manually, as the changes will be overwritten\n'
            'the next time that the generation script is run!\n\n'
            '  Generated on:  {}\n'
            '  Command line:  gen-libvirt-protocol {}\n\n'
            '"""\n\n'.format(datetime.datetime.now().isoformat(), cmdline)
        )
        fh.write('from ipd.libvirt.procedures import ProcedureBase\n')
        fh.write('from ipd.libvirt.types import char, short, int, hyper\n')
        fh.write('from ipd.libvirt.types import uchar, ushort, uint, uhyper\n')
        fh.write('from ipd.libvirt.types import fstring, string, fopaque, opaque\n')
        fh.write('from ipd.libvirt.types import farray, array, optional\n')
        fh.write('from ipd.libvirt.types import not_implemented, compound, enum\n')
        fh.write('\n\n')

        fh.write('PROGRAM = {}\n'.format(hex(constants['REMOTE_PROGRAM'])))
        fh.write('PROTOCOL_VERSION = {}\n\n'.format(hex(constants['REMOTE_PROTOCOL_VERSION'])))

        for name, type in types.iteritems():
            if name in set(['remote_procedure']):
                continue
            if not isinstance(type, (xdrtypes.ComplexType, xdrtypes.Enum)):
                continue
            if name.startswith('remote_'):
                name = name[len('remote_'):]

            if isinstance(type, xdrtypes.Enum):
                fh.write('{} = enum({!r}, [\n'.format(name, name))
                for k, v in type.values:
                    fh.write('    ({!r}, {}),\n'.format(k, v))
                fh.write('])\n\n')
                continue

            fh.write('{} = compound({!r}, [\n'.format(name, name))
            for k, v in type.fields:
                if isinstance(v, xdrtypes.ComplexType):
                    v = v.name
                    if v.startswith('remote_'):
                        v = v[len('remote_'):]
                fh.write('    ({!r}, {}),\n'.format(k, v))
            fh.write('])\n\n')

        for k, v in types['remote_procedure']:
            _, _, k = k.lower().split('_', 2)
            args_struct_name = 'remote_' + k + '_args'
            ret_struct_name = 'remote_' + k + '_ret'

            try:
                args = types[args_struct_name]
            except KeyError:
                args = None

            try:
                ret = types[ret_struct_name]
            except KeyError:
                ret = None

            name = to_camelcase(k)

            fh.write('class {}(ProcedureBase):\n'.format(name))
            fh.write('    id = {}\n'.format(v))
            fh.write('    name = {!r}\n'.format(k))
            fh.write('    args = {}\n'.format(args.name if args else None))
            fh.write('    ret = {}\n'.format(ret.name if ret else None))
            fh.write('\n')


        fh.write('PROCEDURE_BY_NAME = {\n')
        for k, v in types['remote_procedure']:
            _, _, k = k.lower().split('_', 2)
            name = to_camelcase(k)
            fh.write('    {!r}: {},\n'.format(k, name))
        fh.write('}\n')

        fh.write('PROCEDURE_BY_ID = {\n')
        for k, v in types['remote_procedure']:
            _, _, k = k.lower().split('_', 2)
            name = to_camelcase(k)
            fh.write('    {}: {},\n'.format(v, name))
        fh.write('}\n')
