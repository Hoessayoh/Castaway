import pygame
from settings import *
from world import World
import os

os.environ["SDL_AUDIODRIVER"] = "dummy"  # Disables ALSA errors

# Initialize Pygame
pygame.init()

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Castaway")

# Create world instance
world = World()

# Game Loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Render the world
    world.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
