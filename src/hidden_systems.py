"""
Hidden Systems & Secret Mechanics
Inspired by Shangri-La Frontier's depth and discovery
"""
import pygame
import random
import json
import os
from datetime import datetime


class CharacterStats:
    """Hidden character stat spread that affects gameplay"""

    def __init__(self):
        # Core stats (0-100, start at 10)
        self.luck = 10  # Affects shiny chance, rare fish chance
        self.patience = 10  # Reduces bite time, increases catch window
        self.technique = 10  # Better rod efficiency, combo bonuses
        self.perception = 10  # See hidden fish patterns, weather bonuses
        self.endurance = 10  # Consecutive fishing bonuses, streak multipliers

        # Hidden affinity stats (discovered through gameplay)
        self.water_affinity = 0  # Bonus in water zones
        self.moon_affinity = 0  # Time-based bonuses
        self.void_affinity = 0  # Rare fish attraction

        # Special unlockable traits
        self.traits = []
        self.discovered_secrets = []

        # Load from file
        self.load()

    def add_stat(self, stat_name, amount):
        """Increase a stat (caps at 100)"""
        if hasattr(self, stat_name):
            current = getattr(self, stat_name)
            setattr(self, stat_name, min(100, current + amount))

    def has_trait(self, trait_name):
        """Check if player has unlocked a trait"""
        return trait_name in self.traits

    def unlock_trait(self, trait_name):
        """Unlock a special trait"""
        if trait_name not in self.traits:
            self.traits.append(trait_name)
            return True
        return False

    def discover_secret(self, secret_name):
        """Mark a secret as discovered"""
        if secret_name not in self.discovered_secrets:
            self.discovered_secrets.append(secret_name)
            return True
        return False

    def save(self):
        """Save stats to file"""
        data = {
            'luck': self.luck,
            'patience': self.patience,
            'technique': self.technique,
            'perception': self.perception,
            'endurance': self.endurance,
            'water_affinity': self.water_affinity,
            'moon_affinity': self.moon_affinity,
            'void_affinity': self.void_affinity,
            'traits': self.traits,
            'discovered_secrets': self.discovered_secrets
        }
        with open('character_stats.json', 'w') as f:
            json.dump(data, f)

    def load(self):
        """Load stats from file"""
        if os.path.exists('character_stats.json'):
            try:
                with open('character_stats.json', 'r') as f:
                    data = json.load(f)
                    for key, value in data.items():
                        if hasattr(self, key):
                            setattr(self, key, value)
            except:
                pass


# Hidden trait definitions
HIDDEN_TRAITS = {
    "moonlight_fisher": {
        "name": "Moonlight Fisher",
        "description": "Catch 100 fish between 8pm-4am (system time)",
        "unlock_condition": "night_catches_100",
        "effect": "2x shiny chance during night",
        "secret": True
    },
    "perfect_cast": {
        "name": "Perfect Cast",
        "description": "Land 50 perfect casts (instant bite)",
        "unlock_condition": "perfect_casts_50",
        "effect": "Guaranteed perfect cast every 10 casts",
        "secret": True
    },
    "void_seeker": {
        "name": "Void Seeker",
        "description": "Catch 10 Void Fish",
        "unlock_condition": "void_fish_10",
        "effect": "Void Fish appear 3x more often",
        "secret": True
    },
    "shiny_master": {
        "name": "Shiny Master",
        "description": "Catch 100 shiny fish",
        "unlock_condition": "shinies_100",
        "effect": "Shiny chance increased by 50%",
        "secret": True
    },
    "combo_king": {
        "name": "Combo King",
        "description": "Achieve a 50-catch combo",
        "unlock_condition": "combo_50",
        "effect": "Combo bonuses last 2x longer",
        "secret": True
    },
    "weather_sage": {
        "name": "Weather Sage",
        "description": "Fish during all 5 weather conditions",
        "unlock_condition": "all_weather",
        "effect": "Weather bonuses are doubled",
        "secret": False
    },
    "rod_master": {
        "name": "Rod Master",
        "description": "Catch 100 fish with each rod type",
        "unlock_condition": "all_rods_100",
        "effect": "All rod stats +10%",
        "secret": False
    },
    "speedrunner": {
        "name": "Speedrunner",
        "description": "Catch 10 fish in under 2 minutes",
        "unlock_condition": "speed_10_fish",
        "effect": "Bite time reduced by 25%",
        "secret": True
    },
    "patient_monk": {
        "name": "Patient Monk",
        "description": "Wait 10 minutes before catching a fish",
        "unlock_condition": "wait_10_min",
        "effect": "+50 Patience stat permanently",
        "secret": True
    },
    "golden_touch": {
        "name": "Golden Touch",
        "description": "Earn 1,000,000 gold",
        "unlock_condition": "gold_1m",
        "effect": "All fish give 25% more gold",
        "secret": False
    }
}


