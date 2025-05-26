# src/systems/experience_system.py

def get_xp_for_level(level):
    """Calculates XP needed to reach the next level from the current one."""
    # Example: Level 1 needs 100 to get to L2, L2 needs 200 to get to L3, etc.
    return level * 100

def grant_experience(player, points):
    """Grants experience points to the player."""
    if player.level >= 50: # Example max level
        player.current_xp = 0 
        return False # No more XP gain at max level

    player.current_xp += points
    print(f"Player gained {points} XP, total current XP: {player.current_xp}")
    return True # XP granted

def check_level_up(player):
    """Checks if the player has enough XP to level up and handles the level up process."""
    leveled_up = False
    while player.current_xp >= player.xp_to_next_level and player.level < 50:
        leveled_up = True
        player.level += 1
        excess_xp = player.current_xp - player.xp_to_next_level
        player.current_xp = excess_xp
        player.xp_to_next_level = get_xp_for_level(player.level)
        
        # Apply stat increases
        player.base_attack_power += 2
        player.max_health += 10
        player.health = player.max_health # Heal on level up

        print(f"Player leveled up to Level {player.level}!")
        print(f"New Stats - Base Atk: {player.base_attack_power}, Max Health: {player.max_health}")
        print(f"XP for next level ({player.level+1}): {player.xp_to_next_level}, Current XP: {player.current_xp}")

    if player.level >= 50: # Ensure XP doesn't exceed cap if max level hit
        player.current_xp = 0
        player.xp_to_next_level = 0


    return leveled_up
