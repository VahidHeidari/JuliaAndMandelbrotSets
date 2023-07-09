import os
import math

import bitmap
import mandelbrot



NUM_FRAMES = 30 * 4



def FillBitmap(bw, x, y, zoom, cr, ci):
    scale = 2.0 / min(bw.GetWidth(), bw.GetHeight()) / zoom
    x = x_start = x - (bw.GetWidth() / 2.0) * scale
    y = y + (bw.GetHeight() / 2.0) * scale
    c = mandelbrot.Z(0, 0)
    for j in range(bw.GetHeight()):
        for i in range(bw.GetWidth()):
            c = mandelbrot.Z(cr, ci)
            clr = mandelbrot.GetColor(c, x, y)
            bw.PutPixelInt(i, j, clr)
            x += scale
        x = x_start
        y -= scale


def DrawJulia(x, y, zoom, cr, ci):
    out_name = '%0.2f,%0.2f-%0.2f,%0.2f-%0.2f.bmp' % (cr, ci, x, y, zoom)
    out_path = os.path.join('julia', out_name)
    if not os.path.isdir('julia'):
        os.makedirs('julia')

    bw = bitmap.BitmapWriter(mandelbrot.IMG_WIDTH, mandelbrot.IMG_HEIGHT)
    FillBitmap(bw, x, y, zoom, cr, ci)
    bw.Save(out_path)


def DrawJuliaXY(x1, y1, x2, y2):
    base_dir = os.path.join('julia', 'animated')
    if not os.path.isdir(base_dir):
        os.makedirs(base_dir)
    bw = bitmap.BitmapWriter(mandelbrot.IMG_WIDTH, mandelbrot.IMG_HEIGHT)
    for i in range(NUM_FRAMES):
        cx = x1 + (x2 - x1) / float(NUM_FRAMES) * i
        cy = y1 + (y2 - y1) / float(NUM_FRAMES) * i
        FillBitmap(bw, 0, 0, 0.7, cx, cy)
        bw.Save(os.path.join(base_dir, '%03d.bmp' % i))


def DrawJuliaCircle(cx, cy, r):
    base_dir = os.path.join('julia', 'animated')
    if not os.path.isdir(base_dir):
        os.makedirs(base_dir)
    bw = bitmap.BitmapWriter(mandelbrot.IMG_WIDTH, mandelbrot.IMG_HEIGHT)
    for i in range(NUM_FRAMES):
        d_theta = 360.0 / float(NUM_FRAMES) * i
        # d / 180 = r / pi -> r = d * pi / 180
        theta = d_theta * math.pi / 180.0
        x = cx + r * math.cos(theta)
        y = cy + r * math.sin(theta)
        FillBitmap(bw, 0, 0, 0.7, x, y)
        bw.Save(os.path.join(base_dir, '%03d.bmp' % i))



def DoMain():
    # Wikipedia parameters
    # https://en.wikipedia.org/wiki/Julia_set
    DrawJulia(0, 0, 0.7, -0.5251993, -0.5251993)
    DrawJulia(0, 0, 0.7, -0.4, 0.6)
    DrawJulia(0, 0, 0.7, -0.7269, 0.1889)
    DrawJulia(0, 0, 0.7, 0.285, 0)
    DrawJulia(0, 0, 0.7, 0.285, 0.01)
    DrawJulia(0, 0, 0.7, 0.45, 0.1428)
    DrawJulia(0, 0, 0.7, -0.70176, -0.3842)
    DrawJulia(0, 0, 0.7, -0.835, -0.2321)
    DrawJulia(0, 0, 0.7, -0.8, 0.156)
    DrawJulia(0, 0, 0.7, 0, 0.8)
    DrawJulia(0, 0, 0.7, -0.74543, 0.11301)
    DrawJulia(0, 0, 0.7, -0.1, 0.651)

    DrawJulia(0, 0, 0.7, 0.4, 0.6)
    DrawJulia(0, 0, 0.7, -1.125, 0.21650635094611)

    DrawJuliaCircle(-0.2, 0, 0.7)


if __name__ == '__main__':
    DoMain()

