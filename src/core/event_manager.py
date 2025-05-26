# src/core/event_manager.py
from collections import defaultdict

class EventManager:
    def __init__(self):
        """ Initializes a new event manager. """
        self.listeners = defaultdict(list)
        print("EventManager initialized.")

    def subscribe(self, event_type, listener_callback):
        """ Subscribes a listener callback to an event type. """
        self.listeners[event_type].append(listener_callback)
        print(f"Listener {listener_callback.__name__} subscribed to {event_type}")

    def unsubscribe(self, event_type, listener_callback):
        """ Unsubscribes a listener callback from an event type. """
        if listener_callback in self.listeners[event_type]:
            self.listeners[event_type].remove(listener_callback)
            print(f"Listener {listener_callback.__name__} unsubscribed from {event_type}")
        else:
            print(f"Warning: Listener {listener_callback.__name__} not found for event {event_type}")

    def post(self, event_type, **data):
        """ Posts an event to all subscribed listeners. """
        print(f"Posting event: {event_type} with data: {data}")
        if event_type in self.listeners:
            for listener_callback in self.listeners[event_type]:
                listener_callback(**data) # Pass data as keyword arguments
        # else:
        #     print(f"No listeners for event: {event_type}")
