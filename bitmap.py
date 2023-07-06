import os

import struct_utils



HEADER = [
    ('2c', 'Signature'),
    ('I',  'FileSize'),
    ('I',  'reserved'),
    ('I',  'DataOffset'),
]

INFO_HEADER = [
    ('I', 'Size'),
    ('I', 'Width'),
    ('I', 'Height'),
    ('H', 'Planes'),
    ('H', 'BitsPerPixel'),
    ('I', 'Compression'),
    ('I', 'ImageSize'),
    ('I', 'XPixelsPerM'),
    ('I', 'YPixelsPerM'),
    ('I', 'ColorsUsed'),
    ('I', 'ImportantColors'),
]

COLOR_TABLE = [
    ('B', 'blue'),
    ('B', 'green'),
    ('B', 'red'),
    ('B', 'reserved'),
]



def MkColor(r, g, b):
    c = (r << 16) | (g << 8) | b
    return c


def GetRGBColor(c):
    r = (c >> 16) & 0xff
    g = (c >> 8) & 0xff
    b = c & 0xff
    return r, g, b


class BitmapReader:
    def __init__(self, path):
        if not os.path.isfile(path):
            raise Exception('Could not open `{}\' file!'.format(path))

        with open(path, 'rb') as f:
            blocks = f.read()

        # Check signature.
        if len(blocks) < 2 or blocks[0:2] != 'BM':
            raise Exception('Header signature of `{}\' is not correct'.format(path))

        # Check header size.
        hdr_sz = struct_utils.CalcSize(HEADER)
        if len(blocks) < hdr_sz:
            raise Exception('The size of `{}\' is less than header!'.format(path))

        # Extract header.
        self.header = struct_utils.Unpack(HEADER, blocks[0 : hdr_sz])

        # Check info header.
        info_hdr_sz = struct_utils.CalcSize(INFO_HEADER)
        if len(blocks) < hdr_sz + info_hdr_sz:
            raise Exception('The size of `{}\' is less than header and info header!'.format(path))

        # Extract info header.
        self.info_header = struct_utils.Unpack(INFO_HEADER, blocks[hdr_sz : hdr_sz + info_hdr_sz])

        # Check info header size.
        if self.info_header['Size'] != 40:
            sz = self.info_header['Size']
            raise Exception('The info header (size:{}) of `{}\' is not supported!'.format(sz, path))

        # Extract color table.
        self.color_table = []
        b_idx = hdr_sz + info_hdr_sz
        if self.IsPixelIndexed():
            num_colors = self.GetNumColors()
            for i in range(num_colors):
                clr_tbl = struct_utils.Unpack(COLOR_TABLE, blocks[b_idx : b_idx + 4])
                self.color_table.append(clr_tbl)
                b_idx += 4

        # Extract pixel data.
        self.pixel_mask = (1 << self.info_header['BitsPerPixel']) - 1
        self.pixel_data = blocks[b_idx : ]


    def GetNumColors(self):
        num_colors = 2 ** self.info_header['BitsPerPixel']
        return num_colors


    def GetRowBytes(self):
        num_bits = self.info_header['BitsPerPixel'] * self.info_header['Width']
        num_bytes = (num_bits + 31) // 32
        num_bytes *= 4
        return num_bytes


    def GetPixel(self, x, y):
        w = self.info_header['Width']
        h = self.info_header['Height']
        if x < 0 or x >= w or y < 0 or y >= h:                  # Check boundary
            return 0

        y = w - y - 1                                           # Transform y coordinate to pixel offset.
        row_idx = y * self.GetRowBytes()                        # Calculate row offset.
        col_bit_idx = x * self.info_header['BitsPerPixel']      # Calculate column bit offset.
        col_byte_idx = col_bit_idx // 8                         # Calculate column byte offset.

        p_idx = row_idx + col_byte_idx                          # Calculate pixel data offset.
        pixel_data = ord(self.pixel_data[p_idx])                # Read pixel data.
        if self.IsPixelIndexed():                               # Read indexed color.
            sft = 8 - (col_bit_idx % 8) - self.info_header['BitsPerPixel']
            pixel_data = pixel_data >> sft
            pixel_data = pixel_data & self.pixel_mask
            c_tbl = self.color_table[pixel_data]
            pixel_color = MkColor(c_tbl['red'], c_tbl['green'], c_tbl['blue'])
            return pixel_color

        num_bytes = self.info_header['BitsPerPixel'] // 8
        sft = 8
        for i in range(1, num_bytes):
            pd = self.pixel_data[p_idx + i]
            pixel_data |= ord(pd) << sft                        # Read true color.
            sft += 8
        return pixel_data


    def IsPixelIndexed(self):
        return self.info_header['BitsPerPixel'] <= 8


    def Print(self):
        struct_utils.PrintPretty(HEADER, self.header)
        print('----------')
        struct_utils.PrintPretty(INFO_HEADER, self.info_header)
        print('----------')
        print('Color table size : {}'.format(len(self.color_table)))
        i = 0
        for c in self.color_table:
            i += 1
            struct_utils.PrintPretty(COLOR_TABLE, c, '  ')
            print('  {:3d} ----------'.format(i))
        print('----------')
        print('pixel data size : {}'.format(len(self.pixel_data)))
        print('Pixel mask      : {:x}'.format(self.pixel_mask))
        print('Row bytes       : {}'.format(self.GetRowBytes()))


    def PrintPixelData(self):
        idx = 0
        for y in range(self.info_header['Height']):
            s = ''
            for x in range(self.GetRowBytes()):
                s += '{:02x}'.format(ord(self.pixel_data[idx]))
                idx += 1
            print('{:>4d} {}'.format(self.info_header['Height'] - y - 1, s))


    def GetWidth(self):
        return self.info_header['Width']


    def GetHeight(self):
        return self.info_header['Height']


