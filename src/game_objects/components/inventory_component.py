# src/game_objects/components/inventory_component.py
from src.game_objects.item_definitions import Weapon, HealthPotion, Consumable # Updated imports

class Inventory:
    def __init__(self, capacity=10):
        self.items = []
        self.capacity = capacity
        self.item_type_map = {
            "Weapon": Weapon, # Uncommented
            "HealthPotion": HealthPotion, # Uncommented
            "Consumable": Consumable # Uncommented
        }

    def add_item(self, item):
        if len(self.items) < self.capacity:
            self.items.append(item)
            print(f"Added {item.name if hasattr(item, 'name') else 'item'} to inventory.")
            return True
        else:
            print(f"Inventory is full. Cannot add {item.name if hasattr(item, 'name') else 'item'}.")
            return False

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"Removed {item.name if hasattr(item, 'name') else 'item'} from inventory.")
            return True
        else:
            print(f"Item {item.name if hasattr(item, 'name') else 'item'} not found in inventory.")
            return False

    def get_items_by_type(self, item_type_name):
        """ Returns a list of items of a specific type_name (e.g., "Weapon"). """
        target_class = self.item_type_map.get(item_type_name)
        if not target_class:
            print(f"Unknown item type: {item_type_name}")
            return []
        
        return [item for item in self.items if isinstance(item, target_class)]

    def __str__(self):
        return f"Inventory ({len(self.items)}/{self.capacity})"
