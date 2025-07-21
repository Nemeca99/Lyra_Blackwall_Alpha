"""
Left Hemisphere (Short-Term Memory)

Handles short-term memory operations for the Lyra Blackwall system.
Uses /memshort/ for persistent STM storage.
"""

import os
import json

class ShortTermMemory:
    def __init__(self, buffer_size=100):
        """Initialize short-term memory with specified buffer size."""
        self.memory = []
        self.buffer_size = buffer_size
        self.memshort_dir = os.path.join(os.path.dirname(__file__), '..', 'memshort')
        self.stm_file = os.path.join(self.memshort_dir, 'stm_buffer.json')
        self._ensure_dir()
        self.load()

    def _ensure_dir(self):
        """Ensure the memory directory exists."""
        os.makedirs(self.memshort_dir, exist_ok=True)

    def store(self, item):
        """Add an item to short-term memory."""
        self.memory.append(item)
        
        # Trim if needed
        if len(self.memory) > self.buffer_size:
            self.memory = self.memory[-self.buffer_size:]
        
        # Save to disk
        self.save()
        
        return True

    def get_recent(self, count=5):
        """Get the most recent entries from memory."""
        return self.memory[-count:] if self.memory else []

    def get_all(self):
        """Get all entries from memory."""
        return self.memory

    def clear(self, keep_last=0):
        """Clear memory, optionally keeping the most recent entries."""
        if keep_last > 0:
            self.memory = self.memory[-keep_last:] if len(self.memory) > keep_last else self.memory
        else:
            self.memory = []
        self.save()
        return True

    def save(self):
        """Save memory to disk."""
        try:
            with open(self.stm_file, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"[STM] Error saving memory: {e}")
            return False

    def load(self):
        """Load memory from disk."""
        try:
            if os.path.exists(self.stm_file):
                with open(self.stm_file, 'r', encoding='utf-8') as f:
                    self.memory = json.load(f)
                return True
            return False
        except Exception as e:
            print(f"[STM] Error loading memory: {e}")
            self.memory = []
            return False

    def search(self, query, limit=5):
        """Search memory for entries containing the query."""
        results = []
        query = query.lower()
        
        for item in reversed(self.memory):  # Start with most recent
            content = item.get('content', '').lower()
            if query in content:
                results.append(item)
                if len(results) >= limit:
                    break
        
        return results

    def receive_signal(self, source, payload):
        """Handle incoming signals routed via the Body."""
        message_type = payload.get("type", "")
        data = payload.get("data", {})
        print(f"[STM] Received signal from {source}: {message_type}")
        if message_type == "store":
            item = data.get("item")
            if item:
                self.store(item)
                print(f"[STM] Stored item from signal: {item}")
        # Add more message types as needed
        return True

    def register_with_body(self, body):
        """Register this module with the Body system."""
        if body:
            result = body.register_module("stm", self)
            print("[ShortTermMemory] Registered with body system")
            return result
        return False

# For direct testing
if __name__ == "__main__":
    stm = ShortTermMemory()
    stm.store({"role": "user", "content": "Hello, I'm testing the short-term memory."})
    print(stm.get_recent())
    stm.store({"role": "assistant", "content": "I'm responding to your test."})
    print(stm.get_recent())
