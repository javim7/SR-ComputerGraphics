from math import *
from utilities import *
from reader import *
from vector import *
from matrix import *
from textures import *
from progress.bar import Bar

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
RED = color(255, 0, 0)
BLUE = color(0, 0, 255)
GREEN = color(0, 255, 0)

size = 0


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
        self.shader = None
        self.vertex_array = []
        self.vertex_buffer_object = []
        self.clear()
        self.Model = None
        self.View = None
        self.light = V3(0, 0, 1)
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
        global size
        size = len(model.faces)
        bar = Bar('Generate Obj', max=len(model.faces))
        for face in model.faces:

            if len(face) == 4:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1
                f4 = face[3][0] - 1

                v1 = self.transform_vertex(model.vertices[f1])
                v2 = self.transform_vertex(model.vertices[f2])
                v3 = self.transform_vertex(model.vertices[f3])
                v4 = self.transform_vertex(model.vertices[f4])

                if self.texture and len(model.tvertices) != 0:
                    ft1 = face[0][1] - 1
                    ft2 = face[1][1] - 1
                    ft3 = face[2][1] - 1
                    ft4 = face[3][1] - 1

                    vt1 = V3(*model.tvertices[ft1])
                    vt2 = V3(*model.tvertices[ft2])
                    vt3 = V3(*model.tvertices[ft3])
                    vt4 = V3(*model.tvertices[ft4])

                    self.vertex_buffer_object.append(v1)
                    self.vertex_buffer_object.append(v2)
                    self.vertex_buffer_object.append(v3)

                    self.vertex_buffer_object.append(vt1)
                    self.vertex_buffer_object.append(vt2)
                    self.vertex_buffer_object.append(vt3)

                if self.shader:

                    fn1 = face[0][2] - 1
                    fn2 = face[1][2] - 1
                    fn3 = face[2][2] - 1

                    vn1 = V3(*model.nvertices[fn1])
                    vn2 = V3(*model.nvertices[fn2])
                    vn3 = V3(*model.nvertices[fn3])

                    self.vertex_buffer_object.append(vn1)
                    self.vertex_buffer_object.append(vn2)
                    self.vertex_buffer_object.append(vn3)

                self.vertex_buffer_object.append(v1)
                self.vertex_buffer_object.append(v3)
                self.vertex_buffer_object.append(v4)

                self.vertex_buffer_object.append(vt1)
                self.vertex_buffer_object.append(vt3)
                self.vertex_buffer_object.append(vt4)

                if self.shader:
                    fn1 = face[0][2] - 1
                    fn3 = face[2][2] - 1
                    fn4 = face[3][2] - 1

                    vn1 = V3(*model.nvertices[fn1])
                    vn3 = V3(*model.nvertices[fn3])
                    vn4 = V3(*model.nvertices[fn4])

                    self.vertex_buffer_object.append(vn1)
                    self.vertex_buffer_object.append(vn3)
                    self.vertex_buffer_object.append(vn4)

                else:
                    self.vertex_buffer_object.append(v1)
                    self.vertex_buffer_object.append(v2)
                    self.vertex_buffer_object.append(v3)

                    if self.shader:
                        fn1 = face[0][2] - 1
                        fn2 = face[1][2] - 1
                        fn3 = face[2][2] - 1
                        fn4 = face[3][2] - 1

                        vn1 = V3(*model.nvertices[fn1])
                        vn2 = V3(*model.nvertices[fn2])
                        vn3 = V3(*model.nvertices[fn3])
                        vn4 = V3(*model.nvertices[fn4])

                        self.vertex_buffer_object.append(vn1)
                        self.vertex_buffer_object.append(vn2)
                        self.vertex_buffer_object.append(vn3)

                        self.vertex_buffer_object.append(v1)
                        self.vertex_buffer_object.append(v3)
                        self.vertex_buffer_object.append(v4)

                    if self.shader:
                        fn1 = face[0][2] - 1
                        fn2 = face[1][2] - 1
                        fn3 = face[2][2] - 1
                        fn4 = face[3][2] - 1

                        vn1 = V3(*model.nvertices[fn1])
                        vn2 = V3(*model.nvertices[fn2])
                        vn3 = V3(*model.nvertices[fn3])
                        vn4 = V3(*model.nvertices[fn4])

                        self.vertex_buffer_object.append(vn1)
                        self.vertex_buffer_object.append(vn3)
                        self.vertex_buffer_object.append(vn4)

            if len(face) == 3 and len(model.tvertices) != 0:
                f1 = face[0][0] - 1
                f2 = face[1][0] - 1
                f3 = face[2][0] - 1

                v1 = self.transform_vertex(model.vertices[f1])
                v2 = self.transform_vertex(model.vertices[f2])
                v3 = self.transform_vertex(model.vertices[f3])

                self.vertex_buffer_object.append(v1)
                self.vertex_buffer_object.append(v2)
                self.vertex_buffer_object.append(v3)

                if self.texture:
                    ft1 = face[0][1] - 1
                    ft2 = face[1][1] - 1
                    ft3 = face[2][1] - 1

                    vt1 = V3(*model.tvertices[ft1])
                    vt2 = V3(*model.tvertices[ft2])
                    vt3 = V3(*model.tvertices[ft3])

                    self.vertex_buffer_object.append(vt1)
                    self.vertex_buffer_object.append(vt2)
                    self.vertex_buffer_object.append(vt3)

                fn1 = face[0][2] - 1
                fn2 = face[1][2] - 1
                fn3 = face[2][2] - 1

                vn1 = V3(*model.nvertices[fn1])
                vn2 = V3(*model.nvertices[fn2])
                vn3 = V3(*model.nvertices[fn3])

                self.vertex_buffer_object.append(vn1)
                self.vertex_buffer_object.append(vn2)
                self.vertex_buffer_object.append(vn3)

            bar.next()
        bar.finish()

    def draw(self, polygon):
        self.vertex_array = iter(self.vertex_buffer_object)
        global size
        bar = Bar('Draw', max=size)

        if polygon == 'TRIANGLES':
            try:
                while True:
                    self.triangle2Vectors()
                    bar.next()
            except StopIteration:
                print('Done.')
        bar.finish()
        if polygon == 'WIREFRAME':
            try:
                while True:
                    self.triangle_wireframe()
            except StopIteration:
                print(" done . ")

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

    def triangle_wireframe(self):
        A = next(self.vertex_array)
        B = next(self.vertex_array)
        C = next(self.vertex_array)

        if self.texture:
            tA = next(self.vertex_array)
            tB = next(self.vertex_array)
            tC = next(self.vertex_array)

        self.line(A, B)
        self.line(B, C)
        self.line(C, A)

    def triangle2Vectors(self):

        A = next(self.vertex_array)
        B = next(self.vertex_array)
        C = next(self.vertex_array)

        if self.texture:
            tA = next(self.vertex_array)
            tB = next(self.vertex_array)
            tC = next(self.vertex_array)

        nA = next(self.vertex_array)
        nB = next(self.vertex_array)
        nC = next(self.vertex_array)

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

                        self.current_color = self.shader(
                            self,
                            bar=(w, u, v),
                            vertices=(A, B, C),
                            texture_coords=(tA, tB, tC),
                            normals=(nA, nB, nC),
                            light=self.light,

                        )
                        self.point(y, x)
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
