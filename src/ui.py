import pygame

class UI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)  # Default font with size 36
        self.score = 0

    def update(self):
        # Logic to update score or other UI elements
        pass

    def draw(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))  # White text
        screen.blit(score_text, (10, 10))  # Draw at top-left corner
