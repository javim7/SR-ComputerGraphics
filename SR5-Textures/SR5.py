from gl import *
from render import *
from reader import *
from vector import *
from textures import *

'''
Dibujando los vectores de la textura
'''
glCreateWindow(2000, 2000)
glVector('ant')
glFinish('SR5Vectors')

'''
Aplicarle la textura al modelo
'''
glCreateWindow(1000, 1000)
glClearColor(0, 0, 0)
glColor(1, 0, 0)

glTexture('./models/ant.bmp')
glModel('./models/ant.obj', (400, 400, 500), (500, 100, 0))
glFinish('SR5')
