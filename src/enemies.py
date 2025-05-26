import pygame
from src.items import Weapon, RARITY_COMMON, RARITY_UNCOMMON, RARITY_RARE # Import rarities
from src.consumables import HealthPotion
import random

class Enemy:
    def __init__(self, x, y, width=32, height=48, health=50, xp_value=25):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.max_health = health
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (0, 0, 255)  # Blue color for the enemy
        self.loot_table = [
            (Weapon, "Iron Sword", 5),
            (Weapon, "Steel Axe", 7),
            (HealthPotion, "Minor Health Potion", 25),
            (HealthPotion, "Lesser Health Potion", 50),
            (Weapon, "Short Bow", 6)
        ] # Redefined
        self.xp_value = xp_value

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

    def drop_loot(self):
        if not self.loot_table:
            return None

        # 1. Choose an item template from the loot table
        item_template = random.choice(self.loot_table)
        item_class, item_name, base_stat = item_template

        # 2. Determine rarity randomly
        rand_val = random.random() # Value between 0.0 and 1.0
        chosen_rarity = RARITY_COMMON # Default
        if rand_val < 0.05: # 5% chance for Rare
            chosen_rarity = RARITY_RARE
        elif rand_val < 0.30: # 25% chance for Uncommon (0.05 + 0.25 = 0.30)
            chosen_rarity = RARITY_UNCOMMON
        # Else it's Common (remaining 70%)

        # 3. Instantiate the item with the chosen rarity and base stats
        dropped_item = None
        if item_class == Weapon:
            dropped_item = Weapon(name=item_name, base_attack_bonus=base_stat, rarity=chosen_rarity)
        elif item_class == HealthPotion:
            dropped_item = HealthPotion(name=item_name, base_heal_amount=base_stat, rarity=chosen_rarity)
        
        if dropped_item:
            print(f"Enemy dropped: {dropped_item}") # Uses __str__ which includes rarity
            return dropped_item
        return None
