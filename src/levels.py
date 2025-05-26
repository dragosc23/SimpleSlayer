import pygame

class Level:
    def __init__(self, level_name):
        print(f"Level {level_name} loaded")
        self.platforms = []
        # Basic ground platform (assuming screen width 800)
        self.platforms.append(pygame.Rect(0, 550, 800, 50))

    def update(self):
        pass

    def draw(self, screen):
        for platform in self.platforms:
            pygame.draw.rect(screen, (100, 100, 100), platform)
