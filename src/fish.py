import pygame
from settings import FISH_COLOR

class Fish(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 15))  # Fish size
        self.image.fill(FISH_COLOR)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 3

    def update(self):
        self.rect.x -= self.speed  # Fish swims to the left
        if self.rect.right < 0:  # Reset fish to the right of the screen if it exits
            self.rect.left = 800

    def draw(self, screen):
        screen.blit(self.image, self.rect)
