import pygame

class Enemy:
    def __init__(self, x, y, width=32, height=48, health=50):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.max_health = health
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (0, 0, 255)  # Blue color for the enemy

    def update(self):
        # Future: Add enemy AI, movement, etc.
        # Update rect for drawing and collision
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        print(f"Enemy took {amount} damage, health is now {self.health}") # Basic feedback
