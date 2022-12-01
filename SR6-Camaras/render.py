from math import *
from utilities import *
from reader import *
from vector import *
from matrix import *
from textures import *

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
        self.copiaZ = []
        self.texture = None
        self.clear()
        self.Model = None
        self.View = None
        # self.Projection = None

    def loadModelMatrix(self, translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):
        translate = V3(*translate)
        scale = V3(*scale)
        rotate = V3(*rotate)

        translation_matrix = matriz([
            [1, 0, 0, translate.x],
            [0, 1, 0, translate.y],
            [0, 0, 1, translate.z],
            [0, 0, 0,           1]
        ])

        scale_matrix = matriz([
            [scale.x, 0, 0, 0],
            [0, scale.y, 0, 0],
            [0, 0, scale.z, 0],
            [0, 0, 0, 1]
        ])

        a = rotate.x
        rotation_x = matriz([
            [1,      0,       0, 0],
            [0, cos(a), -sin(a), 0],
            [0, sin(a),  cos(a), 0],
            [0,      0,       0, 1]
        ])

        a = rotate.y
        rotation_y = matriz([
            [cos(a), 0, sin(a), 0],
            [0, 1,      0, 0],
            [-sin(a), 0, cos(a), 0],
            [0, 0,      0, 1]
        ])

        a = rotate.z
        rotation_z = matriz([
            [cos(a), -sin(a), 0, 0],
            [sin(a), cos(a), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        rotation_matrix = rotation_x * rotation_y * rotation_z

        self.Model = translation_matrix * rotation_matrix * scale_matrix

    def loadViewMatrix(self, x, y, z, center):

        Mi = matriz([
            [x.x, x.y, x.z, 0],
            [y.x, y.y, y.z, 0],
            [z.x, z.y, z.z, 0],
            [0, 0, 0, 1],
        ])

        Op = matriz([
            [1, 0, 0, -center.x],
            [0, 1, 0, -center.y],
            [0, 0, 1, -center.z],
            [0, 0, 0,         1]
        ])

        self.View = Mi * Op

    def loadProjectionViewMatrix(self, eyes, center):
        coeff = -1/(eyes.length() - center.length())
        self.Projection = matriz([
            [1, 0,      0, 0],
            [0, 1,      0, 0],
            [0, 0,      1, 0],
            [0, 0, coeff, 1]
        ])

    def loadViewPortMatrix(self, width=0, height=0):
        x = 0
        y = 0

        if width != 0:
            w = width
        else:
            w = self.width/2

        if height != 0:
            h = height
        else:
            h = self.height/2

        self.Viewport = matriz([
            [w, 0,   0, x + w],
            [0, h,   0, y + h],
            [0, 0, 128,   128],
            [0, 0,   0,     1]
        ])

    def lookAt(self, eyes, center, up):

        z = (eyes-center).normalize()
        x = (up * z).normalize()
        y = (z * x).normalize()

        self.loadViewMatrix(x, y, z, center)
        self.loadProjectionViewMatrix(eyes, center)
        self.loadViewPortMatrix()

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
        for y in range(self.height):
            for x in range(self.width):
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
                self.point(x, y)
            else:
                self.point(y, x)

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

    def transform_vertex(self, vertex):
        augmented_vertex = matriz([
            [vertex[0]],
            [vertex[1]],
            [vertex[2]],
            [1]
        ])

        if(self.View and self.Projection):
            transformed_vertex = (self.Viewport * self.Projection *
                                  self.View * self.Model * augmented_vertex).matriz
        else:
            transformed_vertex = (self.Model * augmented_vertex).matriz

        return V3(
            transformed_vertex[0][0] / transformed_vertex[3][0],
            transformed_vertex[1][0] / transformed_vertex[3][0],
            transformed_vertex[2][0] / transformed_vertex[3][0],
        )

    def generate_obj(self, modelo,  translate=(0, 0, 0), scale=(1, 1, 1), rotate=(0, 0, 0)):

        self.loadModelMatrix(translate, scale, rotate)
        model = Obj(modelo)

        for face in model.faces:

            if len(face) == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                v1 = self.transform_vertex(
                    model.vertices[f1])
                v2 = self.transform_vertex(
                    model.vertices[f2])
                v3 = self.transform_vertex(
                    model.vertices[f3])
                v4 = self.transform_vertex(
                    model.vertices[f4])

                if self.texture and len(model.tvertices) != 0:
                    ft1 = face[0][1] - 1
                    ft2 = face[1][1] - 1
                    ft3 = face[2][1] - 1
                    ft4 = face[3][1] - 1

                    vt1 = V3(*model.tvertices[ft1])
                    vt2 = V3(*model.tvertices[ft2])
                    vt3 = V3(*model.tvertices[ft3])
                    vt4 = V3(*model.tvertices[ft4])

                    # self.triangle2Vectors((v1, v2, v3), (vt1, vt2, vt3))
                    # self.triangle2Vectors((v1, v3, v4), (vt1, vt3, vt4))
                    self.cube((v1, v2, v3, v4), (vt1, vt2, vt3, vt4))
                else:
                    # self.triangle2Vectors((v1, v2, v3))
                    # self.triangle2Vectors((v1, v3, v4))

                    self.cube(v1, v2, v3, v4)

            if len(face) == 3:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                v1 = self.transform_vertex(
                    model.vertices[f1])
                v2 = self.transform_vertex(
                    model.vertices[f2])
                v3 = self.transform_vertex(
                    model.vertices[f3])

                if self.texture and len(model.tvertices) != 0:
                    ft1 = face[0][1] - 1
                    ft2 = face[1][1] - 1
                    ft3 = face[2][1] - 1

                    vt1 = V3(*model.tvertices[ft1])
                    vt2 = V3(*model.tvertices[ft2])
                    vt3 = V3(*model.tvertices[ft3])

                    self.triangle2Vectors((v1, v2, v3), (vt1, vt2, vt3))
                else:
                    self.triangle2Vectors((v1, v2, v3))

    def generateVectors(self, model):

        t = Texture('./models/' + model + '.bmp')
        self.framebuffer = t.pixels
        self.texture = Texture('./models/' + model + '.bmp')
        self.current_color = color(255, 255, 255)

        model = Obj('./models/' + model + '.obj')

        for face in model.faces:

            if len(face) == 4:
                ft1 = face[0][1] - 1
                ft2 = face[1][1] - 1
                ft3 = face[2][1] - 1
                ft4 = face[3][1] - 1

                vt1 = V3(
                    model.tvertices[ft1][0] * t.width,
                    model.tvertices[ft1][1] * t.width
                )
                vt2 = V3(
                    model.tvertices[ft2][0] * t.width,
                    model.tvertices[ft2][1] * t.width
                )
                vt3 = V3(
                    model.tvertices[ft3][0] * t.width,
                    model.tvertices[ft3][1] * t.width
                )
                vt4 = V3(
                    model.tvertices[ft4][0] * t.width,
                    model.tvertices[ft4][1] * t.width
                )

                self.line(vt1, vt2)
                self.line(vt2, vt3)
                self.line(vt3, vt4)
                self.line(vt4, vt1)

            if len(face) == 3:
                ft1 = face[0][1] - 1
                ft2 = face[1][1] - 1
                ft3 = face[2][1] - 1

                vt1 = V3(
                    model.tvertices[ft1][0] * t.width,
                    model.tvertices[ft1][1] * t.width
                )
                vt2 = V3(
                    model.tvertices[ft2][0] * t.width,
                    model.tvertices[ft2][1] * t.width
                )
                vt3 = V3(
                    model.tvertices[ft3][0] * t.width,
                    model.tvertices[ft3][1] * t.width
                )

                self.line(vt1, vt2)
                self.line(vt2, vt3)
                self.line(vt3, vt1)

    def prodPunto(self, v1, v2):
        return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

    def triangle(self, A, B, C):

        Light = V3(0, 0, -1)
        N = (B - A) * (C-A)
        intensity = N.normalize() @ Light.normalize()

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

                if (x < len(self.zBuffer) and y < len(self.zBuffer[0]) and self.zBuffer[x][y] < z):
                    self.zBuffer[x][y] = z
                    # self.zBufferClear[x][y] = color(
                    #     self.clamping(depth*255),
                    #     self.clamping(depth*255),
                    #     self.clamping(depth*255)
                    # )
                    self. point(x, y)

    def triangle2Vectors(self, vertices, tvertices=()):

        A, B, C = vertices

        if self.texture:
            tA, tB, tC = tvertices

        Light = V3(0, 0, 1)
        N = (B - A) * (C-A)
        intensity = N.normalize() @ Light.normalize()

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

                z = A.z * w + B.z * v + C.z * u
                depth = z/self.width
                try:
                    if (self.zBuffer[x][y] < z):
                        self.zBuffer[x][y] = z
                        self.zBufferClear[x][y] = color(
                            self.clamping(depth*255),
                            self.clamping(depth*255),
                            self.clamping(depth*255)
                        )

                        if self.texture and tvertices != 0:
                            tx = tA.x * w + tB.x * u + tC.x * v
                            ty = tA.y * w + tB.y * u + tC.y * v

                            self.current_color = self.texture.get_color_with_intensity(
                                tx, ty, intensity)
                        self. point(y, x)
                except:
                    continue

    def cube(self, vertices, tvertices=()):
        A, B, C, D = vertices

        if self.texture and tvertices != 0:
            tA, tB, tC, tD = tvertices

            self.triangle2Vectors((A, B, C), (tA, tB, tC))
            self.triangle2Vectors((A, C, D), (tA, tC, tD))
        else:
            self.triangle2Vectors((A, B, C))
            self.triangle2Vectors((A, C, D))
