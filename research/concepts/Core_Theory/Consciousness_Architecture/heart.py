"""
Heart

Core timing and autonomous loop driver for Lyra Blackwall.
Coordinates system pulses, synchronization, and drives autonomous processes like:
- Memory consolidation cycles
- Self-maintenance routines
- Dream cycles for identity reinforcement
- System state monitoring
- Information flow control (through pulse capacity)
"""

import time
import threading
from datetime import datetime

class Heart:
    """
    The Heart module drives the autonomous processes of the system.
    It creates regular pulses (heartbeats) that other components can respond to.
    
    The heart controls both the rate (heartbeat_rate) and volume (pulse_capacity)
    of information flowing through the system:
    - heartbeat_rate: time between pulses (like CPU clock speed)
    - pulse_capacity: items processed per beat (like CPU cores/threads)
    """
    
    def __init__(self, brainstem=None, body=None, queue_manager=None):
        """
        Initialize heart with references to other system components.
        
        Args:
            brainstem: The system's central processor
            body: The central event bus/routing system
            queue_manager: The system's queue manager for controlled processing
        """
        self.brainstem = brainstem
        self.body = body
        self.queue_manager = queue_manager
        self.heartbeat_rate = 1.0  # Default: 1 second between pulses
        self.pulse_capacity = 10   # Default: 10 items processed per beat
        self.alive = False
        self.beat_count = 0
        self.last_beat_time = None
        self.thread = None
        self.state = "idle"
        
        # Timing for different cycle types
        self.cycles = {
            "maintenance": {
                "frequency": 10,  # Every 10 beats
                "last_time": None
            },
            "memory_consolidation": {
                "frequency": 50,  # Every 50 beats
                "last_time": None
            },
            "dream": {
                "frequency": 100,  # Every 100 beats
                "last_time": None
            },
            "status_report": {
                "frequency": 5,  # Every 5 beats
                "last_time": None
            },
            "queue_stats": {
                "frequency": 20,  # Every 20 beats
                "last_time": None
            }
        }
        
        print("[Heart] Initialized with heartbeat rate:", self.heartbeat_rate, "and pulse capacity:", self.pulse_capacity)
    
    def register_with_body(self, body):
        """Register this heart with a body system."""
        self.body = body
        if self.body:
            self.body.register_module("heart", self)
            print("[Heart] Registered with body system")
            return True
        return False
    
    def set_queue_manager(self, queue_manager):
        """Connect the heart to a queue manager for information flow control."""
        self.queue_manager = queue_manager
        if self.queue_manager and hasattr(self.queue_manager, "set_pulse_capacity"):
            self.queue_manager.set_pulse_capacity(self.pulse_capacity)
            print("[Heart] Connected to queue manager")
            return True
        return False
    
    def set_pulse_capacity(self, capacity):
        """
        Set the system's pulse capacity (items processed per beat).
        
        This is like setting how many "blood cells" can flow through
        the system with each heartbeat.
        """
        self.pulse_capacity = max(1, capacity)  # Ensure at least 1
        if self.queue_manager and hasattr(self.queue_manager, "set_pulse_capacity"):
            self.queue_manager.set_pulse_capacity(self.pulse_capacity)
        print(f"[Heart] Pulse capacity set to {self.pulse_capacity}")
        return True
    
    def start(self, cycles=None):
        """Start the heart's pulse loop."""
        if self.alive:
            print("[Heart] Already beating.")
            return False
        
        self.alive = True
        self.state = "active"
        
        # If cycles specified, run for that many beats
        if cycles:
            self._run_for_cycles(cycles)
        else:
            # Otherwise start in background thread
            self._start_background()
            
        return True
    
    def _run_for_cycles(self, cycles):
        """Run the heart for a specified number of cycles."""
        print(f"[Heart] Starting for {cycles} cycles")
        for _ in range(cycles):
            self.pulse()
            time.sleep(self.heartbeat_rate)
        self.alive = False
        self.state = "idle"
        print("[Heart] Completed cycle run")
    
    def _start_background(self):
        """Start heart in background thread."""
        if self.thread and self.thread.is_alive():
            print("[Heart] Background thread already running")
            return False
        
        print("[Heart] Starting background thread")
        self.thread = threading.Thread(
            target=self._beat_loop,
            name="HeartThread",
            daemon=True  # Allow program to exit even if thread is running
        )
        self.thread.start()
        return True
    
    def _beat_loop(self):
        """Internal loop for continuous beating."""
        print("[Heart] Beginning beat loop")
        while self.alive:
            self.pulse()
            time.sleep(self.heartbeat_rate)
        print("[Heart] Beat loop ended")
    
    def stop(self):
        """Stop the heart's beating."""
        if not self.alive:
            print("[Heart] Already stopped")
            return True
            
        print("[Heart] Stopping...")
        self.alive = False
        self.state = "stopping"
        
        # Wait for thread to end if it exists
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)  # Wait up to 2 seconds
            if self.thread.is_alive():
                print("[Heart] Warning: Heart thread didn't stop cleanly")
            
        self.state = "idle"
        print("[Heart] Stopped")
        return True
    
    def set_rate(self, rate):
        """Set the heartbeat rate in seconds."""
        if rate <= 0:
            print("[Heart] Error: Rate must be positive")
            return False
            
        self.heartbeat_rate = rate
        print(f"[Heart] Rate set to {rate} seconds")
        return True
        
    def pulse(self):
        """
        Trigger a system pulse.
        
        This is the main function that drives the system rhythm,
        notifying all components of the heartbeat and triggering
        various maintenance cycles based on their frequencies.
        """
        now = datetime.now()
        self.beat_count += 1
        self.last_beat_time = now
        
        # Format only needed for display
        timestamp = now.strftime("%H:%M:%S.%f")[:-3]
        
        # Notify the queue manager first (for controlled concurrency)
        if self.queue_manager and hasattr(self.queue_manager, "on_heartbeat"):
            self.queue_manager.on_heartbeat({
                "beat": self.beat_count,
                "time": now,
                "source": "heart",
                "pulse_capacity": self.pulse_capacity
            })
        
        # Notify the body (event bus) next
        if self.body:
            self.body.emit_event("heartbeat", {
                "beat": self.beat_count,
                "time": now,
                "source": "heart"
            })
        
        # Notify the brainstem directly
        if self.brainstem:
            if hasattr(self.brainstem, "pulse"):
                self.brainstem.pulse(self.beat_count)
        
        # Check for special cycles
        self._check_cycle_triggers()
        
        if self.beat_count % 10 == 0 or self.beat_count < 5:
            print(f"[Heart] Pulse {self.beat_count} @ {timestamp}")
    
    def _check_cycle_triggers(self):
        """Check if any special cycles need to be triggered."""
        for cycle_name, cycle_data in self.cycles.items():
            frequency = cycle_data["frequency"]
            
            if self.beat_count % frequency == 0:
                cycle_data["last_time"] = datetime.now()
                
                # Trigger the appropriate cycle
                if cycle_name == "maintenance":
                    self._trigger_maintenance()
                elif cycle_name == "memory_consolidation":
                    self._trigger_memory_consolidation()
                elif cycle_name == "dream":
                    self._trigger_dream()
                elif cycle_name == "status_report":
                    self._trigger_status_report()
                elif cycle_name == "queue_stats":
                    self._trigger_queue_stats()
    
    def _trigger_maintenance(self):
        """Trigger system maintenance cycle."""
        print("[Heart] Triggering maintenance cycle")
        if self.body:
            self.body.emit_event("maintenance", {
                "beat": self.beat_count,
                "source": "heart"
            })
    
    def _trigger_memory_consolidation(self):
        """Trigger memory consolidation cycle."""
        print("[Heart] Triggering memory consolidation")
        if self.brainstem:
            # WARNING: Accessing protected member _consolidate_memory. Consider using a public method if available.
            if hasattr(self.brainstem, "_consolidate_memory"):
                self.brainstem._consolidate_memory()
            
        if self.body:
            self.body.emit_event("memory_consolidation", {
                "beat": self.beat_count,
                "source": "heart"
            })
    
    def _trigger_dream(self):
        """Trigger dream cycle for identity reinforcement."""
        print("[Heart] Triggering dream cycle")
        if self.body:
            self.body.emit_event("dream", {
                "beat": self.beat_count,
                "source": "heart"
            })
    
    def _trigger_status_report(self):
        """Trigger a system status report."""
        print(f"[Heart] Status Report: {self.beat_count} beats, state={self.state}")
        
        # Collect status from components if body is available
        if self.body:
            self.body.emit_event("status_report", {
                "beat": self.beat_count,
                "source": "heart",
                "state": self.state
            })
    
    def _trigger_queue_stats(self):
        """Get queue statistics if queue manager is available."""
        if self.queue_manager and hasattr(self.queue_manager, "get_stats"):
            stats = self.queue_manager.get_stats()
            print(f"[Heart] Queue Stats: {stats}")
    
    def get_status(self):
        """Get the heart's status information."""
        return {
            "alive": self.alive,
            "beat_count": self.beat_count,
            "rate": self.heartbeat_rate,
            "state": self.state,
            "last_beat": self.last_beat_time,
            "cycles": self.cycles,
            "pulse_capacity": self.pulse_capacity
        }

    def receive_signal(self, source, payload):
        """Receive signal from the body system."""
        message_type = payload.get("type", "")
        
        if message_type == "set_rate":
            rate = payload.get("data", {}).get("rate")
            if rate:
                self.set_rate(rate)
        elif message_type == "set_pulse_capacity":
            capacity = payload.get("data", {}).get("capacity")
            if capacity:
                self.set_pulse_capacity(capacity)
        elif message_type == "start":
            cycles = payload.get("data", {}).get("cycles")
            self.start(cycles=cycles)
        elif message_type == "stop":
            self.stop()
        else:
            print(f"[Heart] Received signal: {message_type} from {source}")
        
        return True
