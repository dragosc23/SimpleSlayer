import pygame
from src.enemies import Enemy # Added import

class Level:
    def __init__(self, level_name):
        print(f"Level {level_name} loaded")
        self.platforms = []
        # Basic ground platform (assuming screen width 800, enemy height ~48)
        # Enemy y should be around 550 - 48 = 502 for ground
        self.platforms.append(pygame.Rect(0, 550, 800, 50))
        
        self.wave_number = 0
        # Each tuple: (enemy_type_placeholder, x, y, health_multiplier)
        self.enemy_waves = [
            [('goblin', 600, 502, 1.0), ('goblin', 700, 502, 1.0)],  # Wave 1
            [('orc', 550, 502, 1.5), ('orc', 750, 502, 1.5)],      # Wave 2
            [('troll', 650, 482, 2.0)] # Wave 3 (y=482 for slightly different placement, maybe on a higher platform if one existed)
        ]

    def spawn_wave(self, game_enemies_list):
        # Assuming game_enemies_list is the list of active enemies from the Game class
        # and it's managed (cleared or checked) before calling this for a new wave.
        # For this implementation, we assume it's called when the previous wave is cleared.
        
        if self.wave_number < len(self.enemy_waves):
            current_wave_data = self.enemy_waves[self.wave_number]
            print(f"Spawning wave {self.wave_number + 1}") # User-friendly wave number
            for enemy_type, x, y, health_mult in current_wave_data:
                # Base health for an enemy, e.g., 50
                base_health = 50
                base_xp = 20 # Base XP for an enemy
                game_enemies_list.append(Enemy(x=x, y=y, health=int(base_health * health_mult), xp_value=int(base_xp * health_mult)))
            self.wave_number += 1
            return True # Wave spawned
        else:
            print("All waves defeated for this level!")
            return False # No more waves

    def update(self):
        pass

    def draw(self, screen):
        for platform in self.platforms:
            pygame.draw.rect(screen, (100, 100, 100), platform)
