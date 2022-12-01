from render import *

r = Render(100, 100)
# UN SOLO PUNTO
#r.point(100, 100)

# CUADRADO EN LA PANTALLA
# for x in range(100, 200):
#     for y in range(100, 200):
#         r.point(x, y)

# PUNTOS RANDOM DE DIFERENTE COLOR
# for x in range(0, 1024):
#     for y in range(0, 1024):
#         r.current_color = color(
#             random.randint(0, 255),
#             random.randint(0, 255),
#             random.randint(0, 255)
#         )
#         r.point(x, y)


# FUNCION LINEA
# def line(x0, y0, x1, y1):
#     for x in range(x0, x1):
#         for y in range(y0, y1):
#             if x == y:
#                 r.point(x, y)

# FUNCION LINEA 2
# def line(x0, y0, x1, y1):
#     i = 0
#     while i <= 1:
#         x = x0 + (x1 - x0) * i
#         y = y0 + (y1 - y0) * i
#         r.point(round(x), round(y))
#         i += 0.01

# FUNCION LINEA 3
# def line(x0, y0, x1, y1):
#     dy = y1 - y0
#     dx = x1 - x0
#     m = dy/dx

#     isSteep = dy > dx

#     if isSteep:
#         x0, y0 = y0, x0
#         x1, y1, = y1, x1

#     dy = y1 - y0
#     dx = x1 - x0
#     m = dy/dx

#     for x in range(x0, x1):
#         y = y0 + m * (x - x0)
#         if isSteep:
#             r.point(round(y), round(x))
#         else:
#             r.point(round(x), round(y))

# FUNCION LINEA 4
# def line(x0, y0, x1, y1):
#     dy = y1 - y0
#     dx = x1 - x0
#     m = dy/dx

#     isSteep = dy > dx

#     if isSteep:
#         x0, y0 = y0, x0
#         x1, y1, = y1, x1

#     dy = y1 - y0
#     dx = x1 - x0
#     m = dy/dx

#     offset = 0

#     for x in range(x0, x1):
#         offset += m

#         y = y0 + round(offset)

#         if isSteep:
#             r.point(y, x)
#         else:
#             r.point(x, y)

# # FUNCION LINEA 5
# def line(x0, y0, x1, y1):
#     dy = y1 - y0
#     dx = x1 - x0
#     m = dy/dx

#     isSteep = dy > dx

#     if isSteep:
#         x0, y0 = y0, x0
#         x1, y1, = y1, x1

#     dy = y1 - y0
#     dx = x1 - x0
#     m = dy/dx

#     offset = 0
#     threshold = 0.5
#     y = y0

#     for x in range(x0, x1):
#         offset += m

#         if offset >= threshold:
#             y += 1
#             threshold += 1

#         if isSteep:
#             r.point(y, x)
#         else:
#             r.point(x, y)

# FUNCION LINEA 6
def line(x0, y0, x1, y1):
    dy = abs(y1 - y0)
    dx = abs(x1 - x0)

    isSteep = dy > dx

    if isSteep:
        x0, y0 = y0, x0
        x1, y1, = y1, x1

    if x0 > x1:
        x0, x1, = x1, x0
        y0, y1 = y1, y0

    dy = y1 - y0
    dx = x1 - x0

    offset = 0
    threshold = dx
    y = y0

    for x in range(x0, x1):
        offset += dy * 2

        if offset >= threshold:
            y += 1 if y0 < y1 else -1
            threshold += dx * 2

        if isSteep:
            r.point(y, x)
        else:
            r.point(x, y)


line(80, 40, 13, 20)
