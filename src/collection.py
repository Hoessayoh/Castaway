import pygame
from fish import FISH_DATABASE, RARITY_WEIGHTS


class Collection:
    """Pokedex-style fish collection tracker"""

    def __init__(self):
        # Track what fish have been caught (fish_id -> {'normal': count, 'shiny': count})
        self.caught_fish = {}

        # Statistics
        self.total_catches = 0
        self.unique_fish_caught = 0
        self.total_shiny_caught = 0

        # Initialize all fish as not caught
        for fish_id in FISH_DATABASE.keys():
            self.caught_fish[fish_id] = {'normal': 0, 'shiny': 0}

    def add_catch(self, fish_id, is_shiny=False):
        """Record a fish catch"""
        if fish_id not in self.caught_fish:
            self.caught_fish[fish_id] = {'normal': 0, 'shiny': 0}

        if is_shiny:
            self.caught_fish[fish_id]['shiny'] += 1
            self.total_shiny_caught += 1
        else:
            self.caught_fish[fish_id]['normal'] += 1

        self.total_catches += 1
        self.update_stats()

    def update_stats(self):
        """Update collection statistics"""
        self.unique_fish_caught = sum(
            1 for fish_data in self.caught_fish.values()
            if fish_data['normal'] > 0 or fish_data['shiny'] > 0
        )

    def has_caught(self, fish_id, shiny=False):
        """Check if a specific fish has been caught"""
        if fish_id not in self.caught_fish:
            return False
        if shiny:
            return self.caught_fish[fish_id]['shiny'] > 0
        return self.caught_fish[fish_id]['normal'] > 0

    def get_catch_count(self, fish_id, shiny=False):
        """Get the number of times a fish has been caught"""
        if fish_id not in self.caught_fish:
            return 0
        return self.caught_fish[fish_id]['shiny' if shiny else 'normal']

    def get_completion_percentage(self):
        """Get overall collection completion percentage"""
        total_fish = len(FISH_DATABASE)
        return (self.unique_fish_caught / total_fish * 100) if total_fish > 0 else 0

    def get_shiny_completion_percentage(self):
        """Get shiny collection completion percentage"""
        total_fish = len(FISH_DATABASE)
        shiny_caught = sum(
            1 for fish_data in self.caught_fish.values()
            if fish_data['shiny'] > 0
        )
        return (shiny_caught / total_fish * 100) if total_fish > 0 else 0

    def get_rarity_stats(self):
        """Get statistics by rarity tier"""
        rarity_stats = {
            "common": {"caught": 0, "total": 0},
            "uncommon": {"caught": 0, "total": 0},
            "rare": {"caught": 0, "total": 0},
            "epic": {"caught": 0, "total": 0},
            "legendary": {"caught": 0, "total": 0},
            "mythic": {"caught": 0, "total": 0}
        }

        for fish_id, fish_data in FISH_DATABASE.items():
            rarity = fish_data['rarity']
            rarity_stats[rarity]['total'] += 1

            if self.has_caught(fish_id):
                rarity_stats[rarity]['caught'] += 1

        return rarity_stats


