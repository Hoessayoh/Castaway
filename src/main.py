import pygame
import sys
from player import Player
from world import World
from ui import UI
from collection import Collection, CollectionUI
from achievements import AchievementSystem, AchievementUI
from progression import PlayerProgression, ProgressionUI
from daily_rewards import DailyRewards, DailyRewardsUI
from particles import ParticleSystem, FloatingTextSystem
from statistics import StatisticsTracker, StatisticsUI
from hidden_systems import CharacterStats, EnvironmentalSystem, SecretQuestSystem, LoreDiscoverySystem
from camera import Camera
from fish import FISH_DATABASE
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WATER_COLOR

class Game:
    def __init__(self):
        pygame.init()
        # Fullscreen 1080p for maximum quality
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        pygame.display.set_caption("Castaway - Fishing Simulator [1080p 240FPS]")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "menu"  # menu, playing, paused, game_over, collection, achievements, shop, stats

        # Initialize game objects
        self.player = Player()
        self.world = World()
        self.ui = UI()

        # Pokemon-style collection system
        self.collection = Collection()
        self.collection_ui = CollectionUI()

        # Achievement system
        self.achievement_system = AchievementSystem()
        self.achievement_ui = AchievementUI()

        # Progression system
        self.progression = PlayerProgression()
        self.progression_ui = ProgressionUI()
        self.level_up_timer = 0  # For level up notification

        # Daily rewards system
        self.daily_rewards = DailyRewards()
        self.daily_rewards_ui = DailyRewardsUI()
        self.show_daily_reward = self.daily_rewards.has_unclaimed_reward()

        # Particle effects
        self.particle_system = ParticleSystem()
        self.floating_text_system = FloatingTextSystem()

        # Statistics tracking
        self.statistics = StatisticsTracker()
        self.statistics_ui = StatisticsUI()

        # Hidden systems (Shangri-La Frontier style)
        self.character_stats = CharacterStats()
        self.environment = EnvironmentalSystem()
        self.secret_quests = SecretQuestSystem()
        self.lore = LoreDiscoverySystem()

        # Camera system for screen shake and effects
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        # No visible fish - they're caught from a pool like Pokemon
        # Fish collection tracking
        self.total_catches = 0
        self.collection_dict = {}  # Track how many of each fish caught
        self.catch_streak = 0  # Track consecutive successful catches
        self.last_bite_time = 0  # For tracking reaction time

    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "menu":
                        self.running = False
                    elif self.state in ["collection", "achievements", "shop", "stats"]:
                        self.state = "menu"
                    else:
                        self.state = "menu"
                elif event.key == pygame.K_c:
                    if self.state == "playing" or self.state == "paused":
                        self.state = "collection"
                    elif self.state == "collection":
                        self.state = "playing"
                elif event.key == pygame.K_a:
                    if self.state == "playing" or self.state == "paused":
                        self.state = "achievements"
                    elif self.state == "achievements":
                        self.state = "playing"
                elif event.key == pygame.K_s:
                    if self.state == "playing" or self.state == "paused":
                        self.state = "shop"
                    elif self.state == "shop":
                        self.state = "playing"
                elif event.key == pygame.K_t:
                    if self.state == "playing" or self.state == "paused":
                        self.state = "stats"
                    elif self.state == "stats":
                        self.state = "playing"
                elif event.key == pygame.K_p and self.state == "playing":
                    self.state = "paused"
                elif event.key == pygame.K_p and self.state == "paused":
                    self.state = "playing"
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    # ENTER key for menu navigation and confirmations
                    if self.show_daily_reward and self.state == "playing":
                        # Claim daily reward (only when playing and popup is shown)
                        gold, exp = self.daily_rewards.claim_daily_reward()
                        if gold and exp:
                            self.ui.score += gold
                            self.progression.add_experience(exp)
                        self.show_daily_reward = False
                        # Create particles for reward
                        center_x = SCREEN_WIDTH // 2
                        center_y = SCREEN_HEIGHT // 2
                        self.particle_system.create_achievement_effect(center_x, center_y)
                    elif self.state == "menu":
                        self.state = "playing"
                elif event.key == pygame.K_SPACE:
                    # SPACE key for fishing ONLY
                    if self.state == "playing" and not self.show_daily_reward:
                        # Track bite time for quick reflexes achievement
                        if self.player.fishing_state == 'bite':
                            self.last_bite_time = pygame.time.get_ticks()
                        self.player.cast_fishing_line()

    def update(self):
        """Update game state"""
        # Always update camera for screen shake
        self.camera.update()

        if self.state == "playing":
            # Update environment (weather, time of day)
            self.environment.update_weather()

            # Get environmental multipliers
            env_mults = self.environment.get_environment_multipliers(self.character_stats)

            # Apply rod and environmental modifiers to player
            if self.progression.current_rod:
                total_bite_mult = self.progression.current_rod.bite_speed_mult * env_mults["bite_speed"]
                self.player.rod_bite_speed_mult = total_bite_mult

            self.player.update()
            self.world.update()

            # Update statistics
            self.statistics.check_daily_reset()
            self.statistics.update_playtime()

            # Track when fish bites for achievement tracking
            if self.player.fishing_state == 'bite' and not hasattr(self, '_bite_start_time'):
                self._bite_start_time = pygame.time.get_ticks()

            # Pokemon-style fishing - catch when reeling
            if self.player.fishing_state == 'reeling':
                # Player successfully reacted to bite - catch a random fish!
                from fish import Fish

                # Apply rod bonuses to fish selection
                fish_id = None
                force_shiny = False

                # Rod and environmental affects shiny chance and rarity
                if self.progression.current_rod:
                    import random
                    # Combine rod and environmental shiny multipliers
                    total_shiny_mult = self.progression.current_rod.shiny_mult * env_mults["shiny_mult"]
                    shiny_chance = 0.01 * total_shiny_mult
                    force_shiny = random.random() < shiny_chance

                caught_fish = Fish(0, 0, fish_id=fish_id, force_shiny=force_shiny)

                # Calculate reaction time FIRST
                reaction_time = 0
                if hasattr(self, '_bite_start_time'):
                    reaction_time = (pygame.time.get_ticks() - self._bite_start_time) / 1000
                    delattr(self, '_bite_start_time')

                # Record catch in statistics
                is_perfect_cast = reaction_time < 0.3 if reaction_time > 0 else False
                self.statistics.record_catch(
                    caught_fish,
                    self.progression.current_rod.name if self.progression.current_rod else "Basic Rod",
                    self.environment.current_weather,
                    self.environment.time_of_day,
                    self.environment.moon_phase,
                    reaction_time,
                    is_perfect_cast
                )

                # Update character stats based on catch
                self.character_stats.add_stat('luck', 0.1 if caught_fish.is_shiny else 0.05)
                self.character_stats.add_stat('patience', 0.05)
                if caught_fish.rarity in ['legendary', 'mythic']:
                    self.character_stats.add_stat('perception', 0.2)

                # Update stats with new fish system
                gold_earned = caught_fish.points
                self.ui.add_score(
                    gold_earned,
                    caught_fish.get_display_name(),
                    caught_fish.get_rarity_color(),
                    caught_fish.is_shiny
                )
                self.player.add_to_collection(caught_fish)
                self.total_catches += 1
                self.catch_streak += 1

                # Add experience and check for level up
                exp_gained = self.progression.get_exp_for_fish(caught_fish.rarity, caught_fish.is_shiny)
                leveled_up = self.progression.add_experience(exp_gained)
                if leveled_up:
                    self.level_up_timer = 180  # Show level up for 3 seconds
                    # Level up particle effect
                    self.particle_system.create_level_up_effect(self.player.rect.centerx, self.player.rect.centery)

                # Create catch particle effects
                self.particle_system.create_catch_explosion(
                    self.player.rect.centerx,
                    self.player.rect.top - 20,
                    caught_fish.get_rarity_color(),
                    caught_fish.is_shiny
                )

                # Screen shake based on fish rarity (more juice!)
                rarity_shake_map = {
                    'common': 2,
                    'uncommon': 3,
                    'rare': 5,
                    'epic': 8,
                    'legendary': 12,
                    'mythic': 18
                }
                shake_amount = rarity_shake_map.get(caught_fish.rarity, 2)
                if caught_fish.is_shiny:
                    shake_amount *= 1.5  # Extra shake for shinies!
                self.camera.apply_shake(shake_amount, duration=20)

                # Floating text for EXP and gold
                self.floating_text_system.add_exp_text(
                    self.player.rect.centerx - 40,
                    self.player.rect.top - 40,
                    exp_gained
                )
                self.floating_text_system.add_gold_text(
                    self.player.rect.centerx + 40,
                    self.player.rect.top - 40,
                    gold_earned
                )

                # Add to collection tracker
                self.collection.add_catch(caught_fish.fish_id, caught_fish.is_shiny)

                # Track in collection (separate tracking for normal and shiny)
                collection_key = f"{caught_fish.fish_id}_{'shiny' if caught_fish.is_shiny else 'normal'}"
                if collection_key not in self.collection_dict:
                    self.collection_dict[collection_key] = {
                        'fish_id': caught_fish.fish_id,
                        'name': caught_fish.name,
                        'rarity': caught_fish.rarity,
                        'is_shiny': caught_fish.is_shiny,
                        'count': 0
                    }
                self.collection_dict[collection_key]['count'] += 1

                # Check achievements with detailed stats
                self.check_achievements(caught_fish, reaction_time)

                # Reset fishing
                self.player.cancel_fishing()

            # Update level up timer
            if self.level_up_timer > 0:
                self.level_up_timer -= 1

            # Handle failed fishing (for streak tracking)
            if self.player.fishing_state == 'failed':
                self.catch_streak = 0
                if hasattr(self, '_bite_start_time'):
                    delattr(self, '_bite_start_time')

            self.ui.update()
            self.achievement_system.update()
            self.particle_system.update()
            self.floating_text_system.update()

    def check_achievements(self, caught_fish, reaction_time):
        """Check and unlock achievements based on game state"""
        # Build stats dictionary for achievement checking
        rarity_counts = {
            'common': 0, 'uncommon': 0, 'rare': 0,
            'epic': 0, 'legendary': 0, 'mythic': 0
        }

        for key, data in self.collection_dict.items():
            rarity = data['rarity']
            rarity_counts[rarity] += data['count']

        # Check if collection is complete (both normal and shiny of each fish)
        complete_collection = True
        for fish_id in FISH_DATABASE.keys():
            if not (self.collection.has_caught(fish_id, False) and
                    self.collection.has_caught(fish_id, True)):
                complete_collection = False
                break

        stats = {
            'total_catches': self.total_catches,
            'unique_species': self.collection.unique_fish_caught,
            'total_shinies': self.collection.total_shiny_caught,
            'total_gold': self.ui.score,
            'uncommon_plus': sum([rarity_counts[r] for r in ['uncommon', 'rare', 'epic', 'legendary', 'mythic']]),
            'rare_plus': sum([rarity_counts[r] for r in ['rare', 'epic', 'legendary', 'mythic']]),
            'epic_plus': sum([rarity_counts[r] for r in ['epic', 'legendary', 'mythic']]),
            'legendary_plus': sum([rarity_counts[r] for r in ['legendary', 'mythic']]),
            'mythic_count': rarity_counts['mythic'],
            'complete_collection': complete_collection,
            'catch_streak': self.catch_streak,
            'quick_catch': reaction_time < 0.5 if reaction_time > 0 else False,
            'patient_catch': self.player.bite_timer > 180 if hasattr(self.player, 'bite_timer') else False,
            'all_unlocked': self.achievement_system.get_unlocked_count() >= self.achievement_system.get_total_count() - 1
        }

        # Check achievements and award gold
        self.achievement_system.check_achievements(stats)

        # Add any achievement rewards to score
        if self.achievement_system.newly_unlocked:
            for achievement in self.achievement_system.newly_unlocked:
                if not hasattr(achievement, '_reward_claimed'):
                    self.ui.score += achievement.reward_gold
                    achievement._reward_claimed = True

    def draw(self):
        """Draw all game elements"""
        # Get camera offset for screen shake
        cam_offset_x, cam_offset_y = self.camera.get_offset()

        # Create a temporary surface for camera effects
        if cam_offset_x != 0 or cam_offset_y != 0:
            temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            draw_surface = temp_surface
        else:
            draw_surface = self.screen

        draw_surface.fill(WATER_COLOR)

        if self.state == "menu":
            self.draw_menu()
        elif self.state == "collection":
            # Draw game in background
            self.world.draw(self.screen)
            self.player.draw(self.screen)
            self.ui.draw(self.screen, self.player, self.progression)
            # Draw collection UI on top
            self.collection_ui.draw(self.screen, self.collection, SCREEN_WIDTH, SCREEN_HEIGHT)
        elif self.state == "achievements":
            # Draw game in background
            self.world.draw(self.screen)
            self.player.draw(self.screen)
            self.ui.draw(self.screen, self.player, self.progression)
            # Draw achievements UI on top
            self.achievement_ui.draw(self.screen, self.achievement_system, SCREEN_WIDTH, SCREEN_HEIGHT)
        elif self.state == "shop":
            # Draw game in background
            self.world.draw(self.screen)
            self.player.draw(self.screen)
            self.ui.draw(self.screen, self.player, self.progression)
            # Draw shop UI on top
            self.progression_ui.draw_shop(self.screen, self.progression, self.ui.score, SCREEN_WIDTH, SCREEN_HEIGHT)
        elif self.state == "stats":
            # Draw game in background
            self.world.draw(self.screen)
            self.player.draw(self.screen)
            self.ui.draw(self.screen, self.player, self.progression)
            # Draw statistics UI on top
            self.statistics_ui.draw(self.screen, self.statistics, SCREEN_WIDTH, SCREEN_HEIGHT)
        else:
            self.world.draw(self.screen)
            self.player.draw(self.screen)

            # Draw particles behind UI
            self.particle_system.draw(self.screen)
            self.floating_text_system.draw(self.screen)

            self.ui.draw(self.screen, self.player, self.progression)

            # Draw fishing elements (bobber, line) AFTER UI so they don't clip behind stats
            self.player.draw_fishing_elements(self.screen)

            # Draw streak indicator
            self.daily_rewards_ui.draw_streak_indicator(self.screen, self.daily_rewards, SCREEN_WIDTH)

            # Draw level up notification
            if self.level_up_timer > 0:
                self.progression_ui.draw_level_up_notification(self.screen, self.progression.level, SCREEN_WIDTH)

            # Draw achievement notifications on top
            self.achievement_ui.draw_notification(self.screen, self.achievement_system, SCREEN_WIDTH)

            # Draw daily reward popup if unclaimed
            if self.show_daily_reward:
                self.daily_rewards_ui.draw_daily_reward_popup(
                    self.screen, self.daily_rewards, SCREEN_WIDTH, SCREEN_HEIGHT
                )

            # Draw pause text if paused
            if self.state == "paused":
                font = pygame.font.Font(None, 72)
                pause_text = font.render("PAUSED", True, (255, 255, 255))
                text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(pause_text, text_rect)

                # Draw resume instruction
                small_font = pygame.font.Font(None, 36)
                resume_text = small_font.render("Press P to Resume", True, (200, 200, 200))
                resume_rect = resume_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
                self.screen.blit(resume_text, resume_rect)

        # Apply camera shake by blitting temp surface with offset
        if cam_offset_x != 0 or cam_offset_y != 0:
            self.screen.fill((0, 0, 0))  # Fill with black
            self.screen.blit(temp_surface, (cam_offset_x, cam_offset_y))

        pygame.display.flip()

    def draw_menu(self):
        """Draw the main menu with Stardew Valley aesthetic"""
        from settings import UI_BG, UI_ACCENT, UI_BORDER, GRASS_COLOR

        # Draw a nice background
        # Sky/water gradient
        for y in range(0, SCREEN_HEIGHT, 20):
            color_factor = y / SCREEN_HEIGHT
            color = (
                int(76 + (139 - 76) * color_factor),
                int(145 + (195 - 145) * color_factor),
                int(178 + (74 - 178) * color_factor)
            )
            pygame.draw.rect(self.screen, color, (0, y, SCREEN_WIDTH, 20))

        # Draw decorative grass at bottom (scaled)
        grass_rect = pygame.Rect(0, SCREEN_HEIGHT - 200, SCREEN_WIDTH, 200)
        pygame.draw.rect(self.screen, GRASS_COLOR, grass_rect)

        # Title box (scaled for 1080p)
        title_width = 1000
        title_height = 200
        title_x = SCREEN_WIDTH // 2 - title_width // 2
        title_y = 160

        # Title box background
        pygame.draw.rect(self.screen, (0, 0, 0, 50), (title_x + 10, title_y + 10, title_width, title_height))
        pygame.draw.rect(self.screen, UI_BG, (title_x, title_y, title_width, title_height))
        pygame.draw.rect(self.screen, UI_BORDER, (title_x, title_y, title_width, title_height), 8)

        # Title (with shadow for depth) - scaled
        title_font = pygame.font.Font(None, 128)
        # Shadow
        title_shadow = title_font.render("CASTAWAY", True, (20, 10, 5))
        shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 6, title_y + 76))
        self.screen.blit(title_shadow, shadow_rect)
        # Main title
        title_text = title_font.render("CASTAWAY", True, UI_ACCENT)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, title_y + 70))
        self.screen.blit(title_text, title_rect)

        # Subtitle (scaled)
        subtitle_font = pygame.font.Font(None, 56)
        subtitle_text = subtitle_font.render("Wooper's Fishing Adventure", True, (144, 238, 144))
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, title_y + 140))
        self.screen.blit(subtitle_text, subtitle_rect)

        # Instructions box (scaled)
        box_width = 900
        box_height = 500
        box_x = SCREEN_WIDTH // 2 - box_width // 2
        box_y = 420

        pygame.draw.rect(self.screen, (0, 0, 0, 50), (box_x + 10, box_y + 10, box_width, box_height))
        pygame.draw.rect(self.screen, UI_BG, (box_x, box_y, box_width, box_height))
        pygame.draw.rect(self.screen, UI_BORDER, (box_x, box_y, box_width, box_height), 8)

        # Instructions (scaled for 1080p)
        instructions_font = pygame.font.Font(None, 40)
        instructions = [
            "How to Play:",
            "",
            "↑↓←→ Move | SPACE Cast/Reel | ENTER Confirm",
            "C Collection | A Achievements | S Shop | T Stats",
            "P Pause | ESC Back to Menu",
            "",
            "Features:",
            "18 fish species with shiny variants",
            "Hidden character stats & secret traits",
            "Dynamic weather & time-of-day effects",
            "Daily rewards & login streaks",
            "7 upgradable rods | 24+ achievements",
            "Complete statistics tracking",
            "Discover lore & unlock secrets!",
        ]

        y_offset = box_y + 40
        for instruction in instructions:
            if instruction.startswith("How to Play:") or instruction.startswith("Features:"):
                text = instructions_font.render(instruction, True, UI_ACCENT)
            elif instruction:
                text = instructions_font.render(instruction, True, (200, 200, 180))
            else:
                y_offset += 16
                continue
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 36

        # Start button (scaled)
        button_font = pygame.font.Font(None, 80)
        start_text = button_font.render("Press ENTER to Start!", True, (255, 255, 100))
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, 980))

        # Pulsing effect
        import math
        pulse = abs(math.sin(pygame.time.get_ticks() / 500))
        start_color = (int(255 * pulse), int(255 * pulse), int(100 + 155 * pulse))
        start_text = button_font.render("Press ENTER to Start!", True, start_color)

        self.screen.blit(start_text, start_rect)

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
