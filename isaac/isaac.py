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
        self.surface.fill((0, 0, 0))
        self.rectangle = self.surface.get_rect(center=(400, 600))
    
    # Move player based on pressed key
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rectangle.move_ip(0, -2)
        if pressed_keys[K_DOWN]:
            self.rectangle.move_ip(0, 2)
        if pressed_keys[K_LEFT]:
            self.rectangle.move_ip(-2, 0)
        if pressed_keys[K_RIGHT]:
            self.rectangle.move_ip(2, 0)
        
        # Keep player within game window
        if self.rectangle.left < 0:
            self.rectangle.left = 0
        if self.rectangle.right > SCREEN_WIDTH:
            self.rectangle.right = SCREEN_WIDTH
        if self.rectangle.top < 0:
            self.rectangle.top = 0
        if self.rectangle.bottom > SCREEN_HEIGHT:
            self.rectangle.bottom = SCREEN_HEIGHT

class Statue(pygame.sprite.Sprite):

    def __init__(self, image_name, position):
        super().__init__()
        raw_img = pygame.image.load(f"images/{image_name}")
        self.surface = pygame.transform.scale(raw_img, (100, 150))
        self.rectangle = self.surface.get_rect(center=position)

# Sprite Groups
# all_sprites is for rendering
all_sprites = pygame.sprite.Group()
statues = pygame.sprite.Group()

# Instantiate player and add it to all_sprites
player = Player()
all_sprites.add(player)

# Instantiate statues and add it to all_sprites and statues
draculisa = Statue("drac-and-lisa.webp", (100, 100))
collector = Statue("collector.png", (300, 100))
captain = Statue("captain.webp", (500, 100))
miranda = Statue("miranda.webp", (700, 100))

draculisa.surface.set_colorkey((28, 28, 28), RLEACCEL)
collector.surface.set_colorkey((255, 255, 255), RLEACCEL)
captain.surface.set_colorkey((255, 255, 255), RLEACCEL)
miranda.surface.set_colorkey((255, 255, 255), RLEACCEL)

statues.add(draculisa, collector, captain, miranda)
all_sprites.add(draculisa, collector, captain, miranda)


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

    # Update player position
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Render background
    screen.fill((255, 255, 255))
    # Render sprites
    for sprite in all_sprites:
        screen.blit(sprite.surface, sprite.rectangle)

    pygame.display.update()