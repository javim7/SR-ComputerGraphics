'''
Importando librerias externas
'''
import random
from gl import *


'''
Creando el viewport
'''
glCreateWindow(1000, 1000)
glClearColor(0, 0, 0)
glClear()


'''
Shader a utilizar
'''


def jupiter(**kwargs):
    Light = kwargs['light']
    w, u, v = kwargs['bar']
    y = kwargs['height']
    x = kwargs['width']
    nA, nB, nC = kwargs['normals']

    iA = nA.normalize() @ Light.normalize()
    iB = nB.normalize() @ Light.normalize()
    iC = nC.normalize() @ Light.normalize()

    i = iA * w + iB * u + iC * v

    if y >= 375 and y <= 390 and x >= 330 and x <= 345:
        return color(clamping(0*-i), clamping(0*-i), clamping(0*-i))
    if y <= 230:
        return color(clamping(172*-i), clamping(124*-i), clamping(74*-i))
    if y > 230 and y <= 275:
        return color(clamping(152*-i), clamping(104*-i), clamping(54*-i))
    if y > 275 and y <= 295:
        return color(clamping(172*-i), clamping(143*-i), clamping(100*-i))
    if y > 295 and y <= 345:
        return color(clamping(156*-i), clamping(136*-i), clamping(103*-i))
    if y > 345 and y <= 390:
        return color(clamping(183*-i), clamping(201*-i), clamping(229*-i))
    if y >= 420 and y <= 425 and x >= 500 and x <= 650:
        return color(clamping(183*-i), clamping(201*-i), clamping(229*-i))
    if y >= 390 and y <= 450:
        return color(clamping(182*-i), clamping(143*-i), clamping(100*-i))
    if y >= 470 and y <= 477 and x >= 200 and x <= 550:
        return color(clamping(255*-i), clamping(255*-i), clamping(255*-i))
    if y >= 475 and y <= 485 and x >= 650 and x <= 800:
        return color(clamping(255*-i), clamping(255*-i), clamping(255*-i))
    if y > 450 and y <= 515:
        return color(clamping(183*-i), clamping(201*-i), clamping(229*-i))
    if y > 515 and y <= 570:
        return color(clamping(212*-i), clamping(148*-i), clamping(63*-i))
    if y > 570 and y <= 600:
        return color(clamping(183*-i), clamping(201*-i), clamping(229*-i))
    if y > 600 and y <= 625:
        return color(clamping(172*-i), clamping(143*-i), clamping(100*-i))
    if y > 625 and y <= 635:
        return color(clamping(183*-i), clamping(201*-i), clamping(229*-i))
    if y > 635:
        return color(clamping(172*-i), clamping(143*-i), clamping(100*-i))
    else:
        return color(clamping(255*-i), clamping(255*-i), clamping(255*-i))


'''
Dibujando background del espacio con estrellas
'''
for i in range(2000):
    glColor(random.randint(
        210, 255), random.randint(210, 255), random.randint(210, 255))

    x = random.randint(0, 1000)
    y = random.randint(0, 1000)
    glPoint(x, y)

'''
Camara y modelo
'''
glViewPort(0, 0, 1000, 1000)
glLookAt((0, 0, 100), (0, 0, 0), (0, 1, 0))
glShader(jupiter)
glRenderObject('./models/Sphere.obj', scale=(0.00085,
               0.00085, 0.00085), translate=(0, 0, 0), rotate=(0, 0, 0))


'''
Dibujando la imagen
'''
glFinish('jupiter-lab2')
