import pygame
import sys
from src.game import Game

class SimpleSlayer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
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

            self.game.update()
            self.game.draw()
            
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    game = SimpleSlayer()
    game.run()
