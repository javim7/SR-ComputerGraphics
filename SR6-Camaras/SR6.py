from gl import *
from render import *
from reader import *
from vector import *
from textures import *

'''
Medium Shot
'''
glCreateWindow(1000, 1000)
glClearColor(0, 0, 0)
glColor(1, 0, 0)

#eyes, center, up
glLookAt(V3(0, 0, 10), V3(0, 0, 0), V3(0, 1, 0).normalize())

glTexture('./models/Mask.bmp')
#translate, scale, rotate
glModel('./models/Mask.obj', (0, -0.1, 0), (10, 10, 10), (0, 0, 0))
glFinish('SR6-medium')

'''
Low Angle
'''
glCreateWindow(1024, 1024)
glClearColor(0, 0, 0)
glColor(1, 0, 0)

#eyes, center, up
glLookAt(V3(0, -7, 10), V3(0, 0, 0),  V3(0,  1, 0))

glTexture('./models/Mask.bmp')
#translate, scale, rotate
glModel('./models/Mask.obj', (0, -0.1, 0), (10, 10, 10), (0, 0, 0))
glFinish('SR6-low')

'''
High Angle
'''
glCreateWindow(1024, 1024)
glClearColor(0, 0, 0)
glColor(1, 0, 0)

#eyes, center, up
glLookAt(V3(0, 7, 10), V3(0, 0, 0),  V3(0, 1, 0))

glTexture('./models/Mask.bmp')
#translate, scale, rotate
glModel('./models/Mask.obj', (0, -0.1, 0), (10, 10, 10), (0, 0, 0))
glFinish('SR6-high')

'''
Dutch Angle
'''
glCreateWindow(1024, 1024)
glClearColor(0, 0, 0)
glColor(1, 0, 0)

#eyes, center, up
glLookAt(V3(0, 0, 10), V3(0, 0, 0.4).normalize(),
         V3(0.01, 0.01, 0).normalize())

glTexture('./models/Mask.bmp')
#translate, scale, rotate
glModel('./models/Mask.obj', (0, -0.1, 0), (10, 10, 10), (0, -pi/5, 0))
glFinish('SR6-dutch')
