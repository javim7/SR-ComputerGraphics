import sys
import pygame
from gl import * 

glCreateWindow(1024, 1024)
glTexture('./modelos_prueba/IG.bmp')
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600))
x = 0
while True:
  clock.tick(60)
  glClearColor(0, 0, 0)
  glClear()

  # color de imagen rojo
  glColor(1, 1, 1)

  glLookAt((x, 30, 10), (0, 0, 0), (0, 1, 0))

  glRenderObject('./modelos_prueba/IGCG.obj', (400, 400, 400), (500, 20, -300), (0, 0, 0))
  glFinish('matrices.bmp')
  
  frame = pygame.image.load('matrices.bmp').convert()
  screen.blit(frame, (0,0))
  for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        x -= 10
      if event.key == pygame.K_RIGHT:
        x += 10
    if event.type == pygame.QUIT:
        sys.exit()
  print('frame', x)
  pygame.display.update()