import pygame
from pygame.locals import (RLEACCEL, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT)

pygame.init()

# Setting up window of game
SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 950
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Isaac's Castle of Memories")

# Player Sprite
class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
    
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

# Statue sprite
class Statue(pygame.sprite.Sprite):

    def __init__(self, image_name, position, message):
        super().__init__()
        raw_img = pygame.image.load(f"images/{image_name}")
        self.surf = pygame.transform.scale(raw_img, (100, 150))
        self.rect = self.surf.get_rect(center=position)
        self.message = message

    def show_message(self):
        uncover_text_animation(self.message)

# Sprite Groups
# all_sprites is for rendering
all_sprites = pygame.sprite.Group()
statues = pygame.sprite.Group()

# Instantiate player and add it to all_sprites
player = Player()
all_sprites.add(player)

# Statue position calculations
statue1_x = SCREEN_WIDTH * 0.25 * 0.5
statue2_x = SCREEN_WIDTH * 0.5 - statue1_x
statue3_x = SCREEN_WIDTH * 0.75 -  statue1_x
statue4_x = SCREEN_WIDTH - statue1_x

# Instantiate statues and add it to all_sprites and statues
draculisa = Statue("drac-and-lisa.webp", (statue1_x, 100), "My master and his wife. May they rest in peace.")
collector = Statue("collector.png", (statue2_x, 100), "\"I have a feeling you haven't received many gifts in your life, and it pleases me to improve that balance.\"")
captain = Statue("captain.webp", (statue3_x, 100), "\"It's a cruel world. Maybe we do all deserve to die. But maybe we could be better, too.\"")
miranda = Statue("miranda.webp", (statue4_x, 100), "\"There are worse things in the world than vampires in Styria, Isaac. There are worse things... than betrayal.\"")

draculisa.surf.set_colorkey((28, 28, 28), RLEACCEL)
collector.surf.set_colorkey((255, 255, 255), RLEACCEL)
captain.surf.set_colorkey((255, 255, 255), RLEACCEL)
miranda.surf.set_colorkey((255, 255, 255), RLEACCEL)

statues.add(draculisa, collector, captain, miranda)
all_sprites.add(draculisa, collector, captain, miranda)

# Text flashes (unintended effect) as letters appear
def intro_animation(string):

    screen.fill((255, 255, 255))
    
    # Text to be rendered each frame
    text = ''

    # Add letter to rendered text and update screen
    for i in string:
        text += i
        font = pygame.font.SysFont("arial", 64)
        text_surf = font.render(text, True, (0, 0, 0))
        text_rect = text_surf.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        screen.fill((255, 255, 255))
        screen.blit(text_surf, text_rect)
        pygame.display.update()
        pygame.time.wait(50)
        text_surf.fill((255, 255, 255))
        screen.blit(text_surf, text_rect)
        pygame.display.update()
    
    # Show final text and pause
    font = pygame.font.SysFont("arial", 64)
    text_surf = font.render(text, True, (0, 0, 0))
    text_rect = text_surf.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    screen.fill((255, 255, 255))
    screen.blit(text_surf, text_rect)
    pygame.display.update()
    pygame.time.wait(1000)

# Sliding surface moves to the right, revealing text underneath
def uncover_text_animation(string): 

    # Render string
    font = pygame.font.SysFont("arial", 32)
    text_surf = font.render(string, True, (0, 0, 0))
    text_rect = text_surf.get_rect()
    text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)

    # Position the surfaces
    sliding_surf = pygame.Surface((text_rect.width, text_rect.height))
    white_surf = pygame.Surface((text_rect.width, text_rect.height))
    white_surf.fill((255, 255, 255))
    sliding_surf.fill((255, 255, 255))
    sliding_rect = sliding_surf.get_rect(center = text_rect.center)
    screen.blit(text_surf, text_rect)
    screen.blit(sliding_surf, sliding_rect)

    pygame.display.update()

    # Move the sliding surface
    while (sliding_rect.left < text_rect.right):
        screen.blit(white_surf, sliding_rect)
        screen.blit(text_surf, text_rect)
        sliding_rect.move_ip(5, 0)
        screen.blit(sliding_surf, sliding_rect)
        pygame.display.update()
        pygame.time.wait(10)
    
    # Pause after the quote is loaded
    if (sliding_rect.left >= text_rect.right):
        pygame.time.wait(500)

# Intro
intro_animation("Isaac's Castle of Memories")

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
    elif isinstance(collided_statue, Statue):
        collided_statue.show_message()
        player.rect.move_ip(0, 10)

    # Render background
    screen.fill((255, 255, 255))
    # Render sprites
    for sprite in all_sprites:
        screen.blit(sprite.surf, sprite.rect)

    pygame.display.update()