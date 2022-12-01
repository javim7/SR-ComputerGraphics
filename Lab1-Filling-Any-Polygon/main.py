from gl import *
from render import *

glCreateWindow(800, 800)
glClearColor(1, 1, 1)

'''
Listas de los poligonos
'''
poligono1 = [(165, 380), (185, 360), (180, 330), (207, 345), (233, 330),
             (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]

poligono2 = [(321, 335), (288, 286), (339, 251), (374, 302)]

poligono3 = [(377, 249), (411, 197), (436, 249)]

poligono4 = [(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52), (750, 145), (761, 179),
             (672, 192), (659, 214), (615, 214), (632, 230), (580, 230), (597, 215), (552, 214), (517, 144), (466, 180)]

poligono5 = [(682, 175), (708, 120), (735, 148), (739, 170)]


'''
Funcion fill
'''


def fillPolygon(poligono):

    # separando las tuplas en listas de x, y
    listax = []
    listay = []
    for elemento in poligono:
        listax.append(elemento[0])
        listay.append(elemento[1])

    # encontrando los puntos minimos y maximos
    yMin = min(listay)
    yMax = max(listay)
    xMin = min(listax)
    xMax = max(listax)

    # haciendo un cuadrado al rededor del polygon
    # glColor(0, 1, 0)
    # for j in range(xMin, xMax + 1):
    #     for k in range(yMin, yMax + 1):
    #         glVertex(j, k)

    # pintando los puntos
    # glColor(0, 0, 1)
    for i in range(len(listax)):
        glVertex(listax[i], listay[i])

    intersecciones = []
    # conectando los puntos
    for i in range(len(poligono)):
        if i == len(poligono) - 1:
            intersecciones.append(glLine(poligono[i][0], poligono[i][1],
                                         poligono[0][0], poligono[0][1]))
        else:
            intersecciones.append(glLine(poligono[i][0], poligono[i][1],
                                         poligono[i + 1][0], poligono[i + 1][1]))

    # hacienda la lista de intersecciones en una sola lista
    flat_intersecciones = [
        interseccion for lista in intersecciones for interseccion in lista]

    # lista vacia para almacenar las intersecciones actuales
    ints = []

    # forloop para hacedr el scan line
    for y in range(yMin, yMax + 1):
        for x in range(xMin, xMax + 1):
            # print(x, y)
            if (x, y) in flat_intersecciones:
                ints.append((x, y))
        # print(ints)
        for i in range(len(ints) - 1, -1, -1):
            try:
                # print(ints[i][0] - ints[i-1][0])
                if ints[i][0] - ints[i-1][0] == 1:
                    ints.remove(ints[i])
            except:
                pass
        # print(ints)
        separados = [ints[i:i + 2] for i in range(0, len(ints), 2)]
        # print(separados)
        ints = []
        # print(separados[0][0][0], separados[0][0][1],
        #       separados[0][1][0], separados[0][1][1])
        if len(separados[0]) > 1:
            for lista in range(len(separados)):
                # print(lista)
                # print(len(separados))
                if lista == len(separados)-1 and len(separados[lista]) % 2 != 0:
                    glLine(separados[lista-1][1][0], separados[lista-1][1][1],
                           separados[lista][0][0], separados[lista][0][1])
                else:
                    glLine(separados[lista][0][0], separados[lista][0][1],
                           separados[lista][1][0], separados[lista][1][1])

    glColor(1, 0, 0)
    # print(flat_intersecciones)
    for punto in flat_intersecciones:
        # print(punto[0], punto[1])
        glVertex(punto[0], punto[1])
    for i in range(len(listax)):
        glVertex(listax[i], listay[i])


'''
Llamando a la funcion con cada poligono
'''
glColor(0, 0, 1)
fillPolygon(poligono1)
glColor(0, 0, 1)
fillPolygon(poligono2)
glColor(0, 0, 1)
fillPolygon(poligono3)
glColor(0, 0, 1)
fillPolygon(poligono4)
glColor(1, 1, 1)
fillPolygon(poligono5)

glFinish()
