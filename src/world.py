import pygame
from settings import WATER_COLOR, SAND_COLOR

class World:
    def __init__(self):
        self.island = pygame.Rect(200, 400, 400, 150)  # Sandy island

    def update(self):
        # Add logic for updating the world if needed (e.g., dynamic elements)
        pass

    def draw(self, screen):
        screen.fill(WATER_COLOR)  # Fill background with water
        pygame.draw.rect(screen, SAND_COLOR, self.island)  # Draw the island
