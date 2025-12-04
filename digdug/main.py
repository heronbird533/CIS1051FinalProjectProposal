import pygame
import random
import time

# Initialize Pygame
pygame.init()

#Music
pygame.mixer.init()
pygame.mixer.music.load("digdug/themesong.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)


# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Upside Down- Dig Dig Game")

clock = pygame.time.Clock()

#Title Screen 
title_running = True 
font = pygame.font.SysFont(None, 74)

#Warning messages
warning_messages = [ "HE'S HERE", "RUN", "DON'T LOOK BACK", "IT'S TOO LATE", "THE GATE IS OPEN", "THERE'S NO TIME"]
warning_active = False
warning_text = ""
warning_end_timer = 0

while title_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            title_running = False

    screen.fill((0, 0, 0))
    line1 = font.render("STRANGER THINGS", True, (255, 0, 0))
    line2 = font.render("Upside Down Dig Dug", True, (255, 0, 0))
    line3 = pygame.font.SysFont(None, 32).render("Press ENTER to start", True, (255, 255, 255))
    screen.blit(line1, (SCREEN_WIDTH//2 - line1.get_width()//2, 100))
    screen.blit(line2, (SCREEN_WIDTH//2 - line2.get_width()//2, 200))
    screen.blit(line3, (SCREEN_WIDTH//2 - line3.get_width()//2, 300))
    pygame.display.update()


#Original code background image
background = pygame.image.load("digdug/images/strangerThings.jpg").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))


# Colors
# Dirt Layers
L1 = (20, 20, 40)
L2 = (15, 15, 30)
L3 = (10, 10, 20)
L4 = (5, 5, 10)
BLUE = (80, 120, 255)
RED = (255, 40, 60)
SPORE_COLOR = (200, 220, 255)

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

# Player
player_x = 100
player_y = 100
player_speed = 5
player_image = pygame.Surface((30, 30))
player_image.fill(BLUE) 
player_facing = 'right'
attack_range = 40


#Enemy tunnels
for i in range(10):
    row = random.randint(3, ROWS - 1)
    col = random.randint(0, COLS -1)
    length = random.randint(3, 7)
    direction = random.choice(['horizontal', 'vertical'])
    for j in range(length):
        if direction == "horizontal":
            col += 1
        else:
            row += 1
        if 0 <= row < ROWS and 0 <= col < COLS:
            terrain[row][col] = None

#Enemy
enemies = []
enemy_count = 5
tunnel_positions = [(x, y) for y in range(ROWS) for x in range(COLS) if terrain[y][x] is None]

for _ in range(enemy_count):
        if not tunnel_positions:
            break
        start_tile = random.choice(tunnel_positions)
        tunnel_positions.remove(start_tile)
        enemy_x = start_tile[0] * TILE_SIZE
        enemy_y = start_tile[1] * TILE_SIZE
        enemies.append({
            "x": enemy_x, 
            "y": enemy_y, 
            "speed": 2, 
            "alive": True, 
            "direction": random.choice(['left', 'right', 'up', 'down'])
        })

enemy_image = pygame.Surface((30, 30))
enemy_image.fill(RED)

#Spores
spores = []
for _ in range(50):
    spores.append([
        random.randint(0, SCREEN_WIDTH),
        random.randint(0, SCREEN_HEIGHT), 
        random.uniform(0.2, 1.0)])

#Added fog
fog = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
fog.fill((30, 30, 50, 50))

#Lives, Score, Timer
lives = 3
game_time = 100
start_time = time.time()


#Can move to pygame function
def tile_open(x, y):
    tile_x = x // TILE_SIZE
    tile_y = y // TILE_SIZE
    if 0 <= tile_x < COLS and 0 <= tile_y < ROWS:
        return terrain[tile_y][tile_x] is None
    return False

def within_bounds(x, y):
    tile_x = x // TILE_SIZE
    tile_y = y // TILE_SIZE
    return 0 <= tile_x < COLS and 0 <= tile_y < ROWS

def all_done():
    for row in terrain:
        for tile in row:
            if tile is not None:
                return False
    return True

#Main Game Loop
running = True
while running:
    duration = clock.tick(100)
    elapsed_time = int(time.time() - start_time)
    time_left = game_time - elapsed_time

    if time_left <= 0:
        print("Time's up! Game Over.")
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Player movements
    keys = pygame.key.get_pressed()
    new_x = player_x
    new_y = player_y

    if keys[pygame.K_LEFT]:
        new_x -= player_speed
        player_facing = 'left'
    if keys[pygame.K_RIGHT]:
        new_x += player_speed
        player_facing = 'right'
    if keys[pygame.K_UP]:
        new_y -= player_speed
        player_facing = 'up'
    if keys[pygame.K_DOWN]:
        new_y += player_speed
        player_facing = 'down'

    if within_bounds(new_x, new_y):
        player_x = new_x
        player_y = new_y

    #Player digging
    tile_x = player_x // TILE_SIZE
    tile_y = player_y // TILE_SIZE
    terrain[tile_y][tile_x] = None #This removes the dirt
    
    #Enemy movement
    for enemy in enemies:
        if not enemy["alive"]:
            continue
        
        dx, dy = 0, 0
        if enemy["direction"] == "left":
            dx = -enemy["speed"]
        elif enemy["direction"] == "right":
            dx = enemy["speed"]
        elif enemy["direction"] == "up":
            dy = -enemy["speed"]
        elif enemy["direction"] == "down":
            dy = enemy["speed"]

        if tile_open(enemy["x"] + dx, enemy["y"] + dy):
            enemy["x"] += dx
            enemy["y"] += dy
        else:
            directions = []
            if tile_open(enemy["x"] + enemy["speed"], enemy["y"]):
                directions.append("right")
            if tile_open(enemy["x"] - enemy["speed"], enemy["y"]):
                directions.append("left")
            if tile_open(enemy["x"], enemy["y"] - enemy["speed"]):
                directions.append("up")
            if tile_open(enemy["x"], enemy["y"] + enemy["speed"]):
                directions.append("down")

            if directions:
                enemy["direction"] = random.choice(directions)
            

    #Player Attack 
    if keys[pygame.K_SPACE]:
        for enemy in enemies:
            if enemy["alive"]:
                enemy_x = enemy["x"]
                enemy_y = enemy["y"]
                if player_facing == "right" and player_x < enemy_x < player_x + attack_range and abs(enemy_y - player_y) < 25:
                    enemy["alive"] = False
                elif player_facing == "left" and player_x < enemy_x < player_x + attack_range and abs(enemy_y - player_y) < 25:
                    enemy["alive"] = False
                elif player_facing == "down" and player_y < enemy_y < player_y + attack_range and abs(enemy_x - player_x) < 25:
                    enemy["alive"] = False
                elif player_facing == "up" and player_y < enemy_y < player_y + attack_range and abs(enemy_x - player_x) < 25:
                    enemy["alive"] = False

    #Collision
    for enemy in enemies:
        if enemy["alive"]:
            if abs(player_x - enemy["x"]) < 30 and abs(player_y - enemy["y"]) < 25:
                lives -= 1
                print("Ouch! Lives left:", lives)
                if lives <= 0:
                    print("No lives left! Game Over")
                    running = False
                # Reset player position
                if player_x > enemy["x"]:
                    player_x += 20
                else:
                    player_x -= 20
                if player_y > enemy["y"]:
                    player_y += 20
                else:
                    player_y -= 20

    #Winning
    if all_done():
        print("You've escaped the Upside Down! You win (for now)!")
        running = False

    
    screen.fill((0, 0, 0))
## if i figure out the background 
    screen.blit(background, (0, 0))

    #Warming lights
    if not warning_active and random.random() < 0.01:
        warning_active = True
        warning_text = random.choice(warning_messages)
        warning_end_timer = time.time() + 3
    #End warning
    if warning_active and time.time() > warning_end_timer:
        warning_active = False

    # Draw terrain
    for y in range(ROWS):
        for x in range(COLS):
            tile_color = terrain[y][x]
            if tile_color is not None:
                pygame.draw.rect(screen, tile_color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Draw player
    screen.blit(player_image, (player_x, player_y))

    # Draw enemy
    for enemy in enemies:
        if enemy["alive"]:
            screen.blit(enemy_image, (enemy["x"], enemy["y"]))

    # Draw spores
    for spore in spores:
        pygame.draw.circle(screen, SPORE_COLOR, (int(spore[0]), int(spore[1])), 2)
        spore[1] += spore[2] 
        if spore[1] > SCREEN_HEIGHT:
            spore[0] = random.randint(0, SCREEN_WIDTH)
            spore[1] = 0
    #Fog 
    screen.blit(fog, (0, 0))

    font = pygame.font.SysFont(None, 36)
    screen.blit(font.render("Time: " + str(time_left), True, (255, 255, 255)), (10, 10))
    screen.blit(font.render("Lives: " + str(lives), True, (255, 255, 255)), (10, 40))


    #Christmas lights effect
    if warning_active: 
        glow_colors = [(255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 150, 255), (255, 100, 200)]
        glow = random.choice(glow_colors)

        warning_surface = font.render(warning_text, True, glow)
        screen.blit(warning_surface, (SCREEN_WIDTH//2 - warning_surface.get_width()//   2, 50))

    pygame.display.update()

#pygame.mixer.music.stop()
pygame.quit()