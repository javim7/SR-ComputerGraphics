from utilities import *

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)


class Render(object):
    def __init__(self, width, height):
        self.width = width  # ancho de la ventana
        self.height = height  # ancho de la ventana
        self.current_color = WHITE  # color default de la ventana
        self.clear_color = BLACK  # color para hacerle clear a la ventana
        self.viewX = 0
        self.viewY = 0
        self.viewWidth = 0
        self.viewHeight = 0
        self.clear()

    def clear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]

    def write(self, filename):
        f = open(filename, 'bw')

        # pixel header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(word(0))
        f.write(word(0))
        f.write(dword(14 + 40))

        # info header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        # pixel data
        for x in range(self.height):
            for y in range(self.width):
                f.write(self.framebuffer[y][x])

        f.close()

    def point(self, x, y):
        self.framebuffer[x][y] = self.current_color

    def line(self, x0, y0, x1, y1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        # Si es empinado, poco movimiento en x y mucho en y.
        steep = dy > dx

        # Se invierte si es empinado
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        # Si la linea tiene direccion contraria, invertir
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        threshold = dx
        y = y0

        for x in range(x0, x1):
            if steep:
                self.point(y, x)
            else:
                self.point(x, y)

            offset += dy * 2

            if offset >= threshold:
                y += 1 if y0 < y1 else -1

                threshold += dx * 2

    def cordsFinales(self, x, y):
        viewX = self.viewX
        viewY = self.viewY
        ancho = self.viewWidth
        alto = self.viewHeight

        medioX = round(viewX + (ancho/2))
        medioY = round(viewY + (alto/2))

        x = medioX + round(x * (ancho / 2))
        y = medioY + round(y * (alto / 2))

        return [x, y]
