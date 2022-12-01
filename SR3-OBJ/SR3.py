from gl import *
from render import *
from reader import *

glCreateWindow(1300, 1300)
glClearColor(0, 0, 0)
glColor(1, 0, 0)


glModel('Pharaoh.obj', (100, 100, 0), (650, 0, 0))


glFinish()
