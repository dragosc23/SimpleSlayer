import pygame

# Initialize font (call this once, perhaps in Game.__init__ or here if ui_init is called)
# pygame.font.init() # Ensure font module is initialized
# For now, assume font module is initialized by pygame.init() in main.py
HEALTH_FONT = None

def init_ui():
    global HEALTH_FONT
    HEALTH_FONT = pygame.font.SysFont('arial', 30) # Or any other preferred font

def draw_player_health(screen, player_health, player_max_health):
    if HEALTH_FONT is None: # Fallback if not initialized
        init_ui()

    text_surface = HEALTH_FONT.render(f"Health: {player_health}/{player_max_health}", True, (255, 255, 255)) # White text
    screen.blit(text_surface, (10, 10)) # Display at top-left

# (Optional for now, but good practice for future UI elements)
# class UIManager:
#     def __init__(self):
#         pygame.font.init() # Initialize font module
#         self.health_font = pygame.font.SysFont('arial', 30)
#
#     def draw_player_health(self, screen, player_health, player_max_health):
#         text_surface = self.health_font.render(f"Health: {player_health}/{player_max_health}", True, (255, 255, 255))
#         screen.blit(text_surface, (10, 10))
