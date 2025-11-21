import pygame
import random
# Delete if not needed
#import os
#print("Current working directory:", os.getcwd())
#print("Files in this directory:", os.listdir())
#print("Files in images folder:", os.listdir("images"))

# Initialize Pygame
#pygame.init()
#pygame.mixer.init()
#pygame.mixer.music.load("themesong.mp3")
#pygame.mixer.music.play(-1)
#pygame.mixer.music.set_volume(0.5)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Upside Down- Dig Dig Game")

#Adding background image, alternate code found image wasn't loading
#bg_path = "images/strangerThings.jpg"
#if not os.path.exists(bg_path):
    #raise FileNotFoundError("Cannot find background image at " + bg_path)
#background = pygame.image.load(bg_path).convert()
#background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()

# Colors
# Dirt Layers
L1 = (20, 20, 40)
L2 = (15, 15, 30)
L3 = (10, 10, 20)
L4 = (5, 5, 10)
BLUE = (80, 120, 255)
RED = (255, 40, 60)
SPORE_COLOR = (200, 220, 255)

# Player
player_x = 100
player_y = 100
player_speed = 5
player_image = pygame.Surface((30, 30))
player_image.fill(BLUE) 

#Enemy
enemy_x = 600
enemy_y = 400
enemy_speed = 3
enemy_image = pygame.Surface((30, 30))
enemy_image.fill(RED)

#Terrain Grid
ROWS = SCREEN_HEIGHT // TILE_SIZE
COLS = SCREEN_WIDTH // TILE_SIZE
terrain = []
for row in range(ROWS):
    if row < 3:
        color = L1
    elif row < 6:
        color = L2
    elif row < 9:
        color = L3
    else:
        color = L4
    terrain.append([color for _ in range(COLS)]) # color = dirt, none = empty space

#Spores
spores = []
for _ in range(50):
    spores.append([
        random.randint(0, SCREEN_WIDTH),
        random.randint(0, SCREEN_HEIGHT), 
        random.uniform(0.2, 1.0)
    ])

#Added fog
fog = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
fog.fill((30, 30, 50, 100))

#Can move to pygame function
def can_move(x, y):
    tile_x = x // TILE_SIZE
    tile_y = y // TILE_SIZE
    #Helps stay in the grid
    if tile_x < 0 or tile_x >= COLS or tile_y < 0 or tile_y >= ROWS:
        return False
    #can dig through dirt
    return True

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Player movements
    keys = pygame.key.get_pressed()
    new_x = player_x
    new_y = player_y

    if keys[pygame.K_LEFT]:
        new_x -= player_speed
    if keys[pygame.K_RIGHT]:
        new_x += player_speed
    if keys[pygame.K_UP]:
        new_y -= player_speed
    if keys[pygame.K_DOWN]:
        new_y += player_speed

    if can_move(new_x, new_y):
        player_x = new_x
        player_y = new_y

    #Player digging
    tile_x = player_x // TILE_SIZE
    tile_y = player_y // TILE_SIZE
    terrain[tile_y][tile_x] = None #This removes the dirt
    
    #Enemy movement
    dx = player_x - enemy_x
    dy = player_y - enemy_y
    if abs(dx) > abs(dy):
        enemy_x += enemy_speed if dx > 0 else -enemy_speed
    else:
        enemy_y += enemy_speed if dy > 0 else -enemy_speed

    #Enemy digging
    e_tile_x = enemy_x // TILE_SIZE
    e_tile_y = enemy_y // TILE_SIZE
    if 0 <= e_tile_x < COLS and 0 <= e_tile_y < ROWS:
        terrain[e_tile_y][e_tile_x] = None

    ## if i figure out the background 
    #screen.blit(background, (0, 0))

    # Draw terrain
    for y in range(ROWS):
        for x in range(COLS):
            color = terrain[y][x]
            if color: 
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw player
    screen.blit(player_image, (player_x, player_y))

    # Draw enemy
    screen.blit(enemy_image, (enemy_x, enemy_y))

    # Draw spores
    for spore in spores:
        pygame.draw.circle(screen, SPORE_COLOR, (int(spore[0]), int(spore[1])), 2)
        spore[1] += spore[2]  # Move down
        if spore[1] > SCREEN_HEIGHT:
            spore[0] = random.randint(0, SCREEN_WIDTH)
            spore[1] = 0
    #Fog 
    screen.blit(fog, (0, 0))

    pygame.display.update()
    clock.tick(60)

#pygame.mixer.music.stop()
pygame.quit()