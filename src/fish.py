import pygame
import random
from settings import SCREEN_WIDTH

# Comprehensive fish database with Pokemon-style rarity tiers
# Each fish has normal and shiny variants (1/100 chance for shiny)
FISH_DATABASE = {
    # COMMON (50% chance) - 10-25 gold
    "sardine": {
        "name": "Sardine",
        "rarity": "common",
        "body_color": (169, 169, 169),  # Gray
        "accent_color": (128, 128, 128),  # Dark gray
        "belly_color": (211, 211, 211),  # Light gray
        "shiny_body": (255, 215, 180),  # Peach
        "shiny_accent": (255, 160, 122),  # Light salmon
        "shiny_belly": (255, 250, 240),  # Floral white
        "size": (28, 16),
        "points": 10,
        "habitat": "Surface water",
        "description": "A tiny, common fish found everywhere."
    },
    "carp": {
        "name": "Carp",
        "rarity": "common",
        "body_color": (139, 90, 43),  # Brown
        "accent_color": (101, 67, 33),  # Dark brown
        "belly_color": (222, 184, 135),  # Burlywood
        "shiny_body": (255, 215, 0),  # Gold
        "shiny_accent": (218, 165, 32),  # Goldenrod
        "shiny_belly": (255, 239, 213),  # Papaya whip
        "size": (32, 18),
        "points": 15,
        "habitat": "Shallow water",
        "description": "A common bottom-feeder fish."
    },
    "smallmouth_bass": {
        "name": "Smallmouth Bass",
        "rarity": "common",
        "body_color": (107, 142, 35),  # Olive green
        "accent_color": (85, 107, 47),  # Dark olive
        "belly_color": (189, 183, 107),  # Dark khaki
        "shiny_body": (0, 255, 127),  # Spring green
        "shiny_accent": (46, 139, 87),  # Sea green
        "shiny_belly": (144, 238, 144),  # Light green
        "size": (36, 20),
        "points": 20,
        "habitat": "Rivers and lakes",
        "description": "A popular sport fish."
    },
    "perch": {
        "name": "Perch",
        "rarity": "common",
        "body_color": (154, 205, 50),  # Yellow green
        "accent_color": (124, 252, 0),  # Lawn green
        "belly_color": (240, 230, 140),  # Khaki
        "shiny_body": (255, 0, 255),  # Magenta
        "shiny_accent": (186, 85, 211),  # Medium orchid
        "shiny_belly": (221, 160, 221),  # Plum
        "size": (30, 18),
        "points": 18,
        "habitat": "Clear water",
        "description": "A striped fish with spiny fins."
    },

    # UNCOMMON (25% chance) - 30-50 gold
    "rainbow_trout": {
        "name": "Rainbow Trout",
        "rarity": "uncommon",
        "body_color": (147, 112, 219),  # Medium purple
        "accent_color": (255, 182, 193),  # Light pink
        "belly_color": (255, 239, 213),  # Papaya whip
        "shiny_body": (255, 105, 180),  # Hot pink
        "shiny_accent": (255, 20, 147),  # Deep pink
        "shiny_belly": (255, 240, 245),  # Lavender blush
        "size": (40, 24),
        "points": 35,
        "habitat": "Cold streams",
        "description": "A beautiful fish with rainbow colors."
    },
    "catfish": {
        "name": "Catfish",
        "rarity": "uncommon",
        "body_color": (72, 61, 139),  # Dark slate blue
        "accent_color": (47, 79, 79),  # Dark slate gray
        "belly_color": (176, 196, 222),  # Light steel blue
        "shiny_body": (138, 43, 226),  # Blue violet
        "shiny_accent": (75, 0, 130),  # Indigo
        "shiny_belly": (230, 230, 250),  # Lavender
        "size": (42, 22),
        "points": 40,
        "habitat": "Murky depths",
        "description": "A whiskered bottom-dweller."
    },
    "pike": {
        "name": "Pike",
        "rarity": "uncommon",
        "body_color": (34, 139, 34),  # Forest green
        "accent_color": (0, 100, 0),  # Dark green
        "belly_color": (152, 251, 152),  # Pale green
        "shiny_body": (255, 69, 0),  # Red orange
        "shiny_accent": (178, 34, 34),  # Firebrick
        "shiny_belly": (255, 160, 122),  # Light salmon
        "size": (44, 20),
        "points": 45,
        "habitat": "Weedy areas",
        "description": "An aggressive predator fish."
    },
    "salmon": {
        "name": "Salmon",
        "rarity": "uncommon",
        "body_color": (250, 128, 114),  # Salmon
        "accent_color": (233, 150, 122),  # Dark salmon
        "belly_color": (255, 218, 185),  # Peach puff
        "shiny_body": (0, 191, 255),  # Deep sky blue
        "shiny_accent": (30, 144, 255),  # Dodger blue
        "shiny_belly": (173, 216, 230),  # Light blue
        "size": (46, 24),
        "points": 50,
        "habitat": "Ocean and rivers",
        "description": "A migratory fish that swims upstream."
    },

    # RARE (15% chance) - 60-100 gold
    "sturgeon": {
        "name": "Sturgeon",
        "rarity": "rare",
        "body_color": (105, 105, 105),  # Dim gray
        "accent_color": (169, 169, 169),  # Dark gray
        "belly_color": (192, 192, 192),  # Silver
        "shiny_body": (255, 215, 0),  # Gold
        "shiny_accent": (184, 134, 11),  # Dark goldenrod
        "shiny_belly": (255, 250, 205),  # Lemon chiffon
        "size": (52, 26),
        "points": 75,
        "habitat": "Deep water",
        "description": "An ancient armored fish."
    },
    "tuna": {
        "name": "Tuna",
        "rarity": "rare",
        "body_color": (25, 25, 112),  # Midnight blue
        "accent_color": (0, 0, 128),  # Navy
        "belly_color": (176, 224, 230),  # Powder blue
        "shiny_body": (255, 99, 71),  # Tomato
        "shiny_accent": (220, 20, 60),  # Crimson
        "shiny_belly": (255, 182, 193),  # Light pink
        "size": (48, 28),
        "points": 80,
        "habitat": "Open ocean",
        "description": "A fast, powerful ocean fish."
    },
    "dorado": {
        "name": "Dorado",
        "rarity": "rare",
        "body_color": (255, 215, 0),  # Gold
        "accent_color": (255, 140, 0),  # Dark orange
        "belly_color": (255, 255, 224),  # Light yellow
        "shiny_body": (0, 255, 255),  # Cyan
        "shiny_accent": (0, 206, 209),  # Dark turquoise
        "shiny_belly": (224, 255, 255),  # Light cyan
        "size": (50, 26),
        "points": 90,
        "habitat": "Tropical waters",
        "description": "A vibrant golden fish."
    },

    # EPIC (7% chance) - 120-180 gold
    "legend_fish": {
        "name": "Legend Fish",
        "rarity": "epic",
        "body_color": (255, 215, 0),  # Gold
        "accent_color": (255, 140, 0),  # Dark orange
        "belly_color": (255, 255, 224),  # Light yellow
        "shiny_body": (138, 43, 226),  # Blue violet
        "shiny_accent": (148, 0, 211),  # Dark violet
        "shiny_belly": (238, 130, 238),  # Violet
        "size": (54, 30),
        "points": 150,
        "habitat": "Mountain lake",
        "description": "A legendary fish of immense power."
    },
    "glacierfish": {
        "name": "Glacierfish",
        "rarity": "epic",
        "body_color": (176, 224, 230),  # Powder blue
        "accent_color": (135, 206, 250),  # Light sky blue
        "belly_color": (240, 248, 255),  # Alice blue
        "shiny_body": (255, 0, 255),  # Magenta
        "shiny_accent": (199, 21, 133),  # Medium violet red
        "shiny_belly": (255, 192, 203),  # Pink
        "size": (52, 28),
        "points": 120,
        "habitat": "Frozen lake",
        "description": "A fish that thrives in icy waters."
    },
    "crimsonfish": {
        "name": "Crimsonfish",
        "rarity": "epic",
        "body_color": (220, 20, 60),  # Crimson
        "accent_color": (178, 34, 34),  # Firebrick
        "belly_color": (255, 160, 122),  # Light salmon
        "shiny_body": (0, 255, 0),  # Lime
        "shiny_accent": (50, 205, 50),  # Lime green
        "shiny_belly": (144, 238, 144),  # Light green
        "size": (56, 30),
        "points": 180,
        "habitat": "Ocean depths",
        "description": "A rare crimson-colored ocean dweller."
    },

    # LEGENDARY (2.5% chance) - 250-400 gold
    "mutant_carp": {
        "name": "Mutant Carp",
        "rarity": "legendary",
        "body_color": (0, 255, 0),  # Lime
        "accent_color": (50, 205, 50),  # Lime green
        "belly_color": (173, 255, 47),  # Green yellow
        "shiny_body": (255, 0, 0),  # Red
        "shiny_accent": (139, 0, 0),  # Dark red
        "shiny_belly": (255, 99, 71),  # Tomato
        "size": (58, 32),
        "points": 250,
        "habitat": "Sewers",
        "description": "A radioactive mutant from the depths."
    },
    "angler": {
        "name": "Angler",
        "rarity": "legendary",
        "body_color": (72, 61, 139),  # Dark slate blue
        "accent_color": (25, 25, 112),  # Midnight blue
        "belly_color": (123, 104, 238),  # Medium slate blue
        "shiny_body": (255, 215, 0),  # Gold
        "shiny_accent": (255, 165, 0),  # Orange
        "shiny_belly": (255, 255, 0),  # Yellow
        "size": (60, 34),
        "points": 300,
        "habitat": "Deep ocean",
        "description": "A bioluminescent deep-sea predator."
    },

    # MYTHIC (0.5% chance) - 500-1000 gold
    "celestial_fish": {
        "name": "Celestial Fish",
        "rarity": "mythic",
        "body_color": (138, 43, 226),  # Blue violet
        "accent_color": (147, 112, 219),  # Medium purple
        "belly_color": (230, 230, 250),  # Lavender
        "shiny_body": (255, 215, 0),  # Gold
        "shiny_accent": (255, 255, 255),  # White
        "shiny_belly": (255, 250, 205),  # Lemon chiffon
        "size": (64, 36),
        "points": 500,
        "habitat": "Celestial realm",
        "description": "A mystical fish from the stars."
    },
    "void_fish": {
        "name": "Void Fish",
        "rarity": "mythic",
        "body_color": (25, 25, 112),  # Midnight blue
        "accent_color": (0, 0, 0),  # Black
        "belly_color": (72, 61, 139),  # Dark slate blue
        "shiny_body": (255, 255, 255),  # White
        "shiny_accent": (192, 192, 192),  # Silver
        "shiny_belly": (211, 211, 211),  # Light gray
        "size": (62, 34),
        "points": 750,
        "habitat": "Void dimension",
        "description": "A fish from the void between worlds."
    },
    "prism_fish": {
        "name": "Prism Fish",
        "rarity": "mythic",
        "body_color": (255, 105, 180),  # Hot pink
        "accent_color": (0, 191, 255),  # Deep sky blue
        "belly_color": (50, 205, 50),  # Lime green
        "shiny_body": (255, 215, 0),  # Gold
        "shiny_accent": (255, 0, 255),  # Magenta
        "shiny_belly": (0, 255, 255),  # Cyan
        "size": (66, 38),
        "points": 1000,
        "habitat": "Rainbow waters",
        "description": "A legendary fish that shimmers with all colors."
    }
}

