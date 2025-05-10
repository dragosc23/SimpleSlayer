import pygame

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 48
        self.vel_x = 0
        self.vel_y = 0
        self.jumping = False
        self.health = 100
        self.max_health = 100
        self.attack_power = 10
        self.defense = 5

    def move_left(self):
        self.vel_x = -5

    def move_right(self):
        self.vel_x = 5

    def jump(self):
        if not self.jumping:
            self.vel_y = -15
            self.jumping = True

    def update(self):
        # Apply gravity
        self.vel_y += 0.8
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Basic ground collision
        if self.y > 500:  # Ground level
            self.y = 500
            self.vel_y = 0
            self.jumping = False

        # Friction
        self.vel_x *= 0.9

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), 
                        (self.x, self.y, self.width, self.height))
