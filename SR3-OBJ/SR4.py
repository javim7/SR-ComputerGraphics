from gl import *
from render import *
from reader import *
from vector import *

glCreateWindow(300, 300)
glClearColor(0, 0, 0)
glColor(1, 0, 0)


# glModel('Pharaoh.obj', (100, 100, 0), (650, 0, 0))

glLine(V3(10, 70), V3(50, 160))
glLine(V3(50, 160), V3(70, 80))
glLine(V3(70, 80), V3(10, 70))

glFinish()
