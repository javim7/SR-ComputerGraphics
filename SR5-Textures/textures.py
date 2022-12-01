import struct
from utilities import *
from render import *


class Texture:
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        with open(self.path, 'rb') as image:
            image.seek(2 + 4 + 2 + 2)
            header_size = struct.unpack('=l', image.read(4))[0]

            image.seek(2 + 4 + 2 + 2 + 4 + 4)
            self.width = struct.unpack('=l', image.read(4))[0]
            self.height = struct.unpack('=l', image.read(4))[0]

            image.seek(header_size)

            self.pixels = []
            for y in range(self.height):
                self.pixels.append([])
                for x in range(self.width):
                    b = ord(image.read(1))
                    g = ord(image.read(1))
                    r = ord(image.read(1))

                    self.pixels[y].append(
                        color(r, g, b)
                    )

    def get_color(self, tx, ty):
        x = round(tx * self.width)
        y = round(ty * self.height)

        return self.pixels[y][x]

    def get_color_with_intensity(self, tx, ty, intensity):
        x = round(tx * self.width)
        y = round(ty * self.height)

        b = round(self.pixels[y][x][0] * intensity)
        g = round(self.pixels[y][x][1] * intensity)
        r = round(self.pixels[y][x][2] * intensity)

        return color(r, g, b)

    # def generate_obj(self, modelo, scale_depth, translate_depth):
    #     model = Obj(modelo)

    #     for face in model.faces:

    #         if len(face) == 3:
    #             f1 = face[0][0] - 1
    #             f2 = face[1][0] - 1
    #             f3 = face[2][0] - 1

    #             vt1 = V3(*model.tvertices[f1])
    #             vt2 = V3(*model.tvertices[f1])
    #             vt3 = V3(*model.tvertices[f1])

    #             # self.triangle(vt1, vt2, vt3)
    #             self.line(vt1, vt2)
    #             self.line(vt2, vt3)
    #             self.line(vt3, vt1)
