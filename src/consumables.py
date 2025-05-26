# src/consumables.py
from src.items import RARITY_COMMON, RARITY_UNCOMMON, RARITY_RARE, RARITY_MULTIPLIERS # Added import

class Consumable:
    def __init__(self, name, item_type="Consumable"): # Rarity could be added here too if needed for general consumables
        self.name = name
        self.item_type = item_type

    def __str__(self):
        return self.name # Base consumables might not show rarity unless specified

    def use(self, player):
        """ Base use method, to be overridden by specific consumables. """
        print(f"Using {self.name} on {player.name if hasattr(player, 'name') else 'player'}.")
        pass

class HealthPotion(Consumable):
    def __init__(self, name, base_heal_amount, rarity=RARITY_COMMON): # Modified
        super().__init__(name, item_type="HealthPotion")
        self.rarity = rarity # Added

        self.base_heal_amount = base_heal_amount # Added
        multiplier = RARITY_MULTIPLIERS.get(rarity, 1.0)
        self.heal_amount = int(round(base_heal_amount * multiplier)) # Modified

    def __str__(self):
        return f"[{self.rarity}] {self.name}" # Modified

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