class EnvironmentalSystem:
    """Environmental effects and hidden mechanics"""

    def __init__(self):
        self.current_weather = "clear"
        self.weather_timer = 0
        self.time_of_day = "day"

        # Environmental modifiers
        self.weather_effects = {
            "clear": {"rarity_mult": 1.0, "bite_speed": 1.0, "shiny_mult": 1.0},
            "rain": {"rarity_mult": 1.3, "bite_speed": 0.8, "shiny_mult": 1.5},
            "storm": {"rarity_mult": 2.0, "bite_speed": 0.6, "shiny_mult": 2.0},
            "fog": {"rarity_mult": 1.5, "bite_speed": 1.2, "shiny_mult": 1.2},
            "aurora": {"rarity_mult": 3.0, "bite_speed": 1.0, "shiny_mult": 5.0}  # Very rare
        }

        # Time-based effects
        self.time_effects = {
            "dawn": {"rarity_mult": 1.2, "mythic_boost": 0.01},  # 5am-7am
            "day": {"rarity_mult": 1.0, "mythic_boost": 0.0},    # 7am-6pm
            "dusk": {"rarity_mult": 1.5, "mythic_boost": 0.02},  # 6pm-8pm
            "night": {"rarity_mult": 1.8, "mythic_boost": 0.03}  # 8pm-5am
        }

        # Special moon phases
        self.moon_phase = self.get_moon_phase()

    def get_moon_phase(self):
        """Calculate current moon phase (simplified)"""
        day_of_month = datetime.now().day
        phase_index = (day_of_month - 1) // 7  # 0-3
        phases = ["new", "waxing", "full", "waning"]
        return phases[phase_index]

    def get_time_of_day(self):
        """Get current time of day"""
        hour = datetime.now().hour
        if 5 <= hour < 7:
            return "dawn"
        elif 7 <= hour < 18:
            return "day"
        elif 18 <= hour < 20:
            return "dusk"
        else:
            return "night"

    def update_weather(self):
        """Update weather randomly"""
        self.weather_timer += 1

        # Change weather every ~5 minutes
        if self.weather_timer >= 300 * 60:  # 5 minutes at 60fps
            self.weather_timer = 0

            # Weather probabilities
            weather_roll = random.random()
            if weather_roll < 0.50:
                self.current_weather = "clear"
            elif weather_roll < 0.70:
                self.current_weather = "rain"
            elif weather_roll < 0.85:
                self.current_weather = "fog"
            elif weather_roll < 0.98:
                self.current_weather = "storm"
            else:
                self.current_weather = "aurora"  # 2% chance - ultra rare!

        # Update time of day
        self.time_of_day = self.get_time_of_day()

    def get_environment_multipliers(self, character_stats):
        """Get all active environmental multipliers"""
        weather_mod = self.weather_effects.get(self.current_weather, self.weather_effects["clear"])
        time_mod = self.time_effects.get(self.time_of_day, self.time_effects["day"])

        # Moon phase bonuses
        moon_bonus = {
            "new": {"shiny_mult": 0.5, "void_boost": 2.0},
            "waxing": {"shiny_mult": 1.0, "void_boost": 1.0},
            "full": {"shiny_mult": 3.0, "void_boost": 1.0},
            "waning": {"shiny_mult": 1.0, "void_boost": 1.0}
        }

        current_moon = moon_bonus.get(self.moon_phase, moon_bonus["waxing"])

        # Apply character stat bonuses
        stat_multipliers = {
            "rarity_mult": 1.0 + (character_stats.perception / 100) * 0.5,
            "shiny_mult": 1.0 + (character_stats.luck / 100) * 1.0,
            "bite_speed": 1.0 - (character_stats.patience / 100) * 0.3,
        }

        # Combine all multipliers
        combined = {
            "rarity_mult": weather_mod["rarity_mult"] * time_mod["rarity_mult"] * stat_multipliers["rarity_mult"],
            "shiny_mult": weather_mod["shiny_mult"] * current_moon["shiny_mult"] * stat_multipliers["shiny_mult"],
            "bite_speed": weather_mod["bite_speed"] * stat_multipliers["bite_speed"],
            "mythic_boost": time_mod.get("mythic_boost", 0.0)
        }

        return combined


