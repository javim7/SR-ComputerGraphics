from utilities import *
from reader import *
from vector import *

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
        if(0 < x < self.width and 0 < y < self.height):
            self.framebuffer[x][y] = self.current_color

    def line(self, v1, v2):
        x0 = round(v1.x)
        x1 = round(v1.y)
        y0 = round(v2.x)
        y1 = round(v2.y)

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

        puntos = []
        for x in range(x0, x1 + 1):
            if steep:
                self.point(y, x)
                puntos.append((y, x))
            else:
                self.point(x, y)
                puntos.append((x, y))

            offset += dy * 2

            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += dx * 2

        # print(len(puntos), "len puntos")
        return puntos

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

    def transform_vertex(self, vertex, scale, translate):
        return [
            # primero movemos 0,0, luego escalamos y despues regresamos al centro
            (vertex[0] * scale[0]) + translate[0],
            (vertex[1] * scale[1]) + translate[1]
            # (vertex[2] * scale[2]) + translate[2]
        ]

    def generate_obj(self, modelo, scale_factor, translate_factor):
        model = Obj(modelo)

        for face in model.faces:

            if len(face) == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                v1 = self.transform_vertex(
                    model.vertices[f1], scale_factor, translate_factor)
                v2 = self.transform_vertex(
                    model.vertices[f2], scale_factor, translate_factor)
                v3 = self.transform_vertex(
                    model.vertices[f3], scale_factor, translate_factor)
                v4 = self.transform_vertex(
                    model.vertices[f4], scale_factor, translate_factor)

                self.line(V3(v1[0], v1[1]), V3(v2[0], v2[1]))
                self.line(V3(v2[0], v2[1]), V3(v3[0], v3[1]))
                self.line(V3(v3[0], v3[1]), V3(v4[0], v4[1]))
                self.line(V3(v4[0], v4[1]), V3(v1[0], v1[1]))

            else:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                v1 = self.transform_vertex(
                    model.vertices[f1], scale_factor, translate_factor)
                v2 = self.transform_vertex(
                    model.vertices[f2], scale_factor, translate_factor)
                v3 = self.transform_vertex(
                    model.vertices[f3], scale_factor, translate_factor)

                self.line(V3(v1[0], v1[1]), V3(v2[0], v2[1]))
                self.line(V3(v2[0], v2[1]), V3(v3[0], v3[1]))
                self.line(V3(v3[0], v3[1]), V3(v1[0], v1[1]))

    def triangle(self, A, B, C, col):
        self.current_color = col
        self.line(A, B)
        self.line(B, C)
        self.line(C, A)

        if A.y > B.y:
            A, B = B, A
        if A.y > C.y:
            A, C = C, A
        if B.y > C.y:
            B, C = C, B

        self.current_color = color(0, 0, 255)

        dx_ac = C.x - A.x
        dy_ac = C.y - A.y
        mi_ac = dx_ac / dy_ac

        if dy_ac == 0:
            return

        dx_ab = B.x - A.x
        dy_ab = B.y - A.y
        mi_ab = dx_ab / dy_ab

        dx_bc = C.x - B.x
        dy_bc = C.y = B.y
        mi_bc = dx_bc / dy_bc

        for y in range(A.y, B.y + 1):
            xi = round(A.x - mi_ac * (A.y - y))
            xf = round(A.x - mi_ab * (A.y - y))

            if xi > xf:
                xi, xf = xf, xi

            for x in range(xi, xf + 1):
                self.point(x, y)

        for y in range(B.y, C.y + 1):
            xi = round(A.x - mi_ac * (A.y - y))
            xf = round(B.x - mi_bc * (B.y - y))

            if xi > xf:
                xi, xf = xf, xi

            for x in range(xi, xf + 1):
                self.point(x, y)
