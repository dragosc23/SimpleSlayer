# src/utils/constants.py

# Screen Dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 150, 255) # Example for potion count in UI
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100) # Example for level platforms
LIGHT_GRAY = (200, 200, 200) # Example for inventory item text
DARKER_GRAY = (150, 150, 150) # Example for inventory 'more items' text

# Item Rarity (Moved from items.py)
RARITY_COMMON = "Common"
RARITY_UNCOMMON = "Uncommon"
RARITY_RARE = "Rare"

RARITY_MULTIPLIERS = {
    RARITY_COMMON: 1.0,
    RARITY_UNCOMMON: 1.2,
    RARITY_RARE: 1.5
}

# UI Colors for Rarity (Moved from ui.py)
RARITY_COLORS = {
    RARITY_COMMON: GRAY, # Using defined GRAY
    RARITY_UNCOMMON: GREEN, # Using defined GREEN
    RARITY_RARE: BLUE,    # Using defined BLUE
    "Default": WHITE      # Using defined WHITE
}

# Player settings (Example, can be expanded)
PLAYER_INITIAL_X = 400
PLAYER_INITIAL_Y = 300 # This might need adjustment based on new level system
PLAYER_MOVE_SPEED = 2
PLAYER_JUMP_VELOCITY = -15 # From old player code
PLAYER_GRAVITY = 0.8     # From old player code

# Enemy settings (Example)
ENEMY_DEFAULT_HEALTH = 50
ENEMY_DEFAULT_XP = 20

# File paths (Examples, might need to be dynamic later)
# FONT_PATH_ARIAL = "arial" # Pygame can often find system fonts by name

# Game states (Example)
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_MENU = "menu"
STATE_LEVEL_COMPLETE = "level_complete"

# Custom Game Event Types
EVENT_PLAYER_DIED = "player_died_event"
EVENT_ALL_WAVES_CLEARED = "all_waves_cleared_event"
EVENT_ENEMY_DEFEATED = "enemy_defeated_event" # Example for potential future use
# Add more events as needed
