def color(r, g, b):
  return bytes([b, g, r])

def color_range(r, g, b):
  return color(clamping(r*255), clamping(g*255), clamping(b*255))

def clamping(num):
    return int(max(min(num, 255), 0))

