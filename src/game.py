import pygame
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.player import Player
from src.levels import Level
from src.enemies import Enemy
from src.ui import draw_player_health, init_ui, draw_wave_info, draw_player_stats, draw_player_experience, draw_inventory_preview
from src.items import Weapon
from src.consumables import HealthPotion # Added import
from src.experience import grant_experience, check_level_up

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player(400, 300)  # Start position
        self.current_level = Level("eldoria")  # First level
        self.enemies = [] 
        # self.enemies.append(Enemy(x=600, y=502)) # Removed direct spawning
        self.game_state = "playing"
        init_ui()
        self.current_level.spawn_wave(self.enemies) # Initial wave spawn

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # Keep jump for manual control
                self.player.jump()
            # Removed K_a, K_d, K_f for auto movement/attack

    def update(self):
        self.player.update(self.current_level.platforms, self.enemies)
        self.current_level.update()
        for enemy in self.enemies:
            enemy.update()
        
        if self.player.is_attacking and self.player.attack_rect:
            # Use a copy of the list for safe removal
            for i, enemy in reversed(list(enumerate(self.enemies))):
                if self.player.attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(self.player.get_total_attack_power())
                    if enemy.health <= 0:
                        print(f"Enemy defeated, granting {enemy.xp_value} XP.") # Feedback
                        if grant_experience(self.player, enemy.xp_value): # if XP was actually granted (not max level)
                            check_level_up(self.player)
                        
                        dropped_item = enemy.drop_loot()
                        if dropped_item:
                            if isinstance(dropped_item, Weapon):
                                if self.player.equipped_weapon is None or \
                                   dropped_item.attack_bonus > self.player.equipped_weapon.attack_bonus:
                                    old_weapon = self.player.equipped_weapon
                                    self.player.equip_weapon(dropped_item)
                                    if old_weapon:
                                        if not self.player.inventory.add_item(old_weapon):
                                            print(f"Inventory full. Could not add {old_weapon.name} to inventory.")
                                else:
                                    print(f"Player found {dropped_item.name} (not an upgrade), attempting to add to inventory.")
                                    if not self.player.inventory.add_item(dropped_item):
                                        print(f"Inventory full. Could not add {dropped_item.name} to inventory.")
                            elif isinstance(dropped_item, HealthPotion):
                                print(f"Player found a {dropped_item.name}, attempting to add to inventory.")
                                if not self.player.inventory.add_item(dropped_item):
                                    print(f"Inventory full. Could not add {dropped_item.name} to inventory.")
                            else:
                                # Generic item type, try to add to inventory
                                print(f"Player found a {dropped_item.name} (Type: {dropped_item.item_type if hasattr(dropped_item, 'item_type') else 'Unknown'}), attempting to add to inventory.")
                                if not self.player.inventory.add_item(dropped_item):
                                    print(f"Inventory full. Could not add {dropped_item.name} to inventory.")
                        self.enemies.pop(i) # Remove dead enemy
                    # To prevent multiple hits on the same enemy in one attack swing or
                    # to make the attack hit only one enemy, you might want to set
                    # self.player.is_attacking = False here or break the loop.
                    # For now, allowing the attack to hit all enemies in range for its duration.
        
        # Check for wave completion
        if not self.enemies and self.game_state == "playing": # If list is empty and game is active
            # wave_number in Level is already incremented after a successful spawn
            print(f"Wave {self.current_level.wave_number} cleared!") 
            if self.current_level.spawn_wave(self.enemies):
                # spawn_wave prints the "Spawning wave X" message internally
                pass
            else:
                print("All waves cleared for this level!")
                self.game_state = "level_complete" # Example state change


    def draw(self):
        self.screen.fill((0, 0, 0))  # Black background
        self.current_level.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.player.draw(self.screen)
        draw_player_health(self.screen, self.player.health, self.player.max_health)

        total_waves = len(self.current_level.enemy_waves)
        current_display_wave = self.current_level.wave_number
        # wave_number in Level is the number of the wave that has been spawned.
        # If wave_number is 1, it means wave 1 is active or just cleared.
        # If game_state is "level_complete", it means all waves up to total_waves were cleared.
        if self.game_state == "level_complete":
            current_display_wave = total_waves # Show all waves as done

        draw_wave_info(self.screen, current_display_wave, total_waves, len(self.enemies), self.game_state)
        draw_player_stats(self.screen, self.player)
        draw_player_experience(self.screen, self.player)
        draw_inventory_preview(self.screen, self.player.inventory)
