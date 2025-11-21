import pygame
import random
import os
print("Current working directory:", os.getcwd())

print(os.path.exists("images/strangerThings.jpg"))
# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 40
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Upside Down- Dig Dig Game")

#Adding background image
background = pygame.image.load("images/strangerThings.jpg").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))


screen.blit(background, (0, 0))

    