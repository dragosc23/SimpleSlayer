# Rarity definitions
RARITY_COMMON = "Common"
RARITY_UNCOMMON = "Uncommon"
RARITY_RARE = "Rare"

RARITY_MULTIPLIERS = {
    RARITY_COMMON: 1.0,
    RARITY_UNCOMMON: 1.2,
    RARITY_RARE: 1.5
}

class Weapon:
    def __init__(self, name, base_attack_bonus, rarity=RARITY_COMMON, item_type="Weapon"): # Modified
        self.name = name
        self.rarity = rarity # Store rarity
        self.item_type = item_type

        self.base_attack_bonus = base_attack_bonus # Store base for reference
        multiplier = RARITY_MULTIPLIERS.get(rarity, 1.0)
        self.attack_bonus = int(round(base_attack_bonus * multiplier))


    def __str__(self):
        return f"[{self.rarity}] {self.name} (+{self.attack_bonus} Atk)" # Modified
