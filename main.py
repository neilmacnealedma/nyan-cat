
import pygame
import game

pygame.init()

display = pygame.display.set_mode((800,600))
pygame.display.set_caption('Nyan Cat')
clock = pygame.time.Clock()

board = game.Board(display)

crashed = False
while not crashed:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      crashed = True

  board.update()
  board.render()
  pygame.display.update()
  clock.tick(60)
