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
from src.systems.experience_system import grant_experience, check_level_up, get_xp_for_level # Added get_xp_for_level
from src.utils.constants import PLAYER_INITIAL_X, PLAYER_INITIAL_Y, BLACK, STATE_PLAYING, STATE_GAME_OVER, STATE_MENU, STATE_LEVEL_COMPLETE, EVENT_PLAYER_DIED, STATE_VICTORY, EVENT_ALL_WAVES_CLEARED
from src.core.game_state_machine import GameStateMachine, MenuState, PlayingState, GameOverState, VictoryState
from src.core.event_manager import EventManager
from src.managers.save_manager import save_player_progress, load_player_progress # Added import

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.event_manager = EventManager()
        self.player = Player(PLAYER_INITIAL_X, PLAYER_INITIAL_Y) # Player initialized with defaults
        self.load_game_data() # Load progress, potentially overriding defaults
        
        self.current_level = Level("eldoria") 
        self.enemies = []
        
        init_ui()

        self.game_state = STATE_PLAYING 

        self.state_machine = GameStateMachine()
        menu_state = MenuState()
        playing_state = PlayingState(game_manager_ref=self)
        game_over_state = GameOverState()
        victory_state = VictoryState()

        self.state_machine.add_state(STATE_MENU, menu_state)
        self.state_machine.add_state(STATE_PLAYING, playing_state)
        self.state_machine.add_state(STATE_GAME_OVER, game_over_state)
        self.state_machine.add_state(STATE_VICTORY, victory_state)
        
        self.state_machine.change_state(STATE_MENU)

    def load_game_data(self):
        print("Attempting to load player progress...")
        loaded_data = load_player_progress() # Uses default filename
        if loaded_data:
            player_level = loaded_data.get('level', 1)
            player_xp = loaded_data.get('xp', 0)
            
            self.player.level = player_level
            self.player.current_xp = player_xp
            self.player.xp_to_next_level = get_xp_for_level(self.player.level)
            
            initial_base_attack = 10 
            initial_max_health = 100 
            
            level_bonus_attack = (player_level - 1) * 2
            level_bonus_health = (player_level - 1) * 10
            
            self.player.base_attack_power = initial_base_attack + level_bonus_attack
            self.player.max_health = initial_max_health + level_bonus_health
            self.player.health = self.player.max_health 

            print(f"Player data loaded: Level {self.player.level}, XP {self.player.current_xp}/{self.player.xp_to_next_level}")
            print(f"Player stats updated: Base Atk {self.player.base_attack_power}, Max Health {self.player.max_health}")
        else:
            print("No save data found or error loading. Starting fresh.")

    def subscribe_to_events(self):
        self.event_manager.subscribe(EVENT_PLAYER_DIED, self.handle_player_death_event)
        self.event_manager.subscribe(EVENT_ALL_WAVES_CLEARED, self.handle_all_waves_cleared_event) # Added

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

    def handle_all_waves_cleared_event(self, **data):
        print(f"GameManager: Received EVENT_ALL_WAVES_CLEARED. Changing to VICTORY state.")
        self.state_machine.change_state(STATE_VICTORY)
        
        print("Saving player progress after clearing all waves...")
        player_data_to_save = {
            'level': self.player.level,
            'xp': self.player.current_xp
            # Add other data to save in future, e.g., inventory, equipped items
        }
        save_player_progress(player_data_to_save)

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
