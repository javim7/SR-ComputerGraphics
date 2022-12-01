from render import *
from utilities import *
from vector import *

# cambiar de color
# r.current_color = color(0, 250, 250)

# instanciando el Render
render = None


def glInit():
    pass


def glCreateWindow(width, height):
    global render
    render = Render(width, height)


def glViewPort(x, y, width, height):
    global render
    render.viewX = x
    render.viewY = y
    render.viewWidth = width
    render.viewHeight = height
    # for j in range(x, width + x):
    #     for k in range(y, height + y):
    #         render.point(j, k)


def glClear():
    global render
    render.clear()


def glClearColor(r, g, b):
    global render
    if r > 1 and r < 0 | g > 1 and g < 0 | b > 1 and b < 0:
        raise ValueError("Valores entre 0 y 1 solamente!")
    else:
        r = round(r * 255)
        g = round(g * 255)
        b = round(b * 255)
        render.clear_color = color(r, g, b)
        glClear()


def glVertex(x, y):
    global render
    # if x > 1 and x < -1 | y > 1 and y < -1:
    #     raise ValueError("Valores entre -1 y 1 solamente!")
    # else:
    # render.cordsFinales(x, y)

    # render.point(x, y)
    render.point(x, y)


def glLine(v1, v2):
    global render
    # print(* render.cordsFinales(x0, y0))
    # if x0 > 1 and x0 < -1 | y0 > 1 and y0 < -1:
    #     raise ValueError("Valores entre -1 y 1 solamente!")
    # else:
    return render.line(v1, v2)


def glTriangle(A, B, C):
    global render

    render.triangle(A, B, C)


def glTriangle2Vectors(A, B, C):
    global render

    render.triangle(A, B, C)


def glTriangle2(A, B, C):
    global render

    render.triangle2(A, B, C)


def glTransVertex(vertex, scale, translate):
    global render

    return render.transform_vertex(vertex, scale, translate)


def glColor(r, g, b):
    global render
    if r > 1 and r < 0 | g > 1 and g < 0 | b > 1 and b < 0:
        raise ValueError("Valores entre 0 y 1 solamente!")
    else:
        r = round(r * 255)
        g = round(g * 255)
        b = round(b * 255)
        render.current_color = color(r, g, b)


def glModel(model, translate_factor=(0, 0, 0), scale_factor=(1, 1, 1), rotate_factor=(0, 0, 0)):
    global render

    return render.generate_obj(model, translate_factor, scale_factor, rotate_factor)


def glLookAt(eye, center, up):
    global render

    return render.lookAt(eye, center, up)


def glVector(model):
    global render

    return render.generateVectors(model)


def glTexture(textura):
    global render
    render.texture = Texture(textura)


def glFinish(filename):
    render.write(filename+'.bmp')
    # render.write2(filename+'ZBuffer.bmp')
