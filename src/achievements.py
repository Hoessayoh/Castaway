import pygame
from fish import FISH_DATABASE


class Achievement:
    """Represents a single achievement"""

    def __init__(self, id, name, description, requirement, reward_gold, icon="🏆"):
        self.id = id
        self.name = name
        self.description = description
        self.requirement = requirement  # Function that checks if achieved
        self.reward_gold = reward_gold
        self.icon = icon
        self.unlocked = False
        self.progress = 0  # For tracking partial progress
        self.date_unlocked = None


class AchievementSystem:
    """Manages all achievements and tracks progress"""

    def __init__(self):
        self.achievements = {}
        self.total_rewards_earned = 0
        self.newly_unlocked = []  # Recently unlocked achievements to display
        self.notification_timer = 0

        # Initialize all achievements
        self.create_achievements()

    def create_achievements(self):
        """Create all game achievements"""

        # Beginner achievements
        self.add_achievement(Achievement(
            "first_catch", "First Catch!", "Catch your first fish",
            lambda stats: stats['total_catches'] >= 1,
            50, "🎣"
        ))

        self.add_achievement(Achievement(
            "early_fisher", "Early Fisher", "Catch 10 fish",
            lambda stats: stats['total_catches'] >= 10,
            100, "🐟"
        ))

        self.add_achievement(Achievement(
            "experienced_angler", "Experienced Angler", "Catch 50 fish",
            lambda stats: stats['total_catches'] >= 50,
            250, "🎯"
        ))

        self.add_achievement(Achievement(
            "master_fisher", "Master Fisher", "Catch 100 fish",
            lambda stats: stats['total_catches'] >= 100,
            500, "⭐"
        ))

        self.add_achievement(Achievement(
            "legendary_angler", "Legendary Angler", "Catch 500 fish",
            lambda stats: stats['total_catches'] >= 500,
            2000, "👑"
        ))

        # Collection achievements
        self.add_achievement(Achievement(
            "collector", "Collector", "Catch 5 different species",
            lambda stats: stats['unique_species'] >= 5,
            150, "📚"
        ))

        self.add_achievement(Achievement(
            "pokemon_master", "Pokemon Master", "Catch all fish species",
            lambda stats: stats['unique_species'] >= len(FISH_DATABASE),
            5000, "🎖️"
        ))

        self.add_achievement(Achievement(
            "pokedex_complete", "Pokedex Complete", "Catch both normal and shiny of every species",
            lambda stats: stats['complete_collection'],
            10000, "💎"
        ))

        # Shiny achievements
        self.add_achievement(Achievement(
            "shiny_hunter", "Shiny Hunter", "Catch your first shiny fish",
            lambda stats: stats['total_shinies'] >= 1,
            200, "✨"
        ))

        self.add_achievement(Achievement(
            "shiny_collector", "Shiny Collector", "Catch 10 shiny fish",
            lambda stats: stats['total_shinies'] >= 10,
            1000, "💫"
        ))

        self.add_achievement(Achievement(
            "shiny_master", "Shiny Master", "Catch 50 shiny fish",
            lambda stats: stats['total_shinies'] >= 50,
            5000, "🌟"
        ))

        # Rarity achievements
        self.add_achievement(Achievement(
            "uncommon_hunter", "Uncommon Hunter", "Catch 10 uncommon or rarer fish",
            lambda stats: stats['uncommon_plus'] >= 10,
            200, "🟢"
        ))

        self.add_achievement(Achievement(
            "rare_collector", "Rare Collector", "Catch 10 rare or rarer fish",
            lambda stats: stats['rare_plus'] >= 10,
            400, "🔵"
        ))

        self.add_achievement(Achievement(
            "epic_seeker", "Epic Seeker", "Catch 5 epic or rarer fish",
            lambda stats: stats['epic_plus'] >= 5,
            800, "🟣"
        ))

        self.add_achievement(Achievement(
            "legendary_finder", "Legendary Finder", "Catch your first legendary fish",
            lambda stats: stats['legendary_plus'] >= 1,
            1000, "🟠"
        ))

        self.add_achievement(Achievement(
            "mythic_champion", "Mythic Champion", "Catch a mythic fish",
            lambda stats: stats['mythic_count'] >= 1,
            3000, "🔴"
        ))

        # Gold achievements
        self.add_achievement(Achievement(
            "first_fortune", "First Fortune", "Earn 1,000 gold",
            lambda stats: stats['total_gold'] >= 1000,
            100, "💰"
        ))

        self.add_achievement(Achievement(
            "wealthy", "Wealthy", "Earn 10,000 gold",
            lambda stats: stats['total_gold'] >= 10000,
            500, "💵"
        ))

        self.add_achievement(Achievement(
            "millionaire", "Millionaire", "Earn 100,000 gold",
            lambda stats: stats['total_gold'] >= 100000,
            5000, "🤑"
        ))

        # Special achievements
        self.add_achievement(Achievement(
            "patient_fisher", "Patient Fisher", "Successfully catch a fish after waiting 3+ seconds",
            lambda stats: stats.get('patient_catch', False),
            100, "⏰"
        ))

        self.add_achievement(Achievement(
            "quick_reflexes", "Quick Reflexes", "Catch a fish within 0.5 seconds of the bite",
            lambda stats: stats.get('quick_catch', False),
            150, "⚡"
        ))

        self.add_achievement(Achievement(
            "perfect_streak", "Perfect Streak", "Catch 10 fish in a row without missing",
            lambda stats: stats.get('catch_streak', 0) >= 10,
            500, "🔥"
        ))

        self.add_achievement(Achievement(
            "completionist", "Completionist", "Unlock all other achievements",
            lambda stats: stats.get('all_unlocked', False),
            20000, "🏅"
        ))

    def add_achievement(self, achievement):
        """Add an achievement to the system"""
        self.achievements[achievement.id] = achievement

    def check_achievements(self, stats):
        """Check all achievements against current stats"""
        for achievement in self.achievements.values():
            if not achievement.unlocked and achievement.requirement(stats):
                self.unlock_achievement(achievement.id)

    def unlock_achievement(self, achievement_id):
        """Unlock an achievement and grant rewards"""
        if achievement_id not in self.achievements:
            return False

        achievement = self.achievements[achievement_id]
        if achievement.unlocked:
            return False

        achievement.unlocked = True
        import datetime
        achievement.date_unlocked = datetime.datetime.now()

        self.newly_unlocked.append(achievement)
        self.notification_timer = 240  # Show for 4 seconds
        self.total_rewards_earned += achievement.reward_gold

        return achievement.reward_gold

    def update(self):
        """Update achievement system (for notifications)"""
        if self.notification_timer > 0:
            self.notification_timer -= 1
            if self.notification_timer == 0:
                self.newly_unlocked.clear()

    def get_unlocked_count(self):
        """Get number of unlocked achievements"""
        return sum(1 for a in self.achievements.values() if a.unlocked)

    def get_total_count(self):
        """Get total number of achievements"""
        return len(self.achievements)

    def get_completion_percentage(self):
        """Get achievement completion percentage"""
        total = self.get_total_count()
        if total == 0:
            return 0
        return (self.get_unlocked_count() / total) * 100

    def get_achievements_by_status(self, unlocked=True):
        """Get achievements filtered by unlock status"""
        return [a for a in self.achievements.values() if a.unlocked == unlocked]


