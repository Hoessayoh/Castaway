import pygame
import random
import math
from settings import (WOOPER_BLUE, WOOPER_DARK_BLUE, WOOPER_PINK, SCREEN_WIDTH, SCREEN_HEIGHT,
                      BITE_WINDOW_FRAMES, FAILED_MESSAGE_DURATION)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        from settings import TILE_SIZE, PLAYER_SPEED
        self.size = TILE_SIZE
        # Create base sprite at 32x32, then scale up
        self.base_size = 32
        self.base_image = pygame.Surface((self.base_size, self.base_size), pygame.SRCALPHA)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(200, 400))
        self.speed = PLAYER_SPEED
        self.collection = []

        # Direction facing (for Pokemon-style sprites)
        self.direction = 'down'  # up, down, left, right

        # Animation system
        self.moving = False
        self.move_progress = 0
        self.animation_frame = 0
        self.animation_timer = 0
        self.frame_duration = 8  # Frames per animation step

        # Draw initial sprite
        self.draw_wooper()

        # Fishing states: 'idle', 'casting', 'waiting', 'bite', 'reeling'
        self.fishing_state = 'idle'
        self.bobber_pos = None
        self.bobber_bob = 0
        self.cast_progress = 0
        self.bite_timer = 0
        self.max_bite_time = random.randint(120, 300)
        self.bite_notification_timer = 0

        # Rod modifier (set by main game)
        self.rod_bite_speed_mult = 1.0

    def draw_wooper(self):
        """Draw Wooper using proper pixel art technique - hand-placed pixels"""
        s = self.base_image
        s.fill((0, 0, 0, 0))

        # Authentic Wooper color palette
        c1 = (79, 164, 210)   # Body blue
        c2 = (47, 116, 163)   # Dark blue (outline/shadow)
        c3 = (140, 200, 235)  # Light blue (highlights)
        c4 = (160, 215, 240)  # Belly blue
        c5 = (255, 128, 171)  # Pink gills
        c6 = (255, 180, 200)  # Light pink
        c7 = (20, 20, 30)     # Eye black
        c8 = (255, 255, 255)  # White

        # Pixel art - draw each pixel deliberately for clean sprite
        # This creates a 32x32 Wooper sprite with proper pixel art technique
        pixels = [
            # Format: (x, y, color)
            # Row 1-3: Head top
            (14, 4, c2), (15, 4, c2), (16, 4, c2), (17, 4, c2),
            (13, 5, c2), (14, 5, c3), (15, 5, c1), (16, 5, c1), (17, 5, c3), (18, 5, c2),
            (12, 6, c2), (13, 6, c1), (14, 6, c1), (15, 6, c1), (16, 6, c1), (17, 6, c1), (18, 6, c1), (19, 6, c2),

            # Row 4-5: Upper head with gills
            (11, 7, c2), (12, 7, c1), (13, 7, c1), (14, 7, c1), (15, 7, c1), (16, 7, c1), (17, 7, c1), (18, 7, c1), (19, 7, c1), (20, 7, c2),
            (10, 8, c2), (11, 8, c1), (12, 8, c1), (13, 8, c4), (14, 8, c4), (15, 8, c4), (16, 8, c4), (17, 8, c4), (18, 8, c1), (19, 8, c1), (20, 8, c2),

            # Left gill top
            (7, 8, c5), (8, 8, c6), (9, 8, c2),
            (6, 9, c5), (7, 9, c6), (8, 9, c5), (9, 9, c2),

            # Right gill top
            (22, 8, c2), (23, 8, c6), (24, 8, c5),
            (22, 9, c2), (23, 9, c5), (24, 9, c6), (25, 9, c5),

            # Row 6: Eyes and gills
            (9, 9, c2), (10, 9, c1), (11, 9, c1), (12, 9, c4), (13, 9, c4), (14, 9, c4), (15, 9, c4), (16, 9, c4), (17, 9, c4), (18, 9, c4), (19, 9, c1), (20, 9, c1), (21, 9, c1), (22, 9, c2),

            # Row 7-8: Eyes
            (9, 10, c2), (10, 10, c1), (11, 10, c8), (12, 10, c8), (13, 10, c4), (14, 10, c4), (15, 10, c4), (16, 10, c4), (17, 10, c4), (18, 10, c4), (19, 10, c8), (20, 10, c8), (21, 10, c1), (22, 10, c2),
            (9, 11, c2), (10, 11, c1), (11, 11, c8), (12, 11, c7), (13, 11, c4), (14, 11, c4), (15, 11, c4), (16, 11, c4), (17, 11, c4), (18, 11, c4), (19, 11, c7), (20, 11, c8), (21, 11, c1), (22, 11, c2),

            # Left gill middle
            (6, 11, c5), (7, 11, c6), (8, 11, c2),
            (5, 12, c5), (6, 12, c6), (7, 12, c5), (8, 12, c2),

            # Right gill middle
            (23, 11, c2), (24, 11, c6), (25, 11, c5),
            (23, 12, c2), (24, 12, c5), (25, 12, c6), (26, 12, c5),

            # Row 9-10: Mouth area
            (9, 12, c2), (10, 12, c1), (11, 12, c1), (12, 12, c1), (13, 12, c4), (14, 12, c4), (15, 12, c4), (16, 12, c4), (17, 12, c4), (18, 12, c1), (19, 12, c1), (20, 12, c1), (21, 12, c1), (22, 12, c2),
            (9, 13, c2), (10, 13, c1), (11, 13, c1), (12, 13, c1), (13, 13, c1), (14, 13, c4), (15, 13, c4), (16, 13, c4), (17, 13, c1), (18, 13, c1), (19, 13, c1), (20, 13, c1), (21, 13, c1), (22, 13, c2),

            # Row 11-12: Lower mouth with smile
            (10, 14, c2), (11, 14, c1), (12, 14, c1), (13, 14, c1), (14, 14, c1), (15, 14, c1), (16, 14, c1), (17, 14, c1), (18, 14, c1), (19, 14, c1), (20, 14, c1), (21, 14, c2),
            (10, 15, c2), (11, 15, c1), (12, 15, c2), (13, 15, c1), (14, 15, c1), (15, 15, c1), (16, 15, c1), (17, 15, c1), (18, 15, c2), (19, 15, c1), (20, 15, c2),

            # Left gill bottom
            (5, 14, c5), (6, 14, c6), (7, 14, c2),
            (6, 15, c5), (7, 15, c6), (8, 15, c2),

            # Right gill bottom
            (24, 14, c2), (25, 14, c6), (26, 14, c5),
            (23, 15, c2), (24, 15, c6), (25, 15, c5),

            # Row 13-16: Body tapering to tail
            (10, 16, c2), (11, 16, c1), (12, 16, c1), (13, 16, c1), (14, 16, c1), (15, 16, c1), (16, 16, c1), (17, 16, c1), (18, 16, c1), (19, 16, c1), (20, 16, c2),
            (11, 17, c2), (12, 17, c1), (13, 17, c1), (14, 17, c2), (15, 17, c2), (16, 17, c2), (17, 17, c2), (18, 17, c1), (19, 17, c2),
            (11, 18, c2), (12, 18, c1), (13, 18, c1), (14, 18, c1), (15, 18, c1), (16, 18, c1), (17, 18, c1), (18, 18, c2),
            (12, 19, c2), (13, 19, c1), (14, 19, c1), (15, 19, c1), (16, 19, c1), (17, 19, c2),

            # Row 17-20: Tail
            (12, 20, c2), (13, 20, c1), (14, 20, c1), (15, 20, c1), (16, 20, c1), (17, 20, c2),
            (13, 21, c2), (14, 21, c1), (15, 21, c1), (16, 21, c2),
            (13, 22, c2), (14, 22, c1), (15, 22, c1), (16, 22, c2),
            (14, 23, c2), (15, 23, c2),

            # Tail fins
            (11, 21, c1), (12, 21, c2), (17, 21, c2), (18, 21, c1),
            (10, 22, c1), (11, 22, c2), (17, 22, c2), (18, 22, c1),
            (10, 23, c1), (11, 23, c2), (17, 23, c2), (18, 23, c1),
            (11, 24, c2), (17, 24, c2),
        ]

        # Draw all pixels
        for x, y, color in pixels:
            s.set_at((x, y), color)

        # Add eye highlights (single white pixels)
        s.set_at((11, 10), c8)  # Left eye highlight
        s.set_at((19, 10), c8)  # Right eye highlight

        # Scale up to actual size using NEAREST for crisp pixels
        self.image = pygame.transform.scale(self.base_image, (self.size, self.size))

    def update(self):
        # Only allow movement when not actively fishing
        was_moving = self.moving
        self.moving = False

        if self.fishing_state == 'idle':
            keys = pygame.key.get_pressed()

            # Pokemon-style movement - one direction at a time
            if keys[pygame.K_UP]:
                self.rect.y -= self.speed
                self.direction = 'up'
                self.moving = True
            elif keys[pygame.K_DOWN]:
                self.rect.y += self.speed
                self.direction = 'down'
                self.moving = True
            elif keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
                self.direction = 'left'
                self.moving = True
            elif keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
                self.direction = 'right'
                self.moving = True

        # Keep player on land/grass area only (below water) - scaled for 1080p
        self.rect.x = max(20, min(self.rect.x, SCREEN_WIDTH - self.rect.width - 20))
        self.rect.y = max(570, min(self.rect.y, SCREEN_HEIGHT - self.rect.height - 20))

        # Update animation
        if self.moving:
            self.animation_timer += 1
            if self.animation_timer >= self.frame_duration:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % 2
                self.draw_wooper()  # Redraw with new frame
        elif was_moving:
            # Just stopped moving - reset to idle frame
            self.animation_frame = 0
            self.animation_timer = 0
            self.draw_wooper()

        # Update fishing mechanics
        self.update_fishing()

    def update_fishing(self):
        """Update fishing mechanics - Pokemon style"""
        if self.fishing_state == 'casting':
            # Animate bobber being cast
            self.cast_progress += 8
            if self.cast_progress >= 100:
                # Bobber always lands in water (upward into water zone) - scaled for 1080p
                # Find a spot in the water relative to player position
                bobber_x = self.rect.centerx + random.randint(-80, 80)
                bobber_y = random.randint(100, 500)  # Anywhere in water zone

                self.bobber_pos = [bobber_x, bobber_y]

                # Keep bobber in water bounds
                self.bobber_pos[0] = max(100, min(self.bobber_pos[0], SCREEN_WIDTH - 100))

                self.fishing_state = 'waiting'
                self.bite_timer = 0
                # Apply rod bite speed modifier (lower = faster bites)
                base_bite_time = random.randint(60, 180)  # 1-3 seconds
                self.max_bite_time = int(base_bite_time * self.rod_bite_speed_mult)
                self.cast_progress = 0

        elif self.fishing_state == 'waiting':
            # Wait for a fish to bite (Pokemon style - ... ... !)
            self.bite_timer += 1
            self.bobber_bob += 0.1

            # Dot animation every 30 frames
            if self.bite_timer % 30 == 0 and self.bite_timer < self.max_bite_time - 30:
                pass  # Will show dots in UI

            if self.bite_timer >= self.max_bite_time:
                # Fish bites! Player has limited time to react
                self.fishing_state = 'bite'
                self.bite_notification_timer = BITE_WINDOW_FRAMES

        elif self.fishing_state == 'bite':
            # Bobber bobs excitedly - player must press space!
            self.bobber_bob += 0.8
            self.bite_notification_timer -= 1

            # If player doesn't react in time, fish gets away
            if self.bite_notification_timer <= 0:
                self.fishing_state = 'failed'
                self.bite_notification_timer = FAILED_MESSAGE_DURATION

        elif self.fishing_state == 'failed':
            self.bite_notification_timer -= 1
            if self.bite_notification_timer <= 0:
                self.cancel_fishing()

        elif self.fishing_state == 'reeling':
            # Reel in the fish (handled in main.py)
            pass

    def cast_fishing_line(self):
        """Cast the fishing line"""
        if self.fishing_state == 'idle':
            self.fishing_state = 'casting'
            self.cast_progress = 0
        elif self.fishing_state == 'bite':
            # Player pressed space during bite - start reeling
            self.fishing_state = 'reeling'

    def cancel_fishing(self):
        """Cancel fishing and return to idle"""
        self.fishing_state = 'idle'
        self.bobber_pos = None
        self.bite_timer = 0
        self.bite_notification_timer = 0

    def add_to_collection(self, fish):
        """Add caught fish to collection"""
        self.collection.append(fish)

    def draw(self, screen):
        """Draw Wooper only (no bobber)"""
        screen.blit(self.image, self.rect)

    def draw_fishing_elements(self, screen):
        """Draw fishing rod, line, and bobber - call this after UI to prevent clipping"""
        # Draw fishing rod and line extending upward into water (Pokemon style)
        if self.fishing_state != 'idle' and self.fishing_state != 'failed':
            # Rod always extends from top of Wooper upward into water
            rod_start = (self.rect.centerx, self.rect.top)

            if self.fishing_state == 'casting':
                # Show casting animation - line extends upward (scaled for 1080p)
                cast_dist = int(self.cast_progress * 4)
                line_end = (rod_start[0], rod_start[1] - cast_dist)

                # Casting line (thicker for 1080p)
                pygame.draw.line(screen, (200, 200, 200), rod_start, line_end, 4)

            elif self.bobber_pos:
                # Draw fishing line to bobber in water (thicker for 1080p)
                pygame.draw.line(screen, (200, 200, 200), rod_start, self.bobber_pos, 3)

                # Draw bobber floating in water (scaled for 1080p)
                bobber_y_offset = int(4 * math.sin(self.bobber_bob))
                if self.fishing_state == 'bite':
                    bobber_y_offset = int(10 * math.sin(self.bobber_bob * 3))  # More dramatic bob

                bobber_pos = (self.bobber_pos[0], self.bobber_pos[1] + bobber_y_offset)

                # Bobber (Pokemon-style - red and white, larger for 1080p)
                pygame.draw.circle(screen, (255, 255, 255), bobber_pos, 12)
                pygame.draw.circle(screen, (255, 50, 50), (bobber_pos[0], bobber_pos[1] - 4), 8)
                # Add highlight for 3D effect
                pygame.draw.circle(screen, (255, 180, 180), (bobber_pos[0] - 2, bobber_pos[1] - 6), 3)

                # Draw exclamation mark if fish is biting (scaled)
                if self.fishing_state == 'bite' and self.bite_notification_timer > 0:
                    font = pygame.font.Font(None, 96)
                    exclaim = font.render("!", True, (255, 255, 0))
                    exclaim_rect = exclaim.get_rect(center=(bobber_pos[0], bobber_pos[1] - 50))

                    # Draw outline for visibility (thicker)
                    outline = font.render("!", True, (0, 0, 0))
                    screen.blit(outline, (exclaim_rect.x + 4, exclaim_rect.y + 4))
                    screen.blit(outline, (exclaim_rect.x - 2, exclaim_rect.y - 2))
                    screen.blit(exclaim, exclaim_rect)