class BitmapWriter:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[[0, 0, 0] for w in range(self.width)] for h in range(self.height) ]


    def GetWidth(self):
        return self.width


    def GetHeight(self):
        return self.height


    def GetPixel(self, x, y):
        if x < 0 or x > self.GetWidth() or y < 0 or y > self.GetHeight():
            return 0

        y = self.GetHeight() - y - 1
        r = self.pixels[y][x][0]
        g = self.pixels[y][x][1]
        b = self.pixels[y][x][2]
        return MkColor(r, g, b)


    def PutPixelRGB(self, x, y, r, g, b):
        if x < 0 or x > self.GetWidth() or y < 0 or y > self.GetHeight():
            return

        y = self.GetHeight() - y - 1
        self.pixels[y][x][0] = r
        self.pixels[y][x][1] = g
        self.pixels[y][x][2] = b


    def PutPixelInt(self, x, y, c):
        r, g, b = GetRGBColor(c)
        self.PutPixelRGB(x, y, r, g, b)


    def ClearRGB(self, r, g, b):
        for y in range(self.GetHeight()):
            for x in range(self.GetWidth()):
                self.PutPixelRGB(x, y, r, g, b)


    def ClearInt(self, clr):
        r, g, b = GetRGBColor(clr)
        self.ClearRGB(r, g, b)


    def Save(self, path):
        with open(path, 'wb') as f:
            row_size = (((self.width * 24) + 31) // 32) * 4
            pad_size = row_size - (self.width * 3)
            px_data_size = row_size * self.height
            data_offset = struct_utils.CalcSize(HEADER) + struct_utils.CalcSize(INFO_HEADER)
            file_size = data_offset + px_data_size
            hdr = [
                ('B', 'M'),         # ('2c', 'Signature'),
                file_size,          # ('I',  'FileSize'),
                0,                  # ('I',  'reserved'),
                data_offset,        # ('I',  'DataOffset'),
            ]
            info_hdr = [
                40,                 # ('I', 'Size'),
                self.width,         # ('I', 'Width'),
                self.height,        # ('I', 'Height'),
                1,                  # ('H', 'Planes'),
                24,                 # ('H', 'BitsPerPixel'),
                0,                  # ('I', 'Compression'),
                0,                  # ('I', 'ImageSize'),
                0,                  # ('I', 'XPixelsPerM'),
                0,                  # ('I', 'YPixelsPerM'),
                0,                  # ('I', 'ColorsUsed'),
                0,                  # ('I', 'ImportantColors'),
            ]
            f.write(struct_utils.Pack(HEADER, hdr))                         # Write header.
            f.write(struct_utils.Pack(INFO_HEADER, info_hdr))               # Write header.
            for y in range(self.height):                                    # Write pixel data
                for x in range(self.width):
                    clr = [self.pixels[y][x][2], self.pixels[y][x][1], self.pixels[y][x][0]]
                    CLR = [('B', 'B'), ('B', 'G'), ('B', 'R')]
                    f.write(struct_utils.Pack(CLR, clr))
                for p in range(pad_size):                                   # Write padding
                    f.write(struct_utils.Pack([('B', 'P')], [0]))



if __name__ == '__main__':
    print('This is a module :)')

