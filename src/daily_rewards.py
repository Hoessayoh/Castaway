import pygame
import json
import os
from datetime import datetime, timedelta


class DailyRewards:
    """Daily login rewards and streak system"""

    def __init__(self):
        self.save_file = "daily_rewards.json"
        self.current_streak = 0
        self.longest_streak = 0
        self.last_login_date = None
        self.total_logins = 0
        self.rewards_claimed_today = False
        self.today_reward_gold = 0
        self.today_reward_exp = 0

        # Load saved data
        self.load()

        # Check and update streak
        self.check_daily_login()

    def load(self):
        """Load daily rewards data from file"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    self.current_streak = data.get('current_streak', 0)
                    self.longest_streak = data.get('longest_streak', 0)
                    last_login = data.get('last_login_date')
                    if last_login:
                        self.last_login_date = datetime.fromisoformat(last_login)
                    self.total_logins = data.get('total_logins', 0)
            except:
                pass

    def save(self):
        """Save daily rewards data to file"""
        data = {
            'current_streak': self.current_streak,
            'longest_streak': self.longest_streak,
            'last_login_date': self.last_login_date.isoformat() if self.last_login_date else None,
            'total_logins': self.total_logins
        }
        with open(self.save_file, 'w') as f:
            json.dump(data, f)

    def check_daily_login(self):
        """Check if this is a new day and update streak"""
        today = datetime.now().date()

        if self.last_login_date is None:
            # First time login
            self.current_streak = 1
            self.longest_streak = 1
            self.last_login_date = datetime.now()
            self.total_logins = 1
            self.rewards_claimed_today = False
            self.calculate_daily_reward()
            self.save()
            return True

        last_date = self.last_login_date.date()

        if last_date == today:
            # Already logged in today
            return False

        yesterday = today - timedelta(days=1)

        if last_date == yesterday:
            # Consecutive day - increase streak
            self.current_streak += 1
            self.longest_streak = max(self.longest_streak, self.current_streak)
        else:
            # Streak broken
            self.current_streak = 1

        self.last_login_date = datetime.now()
        self.total_logins += 1
        self.rewards_claimed_today = False
        self.calculate_daily_reward()
        self.save()
        return True

    def calculate_daily_reward(self):
        """Calculate today's reward based on streak"""
        # Base reward
        base_gold = 50
        base_exp = 25

        # Streak multiplier (caps at 2x for 7+ day streak)
        streak_mult = min(1 + (self.current_streak - 1) * 0.15, 2.0)

        # Milestone bonuses
        milestone_bonus_gold = 0
        milestone_bonus_exp = 0

        if self.current_streak == 7:
            milestone_bonus_gold = 200
            milestone_bonus_exp = 100
        elif self.current_streak == 30:
            milestone_bonus_gold = 1000
            milestone_bonus_exp = 500
        elif self.current_streak == 100:
            milestone_bonus_gold = 5000
            milestone_bonus_exp = 2500

        self.today_reward_gold = int(base_gold * streak_mult) + milestone_bonus_gold
        self.today_reward_exp = int(base_exp * streak_mult) + milestone_bonus_exp

    def claim_daily_reward(self):
        """Claim today's daily reward"""
        if self.rewards_claimed_today:
            return None, None

        self.rewards_claimed_today = True
        return self.today_reward_gold, self.today_reward_exp

    def has_unclaimed_reward(self):
        """Check if there's an unclaimed daily reward"""
        return not self.rewards_claimed_today


