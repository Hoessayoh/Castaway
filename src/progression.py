import pygame


class Rod:
    """Represents a fishing rod with different stats"""

    def __init__(self, id, name, description, level_req, cost, bite_speed_mult, shiny_mult, rarity_boost):
        self.id = id
        self.name = name
        self.description = description
        self.level_req = level_req  # Level required to purchase
        self.cost = cost  # Gold cost
        self.bite_speed_mult = bite_speed_mult  # Multiplier for how fast fish bite (lower = faster)
        self.shiny_mult = shiny_mult  # Multiplier for shiny chance
        self.rarity_boost = rarity_boost  # Boost to rarity chances (0-1, added to rare+ chances)
        self.owned = False


class PlayerProgression:
    """Track player level, experience, and upgrades"""

    def __init__(self):
        # Experience and leveling
        self.experience = 0
        self.level = 1
        self.experience_to_next_level = 100

        # Fishing rods
        self.current_rod = None
        self.owned_rods = []
        self.init_rods()

        # Stats
        self.total_experience_earned = 0
        self.highest_level_reached = 1

    def init_rods(self):
        """Initialize all fishing rods"""
        self.rods = {
            "basic": Rod(
                "basic", "Basic Rod", "A simple fishing rod. Everyone starts here.",
                level_req=1, cost=0, bite_speed_mult=1.0, shiny_mult=1.0, rarity_boost=0.0
            ),
            "training": Rod(
                "training", "Training Rod", "Slightly better than basic. Fish bite faster!",
                level_req=3, cost=500, bite_speed_mult=0.85, shiny_mult=1.0, rarity_boost=0.0
            ),
            "steel": Rod(
                "steel", "Steel Rod", "A sturdy rod. Increases rare fish chances.",
                level_req=5, cost=1500, bite_speed_mult=0.75, shiny_mult=1.0, rarity_boost=0.05
            ),
            "lucky": Rod(
                "lucky", "Lucky Rod", "Infused with luck. Better shiny chance!",
                level_req=8, cost=3000, bite_speed_mult=0.75, shiny_mult=1.5, rarity_boost=0.05
            ),
            "master": Rod(
                "master", "Master Rod", "For experienced anglers. Great all-around stats.",
                level_req=12, cost=7500, bite_speed_mult=0.6, shiny_mult=1.75, rarity_boost=0.10
            ),
            "legendary": Rod(
                "legendary", "Legendary Rod", "A rod of legend. Significantly better everything.",
                level_req=20, cost=20000, bite_speed_mult=0.5, shiny_mult=2.0, rarity_boost=0.15
            ),
            "mythic": Rod(
                "mythic", "Mythic Rod", "The ultimate fishing tool. Unmatched power.",
                level_req=30, cost=50000, bite_speed_mult=0.35, shiny_mult=3.0, rarity_boost=0.25
            )
        }

        # Start with basic rod
        self.rods["basic"].owned = True
        self.owned_rods.append("basic")
        self.current_rod = self.rods["basic"]

    def add_experience(self, amount):
        """Add experience and handle leveling up"""
        self.experience += amount
        self.total_experience_earned += amount
        leveled_up = False

        while self.experience >= self.experience_to_next_level:
            self.experience -= self.experience_to_next_level
            self.level += 1
            self.highest_level_reached = max(self.highest_level_reached, self.level)
            leveled_up = True

            # Increase exp requirement for next level
            self.experience_to_next_level = int(self.experience_to_next_level * 1.15)

        return leveled_up

    def can_purchase_rod(self, rod_id):
        """Check if player can purchase a rod"""
        if rod_id not in self.rods:
            return False

        rod = self.rods[rod_id]
        return (not rod.owned and
                self.level >= rod.level_req)

    def purchase_rod(self, rod_id, player_gold):
        """Attempt to purchase a rod"""
        if not self.can_purchase_rod(rod_id):
            return False, "Requirements not met"

        rod = self.rods[rod_id]
        if player_gold < rod.cost:
            return False, "Not enough gold"

        rod.owned = True
        self.owned_rods.append(rod_id)
        return True, rod.cost

    def equip_rod(self, rod_id):
        """Equip a rod"""
        if rod_id not in self.rods or not self.rods[rod_id].owned:
            return False

        self.current_rod = self.rods[rod_id]
        return True

    def get_exp_for_fish(self, fish_rarity, is_shiny):
        """Calculate experience gain from catching a fish"""
        base_exp = {
            "common": 5,
            "uncommon": 15,
            "rare": 30,
            "epic": 60,
            "legendary": 120,
            "mythic": 250
        }

        exp = base_exp.get(fish_rarity, 5)

        # Shiny bonus
        if is_shiny:
            exp = int(exp * 2)

        return exp


