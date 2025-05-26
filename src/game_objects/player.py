import pygame
from src.game_objects.item_definitions import Weapon, HealthPotion
from src.systems.experience_system import get_xp_for_level
from src.game_objects.components.inventory_component import Inventory
from src.utils.constants import PLAYER_MOVE_SPEED, PLAYER_JUMP_VELOCITY, PLAYER_GRAVITY, PLAYER_INITIAL_X, PLAYER_INITIAL_Y, RARITY_COMMON
from src.core.asset_loader import load_image # Added import

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image("player/player.png", use_alpha=True) # Added
        self.rect = self.image.get_rect(topleft=(self.x, self.y)) # Added
        self.width = self.rect.width # Modified
        self.height = self.rect.height # Modified
        self.vel_y = 0
        self.jumping = False
        self.health = 100
        self.max_health = 100
        self.base_attack_power = 10
        self.defense = 5
        self.equipped_weapon = None
        # Initial weapon is common, base_attack_bonus is its specific value
        self.equip_weapon(Weapon(name="Rusty Sword", base_attack_bonus=2, rarity=RARITY_COMMON))

        self.level = 1
        self.current_xp = 0
        self.xp_to_next_level = get_xp_for_level(self.level)
        print(f"Player initialized: Level {self.level}, XP: {self.current_xp}/{self.xp_to_next_level}")

        self.is_attacking = False
        self.attack_cooldown = 30 
        self.attack_duration = 20
        self.attack_duration_timer = 0
        self.attack_rect = None
        self.move_speed = PLAYER_MOVE_SPEED # Modified
        self.target_enemy = None
        self.inventory = Inventory(capacity=10)

    # Removed move_left and move_right

    def jump(self):
        if not self.jumping:
            self.vel_y = PLAYER_JUMP_VELOCITY # Modified
            self.jumping = True
            
    def equip_weapon(self, weapon):
        if isinstance(weapon, Weapon): # Basic type check
            self.equipped_weapon = weapon
            print(f"Player equipped: {weapon.name}") # Feedback
        else:
            print("Error: Tried to equip an invalid item as a weapon.")

    def get_total_attack_power(self):
        total_attack = self.base_attack_power
        if self.equipped_weapon:
            total_attack += self.equipped_weapon.attack_bonus
        return total_attack

    def attack(self):
        # This method is now called automatically
        self.is_attacking = True
        self.attack_duration_timer = self.attack_duration
        # Define attack hitbox relative to player
        # Assuming player faces right for now. This might need to adjust based on target_enemy position
        # For now, simple right-facing attack
        # Attack rect definition moved to attack() or update() based on enemy direction
        self.attack_rect = None # Initialize as None

    def use_item_by_type(self, item_type_name):
        """ Uses the first available item of a given type from inventory. """
        items_of_type = self.inventory.get_items_by_type(item_type_name)
        if items_of_type:
            item_to_use = items_of_type[0] # Get the first one
            
            # Specific use logic might differ, for HealthPotion it's straightforward
            if hasattr(item_to_use, 'use') and callable(getattr(item_to_use, 'use')):
                if item_to_use.use(self): # Call use() method, pass player instance. It returns True if used.
                    self.inventory.remove_item(item_to_use)
                    print(f"Player used and removed {item_to_use.name} from inventory.")
                    return True # Item was used successfully
                else:
                    # print(f"{item_to_use.name} could not be used (e.g., health full).") # Already printed by potion
                    return False # Item use condition not met
            else:
                print(f"Item {item_to_use.name} does not have a callable 'use' method.")
                return False
        else:
            # print(f"No items of type '{item_type_name}' in inventory.") # Can be noisy
            return False

    def update(self, platforms, enemies):
        # Targeting
        if self.target_enemy is None or self.target_enemy.health <= 0:
            self.target_enemy = None # Ensure it's None if previous target died
            closest_enemy = None
            min_dist = float('inf')
            for enemy in enemies:
                if enemy.health > 0: # Only target live enemies
                    dist = abs(enemy.x - self.x)
                    if dist < min_dist:
                        min_dist = dist
                        closest_enemy = enemy
            self.target_enemy = closest_enemy
        
        # Movement
        if self.target_enemy:
            if self.target_enemy.x > self.x + self.width + 5:  # Move right
                self.x += self.move_speed # PLAYER_MOVE_SPEED is already assigned to self.move_speed
            elif self.target_enemy.x + self.target_enemy.width < self.x - 5:  # Move left
                self.x -= self.move_speed # PLAYER_MOVE_SPEED is already assigned to self.move_speed
            else:
                pass # Stop horizontal movement
        else:
            pass # Player stays put

        # Apply gravity
        self.vel_y += PLAYER_GRAVITY # Modified
        
        # Update position (Y-axis from gravity, X-axis from auto-movement)
        # self.x += self.vel_x # vel_x removed. self.x is modified by movement logic directly
        self.y += self.vel_y
        self.rect.topleft = (self.x, self.y) # Update rect from x, y

        # Attack rect update moved to where attack is initiated / direction is known
        # if self.attack_rect:
        #     # Keep attack_rect relative to player
        #     # This needs to be smarter if player can face left/right
        #     # For now, always attack to the right for simplicity
        #     self.attack_rect.x = self.x + self.width 
        #     self.attack_rect.y = self.y
        
        # player_rect = self.rect # No need to create player_rect, use self.rect directly

        for platform_rect in platforms:
            if self.rect.colliderect(platform_rect): # Modified
                if self.vel_y > 0:  # Player is moving down
                    self.rect.bottom = platform_rect.top # Adjust rect position
                    self.y = self.rect.y # Update y from rect
                    self.vel_y = 0
                    self.jumping = False
                elif self.vel_y < 0: # Player is moving up
                    self.rect.top = platform_rect.bottom # Adjust rect position
                    self.y = self.rect.y # Update y from rect
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
        # self.vel_x *= 0.9 # vel_x removed

        # Automatic Attack Logic
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.target_enemy and self.target_enemy.health > 0 and self.attack_cooldown <= 0:
            # Check distance to target enemy
            # Simple X distance check for now
            dist_to_enemy = abs(self.target_enemy.x - self.x)
            # Consider enemy width and player width for attack range
            attack_range = self.width + 10 # Player width + 10px reach
            
            # Check if player is facing the enemy (simplified)
            # Player is roughly at the enemy's x position or slightly past for attack_rect
            # This logic might need refinement based on attack_rect direction
            can_attack = False
            if self.target_enemy.rect.centerx > self.rect.centerx: # Enemy is to the right
                if dist_to_enemy < attack_range: # Simplified range check
                    can_attack = True
                    self.attack_rect = pygame.Rect(self.rect.right, self.rect.top, self.width, self.height) # Use self.rect
            else: # Enemy is to the left
                 if dist_to_enemy < attack_range: # Simplified range check
                    can_attack = True
                    self.attack_rect = pygame.Rect(self.rect.left - self.width, self.rect.top, self.width, self.height) # Use self.rect


            if can_attack:
                self.attack() # attack() method now only sets flags, actual rect created above
                self.attack_cooldown = 30 # Reset cooldown (e.g. 30 frames)


        if self.is_attacking:
            self.attack_duration_timer -= 1
            if self.attack_duration_timer <= 0:
                self.is_attacking = False
                self.attack_rect = None
        
        # Auto-use health potion if health is low
        if self.health > 0 and self.health / self.max_health < 0.3: # If health below 30%
            # Check for cooldown if we add one later for potion usage
            print(f"Player health low ({self.health}/{self.max_health}). Attempting to use HealthPotion.")
            self.use_item_by_type("HealthPotion") # Try to use a potion

    def draw(self, screen):
        screen.blit(self.image, self.rect) # Modified
        if self.is_attacking and self.attack_rect:
            pygame.draw.rect(screen, (0, 255, 0), self.attack_rect) # Green for attack hitbox
