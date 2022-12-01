from color import * 

class Material(object):
  def __init__(self, filename):

    with open(filename) as f:
      self.lines = f.read().splitlines()

    self.materials = {}
    self.current_material = None

    for line in self.lines:

      if line:

        if ' ' not in line:
          continue

        prefix, value = line.split(' ', 1)

        if prefix == 'Kd':
          self.materials [self.current_material] = {
            'difuse': color_range(*(float(x) for x in value.split(' ')))
          }

        if prefix == 'newmtl':
          self.current_material = value