class DailyRewardsUI:
    """UI for daily rewards"""

    def __init__(self):
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 18)

    def draw_box(self, screen, x, y, width, height, color=(80, 60, 40)):
        """Draw a styled box"""
        pygame.draw.rect(screen, (0, 0, 0, 50), (x + 3, y + 3, width, height))
        pygame.draw.rect(screen, color, (x, y, width, height))
        pygame.draw.rect(screen, (101, 67, 33), (x, y, width, height), 3)
        pygame.draw.rect(screen, (205, 133, 63), (x + 3, y + 3, width - 6, height - 6), 1)

    def draw_daily_reward_popup(self, screen, daily_rewards, screen_width, screen_height):
        """Draw daily reward claim popup"""
        # Semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height))
        overlay.set_alpha(220)
        overlay.fill((10, 10, 30))
        screen.blit(overlay, (0, 0))

        # Popup box
        box_width = 500
        box_height = 400
        box_x = screen_width // 2 - box_width // 2
        box_y = screen_height // 2 - box_height // 2

        # Animated glow
        import math
        pulse = abs(math.sin(pygame.time.get_ticks() / 200))
        glow_color = (int(255 * pulse), int(215 * pulse), 0)

        for i in range(5):
            alpha_surface = pygame.Surface((box_width + i*8, box_height + i*8), pygame.SRCALPHA)
            alpha_value = 100 - (i * 20)
            pygame.draw.rect(alpha_surface, (*glow_color, alpha_value),
                           (0, 0, box_width + i*8, box_height + i*8))
            screen.blit(alpha_surface, (box_x - i*4, box_y - i*4))

        self.draw_box(screen, box_x, box_y, box_width, box_height, (40, 20, 60))

        # Title
        title_text = self.large_font.render("Daily Reward!", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(box_x + box_width // 2, box_y + 40))
        screen.blit(title_text, title_rect)

        # Streak info
        streak_text = self.title_font.render(
            f"🔥 {daily_rewards.current_streak} Day Streak!",
            True, (255, 140, 0)
        )
        streak_rect = streak_text.get_rect(center=(box_x + box_width // 2, box_y + 90))
        screen.blit(streak_text, streak_rect)

        # Best streak
        if daily_rewards.longest_streak > daily_rewards.current_streak:
            best_text = self.small_font.render(
                f"Best: {daily_rewards.longest_streak} days",
                True, (180, 180, 180)
            )
            best_rect = best_text.get_rect(center=(box_x + box_width // 2, box_y + 115))
            screen.blit(best_text, best_rect)

        # Reward amounts
        reward_y = box_y + 160

        # Gold reward
        gold_icon = self.large_font.render("💰", True, (255, 255, 255))
        screen.blit(gold_icon, (box_x + 100, reward_y))

        gold_text = self.title_font.render(
            f"+{daily_rewards.today_reward_gold} Gold",
            True, (255, 215, 0)
        )
        screen.blit(gold_text, (box_x + 150, reward_y + 10))

        # EXP reward
        exp_y = reward_y + 60
        exp_icon = self.large_font.render("⭐", True, (255, 255, 255))
        screen.blit(exp_icon, (box_x + 100, exp_y))

        exp_text = self.title_font.render(
            f"+{daily_rewards.today_reward_exp} EXP",
            True, (144, 238, 144)
        )
        screen.blit(exp_text, (box_x + 150, exp_y + 10))

        # Milestone bonus indicator
        milestone_y = box_y + 290
        milestone_text = ""
        if daily_rewards.current_streak == 7:
            milestone_text = "🎉 7-Day Milestone Bonus! 🎉"
        elif daily_rewards.current_streak == 30:
            milestone_text = "🎊 30-Day Milestone Bonus! 🎊"
        elif daily_rewards.current_streak == 100:
            milestone_text = "👑 100-Day LEGENDARY Bonus! 👑"

        if milestone_text:
            milestone = self.font.render(milestone_text, True, (255, 100, 255))
            milestone_rect = milestone.get_rect(center=(box_x + box_width // 2, milestone_y))
            screen.blit(milestone, milestone_rect)

        # Instructions
        inst_text = self.font.render(
            "Press ENTER to claim!",
            True, (255, 255, 100)
        )
        inst_rect = inst_text.get_rect(center=(box_x + box_width // 2, box_y + box_height - 40))
        screen.blit(inst_text, inst_rect)

        # Daily tip
        tip_text = self.small_font.render(
            "Come back daily to maintain your streak!",
            True, (180, 180, 180)
        )
        tip_rect = tip_text.get_rect(center=(box_x + box_width // 2, box_y + box_height - 15))
        screen.blit(tip_text, tip_rect)

    def draw_streak_indicator(self, screen, daily_rewards, screen_width):
        """Draw small streak indicator in corner"""
        if daily_rewards.current_streak > 0:
            # Small box in top right
            box_width = 120
            box_height = 40
            box_x = screen_width - box_width - 10
            box_y = 10

            # Background
            pygame.draw.rect(screen, (40, 30, 20), (box_x, box_y, box_width, box_height))
            pygame.draw.rect(screen, (101, 67, 33), (box_x, box_y, box_width, box_height), 2)

            # Streak text
            streak_text = self.font.render(
                f"🔥 {daily_rewards.current_streak}",
                True, (255, 140, 0)
            )
            streak_rect = streak_text.get_rect(center=(box_x + box_width // 2, box_y + box_height // 2))
            screen.blit(streak_text, streak_rect)
