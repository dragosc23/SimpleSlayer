# src/core/game_state_machine.py
import pygame
from src.utils.constants import WHITE, BLACK, SCREEN_WIDTH, SCREEN_HEIGHT, EVENT_PLAYER_DIED, STATE_PLAYING, STATE_MENU, STATE_GAME_OVER, EVENT_ALL_WAVES_CLEARED, STATE_LEVEL_COMPLETE # Modified import

class GameState:
    """ Base class for individual game states. """
    def __init__(self):
        self.font = pygame.font.SysFont('arial', 50) # Example font for placeholder text

    def enter(self, **kwargs):
        """ Called when entering this state. """
        print(f"Entering {self.__class__.__name__}")
        pass

    def exit(self):
        """ Called when exiting this state. """
        print(f"Exiting {self.__class__.__name__}")
        pass

    def handle_events(self, events, game_state_machine):
        """ Handle events for this state. Can trigger state changes. """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: # Example global keybind
                    print("Escape key pressed, could quit or go to menu.")
        pass

    def update(self, dt, game_state_machine):
        """ Update logic for this state. Can trigger state changes. """
        pass

    def draw(self, screen):
        """ Draw this state to the screen. """
        screen.fill(BLACK) # Default black background
        text_surface = self.font.render(self.__class__.__name__, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text_surface, text_rect)

class GameStateMachine:
    """ Manages a collection of game states and transitions between them. """
    def __init__(self):
        self.states = {}  # Stores state_name: state_object
        self.current_state_obj = None
        self.current_state_name = None

    def add_state(self, state_name, state_object):
        """ Adds a state to the machine. """
        self.states[state_name] = state_object

    def change_state(self, new_state_name, **kwargs):
        """ Changes the active game state. """
        if self.current_state_obj:
            self.current_state_obj.exit()
        
        if new_state_name in self.states:
            self.current_state_name = new_state_name
            self.current_state_obj = self.states[new_state_name]
            self.current_state_obj.enter(**kwargs)
            print(f"Changed state to {new_state_name}")
        else:
            print(f"Error: State '{new_state_name}' not found in state machine.")
            self.current_state_obj = None # Or handle error appropriately
            self.current_state_name = None


    def handle_events(self, events):
        if self.current_state_obj:
            self.current_state_obj.handle_events(events, self) # Pass machine for state changes
        # else: print("No current state to handle events")

    def update(self, dt):
        if self.current_state_obj:
            self.current_state_obj.update(dt, self) # Pass machine for state changes
        # else: print("No current state to update")

    def draw(self, screen):
        if self.current_state_obj:
            self.current_state_obj.draw(screen)
        else:
            # Default draw if no state (e.g., error or initial setup)
            screen.fill((50, 50, 50)) # Dark gray
            font = pygame.font.SysFont('arial', 30)
            text_surface = font.render("No active state", True, WHITE)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            screen.blit(text_surface, text_rect)

# --- Placeholder States (can be expanded or moved to separate files later) ---

class MenuState(GameState):
    def __init__(self):
        super().__init__()
        self.play_button_rect = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 - 25, 200, 50)
        self.exit_button_rect = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 50, 200, 50) # Added Exit button
        self.button_font = pygame.font.SysFont('arial', 30) # Added button font

    def draw(self, screen):
        super().draw(screen) # Draws state name "MenuState"
        
        # Play Button
        pygame.draw.rect(screen, (0,150,0), self.play_button_rect) # Green button
        play_text_surface = self.button_font.render("Play", True, WHITE)
        play_text_rect = play_text_surface.get_rect(center=self.play_button_rect.center)
        screen.blit(play_text_surface, play_text_rect)

        # Exit Button
        pygame.draw.rect(screen, (150, 0, 0), self.exit_button_rect) # Red button for Exit
        exit_text_surface = self.button_font.render("Exit", True, WHITE)
        exit_text_rect = exit_text_surface.get_rect(center=self.exit_button_rect.center)
        screen.blit(exit_text_surface, exit_text_rect)
    
    def handle_events(self, events, game_state_machine):
        super().handle_events(events, game_state_machine)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button
                    if self.play_button_rect.collidepoint(event.pos):
                        game_state_machine.change_state(STATE_PLAYING) # Used constant
                    elif self.exit_button_rect.collidepoint(event.pos): 
                        print("Exit button clicked. Posting QUIT event.")
                        pygame.event.post(pygame.event.Event(pygame.QUIT))
            if event.type == pygame.KEYDOWN: # For quick testing
                if event.key == pygame.K_p:
                    game_state_machine.change_state(STATE_PLAYING) # Used constant


