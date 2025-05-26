# src/managers/save_manager.py
import json
import os

DEFAULT_SAVE_FILENAME = "savegame.json"
SAVE_DIR = "data/saves" # Store saves in a subfolder of data/

def ensure_save_directory_exists():
    """ Ensures the save directory exists, creating it if necessary. """
    if not os.path.exists(SAVE_DIR):
        try:
            os.makedirs(SAVE_DIR)
            print(f"Created save directory: {SAVE_DIR}")
        except OSError as e:
            print(f"Error creating save directory {SAVE_DIR}: {e}")
            return False
    return True

def get_save_filepath(filename=DEFAULT_SAVE_FILENAME):
    """ Returns the full path to the save file. """
    return os.path.join(SAVE_DIR, filename)

def save_player_progress(player_data, filename=DEFAULT_SAVE_FILENAME):
    """
    Saves player progress data to a JSON file.
    player_data: A dictionary containing data to save (e.g., {'level': 1, 'xp': 0}).
    filename: Name of the save file.
    """
    if not ensure_save_directory_exists():
        print("Could not ensure save directory exists. Save aborted.")
        return False

    filepath = get_save_filepath(filename)
    try:
        with open(filepath, 'w') as f:
            json.dump(player_data, f, indent=4)
        print(f"Player progress saved to {filepath}")
        return True
    except IOError as e:
        print(f"Error saving player progress to {filepath}: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during save: {e}")
        return False


def load_player_progress(filename=DEFAULT_SAVE_FILENAME):
    """
    Loads player progress data from a JSON file.
    filename: Name of the save file.
    Returns the loaded data as a dictionary, or None if an error occurs or file not found.
    """
    filepath = get_save_filepath(filename)
    if not os.path.exists(filepath):
        print(f"Save file {filepath} not found. Starting new game.")
        return None
    
    try:
        with open(filepath, 'r') as f:
            player_data = json.load(f)
        print(f"Player progress loaded from {filepath}: {player_data}")
        return player_data
    except IOError as e:
        print(f"Error loading player progress from {filepath}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {filepath}: {e}. Save file might be corrupted.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during load: {e}")
        return None

# Example Usage (conceptual)
# if __name__ == '__main__':
#     # Test save
#     sample_data = {'level': 5, 'xp': 1250, 'name': 'TestPlayer'}
#     save_player_progress(sample_data)
#
#     # Test load
#     loaded_data = load_player_progress()
#     if loaded_data:
#         print(f"Loaded Level: {loaded_data.get('level')}")
#         print(f"Loaded XP: {loaded_data.get('xp')}")
#
#     # Test loading non-existent file
#     # loaded_data_new = load_player_progress("new_save.json")
#     # print(loaded_data_new)
