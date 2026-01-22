"""
Comprehensive Statistics Tracking System
Tracks everything for leaderboards and player records
"""
import pygame
import json
import os
from datetime import datetime


class StatisticsTracker:
    """Track all player statistics"""

    def __init__(self):
        # Catch statistics
        self.total_catches = 0
        self.total_shinies = 0
        self.total_gold_earned = 0
        self.total_exp_earned = 0

        # Rarity breakdowns
        self.catches_by_rarity = {
            "common": 0, "uncommon": 0, "rare": 0,
            "epic": 0, "legendary": 0, "mythic": 0
        }

        # Time statistics
        self.total_playtime = 0  # in seconds
        self.session_start_time = datetime.now()
        self.longest_session = 0
        self.total_sessions = 0

        # Fishing statistics
        self.total_casts = 0
        self.successful_catches = 0
        self.missed_catches = 0
        self.perfect_casts = 0  # Instant bites
        self.fastest_catch = float('inf')  # Time from cast to catch
        self.slowest_catch = 0

        # Streak statistics
        self.best_catch_streak = 0
        self.current_streak = 0
        self.best_shiny_streak = 0
        self.best_perfect_streak = 0

        # Environmental statistics
        self.catches_by_weather = {
            "clear": 0, "rain": 0, "storm": 0, "fog": 0, "aurora": 0
        }
        self.catches_by_time = {
            "dawn": 0, "day": 0, "dusk": 0, "night": 0
        }
        self.catches_by_moon = {
            "new": 0, "waxing": 0, "full": 0, "waning": 0
        }

        # Rod statistics
        self.catches_by_rod = {}

        # Milestones
        self.first_catch_time = None
        self.first_shiny_time = None
        self.first_mythic_time = None
        self.collection_complete_time = None

        # Records
        self.most_valuable_fish = {"name": "None", "value": 0}
        self.rarest_catch = {"name": "None", "rarity": "common"}
        self.fastest_level_up = float('inf')

        # Daily/Weekly records
        self.catches_today = 0
        self.gold_today = 0
        self.last_daily_reset = datetime.now().date()

        # Load saved stats
        self.load()

    def record_catch(self, fish, rod_name, weather, time_of_day, moon_phase, catch_time, is_perfect):
        """Record a successful catch"""
        self.total_catches += 1
        self.successful_catches += 1
        self.catches_today += 1

        # Rarity tracking
        self.catches_by_rarity[fish.rarity] += 1

        # Shiny tracking
        if fish.is_shiny:
            self.total_shinies += 1
            if self.first_shiny_time is None:
                self.first_shiny_time = datetime.now()

        # Gold tracking
        self.total_gold_earned += fish.points
        self.gold_today += fish.points

        if fish.points > self.most_valuable_fish["value"]:
            self.most_valuable_fish = {"name": fish.name, "value": fish.points}

        # Environmental tracking
        if weather in self.catches_by_weather:
            self.catches_by_weather[weather] += 1
        if time_of_day in self.catches_by_time:
            self.catches_by_time[time_of_day] += 1
        if moon_phase in self.catches_by_moon:
            self.catches_by_moon[moon_phase] += 1

        # Rod tracking
        if rod_name not in self.catches_by_rod:
            self.catches_by_rod[rod_name] = 0
        self.catches_by_rod[rod_name] += 1

        # Time tracking
        if catch_time < self.fastest_catch:
            self.fastest_catch = catch_time
        if catch_time > self.slowest_catch:
            self.slowest_catch = catch_time

        # Perfect cast tracking
        if is_perfect:
            self.perfect_casts += 1

        # First catch milestone
        if self.first_catch_time is None:
            self.first_catch_time = datetime.now()

        # Mythic milestone
        if fish.rarity == "mythic" and self.first_mythic_time is None:
            self.first_mythic_time = datetime.now()

    def record_miss(self):
        """Record a missed catch"""
        self.missed_catches += 1
        self.current_streak = 0

    def record_cast(self):
        """Record a fishing line cast"""
        self.total_casts += 1

    def update_playtime(self):
        """Update total playtime"""
        current_session = (datetime.now() - self.session_start_time).total_seconds()
        if current_session > self.longest_session:
            self.longest_session = current_session

    def check_daily_reset(self):
        """Reset daily statistics if new day"""
        today = datetime.now().date()
        if today != self.last_daily_reset:
            self.catches_today = 0
            self.gold_today = 0
            self.last_daily_reset = today

    def get_catch_rate(self):
        """Get overall catch success rate"""
        total_attempts = self.successful_catches + self.missed_catches
        if total_attempts == 0:
            return 0
        return (self.successful_catches / total_attempts) * 100

    def get_shiny_rate(self):
        """Get shiny catch rate"""
        if self.total_catches == 0:
            return 0
        return (self.total_shinies / self.total_catches) * 100

    def get_average_gold_per_catch(self):
        """Get average gold per catch"""
        if self.total_catches == 0:
            return 0
        return self.total_gold_earned / self.total_catches

    def save(self):
        """Save statistics to file"""
        data = {
            'total_catches': self.total_catches,
            'total_shinies': self.total_shinies,
            'total_gold_earned': self.total_gold_earned,
            'total_exp_earned': self.total_exp_earned,
            'catches_by_rarity': self.catches_by_rarity,
            'total_playtime': self.total_playtime,
            'longest_session': self.longest_session,
            'total_sessions': self.total_sessions,
            'total_casts': self.total_casts,
            'successful_catches': self.successful_catches,
            'missed_catches': self.missed_catches,
            'perfect_casts': self.perfect_casts,
            'fastest_catch': self.fastest_catch,
            'slowest_catch': self.slowest_catch,
            'best_catch_streak': self.best_catch_streak,
            'best_shiny_streak': self.best_shiny_streak,
            'best_perfect_streak': self.best_perfect_streak,
            'catches_by_weather': self.catches_by_weather,
            'catches_by_time': self.catches_by_time,
            'catches_by_moon': self.catches_by_moon,
            'catches_by_rod': self.catches_by_rod,
            'first_catch_time': self.first_catch_time.isoformat() if self.first_catch_time else None,
            'first_shiny_time': self.first_shiny_time.isoformat() if self.first_shiny_time else None,
            'first_mythic_time': self.first_mythic_time.isoformat() if self.first_mythic_time else None,
            'most_valuable_fish': self.most_valuable_fish,
            'rarest_catch': self.rarest_catch,
            'last_daily_reset': self.last_daily_reset.isoformat()
        }
        with open('statistics.json', 'w') as f:
            json.dump(data, f, indent=2)

    def load(self):
        """Load statistics from file"""
        if os.path.exists('statistics.json'):
            try:
                with open('statistics.json', 'r') as f:
                    data = json.load(f)
                    for key, value in data.items():
                        if hasattr(self, key):
                            if 'time' in key and value:
                                setattr(self, key, datetime.fromisoformat(value))
                            elif key == 'last_daily_reset':
                                setattr(self, key, datetime.fromisoformat(value).date())
                            else:
                                setattr(self, key, value)
            except Exception as e:
                print(f"Error loading statistics: {e}")


