# SimpleSlayer (Auto-Battler RPG)

SimpleSlayer is an auto-battler RPG where the player character automatically fights through waves of enemies, collects loot, and progresses through levels. The focus is on strategic equipment choices and character development rather than direct control.

## Current Features

*   **Automated Combat:** Player automatically targets and attacks nearby enemies.
*   **Wave System:** Enemies spawn in predefined waves. Clearing a wave triggers the next one.
*   **Basic Equipment:** Player can equip weapons that increase their attack power.
*   **Loot Drops:** Enemies have a chance to drop better weapons and health potions. Item rarity is randomized on drop.
*   **Basic UI:** Displays player health, wave progress, attack statistics, level, XP, inventory preview (including potion count and item rarity colors).
*   **Level Progression (Wave-based):** Simple progression by clearing all waves in a level.
*   **Player Leveling System:** Player gains experience from defeating enemies and levels up, increasing base stats (attack power and health).
*   **Basic Inventory System:** Player can now store a limited number of items (weapons, potions) in an inventory.
*   **Health Potions & Consumables:** Player can collect Health Potions. Potions are automatically used if player's health drops below 30%. UI shows potion count.
*   **Item Rarity System:** Items (weapons and potions) can now have different rarities (Common, Uncommon, Rare). Rarity affects item stats (attack bonus for weapons, heal amount for potions) through multipliers. Item names in the UI are color-coded by rarity.

## How to Run

1.  Ensure you have Python and Pygame installed.
    *   You can install Pygame with: `pip install pygame`
2.  Clone this repository (or download the source code).
3.  Navigate to the root directory of the project in your terminal.
4.  Run the game using: `python src/main.py`

The game is largely automated. The player character will move and fight on its own. Manual jump (`SPACE` key) is still available but not essential for core progression.

## Future Development Ideas (Post-Phase 1)

*   More equipment types (armor, accessories).
*   Loot rarity and varied item stats.
*   Player skill trees and leveling system.
*   Different character classes and subclasses.
*   Questing system.
*   More diverse enemy types and abilities.
*   Advanced AI for player and enemies.
*   Persistent player save/load.
```
