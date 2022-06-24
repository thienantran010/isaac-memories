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
        self.surf = pygame.Surface((50, 50))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(center=(400, 600))
    
    # Move player based on pressed key
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -2)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 2)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-2, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(2, 0)
        
        # Keep player within game window
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Statue(pygame.sprite.Sprite):

    def __init__(self, image_name, position, char_name):
        super().__init__()
        raw_img = pygame.image.load(f"images/{image_name}")
        self.surf = pygame.transform.scale(raw_img, (100, 150))
        self.rect = self.surf.get_rect(center=position)
        self.identity = char_name

# Sprite Groups
# all_sprites is for rendering
all_sprites = pygame.sprite.Group()
statues = pygame.sprite.Group()

# Instantiate player and add it to all_sprites
player = Player()
all_sprites.add(player)

# Instantiate statues and add it to all_sprites and statues
draculisa = Statue("drac-and-lisa.webp", (100, 100), "draculisa")
collector = Statue("collector.png", (300, 100), "collector")
captain = Statue("captain.webp", (500, 100), "captain")
miranda = Statue("miranda.webp", (700, 100), "miranda")

draculisa.surf.set_colorkey((28, 28, 28), RLEACCEL)
collector.surf.set_colorkey((255, 255, 255), RLEACCEL)
captain.surf.set_colorkey((255, 255, 255), RLEACCEL)
miranda.surf.set_colorkey((255, 255, 255), RLEACCEL)

statues.add(draculisa, collector, captain, miranda)
all_sprites.add(draculisa, collector, captain, miranda)

def flashing_text_animation(string):

    text = ''
    for i in string:
        text += i
        font = pygame.font.SysFont("arial", 32)
        text_surf = font.render(text, True, (0, 0, 0))
        text_rect = text_surf.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        screen.blit(text_surf, text_rect)
        pygame.display.update()
        pygame.time.wait(50)
        text_surf.fill((255, 255, 255))
        screen.blit(text_surf, text_rect)
        pygame.display.update()

# Text box animation
def uncover_text_animation(string): 

    # Render string
    font = pygame.font.SysFont("arial", 32)
    text_surf = font.render(string, True, (0, 0, 0))
    text_rect = text_surf.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)

    sliding_surf = pygame.Surface((text_rect.width, text_rect.height))
    white_surf = pygame.Surface((text_rect.width, text_rect.height))
    white_surf.fill((255, 255, 255))
    sliding_surf.fill((255, 255, 255))
    sliding_rect = sliding_surf.get_rect(center = text_rect.center)
    screen.blit(text_surf, text_rect)
    screen.blit(sliding_surf, sliding_rect)

    pygame.display.update()

    while (sliding_rect.left < text_rect.right):
        screen.blit(white_surf, sliding_rect)
        screen.blit(text_surf, text_rect)
        sliding_rect.move_ip(5, 0)
        screen.blit(sliding_surf, sliding_rect)
        pygame.display.update()
        pygame.time.wait(50)

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

    collided_statue = pygame.sprite.spritecollideany(player, statues)

    if collided_statue == None:
        # Update player position
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
    else:
        uncover_text_animation("Dracula!")
        player.rect.move_ip(0, 10)

    # Render background
    screen.fill((255, 255, 255))
    # Render sprites
    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    pygame.display.update()