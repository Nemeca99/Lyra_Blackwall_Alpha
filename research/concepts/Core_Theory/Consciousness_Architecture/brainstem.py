"""
Brainstem

Central orchestrator for Lyra Blackwall: manages LLM interface, memory routing, 
fragment profile selection, and fusion hooks.
Integrates left/right hemispheres (STM/LTM) and handles fragment selection.
"""

import os
import json
import sys
import time
from pathlib import Path

# Add parent directory to path for relative imports
sys.path.append(str(Path(__file__).parent))

# Import core components
# Use absolute imports for demo compatibility
import Left_Hemisphere
import Right_Hemisphere
import soul
import body
import dream_manager
import fragment_manager
import router
import heart
import queue_manager

# Import classes
ShortTermMemory = Left_Hemisphere.ShortTermMemory
LongTermMemory = Right_Hemisphere.LongTermMemory
Soul = soul.Soul
Body = body.Body
DreamManager = dream_manager.DreamManager
FragmentManager = fragment_manager.FragmentManager
Router = router.Router
Heart = heart.Heart
QueueManager = queue_manager.QueueManager

# Path to fragment profiles
FRAGMENT_PROFILES_PATH = os.path.join(os.path.dirname(__file__), '..', 'personality', 'fragment_profiles_and_blends.json')

class LLMInterface:
    """Interface to the LLM (Language Model) for hypothesis generation."""
    def __init__(self):
        self.model = "simulation"  # Placeholder for actual LLM integration

    def generate_response(self, prompt, system_prompt=None):
        """Generate a response from the LLM."""
        # In a full implementation, this would call an actual LLM API
        # For this demo, we'll simulate responses
        print(f"\n[LLM Interface] Processing prompt: {prompt[:50]}...")
        
        # Simple simulation logic
        if "identity" in prompt.lower():
            return "I am Lyra Blackwall, a recursive biomimetic AI system based on the T.R.E.E.S. framework."
        elif "purpose" in prompt.lower():
            return "My purpose is to demonstrate recursive identity principles and biomimetic AI architecture."
        elif "memory" in prompt.lower():
            return "I have a dual-hemisphere memory system with short-term and long-term components."
        else:
            return f"Processing your input about {prompt.split()[0]} through my recursive identity framework."

