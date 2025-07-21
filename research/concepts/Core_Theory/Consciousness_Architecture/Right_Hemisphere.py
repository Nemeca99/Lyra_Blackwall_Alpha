"""
Right Hemisphere (Long-Term Memory)

Handles long-term memory operations for the Lyra Blackwall system.
Uses /memlong/ for persistent LTM storage.
"""

import os
import json

class LongTermMemory:
    def __init__(self):
        """Initialize long-term memory."""
        self.memory = []
        self.memlong_dir = os.path.join(os.path.dirname(__file__), '..', 'memlong')
        self.ltm_file = os.path.join(self.memlong_dir, 'ltm_buffer.json')
        self._ensure_dir()
        self.load()

    def _ensure_dir(self):
        """Ensure the memory directory exists."""
        os.makedirs(self.memlong_dir, exist_ok=True)

    def store(self, summary):
        """Store a compressed STM summary in LTM and persist."""
        self.memory.append(summary)
        self.save()
        return True

    def get_all(self):
        """Get all entries from memory."""
        return self.memory

    def search(self, query, limit=5):
        """Search memory for entries containing the query."""
        results = []
        query = query.lower()
        
        for item in reversed(self.memory):  # Start with most recent
            summary = item.get('summary', '').lower()
            if query in summary:
                results.append(item)
                if len(results) >= limit:
                    break
        
        return results

    def save(self):
        """Save memory to disk."""
        try:
            with open(self.ltm_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"[LTM] Error saving memory: {e}")
            return False

    def load(self):
        """Load memory from disk."""
        try:
            if os.path.exists(self.ltm_file):
                with open(self.ltm_file, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
                if not isinstance(self.memory, list):
                    print("[LTM] Warning: Loaded memory is not a list, resetting to empty list.")
                    self.memory = []
                return True
            return False
        except Exception as e:
            print(f"[LTM] Error loading memory: {e}")
            self.memory = []
            return False

    def receive_signal(self, source, payload):
        """Handle incoming signals routed via the Body."""
        message_type = payload.get("type", "")
        data = payload.get("data", {})
        print(f"[LTM] Received signal from {source}: {message_type}")
        if message_type == "store":
            summary = data.get("summary")
            if summary:
                self.store(summary)
                print(f"[LTM] Stored summary from signal: {summary}")
        # Add more message types as needed
        return True

    def register_with_body(self, body):
        """Register this module with the Body system."""
        if body:
            result = body.register_module("ltm", self)
            print("[LongTermMemory] Registered with body system")
            return result
        return False

# For direct testing
if __name__ == "__main__":
    ltm = LongTermMemory()
    ltm.store({"summary": "Test conversation about recursive systems", 
              "entries": [{"role": "user", "content": "Tell me about recursive systems"}]})
    print(ltm.get_all())
