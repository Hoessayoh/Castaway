import pygame
import random
import math
from settings import (WATER_COLOR, WATER_DEEP, SAND_COLOR, GRASS_COLOR,
                     SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE)

class World:
    def __init__(self):
        self.tile_size = TILE_SIZE
        self.water_anim_frame = 0

        # Define world layout - Pokemon style with land at bottom (scaled for 1080p)
        self.water_zone = pygame.Rect(0, 0, SCREEN_WIDTH, 540)  # Water at top (half screen)
        self.shore_zone = pygame.Rect(0, 540, SCREEN_WIDTH, 20)  # Shore line
        self.grass_zone = pygame.Rect(0, 560, SCREEN_WIDTH, 520)  # Land/grass at bottom where player walks

    def update(self):
        # Animate water
        self.water_anim_frame += 0.1

    def draw(self, screen):
        # Draw base water layer
        pygame.draw.rect(screen, WATER_COLOR, self.water_zone)

        # Draw animated wave layers for depth (scaled for 1080p)
        for wave_layer in range(5):  # More layers for 1080p
            wave_offset = self.water_anim_frame * (1 + wave_layer * 0.3)
            for x in range(-100, SCREEN_WIDTH + 100, 12):
                # Multiple sine waves at different frequencies
                y1 = 100 + wave_layer * 80 + int(12 * math.sin(x * 0.02 + wave_offset))
                y2 = y1 + int(6 * math.cos(x * 0.03 + wave_offset * 1.5))

                # Draw wave line with transparency-like effect
                wave_alpha = 40 - wave_layer * 6
                wave_color = (
                    min(255, WATER_DEEP[0] + wave_alpha),
                    min(255, WATER_DEEP[1] + wave_alpha),
                    min(255, WATER_DEEP[2] + wave_alpha)
                )

                if y2 < 540:  # Keep within water zone
                    pygame.draw.circle(screen, wave_color, (x, y2), 3)

        # Add subtle sparkles on water surface (more for 1080p)
        sparkle_density = 100
        for i in range(sparkle_density):
            sparkle_seed = i * 100 + int(self.water_anim_frame * 10)
            sparkle_x = (sparkle_seed * 73) % SCREEN_WIDTH
            sparkle_y = ((sparkle_seed * 31) % 480) + 30

            # Sparkle fades in and out
            sparkle_life = (self.water_anim_frame * 20 + i * 10) % 100
            if sparkle_life < 30:
                brightness = int(255 * (sparkle_life / 30))
                sparkle_color = (
                    min(255, WATER_COLOR[0] + brightness // 2),
                    min(255, WATER_COLOR[1] + brightness // 2),
                    min(255, WATER_COLOR[2] + brightness // 2)
                )
                # Draw slightly larger sparkles for 1080p
                if sparkle_x > 0 and sparkle_x < SCREEN_WIDTH and sparkle_y > 0 and sparkle_y < 540:
                    screen.set_at((sparkle_x, sparkle_y), sparkle_color)
                    if sparkle_life > 15:  # Brightest sparkles get extra pixels
                        if sparkle_x + 1 < SCREEN_WIDTH:
                            screen.set_at((sparkle_x + 1, sparkle_y), sparkle_color)
                        if sparkle_y + 1 < 540:
                            screen.set_at((sparkle_x, sparkle_y + 1), sparkle_color)

        # Draw shore/sand transition
        pygame.draw.rect(screen, SAND_COLOR, self.shore_zone)

        # Draw grass area (Pokemon-style with pattern)
        pygame.draw.rect(screen, GRASS_COLOR, self.grass_zone)

        # Draw grass tiles with darker patches (scaled for 1080p)
        for y in range(560, SCREEN_HEIGHT, self.tile_size):
            for x in range(0, SCREEN_WIDTH, self.tile_size):
                # Random darker grass tiles (like Pokemon)
                if (x + y) % (self.tile_size * 3) == 0:
                    darker_grass = (
                        max(0, GRASS_COLOR[0] - 20),
                        max(0, GRASS_COLOR[1] - 20),
                        max(0, GRASS_COLOR[2] - 20)
                    )
                    pygame.draw.rect(screen, darker_grass, (x, y, self.tile_size, self.tile_size))

                # Small grass details (scaled up)
                if (x // self.tile_size + y // self.tile_size) % 4 == 0:
                    grass_x = x + self.tile_size // 2
                    grass_y = y + self.tile_size // 2
                    # Simple grass tuft (thicker for 1080p)
                    pygame.draw.line(screen, (100, 150, 50),
                                   (grass_x - 3, grass_y), (grass_x - 3, grass_y - 8), 2)
                    pygame.draw.line(screen, (120, 170, 60),
                                   (grass_x + 3, grass_y), (grass_x + 3, grass_y - 10), 2)
