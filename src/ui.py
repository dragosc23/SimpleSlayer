import pygame
from src.consumables import HealthPotion
from src.items import RARITY_COMMON, RARITY_UNCOMMON, RARITY_RARE # Added import

# Rarity Colors
RARITY_COLORS = {
    RARITY_COMMON: (180, 180, 180),  # Gray
    RARITY_UNCOMMON: (100, 255, 100), # Green
    RARITY_RARE: (100, 100, 255),   # Blue
    "Default": (255, 255, 255)       # White for items without rarity or fallback
}

# Initialize font (call this once, perhaps in Game.__init__ or here if ui_init is called)
# pygame.font.init() # Ensure font module is initialized
# For now, assume font module is initialized by pygame.init() in main.py
HEALTH_FONT = None
INFO_FONT = None # Declare at global scope

def init_ui():
    global HEALTH_FONT, INFO_FONT # Add INFO_FONT
    HEALTH_FONT = pygame.font.SysFont('arial', 30)
    INFO_FONT = pygame.font.SysFont('arial', 24) # Initialize INFO_FONT

def draw_player_health(screen, player_health, player_max_health):
    if HEALTH_FONT is None: # Fallback if not initialized
        init_ui()

    text_surface = HEALTH_FONT.render(f"Health: {player_health}/{player_max_health}", True, (255, 255, 255)) # White text
    screen.blit(text_surface, (10, 10)) # Display at top-left

def draw_wave_info(screen, wave_number, total_waves, enemies_remaining, game_state): # Add game_state
    if INFO_FONT is None: init_ui() # Fallback
    
    wave_text = f"Wave: {wave_number}/{total_waves} | Enemies: {enemies_remaining}"
    if game_state == "level_complete":
        wave_text = f"Level Complete! (All {total_waves} waves cleared)"
    # This case might be redundant if game_state updates promptly.
    # elif wave_number == total_waves and enemies_remaining == 0 and game_state != "level_complete":
    #     wave_text = f"Wave: {wave_number}/{total_waves} cleared! Final wave."

    text_surface = INFO_FONT.render(wave_text, True, (255, 255, 255))
    screen.blit(text_surface, (10, 40)) # Display below health

def draw_player_stats(screen, player):
    if INFO_FONT is None: init_ui() # Fallback
    
    # Base Attack
    base_atk_text = f"Base Atk: {player.base_attack_power}"
    text_surface_base_atk = INFO_FONT.render(base_atk_text, True, (255, 255, 255))
    screen.blit(text_surface_base_atk, (10, 70)) # Display below wave info

    # Weapon Info
    weapon_name_str = "None"
    # weapon_bonus = 0 # Not strictly needed here if __str__ is used
    weapon_color = RARITY_COLORS["Default"]

    if player.equipped_weapon:
        weapon_name_str = str(player.equipped_weapon) # Relies on __str__
        # weapon_bonus = player.equipped_weapon.attack_bonus # Already correct
        weapon_color = RARITY_COLORS.get(player.equipped_weapon.rarity, RARITY_COLORS["Default"])
            
    display_weapon_text = f"Weapon: {weapon_name_str}" if player.equipped_weapon else "Weapon: None"
    text_surface_weapon = INFO_FONT.render(display_weapon_text, True, weapon_color)
    screen.blit(text_surface_weapon, (10, 95))

    # Total Attack
    total_atk_text = f"Total Atk: {player.get_total_attack_power()}"
    text_surface_total_atk = INFO_FONT.render(total_atk_text, True, (255, 255, 255))
    screen.blit(text_surface_total_atk, (10, 120))

def draw_player_experience(screen, player):
    if INFO_FONT is None: init_ui() # Fallback

    level_text = f"Lvl: {player.level}"
    xp_text = f"XP: {player.current_xp}/{player.xp_to_next_level}"
    
    if player.level >= 50: # Assuming 50 is max level as per experience.py
        xp_text = "XP: MAX LEVEL"

    level_surface = INFO_FONT.render(level_text, True, (255, 255, 255)) # White text
    xp_surface = INFO_FONT.render(xp_text, True, (255, 255, 255))

    screen.blit(level_surface, (10, 145)) # Position below existing player stats
    screen.blit(xp_surface, (80, 145)) # Position next to level

def draw_inventory_preview(screen, player_inventory):
    if INFO_FONT is None: init_ui() # Fallback

    # Display capacity
    capacity_text = f"Inventory: {len(player_inventory.items)}/{player_inventory.capacity}"
    capacity_surface = INFO_FONT.render(capacity_text, True, (255, 255, 255))
    screen.blit(capacity_surface, (10, 170)) # Y position for capacity

    # Display Health Potion count
    health_potions = [item for item in player_inventory.items if isinstance(item, HealthPotion)]
    potion_count_text = f"Health Potions: {len(health_potions)}"
    potion_count_surface = INFO_FONT.render(potion_count_text, True, (200, 220, 255)) # Light blue for potions
    screen.blit(potion_count_surface, (15, 195)) # Y position for potion count
    
    # Simpler: just list all items as before, potion count is a summary line
    item_y_offset = 220 # Adjust starting Y for general item list
    max_items_to_show = 2 # Show fewer general items if potion count is shown separately
    
    items_shown_count = 0
    for i, item in enumerate(player_inventory.items):
        if items_shown_count >= max_items_to_show:
            break
        # Optional: Could decide to not list potions here if already counted above
        # if isinstance(item, HealthPotion):
        #    continue 
        
        item_rarity = getattr(item, 'rarity', None) # Get rarity if item has it
        item_color = RARITY_COLORS.get(item_rarity, RARITY_COLORS["Default"])
            
        item_text_display = f"- {str(item)}" # Use __str__ for consistency

        item_surface = INFO_FONT.render(item_text_display, True, item_color)
        screen.blit(item_surface, (15, item_y_offset + (items_shown_count * 20)))
        items_shown_count += 1
    
    if len(player_inventory.items) > items_shown_count:
        remaining_items = len(player_inventory.items) - items_shown_count
        more_items_text = f"  (...and {remaining_items} more items)"
        more_items_surface = INFO_FONT.render(more_items_text, True, (150,150,150)) # Keep this a bit dimmer
        screen.blit(more_items_surface, (15, item_y_offset + (items_shown_count * 20)))


# (Optional for now, but good practice for future UI elements)
# class UIManager:
#     def __init__(self):
#         pygame.font.init() # Initialize font module
#         self.health_font = pygame.font.SysFont('arial', 30)
#
#     def draw_player_health(self, screen, player_health, player_max_health):
#         text_surface = self.health_font.render(f"Health: {player_health}/{player_max_health}", True, (255, 255, 255))
#         screen.blit(text_surface, (10, 10))