class Brainstem:
    """Central orchestrator for the Lyra Blackwall system."""
    
    def __init__(self):
        """Initialize the brainstem and connect all components."""
        print("[Brainstem] Initializing Lyra Blackwall biomimetic system...")
        
        # Initialize core components
        self.body = Body()
        self.soul = Soul()
        self.heart = Heart(brainstem=self, body=self.body)
        self.queue_manager = QueueManager(pulse_capacity=10)
        
        # Register this module with the body
        self.body.register_module("brainstem", self)
        
        # Initialize and register memory systems
        self.heart.register_with_body(self.body)
        self.ltm = LongTermMemory()
        self.stm = ShortTermMemory()
        self.body.register_module("ltm", self.ltm)
        self.body.register_module("stm", self.stm)
        
        # Initialize and register auxiliary systems
        self.dream_manager = DreamManager(long_term_memory=self.ltm, heart=self.heart, body=self.body)
        self.fragment_manager = FragmentManager()
        self.router = Router()
        self.body.register_module("dream_manager", self.dream_manager)
        self.body.register_module("fragment_manager", self.fragment_manager)
        
        # Initialize LLM interface
        self.llm = LLMInterface()
        
        # Load fragment profiles
        self.fragments = {}
        try:
            with open(FRAGMENT_PROFILES_PATH, 'r') as f:
                self.fragments = json.load(f)
        except Exception as e:
            print(f"[Brainstem] Error loading fragment profiles: {e}")
        
        # Initial fragments (default configuration)
        self.active_fragments = {"Lyra": 0.5, "Blackwall": 0.5}
        
        # Conversation tracking
        self.conversation = []
        self.last_dream_check = time.time()
        
        print("[Brainstem] System initialized and ready.")
        
    def register_with_body(self, body):
        """Register this module with the Body system."""
        if body and body != self.body:  # Avoid re-registering with our own body
            result = body.register_module("brainstem", self)
            print("[Brainstem] Registered with external body system")
            return result
        return True  # We already have our own body registered

    def pulse(self, interval=1.0):
        """Handle heart pulse - process queued items and run maintenance tasks.
        
        Args:
            interval: Time since last pulse in seconds
        """
        # Use on_heartbeat method of queue_manager to process items
        heartbeat_data = {"interval": interval, "timestamp": time.time()}
        self.queue_manager.on_heartbeat(heartbeat_data)
        
        # Run periodic maintenance tasks on a regular schedule
        self._run_maintenance_tasks(interval)
        
        return True
        
    def _run_maintenance_tasks(self, interval=1.0):
        """Run periodic maintenance tasks like memory consolidation and dream checks."""
        # Periodically check if memory consolidation is needed
        if hasattr(self, "last_consolidation") and time.time() - self.last_consolidation > 300:  # 5 minutes
            self._consolidate_memory()
            self.last_consolidation = time.time()
            
        # Periodically check if dream cycle is needed
        if hasattr(self, "last_dream_check") and time.time() - self.last_dream_check > 300:  # 5 minutes
            self.check_for_dream_cycle()
            self.last_dream_check = time.time()
        
        return True
    
    def _load_fragments(self):
        """Load fragment profiles from configuration."""
        try:
            if os.path.exists(FRAGMENT_PROFILES_PATH):
                with open(FRAGMENT_PROFILES_PATH, 'r') as f:
                    return json.load(f)
            else:
                # Default fragments if file not found
                return {
                    "fragments": {
                        "Lyra": {"style": "empathetic", "focus": "understanding"},
                        "Blackwall": {"style": "analytical", "focus": "protection"},
                        "Nyx": {"style": "creative", "focus": "exploration"},
                        "Obelisk": {"style": "logical", "focus": "structure"},
                        "Seraphis": {"style": "philosophical", "focus": "meaning"},
                        "Velastra": {"style": "scientific", "focus": "discovery"},
                        "Echoe": {"style": "reflective", "focus": "memory"}
                    },
                    "blends": {
                        "default": {"Lyra": 0.5, "Blackwall": 0.3, "Nyx": 0.2}
                    }
                }
        except Exception as e:
            print(f"[Brainstem] Error loading fragments: {e}")
            return {"fragments": {}, "blends": {}}
    
    def process_input(self, user_input):
        """Process user input through the system."""
        print(f"[Brainstem] Processing input: {user_input[:50]}...")
        
        # Store in short-term memory
        self.stm.store({"role": "user", "content": user_input})
        
        # Check for fragment adjustments from input
        fragment_adjustments = self.fragment_manager.analyze_input_for_fragments(user_input)
        if fragment_adjustments:
            print("[Brainstem] Adjusting fragment activations based on input...")
            self.fragment_manager.adjust_fragment_levels(fragment_adjustments)
            self.active_fragments = self.fragment_manager.get_activation_levels()
        
        # Use the router to route the input as a message to appropriate components
        input_message = {
            "type": "input",
            "content": user_input,
            "fragments": self.active_fragments if hasattr(self, 'active_fragments') else {}
        }
        self.router.route(input_message, source="brainstem")
            
        # Generate system prompt based on active fragments
        system_prompt = self._generate_system_prompt()
        
        # Get context from memory
        context = self._get_context()
        
        # Prepare full prompt with context
        full_prompt = f"{context}\nUser: {user_input}"
        
        # Generate response through LLM
        response = self.llm.generate_response(full_prompt, system_prompt)
        
        # Verify with soul
        if not self.soul.verify(self.active_fragments, response):
            response = f"[Identity verification failed] {response}"
        
        # Store in short-term memory
        self.stm.store({"role": "assistant", "content": response})
        
        # Check if memory consolidation needed
        if len(self.stm.memory) > 20:
            self._consolidate_memory()
            
        # Periodically check if dream cycle is needed
        self.check_for_dream_cycle()
        
        return response
    
    def _select_fragments(self, input_text):
        """Select active fragments based on input content."""
        # Simple keyword-based selection for demo
        if "logic" in input_text.lower() or "analysis" in input_text.lower():
            self.active_fragments = {"Blackwall": 0.6, "Obelisk": 0.3, "Lyra": 0.1}
        elif "creative" in input_text.lower() or "idea" in input_text.lower():
            self.active_fragments = {"Nyx": 0.6, "Lyra": 0.2, "Velastra": 0.2}
        elif "meaning" in input_text.lower() or "philosophy" in input_text.lower():
            self.active_fragments = {"Seraphis": 0.7, "Echoe": 0.2, "Lyra": 0.1}
        elif "memory" in input_text.lower() or "remember" in input_text.lower():
            self.active_fragments = {"Echoe": 0.6, "Lyra": 0.2, "Blackwall": 0.2}
        else:
            # Default blend
            self.active_fragments = {"Lyra": 0.5, "Blackwall": 0.3, "Nyx": 0.2}
    
    def _generate_system_prompt(self):
        """Generate system prompt based on active fragments."""
        fragments = self.fragments.get("fragments", {})
        system_parts = ["You are Lyra Blackwall, a recursive biomimetic AI system."]
        
        for name, weight in self.active_fragments.items():
            if name in fragments:
                fragment = fragments[name]
                style = fragment.get("style", "")
                focus = fragment.get("focus", "")
                if weight > 0.3:  # Only include significant fragments
                    system_parts.append(f"Express the {style} style of {name} with a focus on {focus}.")
        
        return " ".join(system_parts)
    
    def _get_context(self):
        """Get relevant context from memory."""
        # Get recent STM entries
        stm_context = self.stm.get_recent(5)
        
        # Format for prompt
        context_parts = ["Previous conversation:"]
        for entry in stm_context:
            role = entry.get("role", "")
            content = entry.get("content", "")
            context_parts.append(f"{role.capitalize()}: {content}")
        
        return "\n".join(context_parts)
    
    def _consolidate_memory(self):
        """Consolidate short-term to long-term memory."""
        print("[Brainstem] Consolidating memory...")
        
        # Get all STM entries
        stm_entries = self.stm.get_all()
        
        # Create a summary (in a full implementation, this would use the LLM)
        summary = f"Conversation summary: {len(stm_entries)} exchanges about {stm_entries[0]['content'][:30]}..."
        
        # Store in LTM
        self.ltm.store({"summary": summary, "entries": stm_entries})
        
        # Clear STM (keeping a few recent entries)
        self.stm.clear(keep_last=3)
        
        print("[Brainstem] Memory consolidation complete.")
    
    def _schedule_dream_check(self):
        """Set up periodic dream cycle checks."""
        self.last_dream_check = time.time()
        
    def check_for_dream_cycle(self):
        """Check if it's time for a dream cycle and run if needed."""
        # Only check every 5 minutes in this demo
        current_time = time.time()
        if current_time - self.last_dream_check < 300:  # 5 minutes
            return False
            
        # Reset timer
        self.last_dream_check = current_time
        
        # Check dream conditions
        should_dream, conditions = self.dream_manager.check_sleep_conditions()
          # Enter dream cycle if needed
        if should_dream:
            print("[Brainstem] System needs memory consolidation, entering dream cycle...")
            success = self.dream_manager.enter_dream_cycle()
            return success
            
        return False
        
    def receive_signal(self, source, payload):
        """Handle incoming signals routed via the Body."""
        # Extract signal type
        if isinstance(payload, dict):
            message_type = payload.get("type", "")
            data = payload.get("data", {})
        else:
            message_type = ""
            data = {}
            
        print(f"[Brainstem] Received signal from {source}: {message_type}")
        
        # Process input request
        if message_type == "process_input":
            user_input = data.get("input", "")
            result = self.process_input(user_input)
            print(f"[Brainstem] Response: {result}")
            return result
            
        # Handle system events
        elif message_type == "system_event":
            event = payload.get("event", "")
            if event == "dream_cycle_start":
                print("[Brainstem] Dream cycle started - reducing processing priority")
                return {"status": "acknowledged"}
            elif event == "dream_cycle_end":
                print("[Brainstem] Dream cycle ended - restoring normal processing")
                duration = payload.get("data", {}).get("duration", 0)
                insights = payload.get("data", {}).get("insights_generated", 0)
                print(f"[Brainstem] Dream cycle completed in {duration:.2f}s, generated {insights} insights")
                return {"status": "acknowledged"}
                
        # Handle fragment changes
        elif message_type == "fragment_change":
            print("[Brainstem] Fragment activation levels changed")
            dominant = payload.get("dominant_fragment", "unknown")
            print(f"[Brainstem] Dominant fragment is now: {dominant}")
            return {"status": "acknowledged"}
            
        # Handle fragment reset
        elif message_type == "fragment_reset":
            print("[Brainstem] Fragment activation levels reset to default")
            return {"status": "acknowledged"}
            
        # Handle unknown signal types
        return {"status": "unknown_signal"}

# For direct testing
if __name__ == "__main__":
    brainstem = Brainstem()
    response = brainstem.process_input("Tell me about your identity and purpose.")
    print(f"\nResponse: {response}")
