"""
Body (Bloodstream)

Acts as the main hub and signal carrier for the system. The body routes data, events,
and signals between all other modules, ensuring that every part of Lyra Blackwall
is connected and synchronized.
"""

class Body:
    def __init__(self):
        """Initialize the body interface system."""
        # Registry of connected modules
        self.modules = {}
        
        # Event handlers: event_name -> list of callbacks
        self.event_handlers = {}
        
        print("[Body] Initialized")

    def register_module(self, name, module):
        """Register a module with the body system."""
        self.modules[name] = module
        print(f"[Body] Registered module: {name}")
        return True

    def route_signal(self, source, target, payload):
        """Route a signal from source to target module."""
        if target in self.modules:
            if hasattr(self.modules[target], "receive_signal"):
                self.modules[target].receive_signal(source, payload)
                return True
            else:
                print(f"[Body] Module {target} cannot receive signals")
                return False
        else:
            print(f"[Body] Unknown target module: {target}")
            return False

    def broadcast_signal(self, source, payload, exclude=None):
        """Broadcast a signal to all modules except excluded ones."""
        exclude = exclude or []
        success = True
        
        for name, module in self.modules.items():
            if name != source and name not in exclude:
                if hasattr(module, "receive_signal"):
                    module.receive_signal(source, payload)
                else:
                    success = False
        
        return success

    def register_handler(self, event_name, module_name, callback):
        """Register an event handler."""
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
        
        self.event_handlers[event_name].append((module_name, callback))
        print(f"[Body] Registered handler for event '{event_name}' from {module_name}")
        return True
        
    def emit_event(self, event_name, data=None):
        """Emit an event to all registered handlers."""
        if event_name not in self.event_handlers:
            # If no specific handlers, create empty list
            self.event_handlers[event_name] = []
            
        result = False
        for module_name, callback in self.event_handlers[event_name]:
            try:
                callback(data)
                result = True
            except Exception as e:
                print(f"[Body] Error in {module_name} handler for {event_name}: {e}")
        
        # Also broadcast the event to all modules that have handle_event method
        for name, module in self.modules.items():
            if hasattr(module, "handle_event"):
                try:
                    module.handle_event(event_name, data)
                    result = True
                except Exception as e:
                    print(f"[Body] Error in {name} general handler for {event_name}: {e}")
        
        return result

    def pulse(self, interval=1.0):
        """Send a heartbeat pulse to all modules."""
        self.emit_event("heartbeat", {"interval": interval})
        return True

    def speak(self, response, fragment_weights=None):
        """
        Output a response (typically via the mouth module).
        
        Args:
            response: The text response to output
            fragment_weights: Legacy param, maintained for backwards compatibility.
                              The personality system now handles personality traits.
        """
        if "mouth" in self.modules:
            if hasattr(self.modules["mouth"], "speak"):
                # Pass to mouth module which will use PersonalityCore if available
                self.modules["mouth"].speak(response, fragment_weights)
                return True
        
        # Fallback if no mouth module
        print(f"\n[System Output] {response}")
        return True

# For direct testing
if __name__ == "__main__":
    body = Body()
    body.register_handler("test", "test_module", lambda data: print(f"Received: {data}"))
    body.emit_event("test", "Hello World")
    body.speak("Testing the body interface system.")