class ProgressionUI:
    """UI for player progression and shop"""

    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 18)
        self.large_font = pygame.font.Font(None, 48)

        self.selected_rod = 0  # For shop navigation

    def draw_box(self, screen, x, y, width, height, color=(80, 60, 40)):
        """Draw a styled box"""
        pygame.draw.rect(screen, (0, 0, 0, 50), (x + 3, y + 3, width, height))
        pygame.draw.rect(screen, color, (x, y, width, height))
        pygame.draw.rect(screen, (101, 67, 33), (x, y, width, height), 3)
        pygame.draw.rect(screen, (205, 133, 63), (x + 3, y + 3, width - 6, height - 6), 1)

    def draw_level_up_notification(self, screen, new_level, screen_width):
        """Draw level up notification"""
        notif_width = 400
        notif_height = 100
        notif_x = screen_width // 2 - notif_width // 2
        notif_y = 150

        # Animated glow
        import math
        pulse = abs(math.sin(pygame.time.get_ticks() / 100))
        glow_color = (int(255 * pulse), int(215 * pulse), 0)

        # Draw glow
        for i in range(5):
            alpha_surface = pygame.Surface((notif_width + i*6, notif_height + i*6), pygame.SRCALPHA)
            alpha_value = 120 - (i * 25)
            pygame.draw.rect(alpha_surface, (*glow_color, alpha_value),
                           (0, 0, notif_width + i*6, notif_height + i*6))
            screen.blit(alpha_surface, (notif_x - i*3, notif_y - i*3))

        self.draw_box(screen, notif_x, notif_y, notif_width, notif_height, (60, 30, 90))

        # Level up text
        level_text = self.large_font.render("LEVEL UP!", True, (255, 215, 0))
        level_rect = level_text.get_rect(center=(notif_x + notif_width // 2, notif_y + 35))
        screen.blit(level_text, level_rect)

        # New level
        new_level_text = self.title_font.render(f"Level {new_level}", True, (255, 255, 255))
        new_level_rect = new_level_text.get_rect(center=(notif_x + notif_width // 2, notif_y + 70))
        screen.blit(new_level_text, new_level_rect)

    def draw_shop(self, screen, progression, player_gold, screen_width, screen_height):
        """Draw the rod shop"""
        # Semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 20))
        screen.blit(overlay, (0, 0))

        # Main shop box
        box_width = 700
        box_height = 500
        box_x = screen_width // 2 - box_width // 2
        box_y = screen_height // 2 - box_height // 2

        self.draw_box(screen, box_x, box_y, box_width, box_height)

        # Title
        title_text = self.title_font.render("Rod Shop & Progression", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(box_x + box_width // 2, box_y + 25))
        screen.blit(title_text, title_rect)

        # Player stats
        stats_y = box_y + 60
        level_text = self.font.render(f"Level {progression.level}", True, (144, 238, 144))
        screen.blit(level_text, (box_x + 20, stats_y))

        # Experience bar
        exp_progress = progression.experience / progression.experience_to_next_level
        bar_width = 250
        bar_height = 20
        bar_x = box_x + 120
        bar_y = stats_y

        # Background bar
        pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_width, bar_height))
        # Progress bar
        pygame.draw.rect(screen, (100, 200, 100), (bar_x, bar_y, int(bar_width * exp_progress), bar_height))
        # Border
        pygame.draw.rect(screen, (200, 200, 200), (bar_x, bar_y, bar_width, bar_height), 2)

        # EXP text
        exp_text = self.small_font.render(
            f"{progression.experience}/{progression.experience_to_next_level} EXP",
            True, (255, 255, 255)
        )
        exp_rect = exp_text.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
        screen.blit(exp_text, exp_rect)

        # Gold
        gold_text = self.font.render(f"Gold: {player_gold}", True, (255, 215, 0))
        screen.blit(gold_text, (box_x + box_width - 180, stats_y))

        # Current rod indicator
        current_rod_text = self.small_font.render(
            f"Equipped: {progression.current_rod.name}",
            True, (100, 200, 255)
        )
        screen.blit(current_rod_text, (box_x + 20, stats_y + 25))

        # Divider
        pygame.draw.line(screen, (255, 215, 0),
                        (box_x + 20, stats_y + 50),
                        (box_x + box_width - 20, stats_y + 50), 2)

        # Rod list
        list_y = stats_y + 65
        list_height = box_height - 160

        # Get all rods sorted by level requirement
        sorted_rods = sorted(progression.rods.values(), key=lambda r: r.level_req)

        current_y = list_y
        for rod in sorted_rods:
            if current_y + 70 > list_y + list_height:
                break

            # Rod entry
            is_equipped = progression.current_rod.id == rod.id
            is_owned = rod.owned
            can_buy = progression.can_purchase_rod(rod.id) and player_gold >= rod.cost

            # Entry background color
            if is_equipped:
                entry_color = (50, 70, 90)  # Blue for equipped
            elif is_owned:
                entry_color = (50, 60, 50)  # Green for owned
            elif can_buy:
                entry_color = (60, 60, 40)  # Yellow-ish for available
            else:
                entry_color = (40, 40, 40)  # Gray for locked

            pygame.draw.rect(screen, entry_color, (box_x + 20, current_y, box_width - 40, 65))

            border_color = (100, 150, 200) if is_equipped else (80, 80, 80)
            pygame.draw.rect(screen, border_color, (box_x + 20, current_y, box_width - 40, 65), 2)

            # Rod name
            name_color = (255, 255, 255) if is_owned else (150, 150, 150)
            name_text = self.font.render(rod.name, True, name_color)
            screen.blit(name_text, (box_x + 30, current_y + 8))

            # Level requirement
            level_req_color = (100, 200, 100) if progression.level >= rod.level_req else (200, 100, 100)
            level_req_text = self.small_font.render(f"Lv.{rod.level_req}", True, level_req_color)
            screen.blit(level_req_text, (box_x + box_width - 100, current_y + 8))

            # Description
            desc_text = self.small_font.render(rod.description, True, (180, 180, 180))
            screen.blit(desc_text, (box_x + 30, current_y + 30))

            # Stats preview
            stats_str = f"Bite: {int(rod.bite_speed_mult*100)}% | Shiny: {int(rod.shiny_mult*100)}% | Rarity: +{int(rod.rarity_boost*100)}%"
            stats_text = self.small_font.render(stats_str, True, (200, 200, 150))
            screen.blit(stats_text, (box_x + 30, current_y + 47))

            # Cost/Status
            if is_equipped:
                status_text = self.small_font.render("EQUIPPED", True, (100, 200, 255))
                screen.blit(status_text, (box_x + box_width - 100, current_y + 45))
            elif is_owned:
                status_text = self.small_font.render("OWNED", True, (100, 200, 100))
                screen.blit(status_text, (box_x + box_width - 100, current_y + 30))
                equip_text = self.small_font.render("(Click to equip)", True, (150, 150, 200))
                screen.blit(equip_text, (box_x + box_width - 120, current_y + 47))
            else:
                cost_color = (255, 215, 0) if can_buy else (150, 150, 150)
                cost_text = self.font.render(f"{rod.cost}g", True, cost_color)
                screen.blit(cost_text, (box_x + box_width - 100, current_y + 30))

                if not can_buy and progression.level < rod.level_req:
                    lock_text = self.small_font.render("LOCKED", True, (200, 100, 100))
                    screen.blit(lock_text, (box_x + box_width - 100, current_y + 50))

            current_y += 70

        # Instructions
        inst_text = self.small_font.render(
            "Press S to close | ESC to return to menu",
            True, (180, 180, 180)
        )
        inst_rect = inst_text.get_rect(center=(box_x + box_width // 2, box_y + box_height - 15))
        screen.blit(inst_text, inst_rect)
