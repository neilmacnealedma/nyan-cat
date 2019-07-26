
import random
import pygame

class Board():

  def __init__(self, display):
    self.tiles = {}
    self.tiles_generated_x_min = 0
    self.tiles_generated_x_max = 0
    self.display = display
    self.score = 0
    self.scroll_x = 0
    self.scroll_y = 0
    self.tile_size = 66
    self.player = Player(self)
    self.background_image = pygame.image.load("assets/background.png")
    self.background_image.convert()
    pygame.mixer.music.load('assets/song.mp3')
    pygame.mixer.music.play(-1)

  def update_tiles(self):
    if self.player.x + 20 > self.tiles_generated_x_max:
      for _ in range(5):
        self.create_random_platform()
      for i in range(int(self.player.x) + 20, int(self.player.x) + 40):
        self.tiles[(i, 20)] = Tile((i, 20))
      self.tiles_generated_x_max = self.player.x + 40

  def create_random_platform(self):
    x = random.randrange(int(self.player.x) + 20, int(self.player.x) + 40)
    y = random.randrange(10, 20)
    width = random.randrange(0, 10)
    for i in range(x, x + width):
      self.tiles[(i, y)] = Tile((i, y))

  def update(self):
    self.player.update()
    player_pixel_x = self.player.x * self.tile_size
    player_pixel_y = self.player.y * self.tile_size
    if player_pixel_x - self.scroll_x > 500:
      self.scroll_x += player_pixel_x - self.scroll_x - 500
    if player_pixel_x - self.scroll_x < 300:
      self.scroll_x += player_pixel_x - self.scroll_x - 300
    if player_pixel_y - self.scroll_y > 400:
      self.scroll_y += player_pixel_y - self.scroll_y - 400
    if player_pixel_y - self.scroll_y < 200:
      self.scroll_y += player_pixel_y - self.scroll_y - 200
    self.update_tiles()

  def render(self):
    self.display.blit(self.background_image, ((-self.scroll_x / 2 % 800)      , (-self.scroll_y / 2 % 600)      ))
    self.display.blit(self.background_image, ((-self.scroll_x / 2 % 800) - 800, (-self.scroll_y / 2 % 600)      ))
    self.display.blit(self.background_image, ((-self.scroll_x / 2 % 800)      , (-self.scroll_y / 2 % 600) - 600))
    self.display.blit(self.background_image, ((-self.scroll_x / 2 % 800) - 800, (-self.scroll_y / 2 % 600) - 600))
    for pos in self.tiles:
      self.tiles[pos].render(self.display, self.tile_size, self.scroll_x, self.scroll_y)
    self.player.render(self.display, self.tile_size, self.scroll_x, self.scroll_y)

