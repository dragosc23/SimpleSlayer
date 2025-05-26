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
*   **Basic Image Asset Loading (`src/core/asset_loader.py`):** Implemented a system for loading images with caching and error handling (provides a visual placeholder if an image file is missing). Player character now uses this system to display an image (currently a placeholder).
*   **Enemy Graphics (Placeholder via Asset Loader):** Enemies now use the image asset loading system, displaying a placeholder image.
*   **Basic Game State Machine (`src/core/game_state_machine.py`):** Implemented a state machine to manage different game phases (e.g., Menu, Playing, Game Over). The main game loop now operates based on this state machine.
*   **Functional Menu & Game Over States:** Menu state now has working "Play" and "Exit" buttons. Game Over state has a "Restart" button (returns to menu).
*   **Basic Custom Event Manager (`src/core/event_manager.py`):** Implemented an event manager for custom game events (e.g., `EVENT_PLAYER_DIED`). Player death is now handled through this event system.

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

## Project Structure

The project is organized into the following main directories:

*   **`assets/`**: Contains all game assets like images, sounds, and fonts.
    *   `images/`: Sprites, backgrounds, UI elements.
    *   `sounds/`: Sound effects and music.
    *   `fonts/`: Custom game fonts.
*   **`data/`**: Stores game data files, such as level definitions, item configurations, and quest information.
*   **`src/`**: Contains the Python source code for the game, further divided into:
    *   `core/`: Core engine components (asset loading, state management, event handling).
    *   `game_objects/`: Classes for player, enemies, NPCs, projectiles, etc.
    *   `managers/`: High-level managers for game flow, levels, quests, saving/loading, audio, input.
    *   `systems/`: Specific game systems like AI, physics, animation.
    *   `ui/`: UI elements, screens, and HUD components. (Note: Existing `ui.py` will be refactored into this module).
    *   `utils/`: Utility functions, constants, logging, settings.
    *   *(Existing files like `player.py`, `game.py`, etc., are currently in `src/` and will be refactored into the new structure over time).*
*   **`tests/`**: Houses unit and integration tests.
*   **`docs/`**: For design documents, concept art, and other documentation.
*   **`main.py`**: The main entry point to run the game.
```
