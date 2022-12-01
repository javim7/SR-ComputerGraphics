import struct
from color import color
from vector import * 

class Texture:
  def __init__(self, path):
    self.path = path
    self.read()
  
  def read(self):
    with open(self.path, "rb") as image:
      image.seek(10)
      header_size = struct.unpack("=l", image.read(4))[0]
      image.seek(18)
      self.width = struct.unpack("=l", image.read(4))[0]
      self.height = struct.unpack("=l", image.read(4))[0]

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

  def getColor(self, tx, ty):
    x = round(tx * self.width)
    y = round(ty * self.height)

    return self.pixels[y][x]

  def get_color_with_intensity(self, tx, ty, intensity):
    x = round(tx * self.width)
    y = round(ty * self.height)
    b = round(self.pixels[y][x][0] * intensity)
    g = round(self.pixels[y][x][1] * intensity)
    r = round(self.pixels[y][x][2] * intensity)
    #return color(255, 0, 0)
    return color(self.clamping(r), self.clamping(g), self.clamping(b))

  def clamping(self, num):
    return int(max(min(num, 255), 0))