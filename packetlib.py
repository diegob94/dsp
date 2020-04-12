#!/usr/bin/env python
import yaml
from pathlib import Path
import struct

class Packet:
    def __init__(self, yaml_path):
        self.packet_def = read_packet_yaml(Path(yaml_path))
        self.struct_format = get_struct_format(self.packet_def)
        for field,field_attrs in self.packet_def.items():
            setattr(self, field, field_attrs['default'])
    @property
    def stream(self):
        fields = [getattr(self, k) for k in self.packet_def.keys()]
        return struct.pack(self.struct_format, *fields)

def read_packet_yaml(yaml_path, debug = False):
    yaml_path = yaml_path.resolve()
    packet_def_raw = yaml.safe_load(yaml_path.open('r'))
    packet_def = {}
    for field,field_attrs in packet_def_raw['packet'].items():
        if field_attrs is None:
            field_attrs = {}
        width = field_attrs.get('width', 32)
        byte_width = width // 8;
        default = 0
        unsigned = field_attrs.get('unsigned', False)
        packet_def[field] = dict(
            width = width, 
            unsigned = unsigned, 
            byte_width = byte_width,
            default = default,
        )
    if debug:
        path = Path.cwd() / (f'debug.{yaml_path.stem}.preproc_defaults.yaml')
        yaml.dump(packet_def, path.open('w'))
        print(f'YAML dumped: {path}')
    return packet_def

def write_header(packet_def, header_path):
    header_path = header_path.resolve()
    header_template = """
#ifndef PACKET_H
#define PACKET_H

#define PACKET_SIZE {total_bytes}

typedef union Packet_u {{
    struct __attribute__((__packed__)) fields_s {{
{fields}
    }} fields;
    uint8_t stream[{total_bytes}];
}} Packet;

#endif // PACKET_H
    """.strip()

    map_width_c = {
        8: 'int8_t',
        32: 'int32_t',
    }
    map_unsigned_c = {
        True: 'u',
        False: '',
    }

    lines = []
    total_bytes = 0
    for field, field_attrs in packet_def.items():
        c_type = map_unsigned_c[field_attrs['unsigned']] + map_width_c[field_attrs['width']]
        ident = ' ' * 4
        lines.append(f'{ident}{ident}{c_type} {field};')
        total_bytes += field_attrs['byte_width']
    header = header_template.format(fields = '\n'.join(lines), total_bytes =  total_bytes)
    header_path.write_text(header + '\n')
    print(f"Header generated: {header_path}")

def get_struct_format(packet_def):
    map_width_py = {
        8: 'b',
        32: 'i',
    }
    map_unsigned_py = {
        True: lambda x: x.capitalize(),
        False: lambda x: x,
    }
    struct_format = ['=']
    for field, field_attrs in packet_def.items():
        f = map_unsigned_py[field_attrs['unsigned']](map_width_py[field_attrs['width']])
        struct_format.append(f)
    return ''.join(struct_format)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Generate packet header from YAML definition')
    parser.add_argument('yaml', type=Path, help='Packet definition in YAML format')
    args = parser.parse_args()
    packet_def = read_packet_yaml(args.yaml)
    header_path = Path.cwd() / args.yaml.with_suffix('.h').name
    write_header(packet_def, header_path)
    #print(get_struct_format(packet_def))
