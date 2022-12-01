from gl import *
from render import *
from reader import *
from vector import *
from textures import *

r = Render(540, 540)

'''
Agregando imagen de fondo
'''
background = Texture('./models/background.bmp')
r.framebuffer = background.pixels

'''
Creando shader
'''


def shader(render, **kwargs):

    Light = kwargs['light']
    w, u, v = kwargs['bar']
    A, B, C = kwargs['vertices']
    tA, tB, tC = kwargs['texture_coords']
    nA, nB, nC = kwargs['normals']

    intensityA = nA.normalize() @ Light.normalize()
    intensityB = nB.normalize() @ Light.normalize()
    intensityC = nC.normalize() @ Light.normalize()

    intensity = intensityA * w + intensityB * u + intensityC * v

    if intensity > 1 or intensity <= 0:
        return color(0, 0, 0)

    if render.texture:
        tx = tA.x * w + tB.x * u + tC.x * v
        ty = tA.y * w + tB.y * u + tC.y * v

        return render.texture.get_color_with_intensity(
            tx, ty, intensity)


def shader2(render, **kwargs):

    Light = kwargs['light']
    w, u, v = kwargs['bar']
    A, B, C = kwargs['vertices']
    tA, tB, tC = kwargs['texture_coords']
    nA, nB, nC = kwargs['normals']

    intensityA = nA.normalize() @ Light.normalize()
    intensityB = nB.normalize() @ Light.normalize()
    intensityC = nC.normalize() @ Light.normalize()

    intensity = intensityA * w + intensityB * u + intensityC * v

    if intensity > 1 or intensity <= 0:
        return color(255, 0, 0)

    if render.texture:
        tx = tA.x * w + tB.x * u + tC.x * v
        ty = tA.y * w + tB.y * u + tC.y * v

        b, g, r = render.texture.get_color_with_intensity(
            tx, ty, intensity)

        return color(255, g, r)


def shader3(render, **kwargs):

    Light = kwargs['light']
    w, u, v = kwargs['bar']
    A, B, C = kwargs['vertices']
    tA, tB, tC = kwargs['texture_coords']
    nA, nB, nC = kwargs['normals']

    intensityA = nA.normalize() @ Light.normalize()
    intensityB = nB.normalize() @ Light.normalize()
    intensityC = nC.normalize() @ Light.normalize()

    intensity = intensityA * w + intensityB * u + intensityC * v

    if intensity > 1 or intensity <= 0:
        return color(0, 0, 255)

    if render.texture:
        tx = tA.x * w + tB.x * u + tC.x * v
        ty = tA.y * w + tB.y * u + tC.y * v

        b, g, r = render.texture.get_color_with_intensity(
            tx, ty, intensity)

        return color(b, g, 255)


r.lookAt(V3(0, 0, 5), V3(0, 0, 0), V3(0, 1, 0).normalize())

'''
Dibujando los modelos
'''

#-----------------Luna-----------------#
r.texture = Texture('./models/moon.bmp')
r.shader = shader3
#translate, scale, rotate
r.generate_obj('./models/moon.obj', (0.75, 0.75, 0),
               (.2, .2, .2), (0, 0, 0))
r.draw('TRIANGLES')

# # # -----------------Lapida-----------------#
r.texture = Texture('./models/Tombstone.bmp')
r.shader = shader
#translate, scale, rotate
r.generate_obj('./models/Tombstone.obj', (0.7, -0.9, 0),
               (0.05, 0.05, 0.05), (0, 0, -pi/15))
r.draw('TRIANGLES')

# # # -----------------Calabaza-----------------#
r.texture = Texture('./models/pumpkin.bmp')
r.shader = shader
#translate, scale, rotate
r.generate_obj('./models/pumpkin.obj', (-0.4, -0.9, 0),
               (0.003, 0.003, 0.003), (0, pi/10, 0))
r.draw('TRIANGLES')

# #-----------------Fantasma-----------------#
r.texture = Texture('./models/Ghost.bmp')
r.shader = shader2
#translate, scale, rotate
r.generate_obj('./models/Ghost.obj', (-0.2, 0.3, 0),
               (0.003, 0.003, 0.003), (0, -pi/8, 0))
r.draw('TRIANGLES')

# #-----------------Zombi-----------------#
r.texture = Texture('./models/zombi.bmp')
r.shader = shader
#translate, scale, rotate
r.generate_obj('./models/zombi.obj', (0.1, -0.9, 0),
               (0.0012, 0.0012, 0.0012), (0, 0, 0))
r.draw('TRIANGLES')


r.write('proyecto1.bmp')
