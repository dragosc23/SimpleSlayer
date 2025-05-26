# src/managers/input_manager.py
import pygame

class InputManager:
    def __init__(self):
        """ Initializes the Input Manager. """
        self.mouse_pos = (0, 0)
        self.mouse_buttons = {1: False, 2: False, 3: False} # Left, Middle, Right
        self.keys_pressed = pygame.key.get_pressed() # Current state of all keys

        # For 'just_pressed' or 'just_released' (more advanced, basic for now)
        self.prev_keys_pressed = self.keys_pressed
        self.prev_mouse_buttons = self.mouse_buttons.copy()
        
        print("InputManager initialized.")

    def process_events(self, events):
        """ Processes a list of Pygame events to update input states. """
        # Update previous states at the beginning of a new frame's event processing
        self.prev_keys_pressed = self.keys_pressed
        self.prev_mouse_buttons = self.mouse_buttons.copy()

        # Get current states directly (handles held down keys/buttons)
        self.keys_pressed = pygame.key.get_pressed()
        current_mouse_buttons_tuple = pygame.mouse.get_pressed() # Returns (left, middle, right)
        self.mouse_buttons = {
            1: current_mouse_buttons_tuple[0],
            2: current_mouse_buttons_tuple[1],
            3: current_mouse_buttons_tuple[2]
        }
        self.mouse_pos = pygame.mouse.get_pos()

        # Specific event iteration (for key down/up, mouse down/up for 'just pressed/released')
        # This part is needed if we want reliable 'just_pressed' beyond what pygame.key.get_pressed() offers
        # For now, the direct state polling above is simpler for 'is_key_pressed' and 'is_mouse_button_pressed'

    def is_key_held(self, key_code):
        """ Checks if a key is currently held down. """
        return self.keys_pressed[key_code]

    def is_key_just_pressed(self, key_code):
        """ Checks if a key was pressed in this frame/event batch. """
        # True if currently pressed AND was not pressed in the previous frame
        return self.keys_pressed[key_code] and not self.prev_keys_pressed[key_code]

    def get_mouse_pos(self):
        """ Returns the current mouse position. """
        return self.mouse_pos

    def is_mouse_button_held(self, button_index): # 1 for left, 2 for middle, 3 for right
        """ Checks if a mouse button is currently held down. """
        return self.mouse_buttons.get(button_index, False)

    def is_mouse_button_just_pressed(self, button_index):
        """ Checks if a mouse button was pressed in this frame/event batch. """
        return self.mouse_buttons.get(button_index, False) and \
               not self.prev_mouse_buttons.get(button_index, False)

# Example usage (conceptual, not part of this file):
# input_manager = InputManager()
# running = True
# while running:
#     events = pygame.event.get()
#     input_manager.process_events(events) # Call this once per game loop
#     for event in events: # Still need to iterate for QUIT etc.
#         if event.type == pygame.QUIT:
#             running = False
# 
#     if input_manager.is_key_just_pressed(pygame.K_SPACE):
#         print("Space just pressed!")
#     if input_manager.is_mouse_button_held(1):
#         print(f"Left mouse held at {input_manager.get_mouse_pos()}")
#     pygame.display.flip()
