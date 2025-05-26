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
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_duration = 20  # How long the attack hitbox is active (frames)
        self.attack_duration_timer = 0
        self.attack_rect = None

    def move_left(self):
        self.vel_x = -5

    def move_right(self):
        self.vel_x = 5

    def jump(self):
        if not self.jumping:
            self.vel_y = -15
            self.jumping = True

    def attack(self):
        if self.attack_cooldown <= 0:
            self.is_attacking = True
            self.attack_cooldown = 60  # Cooldown before next attack (frames)
            self.attack_duration_timer = self.attack_duration
            # Define attack hitbox relative to player (e.g., in front of player)
            # Assuming player faces right for now.
            self.attack_rect = pygame.Rect(self.x + self.width, self.y, self.width, self.height)

    def update(self, platforms):
        # Apply gravity
        self.vel_y += 0.8
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y

        if self.attack_rect:
            # Keep attack_rect relative to player, simple example:
            self.attack_rect.x = self.x + self.width 
            self.attack_rect.y = self.y
        
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        for platform_rect in platforms:
            if player_rect.colliderect(platform_rect):
                if self.vel_y > 0:  # Player is moving down
                    self.y = platform_rect.top - self.height
                    self.vel_y = 0
                    self.jumping = False
                elif self.vel_y < 0: # Player is moving up
                    self.y = platform_rect.bottom
                    self.vel_y = 0
                # Basic horizontal collision (can be improved)
                # Check X-axis collision separately
                # Update player_rect for X-axis check if needed
                # For now, this part is simplified / might need separate handling
                # if self.vel_x > 0: # Moving right
                #     self.x = platform_rect.left - self.width
                #     self.vel_x = 0
                # elif self.vel_x < 0: # Moving left
                #     self.x = platform_rect.right
                #     self.vel_x = 0


        # Friction
        self.vel_x *= 0.9

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.is_attacking:
            self.attack_duration_timer -= 1
            if self.attack_duration_timer <= 0:
                self.is_attacking = False
                self.attack_rect = None

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), 
                        (self.x, self.y, self.width, self.height))
        if self.is_attacking and self.attack_rect:
            pygame.draw.rect(screen, (0, 255, 0), self.attack_rect) # Green for attack hitbox
