from math import *
from utilities import *
from matrix import matriz
import color as c
from vector import V3
import Obj


class Render(object):

    def __repr__(self):
        return "render %s x %s " % (self.width, self.height)

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.current_color = c.color(0, 0, 0)
        self.clear_color = c.color(255, 255, 255)
        self.texture = None
        self.material = None
        self.Model = None
        self.light = V3(0, 0, -1)
        self.View = None
        self.Projection = None
        self.active_shader = None
        self.vertex_buffer_object = []
        self.normal_map = None
        self.clear()

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

        O = matriz([
            [1, 0, 0, -center.x],
            [0, 1, 0, -center.y],
            [0, 0, 1, -center.z],
            [0, 0, 0,         1]
        ])

        self.View = Mi * O

    def loadProjectionViewMatrix(self, eyes, center):
        coeff = -1/(eyes.length() - center.length())
        self.Projection = matriz([
            [1, 0,      0, 0],
            [0, 1,      0, 0],
            [0, 0,      1, 0],
            [0, 0, coeff, 1]
        ])

    def loadViewportMatrix(self, width=0, height=0):
        x = 0
        y = 0
        w = width if width != 0 else self.width/2
        h = height if height != 0 else self.height/2

        self.Viewport = matriz([
            [w, 0,   0, x + (w/2)],
            [0, h,   0, y + (h/2)],
            [0, 0, 128,   128],
            [0, 0,   0,     1]
        ])

    def lookAt(self, eyes, center, up):
        eyes = V3(*eyes)
        center = V3(*center)
        up = V3(*up)

        z = (eyes - center).normalize()
        x = (up * z).normalize()
        y = (z * x).normalize()

        self.loadViewMatrix(x, y, z, center)
        self.loadProjectionViewMatrix(eyes, center)

    def clear(self):
        self.framebuffer = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]

        self.zBuffer = [
            [-9999999 for x in range(self.width)]
            for y in range(self.height)
        ]

        self.zClear = [
            [self.clear_color for x in range(self.width)]
            for y in range(self.height)
        ]

    def clamping(self, num):
        return int(max(min(num, 255), 0))

    def set_clear_color(self, r, g, b):
        adjusted_r = self.clamping(r * 255)
        adjusted_g = self.clamping(g * 255)
        adjusted_b = self.clamping(b * 255)
        self.clear_color = c.color(adjusted_r, adjusted_g, adjusted_b)

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

    def write_z(self, filename):
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
                f.write(self.zClear[y][x])

        f.close()

    def set_current_color(self, r, g, b):
        adjusted_r = self.clamping(r * 255)
        adjusted_g = self.clamping(g * 255)
        adjusted_b = self.clamping(b * 255)
        self.current_color = c.color(adjusted_r, adjusted_g, adjusted_b)

    def point(self, x, y):
        if x >= 0 and x < self.width and y >= 0 and y < self.height:
            self.framebuffer[x][y] = self.current_color

    def convert_coordinates(self, x, y):
        if x < -1 or x > 1 or y < -1 or y > 1:
            return

        adjusted_x = x + 1
        adjusted_y = y + 1

        converted_x = (adjusted_x * self.viewport_param["width"])/2
        converted_y = (adjusted_y * self.viewport_param["height"])/2

        final_x = int(converted_x + self.viewport_param["x"])
        final_y = int(converted_y + self.viewport_param["y"])

        return final_x, final_y

    def lineVector(self, v1, v2):
        x0 = round(v1.x)
        x1 = round(v2.x)
        y0 = round(v1.y)
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

        for x in range(x0, x1 + 1):
            if steep:
                self.point(y, x)
            else:
                self.point(x, y)

            offset += dy * 2

            if offset >= threshold:
                y += 1 if y0 < y1 else -1

                threshold += dx * 2

    def transform_vertex(self, vertex):
        augmented_vertex = matriz([
            [vertex[0]],
            [vertex[1]],
            [vertex[2]],
            [1]
        ])

        if(self.View and self.Projection):
            transformed_vertex = self.Viewport * self.Projection * \
                self.View * self.Model * augmented_vertex
        else:
            transformed_vertex = self.Model * augmented_vertex

        transformed_vertex = transformed_vertex.matriz

        return V3(
            transformed_vertex[0][0] / transformed_vertex[3][0],
            transformed_vertex[1][0] / transformed_vertex[3][0],
            transformed_vertex[2][0] / transformed_vertex[3][0],
        )

    def bounding_box(self, A, B, C):
        coords = [(A.x, A.y), (B.x, B.y), (C.x, C.y)]

        xmin = 999999
        xmax = -999999
        ymin = 999999
        ymax = -999999

        for (x, y) in coords:
            if x < xmin:
                xmin = x
            if x > xmax:
                xmax = x
            if y < ymin:
                ymin = y
            if y > ymax:
                ymax = y

        return V3(xmin, ymin), V3(xmax, ymax)

    def cross(self, v1, v2):
        return (
            v1.y * v2.z - v1.z * v2.y,
            v1.z * v2.x - v1.x * v2.z,
            v1.x * v2.y - v1.y * v2.x
        )

    def barycentric(self, A, B, C, P):
        cx, cy, cz = self.cross(
            V3(B.x - A.x, C.x - A.x, A.x - P.x),
            V3(B.y - A.y, C.y - A.y, A.y - P.y)
        )
        if cz == 0:
            return(-1, -1, -1)

        u = cx / cz
        v = cy / cz
        w = 1 - (cx/cz + cy/cz)

        return (w, v, u)

    def triangle(self):

        A = next(self.vertex_buffer_object)
        B = next(self.vertex_buffer_object)
        C = next(self.vertex_buffer_object)

        if self.texture:
            tA = next(self.vertex_buffer_object)
            tB = next(self.vertex_buffer_object)
            tC = next(self.vertex_buffer_object)

        if self.active_shader:
            nA = next(self.vertex_buffer_object)
            nB = next(self.vertex_buffer_object)
            nC = next(self.vertex_buffer_object)

        Bmin, Bmax = self.bounding_box(A, B, C)

        L = self.light
        N = (C - A) * (B - A)
        L = V3(0, 0, -1)
        i = N.normalize() @ L.normalize()

        for x in range(round(Bmin.x), round(Bmax.x) + 1):
            for y in range(round(Bmin.y), round(Bmax.y) + 1):

                w, v, u = self.barycentric(A, B, C, V3(x, y))
                if (w < 0 or v < 0 or u < 0):
                    continue

                z = A.z * w + B.z * u + C.z * v
                factor = z/self.width

                if (self.zBuffer[x][y] <= z):
                    self.zBuffer[x][y] = z
                    self.zClear[x][y] = c.color_range(factor, factor, factor)

                    if self.normal_map:

                        tx = tA.x * w + tB.x * u + tC.x * v
                        ty = tA.y * w + tB.y * u + tC.y * v

                        normal_color = self.normal_map.get_color_with_intensity(
                            tx, ty, 1)
                        #normal_color = normal_color.normalize()
                        #print(normal_color[0], normal_color[1], normal_color[2])

                        i = V3(normal_color[2], normal_color[1],
                               normal_color[0]).normalize() @ L.normalize()
                        i *= -1
                        self.current_color = self.texture.get_color_with_intensity(
                            tx, ty, i)

                    else:

                        if(self.active_shader):
                            self.current_color = self.active_shader(
                                bar=(w, u, v),
                                vertices=(A, B, C),
                                texture_coords=(
                                    tA, tB, tC) if self.texture else None,
                                normals=(nA, nB, nC),
                                light=L,
                                texture=self.texture,
                                height=y,
                                width=x
                            )

                        else:

                            if self.texture:

                                tx = tA.x * w + tB.x * u + tC.x * v
                                ty = tA.y * w + tB.y * u + tC.y * v
                                self.current_color = self.texture.get_color_with_intensity(
                                    tx, ty, i)

                            else:

                                if i <= 0 or i > 1:
                                    return

                                grey = round(255 * i)
                                self.current_color = c.color(grey, grey, grey)

                    self.point(y, x)

    def generate_object(self, modelo, scale=(0, 0, 0), translate=(0, 0, 0), rotate=(0, 0, 0)):

        self.loadModelMatrix(translate, scale, rotate)
        model = Obj.Obj(modelo)

        for faceDict in model.faces:

            face = faceDict['face']
            if len(face) == 4:
                v1 = self.transform_vertex(model.vertices[face[0][0] - 1])
                v2 = self.transform_vertex(model.vertices[face[1][0] - 1])
                v3 = self.transform_vertex(model.vertices[face[2][0] - 1])
                v4 = self.transform_vertex(model.vertices[face[3][0] - 1])

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

                    if (len(model.nvertices) != 0 and self.active_shader):

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

                    if (len(model.nvertices) != 0 and self.active_shader):

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

                    if (len(model.nvertices) != 0 and self.active_shader):
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

                    if (len(model.nvertices) != 0 and self.active_shader):
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

            if len(face) == 3:
                v1 = self.transform_vertex(model.vertices[face[0][0] - 1])
                v2 = self.transform_vertex(model.vertices[face[1][0] - 1])
                v3 = self.transform_vertex(model.vertices[face[2][0] - 1])

                if self.texture and len(model.tvertices) != 0:

                    ft1 = face[0][1] - 1
                    ft2 = face[1][1] - 1
                    ft3 = face[2][1] - 1

                    vt1 = V3(*model.tvertices[ft1])
                    vt2 = V3(*model.tvertices[ft2])
                    vt3 = V3(*model.tvertices[ft3])

                    self.vertex_buffer_object.append(v1)
                    self.vertex_buffer_object.append(v2)
                    self.vertex_buffer_object.append(v3)
                    self.vertex_buffer_object.append(vt1)
                    self.vertex_buffer_object.append(vt2)
                    self.vertex_buffer_object.append(vt3)

                else:
                    self.vertex_buffer_object.append(v1)
                    self.vertex_buffer_object.append(v2)
                    self.vertex_buffer_object.append(v3)

                if (len(model.nvertices) != 0 and self.active_shader):
                    fn1 = face[0][2] - 1
                    fn2 = face[1][2] - 1
                    fn3 = face[2][2] - 1

                    vn1 = V3(*model.nvertices[fn1])
                    vn2 = V3(*model.nvertices[fn2])
                    vn3 = V3(*model.nvertices[fn3])

                    self.vertex_buffer_object.append(vn1)
                    self.vertex_buffer_object.append(vn2)
                    self.vertex_buffer_object.append(vn3)

        self.draw()

    def draw(self):
        self.vertex_buffer_object = iter(self.vertex_buffer_object)
        try:
            while(True):
                self.triangle()
        except StopIteration:
            pass
