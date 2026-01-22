# Screen dimensions - 1080p
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Stardew Valley inspired color palette
WATER_COLOR = (76, 145, 178)  # Soft blue water
WATER_DEEP = (57, 110, 138)  # Deeper water
SAND_COLOR = (237, 201, 175)  # Light sandy beach
GRASS_COLOR = (139, 195, 74)  # Fresh grass
DIRT_COLOR = (161, 130, 98)  # Brown dirt

# Wooper-inspired player colors
WOOPER_BLUE = (79, 164, 210)  # Light blue body
WOOPER_DARK_BLUE = (47, 116, 163)  # Dark blue accents
WOOPER_PINK = (255, 128, 171)  # Pink gills
PLAYER_COLOR = WOOPER_BLUE

# UI Colors (Stardew Valley style)
UI_BG = (51, 31, 24)  # Dark brown
UI_TEXT = (86, 22, 12)  # Brown text
UI_ACCENT = (255, 246, 229)  # Cream
UI_BORDER = (143, 86, 59)  # Medium brown

# Game settings - Ultra smooth
FPS = 240
TILE_SIZE = 64  # Larger tiles for 1080p
PLAYER_SPEED = 4  # Scaled for higher resolution

# Fishing mechanics constants
BITE_WINDOW_FRAMES = 90  # 1.5 seconds at 60 FPS to react to bite
FAILED_MESSAGE_DURATION = 60  # 1 second to show "got away" message
CATCH_DISPLAY_DURATION = 180  # 3 seconds to show catch notification

# Render layers (higher = drawn on top)
LAYER_BACKGROUND = 0
LAYER_WORLD = 1
LAYER_PLAYER = 2
LAYER_PARTICLES = 3
LAYER_UI_BASE = 4
LAYER_FISHING_ELEMENTS = 5  # Bobber/line drawn after base UI
LAYER_UI_OVERLAY = 6  # Popups, notifications
LAYER_UI_TOP = 7  # Pause screen, daily rewards