class Player():

  def __init__(self, board):
    self.x = 0
    self.y = 0
    self.y_vel = 0
    self.board = board
    self.player_image = pygame.image.load("assets/player.gif")
    aspect_ratio = self.player_image.get_rect().width / self.player_image.get_rect().height
    self.pixel_size = int(self.player_image.get_rect().height / int(board.tile_size / aspect_ratio))
    self.player_image = pygame.transform.scale(self.player_image, (board.tile_size, int(board.tile_size / aspect_ratio)))
    self.image_offset_y = board.tile_size - self.player_image.get_rect().height
    self.fart_image = pygame.image.load("assets/fart.png")
    self.fart_image = pygame.transform.scale(self.fart_image, (self.fart_image.get_rect().width * 5, self.fart_image.get_rect().height * 5))
    self.direction = True
    self.boost = 100
    self.boosting = False
    self.animation_frame = 0

  def update(self):
    touching_ground = self.touching_ground()
    if touching_ground:
      self.boost += 3
    if self.boost > 100:
      self.boost = 100
    keys = pygame.key.get_pressed()
    delta_x = 0
    speed_x = 0.1
    old_x = self.x
    jump_vel = -0.18
    if keys[pygame.K_w] and touching_ground:
      self.y_vel = jump_vel
    self.y_vel += 0.006
    if keys[pygame.K_SPACE] and self.boost > 0 and self.y_vel > jump_vel:
      self.boost -= 1
      self.y_vel = 0
      self.boosting = True
      speed_x *= 2
    else:
      self.boosting = False
    if keys[pygame.K_a]:
      delta_x -= speed_x
    if keys[pygame.K_d]:
      delta_x += speed_x
    self.y += self.y_vel
    if self.in_ground():
      self.y -= self.y_vel
      self.y = int(self.y + 0.5)
      self.y_vel = 0
    self.x += delta_x
    if self.in_ground():
      self.x -= delta_x
      self.x = int(self.x + 0.5)
    old_direction = self.direction
    if self.x < old_x:
      self.direction = False
    if self.x > old_x:
      self.direction = True
    if old_direction != self.direction:
      self.player_image = pygame.transform.flip(self.player_image, True, False)

  def in_ground(self):
    nearby_tiles = []
    nearby_offsets = []
    for y in range(-1, 3):
      for x in range(-1, 3):
        nearby_offsets.append((x, y))
    for offset in nearby_offsets:
      pos = (offset[0] + int(self.x), offset[1] + int(self.y))
      if pos in self.board.tiles:
        nearby_tiles.append(self.board.tiles[pos])
    for tile in nearby_tiles:
      if ((self.x     >= tile.x and self.y     >= tile.y and self.x     < tile.x + 1 and self.y     < tile.y + 1) or \
          (self.x + 1 > tile.x and self.y     >= tile.y and self.x + 1 < tile.x + 1 and self.y     < tile.y + 1) or \
          (self.x     >= tile.x and self.y + 1 >  tile.y and self.x     < tile.x + 1 and self.y + 1 < tile.y + 1) or \
          (self.x + 1 > tile.x and self.y + 1 >  tile.y and self.x + 1 < tile.x + 1 and self.y + 1 < tile.y + 1)):
        return True
    return False

  def touching_ground(self):
    nearby_tiles = []
    nearby_offsets = []
    for y in range(-1, 3):
      for x in range(-1, 3):
        nearby_offsets.append((x, y))
    for offset in nearby_offsets:
      pos = (offset[0] + int(self.x), offset[1] + int(self.y))
      if pos in self.board.tiles:
        nearby_tiles.append(self.board.tiles[pos])
    for tile in nearby_tiles:
      if ((self.x     > tile.x and self.y     >= tile.y and self.x     < tile.x + 1 and self.y     < tile.y + 1) or \
          (self.x + 1 > tile.x and self.y     >= tile.y and self.x + 1 < tile.x + 1 and self.y     < tile.y + 1) or \
          (self.x     >= tile.x and self.y + 1 >= tile.y and self.x     < tile.x + 1 and self.y + 1 < tile.y + 1) or \
          (self.x + 1 > tile.x and self.y + 1 >= tile.y and self.x + 1 < tile.x + 1 and self.y + 1 < tile.y + 1)):
        return True
    return False

  def render(self, display, tile_size, scroll_x, scroll_y):
    pygame.draw.rect(display, (120, 117, 28), (20, 600 - 120, 20, 100))
    if self.boost != 0:
      pygame.draw.rect(display, (235, 229, 52), (20, 600 - self.boost - 20, 20, self.boost))
    if self.boosting:
      fart_width = self.fart_image.get_rect().width
      delta_x = -1 if self.direction else 1
      for i in range(100):
        display.blit(self.fart_image, (self.x * tile_size - scroll_x + fart_width * i * delta_x + fart_width + (self.animation_frame % 30) * delta_x, self.image_offset_y + 5 + self.y * tile_size - scroll_y + (i % 2) * 2))
    display.blit(self.player_image, (self.x * tile_size - scroll_x, self.image_offset_y + self.y * tile_size - scroll_y))
    self.animation_frame += 3

class Tile():

  def __init__(self, pos):
    self.x = pos[0]
    self.y = pos[1]

  def render(self, display, tile_size, scroll_x, scroll_y):
    pygame.draw.rect(display, (255, 255, 255), (self.x * tile_size - scroll_x, self.y * tile_size - scroll_y, tile_size, tile_size))

class Food():

  def __init__(self, pos):
    pass
