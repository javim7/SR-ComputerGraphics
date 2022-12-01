from utilities import *
from reader import *
from vector import *

import random
from numpy.linalg import norm

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
RED = color(255, 0, 0)
BLUE = color(0, 0, 255)
GREEN = color(0, 255, 0)


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
        self.copiaZ = []

    def clamping(self, num):
        return int(max(min(num, 255), 0))

    def clear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]
        self.zBufferClear = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]
        self.zBuffer = [
            [-9999 for x in range(self.width)]
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

    def write2(self, filename):
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
                f.write(self.zBufferClear[y][x])

        f.close()

    def point(self, x, y):
        if(0 < x < self.width and 0 < y < self.height):
            self.framebuffer[x][y] = self.current_color

    def line(self, v1, v2):
        x0 = round(v1.x)
        y0 = round(v1.y)
        x1 = round(v2.x)
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

        for x in range(x0, x1 + 1):
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

    def transform_vertex(self, vertex, scale, translate):
        return V3(
            # primero movemos 0,0, luego escalamos y despues regresamos al centro
            (vertex[0] * scale[0]) + translate[0],
            (vertex[1] * scale[1]) + translate[1],
            (vertex[2] * scale[2]) + translate[2]
        )

    def generate_obj(self, modelo, scale_depth, translate_depth):
        model = Obj(modelo)

        for face in model.faces:

            if len(face) == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                v1 = self.transform_vertex(
                    model.vertices[f1], scale_depth, translate_depth)
                v2 = self.transform_vertex(
                    model.vertices[f2], scale_depth, translate_depth)
                v3 = self.transform_vertex(
                    model.vertices[f3], scale_depth, translate_depth)
                v4 = self.transform_vertex(
                    model.vertices[f4], scale_depth, translate_depth)

                self.cube(v1, v2, v3, v4)

            else:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                v1 = self.transform_vertex(
                    model.vertices[f1], scale_depth, translate_depth)
                v2 = self.transform_vertex(
                    model.vertices[f2], scale_depth, translate_depth)
                v3 = self.transform_vertex(
                    model.vertices[f3], scale_depth, translate_depth)

                self.triangle(v1, v2, v3)

    def prodPunto(self, v1, v2):
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

    def triangle(self, A, B, C):

        Light = V3(0, 0, -1)
        N = (B - A) * (C-A)
        intensity = self.prodPunto(N.normalize(), Light.normalize())

        if intensity > 1 or intensity <= 0:
            return

        grey = round(255 * intensity)
        self.current_color = color(
            grey, grey, grey
        )

        Bmin, Bmax = bounding_box(A, B, C)
        Bmin.round()
        Bmax.round()
        for x in range((Bmin.x), Bmax.x + 1):
            for y in range(Bmin.y, Bmax.y + 1):
                w, v, u = barycentric(A, B, C, V3(x, y))

                if (w < 0 or v < 0 or u < 0):
                    continue

                z = A.z * v + B.z * u + C.z * w
                depth = z/self.width

                if (self.zBuffer[x][y] < z):
                    self.zBuffer[x][y] = z
                    self.zBufferClear[x][y] = color(
                        self.clamping(depth*255),
                        self.clamping(depth*255),
                        self.clamping(depth*255)
                    )
                    self. point(x, y)

    def triangle2(self, A, B, C):

        A.round()
        B.round()
        C.round()

        if A.y > B.y:
            A, B = B, A
        if A.y > C.y:
            A, C = C, A
        if B.y > C.y:
            B, C = C, B

        self.current_color = color(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

        dx_ac = C.x - A.x
        dy_ac = C.y - A.y

        if dy_ac == 0:
            return

        mi_ac = dx_ac / dy_ac

        dx_ab = B.x - A.x
        dy_ab = B.y - A.y

        if dy_ab != 0:

            mi_ab = dx_ab / dy_ab

            for y in range(A.y, B.y + 1):
                xi = round(A.x - mi_ac * (A.y - y))
                xf = round(A.x - mi_ab * (A.y - y))

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi, xf + 1):
                    self.point(x, y)

        dx_bc = C.x - B.x
        dy_bc = C.y - B.y

        if dy_bc != 0:

            mi_bc = dx_bc / dy_bc

            for y in range(B.y, C.y + 1):
                xi = round(A.x - mi_ac * (A.y - y))
                xf = round(B.x - mi_bc * (B.y - y))

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi, xf + 1):
                    self.point(x, y)

    def cube(self, A, B, C, D):
        self.triangle(A, B, C)
        self.triangle(B, C, D)
