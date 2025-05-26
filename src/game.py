import pygame
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.player import Player
from src.levels import Level
from src.enemies import Enemy
from src.ui import draw_player_health, init_ui

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player(400, 300)  # Start position
        self.current_level = Level("eldoria")  # First level
        self.enemies = []
        self.enemies.append(Enemy(x=600, y=502)) # Position near the ground platform
        self.game_state = "playing"
        init_ui()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.jump()
            elif event.key == pygame.K_a:
                self.player.move_left()
            elif event.key == pygame.K_d:
                self.player.move_right()
            elif event.key == pygame.K_f:
                self.player.attack()

    def update(self):
        self.player.update(self.current_level.platforms)
        self.current_level.update()
        for enemy in self.enemies:
            enemy.update()
        
        if self.player.is_attacking and self.player.attack_rect:
            # Use a copy of the list for safe removal
            for i, enemy in reversed(list(enumerate(self.enemies))):
                if self.player.attack_rect.colliderect(enemy.rect):
                    enemy.take_damage(self.player.attack_power)
                    if enemy.health <= 0:
                        self.enemies.pop(i) # Remove dead enemy
                    # To prevent multiple hits on the same enemy in one attack swing or
                    # to make the attack hit only one enemy, you might want to set
                    # self.player.is_attacking = False here or break the loop.
                    # For now, allowing the attack to hit all enemies in range for its duration.

    def draw(self):
        self.screen.fill((0, 0, 0))  # Black background
        self.current_level.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.player.draw(self.screen)
        draw_player_health(self.screen, self.player.health, self.player.max_health)
