import struct



DIGITS_STR = '0123456789'



def MakeFieldsStr(struct_info):
    fields_str = [ rec[0] for rec in struct_info ]
    fmt_str = ''.join([ '<' ] + fields_str)
    return fmt_str


def Unpack(struct_info, blocks):
    fmt_str = MakeFieldsStr(struct_info)            # Make format string.
    u = struct.unpack(fmt_str, blocks)              # Unpack binary data.

    u_info = {}                                     # Make struct fields.
    u_idx = 0
    for rec in struct_info:
        fmt = rec[0]
        field_name = rec[1]

        if fmt[0] in DIGITS_STR:                    # Check array type
            num_digits = 1                          # Extract number of elements.
            while fmt[num_digits] in DIGITS_STR:
                num_digits += 1
            num_elems = int(fmt[0 : num_digits])

            u_info[field_name] = []                 # Extract array elements and pack them to a list.
            for i in range(num_elems):
                u_info[field_name].append(u[u_idx + i])
            u_idx += num_digits + 1
            continue

        u_info[field_name] = u[u_idx]               # Extract primitive types.
        u_idx += 1
    return u_info


def CalcSize(struct_info):
    fmt_str = MakeFieldsStr(struct_info)
    sz = struct.calcsize(fmt_str)
    return sz


def PrintPretty(struct_info, struct_fields, indent=''):
    # Find maximum length of field names.
    mx_len = 0
    for rec in struct_info:
        mx_len = max(mx_len, len(rec[1]))

    # Print formated fields.
    fmt_str = '{}{{:{}s}} : {{}}'.format(indent, mx_len)
    for rec in struct_info:
        print(fmt_str.format(rec[1], struct_fields[rec[1]]))


def Pack(struct_info, struct_fields):
    out_str = ''
    for i in range(len(struct_info)):
        fmt = struct_info[i][0]
        v = struct_fields[i]
        if fmt[0] in DIGITS_STR:                    # Check array type
            num_digits = 1                          # Extract number of elements.
            while fmt[num_digits] in DIGITS_STR:
                num_digits += 1
            num_elems = int(fmt[0 : num_digits])
            elem_type = fmt[num_digits:]
            for e in range(num_elems):
                out_str += struct.pack('<' + elem_type, v[e])
            continue

        out_str += struct.pack('<' + fmt, v)
    return out_str



if __name__ == '__main__':
    print('This is a module :)')

