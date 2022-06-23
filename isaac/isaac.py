import pygame
from pygame.locals import (RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT)

pygame.init()

# Setting up window of game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Isaac's Castle of Memories")

# Player Sprite
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surface = pygame.Surface((50, 50))
        self.surface.fill((255, 255, 255))
        self.rectangle = self.surface.get_rect(center=(400, 600))

# Sprite Groups
# all_sprites is for rendering
all_sprites = pygame.sprite.Group()

# Instantiate player and add it to all_sprites
player = Player()
all_sprites.add(player)

# Game Loop
running = True
while running:

    for event in pygame.event.get():

        # If escape button or window X button is pressed, game ends
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
    
    for sprite in all_sprites:
        screen.blit(sprite.surface, sprite.rectangle)

    pygame.display.update()