class CollectionUI:
    """UI for displaying the Pokedex-style collection"""

    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 18)
        self.scroll_offset = 0
        self.selected_fish = None

        # Rarity colors
        self.rarity_colors = {
            "common": (200, 200, 200),      # Gray
            "uncommon": (30, 255, 0),       # Green
            "rare": (0, 112, 221),          # Blue
            "epic": (163, 53, 238),         # Purple
            "legendary": (255, 128, 0),     # Orange
            "mythic": (255, 40, 40)         # Red
        }

    def draw_box(self, screen, x, y, width, height, color=(139, 69, 19)):
        """Draw a styled box"""
        # Shadow
        pygame.draw.rect(screen, (0, 0, 0, 50), (x + 3, y + 3, width, height))
        # Background
        pygame.draw.rect(screen, color, (x, y, width, height))
        # Border
        pygame.draw.rect(screen, (101, 67, 33), (x, y, width, height), 3)
        # Inner highlight
        pygame.draw.rect(screen, (205, 133, 63), (x + 3, y + 3, width - 6, height - 6), 1)

    def draw(self, screen, collection, screen_width, screen_height):
        """Draw the collection UI (Pokedex view)"""
        # Semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 20))
        screen.blit(overlay, (0, 0))

        # Main collection box
        box_width = 700
        box_height = 500
        box_x = screen_width // 2 - box_width // 2
        box_y = screen_height // 2 - box_height // 2

        self.draw_box(screen, box_x, box_y, box_width, box_height, (50, 30, 20))

        # Title
        title_text = self.title_font.render("Fish Collection", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(box_x + box_width // 2, box_y + 25))
        screen.blit(title_text, title_rect)

        # Stats header
        stats_y = box_y + 55
        completion = collection.get_completion_percentage()
        stats_text = self.font.render(
            f"Caught: {collection.unique_fish_caught}/{len(FISH_DATABASE)} ({completion:.1f}%)",
            True, (144, 238, 144)
        )
        screen.blit(stats_text, (box_x + 20, stats_y))

        # Shiny stats
        shiny_completion = collection.get_shiny_completion_percentage()
        shiny_text = self.font.render(
            f"Shinies: {shiny_completion:.1f}% | Total catches: {collection.total_catches}",
            True, (255, 215, 180)
        )
        screen.blit(shiny_text, (box_x + 20, stats_y + 25))

        # Divider line
        pygame.draw.line(screen, (255, 215, 0),
                        (box_x + 20, stats_y + 50),
                        (box_x + box_width - 20, stats_y + 50), 2)

        # Fish list (grid layout)
        list_y = stats_y + 65
        list_height = box_height - 140

        # Sort fish by rarity and name
        sorted_fish = sorted(
            FISH_DATABASE.items(),
            key=lambda x: (
                list(RARITY_WEIGHTS.keys()).index(x[1]['rarity']),
                x[1]['name']
            )
        )

        # Draw fish entries in a grid
        col_width = (box_width - 60) // 2
        row_height = 60
        current_y = list_y
        current_col = 0

        for fish_id, fish_data in sorted_fish:
            if current_y > list_y + list_height - row_height:
                break

            x_pos = box_x + 20 + (current_col * (col_width + 20))
            y_pos = current_y

            # Check if caught
            has_normal = collection.has_caught(fish_id, shiny=False)
            has_shiny = collection.has_caught(fish_id, shiny=True)
            is_caught = has_normal or has_shiny

            # Entry background
            entry_color = (40, 40, 40) if is_caught else (20, 20, 20)
            pygame.draw.rect(screen, entry_color, (x_pos, y_pos, col_width, row_height - 5))

            # Rarity border
            rarity_color = self.rarity_colors.get(fish_data['rarity'], (255, 255, 255))
            pygame.draw.rect(screen, rarity_color, (x_pos, y_pos, col_width, row_height - 5), 2)

            if is_caught:
                # Fish name
                name_text = self.font.render(fish_data['name'], True, rarity_color)
                screen.blit(name_text, (x_pos + 5, y_pos + 5))

                # Catch counts
                normal_count = collection.get_catch_count(fish_id, shiny=False)
                shiny_count = collection.get_catch_count(fish_id, shiny=True)

                count_str = f"×{normal_count}"
                if shiny_count > 0:
                    count_str += f" ✨×{shiny_count}"

                count_text = self.small_font.render(count_str, True, (200, 200, 200))
                screen.blit(count_text, (x_pos + 5, y_pos + 30))

                # Points value
                points_text = self.small_font.render(f"{fish_data['points']} gold", True, (255, 215, 0))
                screen.blit(points_text, (x_pos + col_width - 70, y_pos + 30))
            else:
                # Show ??? for uncaught fish
                mystery_text = self.font.render("???", True, (100, 100, 100))
                screen.blit(mystery_text, (x_pos + 5, y_pos + 5))

                # Show rarity hint
                rarity_text = self.small_font.render(fish_data['rarity'].upper(), True, rarity_color)
                screen.blit(rarity_text, (x_pos + 5, y_pos + 30))

            # Move to next position
            current_col += 1
            if current_col >= 2:
                current_col = 0
                current_y += row_height

        # Rarity breakdown at bottom
        breakdown_y = box_y + box_height - 60
        pygame.draw.line(screen, (255, 215, 0),
                        (box_x + 20, breakdown_y - 10),
                        (box_x + box_width - 20, breakdown_y - 10), 2)

        breakdown_text = self.small_font.render("Rarity Breakdown:", True, (255, 215, 0))
        screen.blit(breakdown_text, (box_x + 20, breakdown_y))

        rarity_stats = collection.get_rarity_stats()
        rarity_x = box_x + 20
        rarity_y = breakdown_y + 20

        for rarity, stats in rarity_stats.items():
            color = self.rarity_colors.get(rarity, (255, 255, 255))
            rarity_label = self.small_font.render(
                f"{rarity.upper()}: {stats['caught']}/{stats['total']}",
                True, color
            )
            screen.blit(rarity_label, (rarity_x, rarity_y))
            rarity_x += 110

        # Instructions
        instruction_text = self.small_font.render(
            "Press C to close collection | ESC to return to menu",
            True, (180, 180, 180)
        )
        inst_rect = instruction_text.get_rect(center=(box_x + box_width // 2, box_y + box_height - 15))
        screen.blit(instruction_text, inst_rect)
