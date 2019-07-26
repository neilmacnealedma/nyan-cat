
import contextlib
with contextlib.redirect_stdout(None):
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

  if board.update():
    crashed = True
  board.render()
  pygame.display.update()
  clock.tick(60)

print("Score: {}".format(board.get_score()))