class SecretQuestSystem:
    """Hidden quests and secret objectives"""

    def __init__(self):
        self.active_secrets = []
        self.completed_secrets = []
        self.progress = {}

        # Load progress
        self.load()

    def check_secret(self, secret_id, current_value):
        """Check if a secret condition is met"""
        secret_conditions = {
            "catch_at_dawn_dusk": {"condition": "catch_during_special_time", "requirement": 50},
            "catch_all_mythic": {"condition": "catch_all_rarity", "requirement": "mythic"},
            "perfect_game": {"condition": "no_missed_fish", "requirement": 100},
            "rod_combo": {"condition": "specific_rod_fish_combo", "requirement": "mythic_rod_mythic_fish"},
            "midnight_legend": {"condition": "catch_at_midnight", "requirement": "legendary"},
            "weather_master": {"condition": "catch_all_weather", "requirement": 5},
            "stat_maxed": {"condition": "max_all_stats", "requirement": 100},
            "collection_complete": {"condition": "full_pokedex", "requirement": "all"},
        }

        # Track progress
        if secret_id not in self.progress:
            self.progress[secret_id] = 0

        # Update progress based on secret type
        # This will be called from main game loop with appropriate contexts

    def unlock_secret(self, secret_id):
        """Unlock a secret achievement"""
        if secret_id not in self.completed_secrets:
            self.completed_secrets.append(secret_id)
            self.save()
            return True
        return False

    def save(self):
        """Save secret quest progress"""
        data = {
            'active_secrets': self.active_secrets,
            'completed_secrets': self.completed_secrets,
            'progress': self.progress
        }
        with open('secret_quests.json', 'w') as f:
            json.dump(data, f)

    def load(self):
        """Load secret quest progress"""
        if os.path.exists('secret_quests.json'):
            try:
                with open('secret_quests.json', 'r') as f:
                    data = json.load(f)
                    self.active_secrets = data.get('active_secrets', [])
                    self.completed_secrets = data.get('completed_secrets', [])
                    self.progress = data.get('progress', {})
            except:
                pass


# Lore and flavor text
LORE_TEXTS = {
    "wooper_origin": "Long ago, Wooper mastered the ancient art of fishing to survive the harsh waters...",
    "mythic_legend": "The Prism Fish is said to appear only to those who have achieved perfect harmony with the water...",
    "void_mystery": "The Void Fish exists between dimensions, appearing when the veil is thinnest...",
    "aurora_phenomenon": "When the aurora appears, the water resonates with otherworldly energy...",
    "moon_blessing": "Under the full moon, all creatures of the water are drawn to the surface...",
    "perfect_cast": "Master fishers speak of a technique where time itself seems to slow...",
    "rod_legend": "The Mythic Rod was forged from stardust and blessed by the water spirits...",
    "hidden_stat": "True masters understand that fishing is not just technique, but a connection with nature itself..."
}


class LoreDiscoverySystem:
    """Discover lore through gameplay"""

    def __init__(self):
        self.discovered_lore = []
        self.load()

    def discover(self, lore_id):
        """Discover a piece of lore"""
        if lore_id in LORE_TEXTS and lore_id not in self.discovered_lore:
            self.discovered_lore.append(lore_id)
            self.save()
            return LORE_TEXTS[lore_id]
        return None

    def save(self):
        """Save discovered lore"""
        with open('lore_discovery.json', 'w') as f:
            json.dump({'discovered': self.discovered_lore}, f)

    def load(self):
        """Load discovered lore"""
        if os.path.exists('lore_discovery.json'):
            try:
                with open('lore_discovery.json', 'r') as f:
                    data = json.load(f)
                    self.discovered_lore = data.get('discovered', [])
            except:
                pass
