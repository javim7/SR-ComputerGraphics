from vector import *
import struct


def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))


def word(w):
    # 2 bytes
    return struct.pack('=h', w)


def dword(d):
    # 4 bytes
    return struct.pack('=l', d)


def color(r, g, b):
    return bytes([b, g, r])


def bounding_box(A, B, C):
    coordenadas = [(A.x, A.y), (B.x, B.y), (C.x, C.y)]

    xmin = 999999
    xmax = -999999
    ymin = 999999
    ymax = -999999

    for (x, y) in coordenadas:
        if x < xmin:
            xmin = x
        if x > xmax:
            xmax = x
        if y < ymin:
            ymin = y
        if y > ymax:
            ymax = y

    return V3(xmin, ymin), V3(xmax, ymax)


def crossProdcut(v1, v2):
    return (
        v1.y * v2.z - v1.z * v2.y,
        v1.z * v2.x - v1.x * v2.z,
        v1.x * v2.y - v1.y * v2.x
    )


def barycentric(A, B, C, P):
    cx, cy, cz = crossProdcut(
        V3(B.x - A.x, C.x - A.x, A.x - P.x),
        V3(B.y - A.y, C.y - A.y, A.y - P.y)
    )
    try:
        u = cx / cz
        v = cy / cz
        w = 1 - (u + v)

        return (w, v, u)

    except:
        u = -1
        v = -1
        w = 1 - (u + v)

        return (w, v, u)
