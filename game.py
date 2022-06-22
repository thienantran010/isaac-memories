import pygame
from pygame.locals import (RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT)
import random

# Initialize modules
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

# set up window to play game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Custom event for adding a new cloud
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Player sprite
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        raw_img = pygame.image.load("jj.webp").convert()
        self.surf = pygame.transform.scale(raw_img, (50, 50))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    # When a key is pressed, move the rect, which also moves the surface
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        
        # Keeps player within screen
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Enemy class
class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        raw_img = pygame.image.load("missle.png").convert()
        self.surf = pygame.transform.scale(raw_img, (50, 50))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)
    
    # Move enemy sprite to the left based on its speed
    # Remove enemy when it passes left edge of screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Cloud class (background image)
class Cloud(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        raw_img = pygame.image.load("cloud.png").convert()
        self.surf = pygame.transform.scale(raw_img, (50, 50))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
    
    # Move cloud to the right until it passes the left edge
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

# Instantiate player
player = Player()

# Sprite groups
# - enemies is used for collision detection and position updates
# - all sprites is used for rendering
# - clouds is used for position updates
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites.add(player)

# Setup clock for playable framerate
clock = pygame.time.Clock()
# Game loop
running = True
while running:

    for event in pygame.event.get():
        
        # If escape key or user x-es out, stop running game
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        
        # Add new enemy to screen
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)


    # Black background
    screen.fill((0, 0, 0))

    # Get pressed keys
    pressed_keys = pygame.key.get_pressed()

    # Update player rect position based on pressed keys
    player.update(pressed_keys)

    # Update enemy position
    enemies.update()

    # Update cloud position
    clouds.update()

    # Sky blue background
    screen.fill((135, 206, 250))

    # Draw all sprites
    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    # If any enemy collided with player, remove player and end game
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False

    # Update screen
    pygame.display.update()

    # Makes sure program maintains 30fps
    clock.tick(30)