# Rarity weights for random fish selection
RARITY_WEIGHTS = {
    "common": 0.50,      # 50%
    "uncommon": 0.25,    # 25%
    "rare": 0.15,        # 15%
    "epic": 0.07,        # 7%
    "legendary": 0.025,  # 2.5%
    "mythic": 0.005      # 0.5%
}

SHINY_CHANCE = 0.01  # 1% chance for shiny (1/100)

class Fish(pygame.sprite.Sprite):
    def __init__(self, x, y, fish_id=None, force_shiny=False):
        super().__init__()

        # Select fish by rarity if not specified
        if fish_id is None:
            fish_id = self.select_random_fish()

        self.fish_id = fish_id
        self.properties = FISH_DATABASE[fish_id]

        # Determine if this fish is shiny (1/100 chance)
        self.is_shiny = force_shiny or (random.random() < SHINY_CHANCE)

        # Set colors based on shiny status
        if self.is_shiny:
            self.body_color = self.properties["shiny_body"]
            self.accent_color = self.properties["shiny_accent"]
            self.belly_color = self.properties["shiny_belly"]
        else:
            self.body_color = self.properties["body_color"]
            self.accent_color = self.properties["accent_color"]
            self.belly_color = self.properties["belly_color"]

        # Create fish sprite with pixel art
        size = self.properties["size"]
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.draw_fish()
        self.rect = self.image.get_rect(center=(x, y))
        self.points = self.properties["points"]

        # Apply shiny bonus (2x points for shiny)
        if self.is_shiny:
            self.points *= 2

        self.name = self.properties["name"]
        self.rarity = self.properties["rarity"]
        self.description = self.properties["description"]
        self.habitat = self.properties["habitat"]

        # Add some vertical movement (not used in Pokemon-style but kept for compatibility)
        self.vertical_speed = random.uniform(-0.3, 0.3)
        self.tail_bob = 0  # For tail animation

    def select_random_fish(self):
        """Select a random fish based on rarity weights"""
        # First, select rarity tier
        rand = random.random()
        cumulative = 0
        selected_rarity = "common"

        for rarity, weight in RARITY_WEIGHTS.items():
            cumulative += weight
            if rand <= cumulative:
                selected_rarity = rarity
                break

        # Get all fish of selected rarity
        fish_of_rarity = [fish_id for fish_id, props in FISH_DATABASE.items()
                         if props["rarity"] == selected_rarity]

        # Randomly select one
        return random.choice(fish_of_rarity)

    def get_display_name(self):
        """Get the display name with shiny indicator"""
        if self.is_shiny:
            return f"✨ Shiny {self.name} ✨"
        return self.name

    def get_rarity_color(self):
        """Get color based on rarity tier"""
        rarity_colors = {
            "common": (200, 200, 200),      # Gray
            "uncommon": (30, 255, 0),       # Green
            "rare": (0, 112, 221),          # Blue
            "epic": (163, 53, 238),         # Purple
            "legendary": (255, 128, 0),     # Orange
            "mythic": (255, 40, 40)         # Red
        }
        return rarity_colors.get(self.rarity, (255, 255, 255))

    def draw_fish(self):
        """Draw a cute pixel art style fish"""
        w, h = self.properties["size"]
        s = self.image

        # Use instance colors (accounts for shiny status)
        body_color = self.body_color
        accent_color = self.accent_color
        belly_color = self.belly_color

        # Body (main oval)
        pygame.draw.ellipse(s, body_color, [w//4, h//4, w//2, h//2])

        # Tail
        tail_points = [(w//4 + 2, h//2), (2, h//4), (2, 3*h//4)]
        pygame.draw.polygon(s, accent_color, tail_points)

        # Fins
        # Top fin
        top_fin = [(w//2, h//4), (w//2 + 4, h//8), (w//2 + 8, h//4)]
        pygame.draw.polygon(s, accent_color, top_fin)

        # Bottom fin
        bottom_fin = [(w//2, 3*h//4), (w//2 + 4, 7*h//8), (w//2 + 8, 3*h//4)]
        pygame.draw.polygon(s, accent_color, bottom_fin)

        # Belly highlight
        pygame.draw.ellipse(s, belly_color, [w//3, h//2 - 2, w//3, h//4])

        # Eye
        eye_x, eye_y = w - w//4, h//3
        pygame.draw.circle(s, (255, 255, 255), (eye_x, eye_y), 4)
        pygame.draw.circle(s, (0, 0, 0), (eye_x + 1, eye_y), 2)

        # Sparkle effect for shiny fish
        if self.is_shiny:
            pygame.draw.circle(s, (255, 255, 255), (w//6, h//6), 2)
            pygame.draw.circle(s, (255, 255, 255), (w - w//6, h - h//6), 2)

        # Scales pattern
        for i in range(3):
            scale_x = w//3 + i * 6
            pygame.draw.circle(s, accent_color, (scale_x, h//2), 2, 1)

    def update(self):
        self.rect.x -= self.speed  # Fish swims to the left
        self.rect.y += self.vertical_speed  # Slight vertical movement

        # Tail bobbing animation
        self.tail_bob += 0.2

        # Keep fish in vertical bounds
        if self.rect.top < 60:
            self.vertical_speed = abs(self.vertical_speed)
        elif self.rect.bottom > 540:
            self.vertical_speed = -abs(self.vertical_speed)

        # Reset fish to the right if it exits the screen
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH + random.randint(50, 200)
            self.rect.y = random.randint(100, 500)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
