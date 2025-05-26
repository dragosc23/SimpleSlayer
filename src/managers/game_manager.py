import pygame
import sys
import os
# Adjusted for new location: one level up to reach 'src'
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.game_objects.player import Player
from src.game_objects.level import Level
from src.game_objects.enemy import Enemy
from src.ui.hud import draw_player_health, init_ui, draw_wave_info, draw_player_stats, draw_player_experience, draw_inventory_preview
from src.game_objects.item_definitions import Weapon, HealthPotion
from src.systems.experience_system import grant_experience, check_level_up
from src.utils.constants import PLAYER_INITIAL_X, PLAYER_INITIAL_Y, BLACK, STATE_PLAYING, STATE_GAME_OVER, STATE_MENU, STATE_LEVEL_COMPLETE, EVENT_PLAYER_DIED # Modified import
from src.core.game_state_machine import GameStateMachine, MenuState, PlayingState, GameOverState
from src.core.event_manager import EventManager # Added import

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.event_manager = EventManager() # Added
        self.player = Player(PLAYER_INITIAL_X, PLAYER_INITIAL_Y)
        self.current_level = Level("eldoria") # Example level name
        self.enemies = []
        
        init_ui()

        self.game_state = STATE_PLAYING 

        self.state_machine = GameStateMachine()
        menu_state = MenuState()
        playing_state = PlayingState(game_manager_ref=self)
        game_over_state = GameOverState()

        self.state_machine.add_state(STATE_MENU, menu_state)
        self.state_machine.add_state(STATE_PLAYING, playing_state)
        self.state_machine.add_state(STATE_GAME_OVER, game_over_state)
        
        self.state_machine.change_state(STATE_MENU)
        # self.subscribe_to_events() # Call moved to reset_game_for_playing

    def subscribe_to_events(self):
        self.event_manager.subscribe(EVENT_PLAYER_DIED, self.handle_player_death_event)
        # Future: self.event_manager.subscribe(EVENT_ALL_WAVES_CLEARED, self.handle_all_waves_cleared_event)

    def reset_game_for_playing(self):
        """ Resets player, level, enemies, and game_state for a new game or replay."""
        print("Resetting game for new playing session...")
        self.player = Player(PLAYER_INITIAL_X, PLAYER_INITIAL_Y) 
        self.current_level = Level("eldoria") 
        self.enemies = []
        self.current_level.spawn_wave(self.enemies) 
        self.game_state = STATE_PLAYING 
        self.subscribe_to_events() # Added call

    def handle_player_death_event(self, **data): # data might be empty or carry info about death
        print(f"GameManager: Received PLAYER_DIED_EVENT. Changing to GAME_OVER state.")
        # Optional: check if current state is PLAYING before changing
        # if self.state_machine.current_state_name == STATE_PLAYING:
        self.state_machine.change_state(STATE_GAME_OVER)
        # else:
        #     print("PLAYER_DIED_EVENT received but not in PLAYING state. Ignored state change.")

    def handle_event_in_playing_state(self, events): 
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()

    def update_in_playing_state(self, dt):
        self.player.update(self.current_level.platforms, self.enemies)
        self.current_level.update()
        for enemy in self.enemies:
            enemy.update()
        
        if self.player.is_attacking and self.player.attack_rect:
            for i, enemy in reversed(list(enumerate(self.enemies))):
                if self.player.attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(self.player.get_total_attack_power())
                    if enemy.health <= 0:
                        print(f"Enemy defeated, granting {enemy.xp_value} XP.")
                        if grant_experience(self.player, enemy.xp_value):
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
                                print(f"Player found a {dropped_item.name} (Type: {dropped_item.item_type if hasattr(dropped_item, 'item_type') else 'Unknown'}), attempting to add to inventory.")
                                if not self.player.inventory.add_item(dropped_item):
                                    print(f"Inventory full. Could not add {dropped_item.name} to inventory.")
                        self.enemies.pop(i)
        
        # Check for wave completion / level completion
        if not self.enemies and self.game_state == STATE_PLAYING: 
            print(f"Wave {self.current_level.wave_number} cleared!") 
            if self.current_level.spawn_wave(self.enemies):
                pass # New wave spawned
            else:
                print("All waves cleared for this level!")
                self.game_state = STATE_LEVEL_COMPLETE # This will be checked by PlayingState

    def draw_playing_state(self, screen):
        screen.fill(BLACK)
        self.current_level.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        self.player.draw(screen)
        
        draw_player_health(screen, self.player.health, self.player.max_health)
        total_waves = len(self.current_level.enemy_waves)
        current_display_wave = self.current_level.wave_number
        # Use the internal game_state for UI display consistency within PlayingState
        if self.game_state == STATE_LEVEL_COMPLETE: 
            current_display_wave = total_waves
        draw_wave_info(screen, current_display_wave, total_waves, len(self.enemies), self.game_state)
        draw_player_stats(screen, self.player)
        draw_player_experience(screen, self.player)
        draw_inventory_preview(screen, self.player.inventory)

    # Main methods now delegate to state machine
    def handle_event(self, event):
        self.state_machine.handle_events([event]) # Pass as a list

    def update(self, dt):
        self.state_machine.update(dt)

    def draw(self):
        self.state_machine.draw(self.screen)
