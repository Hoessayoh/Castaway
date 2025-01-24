import pygame
from settings import *

class World:
    def __init__(self):
        self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background.fill(WATER_COLOR)

        # Create an island (placeholder rectangle for now)
        self.island = pygame.Rect(300, 400, 200, 100)  # (x, y, width, height)

    def draw(self, screen):
        screen.blit(self.background, (0, 0))  # Draw water
        pygame.draw.rect(screen, SAND_COLOR, self.island)  # Draw island
