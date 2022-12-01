from gl import *

glCreateWindow(100, 100)
glClearColor(1, 1, 1)
# glColor(0, 1, 0)
glViewPort(20, 20, 50, 50)

'''
Parte Frontal
'''
glColor(0.83, 0.07, 0.01)
y1 = -0.85
y2 = -0.7

for i in range(10):
    y1 += 0.03
    y2 += 0.03
    glLine(-0.3, y1, 0, y2)


glColor(0.83, 0.07, 0.01)

y1 = -0.55
y2 = -0.15
for i in range(5):
    y1 += 0.03
    y2 += 0.03
    glLine(-0.3, y1, 0.5, y2)


y1 = -0.6
y2 = -0.45

for i in range(10):
    y1 += 0.03
    y2 += 0.03
    glLine(0.2, y1, 0.5, y2)


glLine(-0.3, -0.4, 0.5, 0)

x1 = -0.3
x1 -= 0.1
x2 = 0.5
y1 = -0.4
y2 = 0

for i in range(25):
    x1 += 0.012
    x2 -= 0.017
    y1 += 0.015
    y2 += 0.015
    glLine(x1, y1, x2, y2)

'''
Chimenea
'''

glColor(0.74, 0.09, 0.09)

y1 = 0.3
y2 = 0.15

for i in range(15):
    y1 += 0.03
    y2 += 0.03
    glLine(-0.5, y1, -0.3, y2)

glColor(0.83, 0.07, 0.01)

y1 = 0.15
y2 = 0.3

for i in range(17):
    y1 += 0.03
    y2 += 0.03
    glLine(-0.3, y1, -0.05, y2)

glColor(1, 0, 0)

x1 = -0.5
x2 = -0.25
y1 = 0.75
y2 = 0.99

for i in range(15):
    x1 += 0.01
    x2 += 0.015
    y1 -= 0.01
    y2 -= 0.01
    glLine(x1, y1, x2, y2)

'''
Techo de la casa
'''
glColor(1, 0, 0)

x1 = -1
x2 = -0.3
y1 = -0.05
y2 = -0.43

for i in range(90):
    x1 += 0.004
    x2 += 0.004
    y1 += 0.008
    y2 += 0.008
    glLine(x1, y1, x2, y2)

'''
Lado izquierdo
'''
glColor(0.74, 0.09, 0.09)

y1 = -0.5
y2 = -0.9

for i in range(15):
    y1 += 0.03
    y2 += 0.03
    glLine(-1, y1, -0.3, y2)


glFinish()
