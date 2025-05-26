import pygame
import sys
from src.managers.game_manager import Game # Modified import
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class SimpleSlayer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Modified
        pygame.display.set_caption("SimpleSlayer")
        self.clock = pygame.time.Clock()
        self.game = Game(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.game.handle_event(event)

            dt = self.clock.get_time() / 1000.0 # Calculate dt in seconds
            self.game.update(dt) # Pass dt
            self.game.draw()
            
            pygame.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = SimpleSlayer()
    game.run()