class PlayingState(GameState): # This will eventually hold the main game logic
    def __init__(self, game_manager_ref): # To call game_manager's methods
        super().__init__()
        self.game_manager = game_manager_ref # Reference to the main game logic controller
    
    def enter(self, **kwargs):
        super().enter(**kwargs)
        # Example: Reset level or player if needed when entering playing state
        # self.game_manager.reset_level() 
        print("Entered PlayingState. Game logic should run now.")

    def handle_events(self, events, game_state_machine):
        super().handle_events(events, game_state_machine)
        # Delegate to game_manager's event handling for actual game input
        self.game_manager.handle_event_in_playing_state(events) # New method in game_manager
        # Player death is now handled by posting an event in update, not directly changing state here.


    def update(self, dt, game_state_machine):
        super().update(dt, game_state_machine)
        # Delegate to game_manager's update for actual game logic
        self.game_manager.update_in_playing_state(dt) # New method in game_manager
        
        # Check for player death
        if self.game_manager.player.health <= 0:
            print("PlayingState: Player health <= 0. Posting PLAYER_DIED_EVENT.")
            self.game_manager.event_manager.post(EVENT_PLAYER_DIED)
            # The GameManager will now handle the state change via its subscribed event handler.
            # No direct state change here anymore for this condition.
            return # Return early to prevent further updates in this state if player is dead
            
        if self.game_manager.game_state == STATE_LEVEL_COMPLETE: # This state is set in game_manager.update_in_playing_state
            print("PlayingState: All waves cleared. Posting EVENT_ALL_WAVES_CLEARED.")
            self.game_manager.event_manager.post(EVENT_ALL_WAVES_CLEARED)
            # Remove direct state change: game_state_machine.change_state(STATE_MENU)
            # The GameManager will now handle the state change via its subscribed event handler.
            return # Important to exit update after posting this event


    def draw(self, screen):
        # Delegate to game_manager's draw for actual game rendering
        self.game_manager.draw_playing_state(screen) # New method in game_manager

class GameOverState(GameState):
    def __init__(self):
        super().__init__()
        # Remove self.timer and self.duration
        self.restart_button_rect = pygame.Rect(SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2 + 25, 200, 50)
        self.button_font = pygame.font.SysFont('arial', 30)
        self.game_over_font = pygame.font.SysFont('arial', 72)
        self.game_over_text_surface = self.game_over_font.render("Game Over", True, (200,0,0)) # Dark Red
        self.game_over_text_rect = self.game_over_text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))

    def enter(self, **kwargs):
        super().enter(**kwargs)
        # self.timer related lines removed

    def update(self, dt, game_state_machine):
        super().update(dt, game_state_machine)
        # Timed transition logic removed
        pass

    def draw(self, screen):
        screen.fill(BLACK) # Specific Game Over background color
        screen.blit(self.game_over_text_surface, self.game_over_text_rect)
        
        pygame.draw.rect(screen, (0, 100, 0), self.restart_button_rect) # Dark Green button
        restart_text_surface = self.button_font.render("Restart", True, WHITE)
        restart_text_rect = restart_text_surface.get_rect(center=self.restart_button_rect.center)
        screen.blit(restart_text_surface, restart_text_rect)

    def handle_events(self, events, game_state_machine):
        super().handle_events(events, game_state_machine)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button
                    if self.restart_button_rect.collidepoint(event.pos):
                        print("Restart button clicked. Changing state to MENU.")
                        game_state_machine.change_state(STATE_MENU) # Used constant
            elif event.type == pygame.KEYDOWN: # For quick testing
                if event.key == pygame.K_r:
                    print("R key pressed. Changing state to MENU.")
                    game_state_machine.change_state(STATE_MENU) # Used constant

class VictoryState(GameState):
    def __init__(self):
        super().__init__()
        self.victory_font = pygame.font.SysFont('arial', 72) # Large font for "Victory!"
        self.victory_text_surface = self.victory_font.render("Level Cleared!", True, (0, 200, 0)) # Green text
        self.victory_text_rect = self.victory_text_surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 100))

        self.button_font = pygame.font.SysFont('arial', 30)
        self.main_menu_button_rect = pygame.Rect(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 + 50, 300, 50)
        # Optional: Next Level button placeholder
        # self.next_level_button_rect = pygame.Rect(SCREEN_WIDTH/2 - 150, SCREEN_HEIGHT/2 + 120, 300, 50)

    def draw(self, screen):
        screen.fill(BLACK) # Or a specific victory background color
        screen.blit(self.victory_text_surface, self.victory_text_rect)

        # Draw Main Menu button
        pygame.draw.rect(screen, (0, 100, 150), self.main_menu_button_rect) # Blueish button
        menu_text_surface = self.button_font.render("Main Menu", True, WHITE)
        menu_text_rect = menu_text_surface.get_rect(center=self.main_menu_button_rect.center)
        screen.blit(menu_text_surface, menu_text_rect)

        # Optional: Draw Next Level button placeholder
        # pygame.draw.rect(screen, (50, 50, 50), self.next_level_button_rect) # Disabled look
        # next_level_text_surface = self.button_font.render("Next Level (Coming Soon!)", True, (150,150,150))
        # next_level_text_rect = next_level_text_surface.get_rect(center=self.next_level_button_rect.center)
        # screen.blit(next_level_text_surface, next_level_text_rect)

    def handle_events(self, events, game_state_machine):
        super().handle_events(events, game_state_machine) # For ESC key etc.
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left mouse button
                    if self.main_menu_button_rect.collidepoint(event.pos):
                        print("VictoryState: Main Menu button clicked.")
                        game_state_machine.change_state(STATE_MENU) 
                    # Optional: Handle Next Level button click
                    # if self.next_level_button_rect.collidepoint(event.pos):
                    #     print("VictoryState: Next Level button clicked (Not implemented).")
                    #     # game_state_machine.change_state(STATE_PLAYING, level="next_level_data") # Example
            elif event.type == pygame.KEYDOWN: # For quick testing
                if event.key == pygame.K_m:
                     print("VictoryState: M key pressed. Changing to MENU.")
                     game_state_machine.change_state(STATE_MENU)


    def enter(self, **kwargs):
        super().enter(**kwargs)
        # Any specific logic when victory state is entered, e.g., play victory music
        print("Victory achieved!")

    # update method can be pass or inherited from GameState if no specific update logic