class AchievementUI:
    """UI for displaying achievements"""

    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 18)
        self.scroll_offset = 0

    def draw_box(self, screen, x, y, width, height, color=(60, 40, 30)):
        """Draw a styled box"""
        pygame.draw.rect(screen, (0, 0, 0, 50), (x + 3, y + 3, width, height))
        pygame.draw.rect(screen, color, (x, y, width, height))
        pygame.draw.rect(screen, (101, 67, 33), (x, y, width, height), 3)
        pygame.draw.rect(screen, (205, 133, 63), (x + 3, y + 3, width - 6, height - 6), 1)

    def draw_notification(self, screen, achievement_system, screen_width):
        """Draw achievement unlock notification"""
        if achievement_system.notification_timer > 0 and achievement_system.newly_unlocked:
            achievement = achievement_system.newly_unlocked[-1]

            # Notification box
            notif_width = 400
            notif_height = 100
            notif_x = screen_width // 2 - notif_width // 2
            notif_y = 50

            # Pulse effect
            import math
            pulse = abs(math.sin(achievement_system.notification_timer / 10))
            glow_color = (int(255 * pulse), int(215 * pulse), int(100 * pulse))

            # Draw with glow
            for i in range(3):
                alpha_surface = pygame.Surface((notif_width + i*4, notif_height + i*4), pygame.SRCALPHA)
                alpha_value = 100 - (i * 30)
                pygame.draw.rect(alpha_surface, (*glow_color, alpha_value),
                               (0, 0, notif_width + i*4, notif_height + i*4))
                screen.blit(alpha_surface, (notif_x - i*2, notif_y - i*2))

            self.draw_box(screen, notif_x, notif_y, notif_width, notif_height, (40, 20, 60))

            # Achievement unlocked text
            unlock_text = self.small_font.render("ACHIEVEMENT UNLOCKED!", True, (255, 215, 0))
            unlock_rect = unlock_text.get_rect(center=(notif_x + notif_width // 2, notif_y + 20))
            screen.blit(unlock_text, unlock_rect)

            # Icon and name
            icon_text = self.title_font.render(achievement.icon, True, (255, 255, 255))
            screen.blit(icon_text, (notif_x + 20, notif_y + 35))

            name_text = self.font.render(achievement.name, True, (255, 255, 255))
            screen.blit(name_text, (notif_x + 60, notif_y + 40))

            # Description
            desc_text = self.small_font.render(achievement.description, True, (200, 200, 200))
            screen.blit(desc_text, (notif_x + 60, notif_y + 60))

            # Reward
            reward_text = self.font.render(f"+{achievement.reward_gold} Gold", True, (255, 215, 0))
            screen.blit(reward_text, (notif_x + notif_width - 120, notif_y + 40))

    def draw(self, screen, achievement_system, screen_width, screen_height):
        """Draw achievements screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(200)
        overlay.fill((20, 20, 20))
        screen.blit(overlay, (0, 0))

        # Main box
        box_width = 700
        box_height = 500
        box_x = screen_width // 2 - box_width // 2
        box_y = screen_height // 2 - box_height // 2

        self.draw_box(screen, box_x, box_y, box_width, box_height)

        # Title
        title_text = self.title_font.render("Achievements", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(box_x + box_width // 2, box_y + 25))
        screen.blit(title_text, title_rect)

        # Progress
        unlocked = achievement_system.get_unlocked_count()
        total = achievement_system.get_total_count()
        completion = achievement_system.get_completion_percentage()

        progress_text = self.font.render(
            f"{unlocked}/{total} Unlocked ({completion:.1f}%)",
            True, (144, 238, 144)
        )
        screen.blit(progress_text, (box_x + 20, box_y + 55))

        # Total rewards
        reward_text = self.font.render(
            f"Total Rewards Earned: {achievement_system.total_rewards_earned} Gold",
            True, (255, 215, 0)
        )
        screen.blit(reward_text, (box_x + box_width - 350, box_y + 55))

        # Divider
        pygame.draw.line(screen, (255, 215, 0),
                        (box_x + 20, box_y + 80),
                        (box_x + box_width - 20, box_y + 80), 2)

        # Achievement list
        list_y = box_y + 95
        list_height = box_height - 130

        # Get all achievements sorted (unlocked first)
        sorted_achievements = sorted(
            achievement_system.achievements.values(),
            key=lambda a: (not a.unlocked, a.name)
        )

        current_y = list_y
        for achievement in sorted_achievements:
            if current_y + 65 > list_y + list_height:
                break

            # Achievement entry
            entry_color = (40, 60, 40) if achievement.unlocked else (30, 30, 30)
            pygame.draw.rect(screen, entry_color, (box_x + 20, current_y, box_width - 40, 60))

            border_color = (100, 200, 100) if achievement.unlocked else (60, 60, 60)
            pygame.draw.rect(screen, border_color, (box_x + 20, current_y, box_width - 40, 60), 2)

            # Icon
            icon_text = self.font.render(achievement.icon, True, (255, 255, 255))
            screen.blit(icon_text, (box_x + 30, current_y + 20))

            # Name
            name_color = (255, 255, 255) if achievement.unlocked else (120, 120, 120)
            name_text = self.font.render(achievement.name, True, name_color)
            screen.blit(name_text, (box_x + 65, current_y + 10))

            # Description
            desc_color = (200, 200, 200) if achievement.unlocked else (100, 100, 100)
            desc_text = self.small_font.render(achievement.description, True, desc_color)
            screen.blit(desc_text, (box_x + 65, current_y + 35))

            # Reward
            if achievement.unlocked:
                reward_badge = self.small_font.render("UNLOCKED", True, (100, 200, 100))
                screen.blit(reward_badge, (box_x + box_width - 150, current_y + 15))

            reward_value = self.font.render(f"{achievement.reward_gold}g", True, (255, 215, 0))
            screen.blit(reward_value, (box_x + box_width - 150, current_y + 35))

            current_y += 65

        # Instructions
        inst_text = self.small_font.render(
            "Press A to close | ESC to return to menu",
            True, (180, 180, 180)
        )
        inst_rect = inst_text.get_rect(center=(box_x + box_width // 2, box_y + box_height - 15))
        screen.blit(inst_text, inst_rect)
