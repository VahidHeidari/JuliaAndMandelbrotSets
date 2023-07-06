import os

import bitmap
import mandelbrot



def DrawJulia(x, y, zoom, cr, ci):
    out_name = '%0.2f,%0.2f-%0.2f,%0.2f-%0.2f.bmp' % (cr, ci, x, y, zoom)
    out_path = os.path.join('julia', out_name)
    if not os.path.isdir('julia'):
        os.makedirs('julia')

    bw = bitmap.BitmapWriter(mandelbrot.IMG_WIDTH, mandelbrot.IMG_HEIGHT)

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

    bw.Save(out_path)



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


if __name__ == '__main__':
    DoMain()