class StatisticsUI:
    """UI for displaying statistics"""

    def __init__(self):
        self.font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 16)

    def draw_box(self, screen, x, y, width, height, color=(60, 50, 70)):
        """Draw a styled box"""
        pygame.draw.rect(screen, (0, 0, 0, 50), (x + 3, y + 3, width, height))
        pygame.draw.rect(screen, color, (x, y, width, height))
        pygame.draw.rect(screen, (101, 67, 33), (x, y, width, height), 3)
        pygame.draw.rect(screen, (205, 133, 63), (x + 3, y + 3, width - 6, height - 6), 1)

    def draw(self, screen, stats, screen_width, screen_height):
        """Draw statistics screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(200)
        overlay.fill((15, 15, 25))
        screen.blit(overlay, (0, 0))

        # Main stats box
        box_width = 700
        box_height = 500
        box_x = screen_width // 2 - box_width // 2
        box_y = screen_height // 2 - box_height // 2

        self.draw_box(screen, box_x, box_y, box_width, box_height)

        # Title
        title_text = self.title_font.render("Statistics & Records", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(box_x + box_width // 2, box_y + 20))
        screen.blit(title_text, title_rect)

        # Two column layout
        left_x = box_x + 20
        right_x = box_x + box_width // 2 + 10
        current_y = box_y + 50

        # Left column - Catch Statistics
        self.draw_section_title(screen, left_x, current_y, "Catch Statistics")
        current_y += 25

        catch_stats = [
            f"Total Catches: {stats.total_catches}",
            f"Success Rate: {stats.get_catch_rate():.1f}%",
            f"Total Shinies: {stats.total_shinies}",
            f"Shiny Rate: {stats.get_shiny_rate():.2f}%",
            f"Perfect Casts: {stats.perfect_casts}",
            f"Best Streak: {stats.best_catch_streak}",
        ]

        for stat in catch_stats:
            stat_text = self.font.render(stat, True, (200, 200, 200))
            screen.blit(stat_text, (left_x, current_y))
            current_y += 20

        # Rarity breakdown
        current_y += 10
        self.draw_section_title(screen, left_x, current_y, "By Rarity")
        current_y += 25

        rarity_colors = {
            "common": (200, 200, 200),
            "uncommon": (30, 255, 0),
            "rare": (0, 112, 221),
            "epic": (163, 53, 238),
            "legendary": (255, 128, 0),
            "mythic": (255, 40, 40)
        }

        for rarity, count in stats.catches_by_rarity.items():
            color = rarity_colors.get(rarity, (255, 255, 255))
            rarity_text = self.font.render(f"{rarity.title()}: {count}", True, color)
            screen.blit(rarity_text, (left_x, current_y))
            current_y += 18

        # Right column - Economic & Time Stats
        current_y = box_y + 50
        self.draw_section_title(screen, right_x, current_y, "Economic Stats")
        current_y += 25

        econ_stats = [
            f"Total Gold: {stats.total_gold_earned:,}",
            f"Gold Today: {stats.gold_today:,}",
            f"Avg per Catch: {stats.get_average_gold_per_catch():.1f}",
            f"Most Valuable: {stats.most_valuable_fish['name']}",
            f"  ({stats.most_valuable_fish['value']}g)",
        ]

        for stat in econ_stats:
            stat_text = self.font.render(stat, True, (255, 215, 0))
            screen.blit(stat_text, (right_x, current_y))
            current_y += 20

        # Time stats
        current_y += 10
        self.draw_section_title(screen, right_x, current_y, "Time Stats")
        current_y += 25

        time_stats = [
            f"Total Casts: {stats.total_casts}",
            f"Catches Today: {stats.catches_today}",
        ]

        if stats.fastest_catch != float('inf'):
            time_stats.append(f"Fastest: {stats.fastest_catch:.1f}s")
        if stats.slowest_catch > 0:
            time_stats.append(f"Slowest: {stats.slowest_catch:.1f}s")

        for stat in time_stats:
            stat_text = self.font.render(stat, True, (144, 238, 144))
            screen.blit(stat_text, (right_x, current_y))
            current_y += 20

        # Bottom section - Environment breakdown
        bottom_y = box_y + box_height - 100
        self.draw_section_title(screen, box_x + 20, bottom_y, "Environmental Catches")
        bottom_y += 20

        # Weather breakdown
        weather_x = box_x + 20
        weather_text = self.small_font.render("Weather:", True, (180, 180, 180))
        screen.blit(weather_text, (weather_x, bottom_y))
        bottom_y += 15

        for weather, count in stats.catches_by_weather.items():
            if count > 0:
                w_text = self.small_font.render(f"{weather}: {count}", True, (150, 150, 200))
                screen.blit(w_text, (weather_x, bottom_y))
                bottom_y += 14

        # Instructions
        inst_text = self.small_font.render(
            "Press T to close | ESC to return to menu",
            True, (180, 180, 180)
        )
        inst_rect = inst_text.get_rect(center=(box_x + box_width // 2, box_y + box_height - 15))
        screen.blit(inst_text, inst_rect)

    def draw_section_title(self, screen, x, y, title):
        """Draw a section title"""
        title_surf = self.font.render(title, True, (255, 215, 0))
        screen.blit(title_surf, (x, y))
        # Underline
        pygame.draw.line(screen, (255, 215, 0), (x, y + 18), (x + 200, y + 18), 1)
