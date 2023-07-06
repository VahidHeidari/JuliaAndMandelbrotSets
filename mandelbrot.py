import os

import bitmap



#IMG_SCALE           = 1
IMG_SCALE           = 2
IMG_WIDTH           = 320 * IMG_SCALE
IMG_HEIGHT          = 240 * IMG_SCALE

MAX_ITER            = 200
ESCAPE_RADIUS       = 2
ESCAPE_RADIUS_2     = ESCAPE_RADIUS ** 2

COLORS = [
    (0xff, 0xff, 0xff),         # White
    (0x00, 0x00, 0xff),         # Blue
    (0xff, 0xff, 0x00),         # Yellow
    (0x00, 0xff, 0x00),         # Green
    (0xff, 0x00, 0xff),         # Violet
    (0xff, 0x00, 0x00),         # Red
    (0x00, 0xff, 0xff),         # Violet
    (0x00, 0x00, 0x00),         # Black
]
COLOR_DIV = float(MAX_ITER) / (len(COLORS) - 1)



class Z:
    def __init__(self, r, i):
        self.r = float(r)       # Real part
        self.i = float(i)       # Imaginery part


    def Add(self, z):
        self.r += z.r
        self.i += z.i


    def Square(self):
        r = self.r ** 2 - self.i ** 2
        i = 2 * self.r * self.i
        self.r = r
        self.i = i


    def Length2(self):
        return self.r ** 2 + self.i ** 2



def GetColor(c, z_r=0, z_i=0):
    z = Z(z_r, z_i)
    for itr in range(MAX_ITER):
        z.Square()
        z.Add(c)
        if z.Length2() > ESCAPE_RADIUS_2:
            c_idx = int(itr / COLOR_DIV)
            l = (itr % int(COLOR_DIV)) / COLOR_DIV
            c0 = COLORS[c_idx]
            try:
                c1 = COLORS[c_idx + 1]
            except:
                print(COLOR_DIV * len(COLORS))
                print(COLOR_DIV * (len(COLORS) - 1))
                clr_div = MAX_ITER // len(COLORS)
                print(clr_div, clr_div * len(COLORS), clr_div * (len(COLORS) - 1))
                print(c_idx, len(COLORS), itr, COLOR_DIV, MAX_ITER)
                exit(10)
            r = c0[0] * (1.0 - l) + c1[0] * l
            g = c0[1] * (1.0 - l) + c1[1] * l
            b = c0[2] * (1.0 - l) + c1[2] * l
            c = bitmap.MkColor(int(r), int(g), int(b))
            return c
    return 0


def DrawMandelbrotSet(x, y, zoom):
    out_name = '%0.2f-%0.2f-%0.2f.bmp' % (x, y, zoom)
    out_path = os.path.join('mandelbrot', out_name)
    if not os.path.isdir('mandelbrot'):
        os.makedirs('mandelbrot')

    bw = bitmap.BitmapWriter(IMG_WIDTH, IMG_HEIGHT)

    scale = 2.0 / min(bw.GetWidth(), bw.GetHeight()) / zoom
    x = x_start = x - (bw.GetWidth() / 2.0) * scale
    y = y + (bw.GetHeight() / 2.0) * scale
    c = Z(0, 0)
    for j in range(bw.GetHeight()):
        for i in range(bw.GetWidth()):
            c = Z(x, y)
            clr = GetColor(c)
            bw.PutPixelInt(i, j, clr)
            x += scale
        x = x_start
        y -= scale

    bw.Save(out_path)



def DoMain():
    DrawMandelbrotSet(-0.5, 0, 1)
    DrawMandelbrotSet(-0.5, 0.5, 2)
    DrawMandelbrotSet(-0.725, 0.2, 40)
    DrawMandelbrotSet(-0.73, 0.24, 100)
    DrawMandelbrotSet(-0.733, 0.221, 200)


if __name__ == '__main__':
    DoMain()

