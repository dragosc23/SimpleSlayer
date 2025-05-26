# src/game_objects/item_definitions.py
from src.utils.constants import RARITY_COMMON, RARITY_UNCOMMON, RARITY_RARE, RARITY_MULTIPLIERS

class Weapon:
    def __init__(self, name, base_attack_bonus, rarity=RARITY_COMMON, item_type="Weapon"):
        self.name = name
        self.rarity = rarity
        self.item_type = item_type

        self.base_attack_bonus = base_attack_bonus
        multiplier = RARITY_MULTIPLIERS.get(rarity, 1.0) # Uses imported RARITY_MULTIPLIERS
        self.attack_bonus = int(round(base_attack_bonus * multiplier))

    def __str__(self):
        return f"[{self.rarity}] {self.name} (+{self.attack_bonus} Atk)"

class Consumable:
    def __init__(self, name, item_type="Consumable"):
        self.name = name
        self.item_type = item_type

    def __str__(self):
        return self.name

    def use(self, player):
        """ Base use method, to be overridden by specific consumables. """
        print(f"Using {self.name} on {player.name if hasattr(player, 'name') else 'player'}.")
        pass

class HealthPotion(Consumable):
    def __init__(self, name, base_heal_amount, rarity=RARITY_COMMON):
        super().__init__(name, item_type="HealthPotion")
        self.rarity = rarity

        self.base_heal_amount = base_heal_amount
        multiplier = RARITY_MULTIPLIERS.get(rarity, 1.0) # Uses imported RARITY_MULTIPLIERS
        self.heal_amount = int(round(base_heal_amount * multiplier))

    def __str__(self):
        return f"[{self.rarity}] {self.name}"

    def use(self, player):
        """ Heals the player. """
        if player.health < player.max_health:
            old_health = player.health
            player.health += self.heal_amount
            if player.health > player.max_health:
                player.health = player.max_health
            healed_for = player.health - old_health
            # Use self.__str__() to include rarity in the message
            print(f"{player.name if hasattr(player, 'name') else 'Player'} used {self.__str__()}, healed for {healed_for}. Current health: {player.health}/{player.max_health}")
            return True
        else:
            print(f"{player.name if hasattr(player, 'name') else 'Player'} health is full. Cannot use {self.__str__()}.")
            return False
