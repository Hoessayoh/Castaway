import pygame
from settings import SCREEN_WIDTH, UI_BG, UI_TEXT, UI_ACCENT, UI_BORDER, CATCH_DISPLAY_DURATION

class UI:
    def __init__(self):
        # Scaled fonts for 1080p
        self.font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 44)
        self.title_font = pygame.font.Font(None, 56)
        self.score = 0
        self.fish_caught = 0
        self.last_catch = None
        self.catch_display_timer = 0

    def update(self):
        # Countdown catch display timer
        if self.catch_display_timer > 0:
            self.catch_display_timer -= 1

    def add_score(self, points, fish_name="Fish", rarity_color=(255, 255, 255), is_shiny=False):
        """Add points to the score"""
        self.score += points
        self.fish_caught += 1
        self.last_catch = fish_name
        self.last_catch_points = points
        self.last_catch_color = rarity_color
        self.last_catch_shiny = is_shiny
        self.catch_display_timer = CATCH_DISPLAY_DURATION

    def draw_box(self, screen, x, y, width, height):
        """Draw a Stardew Valley style box"""
        # Shadow
        pygame.draw.rect(screen, (0, 0, 0, 50), (x + 3, y + 3, width, height))
        # Background
        pygame.draw.rect(screen, UI_BG, (x, y, width, height))
        # Border
        pygame.draw.rect(screen, UI_BORDER, (x, y, width, height), 3)
        # Inner highlight
        pygame.draw.rect(screen, UI_ACCENT, (x + 3, y + 3, width - 6, height - 6), 1)

    def draw(self, screen, player=None, progression=None):
        # Top left info box (taller for level) - scaled for 1080p
        box_height = 210 if progression else 160
        self.draw_box(screen, 20, 20, 360, box_height)

        # Score
        score_text = self.title_font.render("Gold", True, UI_ACCENT)
        screen.blit(score_text, (40, 36))
        score_value = self.font.render(f"{self.score}", True, (255, 215, 0))
        screen.blit(score_value, (40, 84))

        # Fish caught
        fish_icon = self.small_font.render("Fish:", True, UI_ACCENT)
        screen.blit(fish_icon, (220, 40))
        fish_value = self.title_font.render(f"{self.fish_caught}", True, (100, 200, 255))
        screen.blit(fish_value, (240, 90))

        # Level display if progression exists
        if progression:
            level_text = self.small_font.render("Level:", True, UI_ACCENT)
            screen.blit(level_text, (40, 140))
            level_value = self.title_font.render(f"{progression.level}", True, (144, 238, 144))
            screen.blit(level_value, (140, 136))

            # Mini EXP bar (scaled)
            exp_progress = progression.experience / progression.experience_to_next_level
            bar_width = 160
            bar_height = 16
            bar_x = 220
            bar_y = 150

            pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (100, 200, 100), (bar_x, bar_y, int(bar_width * exp_progress), bar_height))
            pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)

        # Show last catch notification with rarity color (scaled for 1080p)
        if self.catch_display_timer > 0:
            catch_width = 560
            catch_height = 180
            catch_x = SCREEN_WIDTH // 2 - catch_width // 2
            catch_y = 160

            self.draw_box(screen, catch_x, catch_y, catch_width, catch_height)

            # "Caught!" text (scaled)
            caught_text = self.small_font.render("Caught!", True, UI_ACCENT)
            caught_rect = caught_text.get_rect(center=(catch_x + catch_width // 2, catch_y + 30))
            screen.blit(caught_text, caught_rect)

            # Fish name with rarity color (with subtle outline for emphasis)
            fish_color = getattr(self, 'last_catch_color', (255, 255, 255))
            # Draw outline/shadow for better readability (scaled)
            outline_offsets = [(-2, -2), (2, -2), (-2, 2), (2, 2)]
            fish_outline = self.title_font.render(self.last_catch, True, (20, 20, 20))
            for offset_x, offset_y in outline_offsets:
                outline_rect = fish_outline.get_rect(center=(catch_x + catch_width // 2 + offset_x, catch_y + 80 + offset_y))
                screen.blit(fish_outline, outline_rect)
            # Main fish name
            fish_text = self.title_font.render(self.last_catch, True, fish_color)
            fish_rect = fish_text.get_rect(center=(catch_x + catch_width // 2, catch_y + 80))
            screen.blit(fish_text, fish_rect)

            # Points (scaled)
            points_text = self.title_font.render(f"+{self.last_catch_points} Gold", True, (255, 215, 0))
            points_rect = points_text.get_rect(center=(catch_x + catch_width // 2, catch_y + 130))
            screen.blit(points_text, points_rect)

            # Shiny sparkle effect (scaled)
            if getattr(self, 'last_catch_shiny', False):
                import math
                sparkle_offset = int(10 * abs(math.sin(self.catch_display_timer / 10)))
                sparkle_text = self.font.render("✨", True, (255, 255, 255))
                screen.blit(sparkle_text, (catch_x + 20 + sparkle_offset, catch_y + 60))
                screen.blit(sparkle_text, (catch_x + catch_width - 80 - sparkle_offset, catch_y + 60))

        # Show Pokemon-style fishing status (scaled for 1080p)
        if player:
            if player.fishing_state == 'waiting':
                # Show dots like Pokemon (... ... ...)
                dots = "." * ((player.bite_timer // 30) % 4)
                status_text = self.title_font.render(f"...{dots}", True, (255, 255, 255))
                screen.blit(status_text, (SCREEN_WIDTH // 2 - 60, 940))
            elif player.fishing_state == 'bite':
                # Show "Oh! A bite!" message
                status_text = self.font.render("Oh! A bite!", True, (255, 255, 100))
                screen.blit(status_text, (SCREEN_WIDTH // 2 - 140, 930))
                prompt_text = self.small_font.render("Press SPACE!", True, (255, 255, 255))
                screen.blit(prompt_text, (SCREEN_WIDTH // 2 - 100, 990))
            elif player.fishing_state == 'failed':
                # Show "It got away!" message
                status_text = self.font.render("It got away...", True, (200, 100, 100))
                screen.blit(status_text, (SCREEN_WIDTH // 2 - 160, 940))

        # Bottom right controls (subtle, organized by category)
        controls = [
            ("Movement", [
                "↑↓←→ Move"
            ]),
            ("Fishing", [
                "SPACE Cast/Reel",
                "ENTER Confirm"
            ]),
            ("Menus", [
                "C Collection",
                "A Achievements",
                "S Shop",
                "T Stats"
            ]),
            ("System", [
                "P Pause",
                "ESC Back"
            ])
        ]

        y_offset = 580  # Fixed position for 1080p
        for category, category_controls in controls:
            # Category header (slightly brighter) - scaled
            header_text = self.small_font.render(category, True, (255, 215, 0))
            screen.blit(header_text, (SCREEN_WIDTH - 300, y_offset))
            y_offset += 40

            # Controls in category - scaled
            for control in category_controls:
                control_text = self.small_font.render(control, True, (180, 180, 180))
                screen.blit(control_text, (SCREEN_WIDTH - 290, y_offset))
                y_offset += 36

            y_offset += 10  # Extra spacing between categories
