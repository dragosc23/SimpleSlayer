import pygame
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.player import Player
from src.levels import Level

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.player = Player(400, 300)  # Start position
        self.current_level = Level("eldoria")  # First level
        self.game_state = "playing"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.player.jump()
            elif event.key == pygame.K_a:
                self.player.move_left()
            elif event.key == pygame.K_d:
                self.player.move_right()

    def update(self):
        self.player.update()
        self.current_level.update()
        # Add collision detection and combat updates here

    def draw(self):
        self.screen.fill((0, 0, 0))  # Black background
        self.current_level.draw(self.screen)
        self.player.draw(self.screen)
