"""
QueueManager

Manages the flow of information through the BlackwallV2 system, controlling
how many items are processed per heartbeat and maintaining processing queues.

Works with the heart module to create a biomimetic processing flow.
"""

import time
import threading
from collections import deque
from datetime import datetime
import json
from pathlib import Path
from typing import Dict, Any, Callable, Union
import uuid

class ProcessingItem:
    """
    Represents an item to be processed in the system.
    
    An item flows through the system, being modified by different components
    and accumulating context, responses, and metadata along the way.
    """
    
    def __init__(self, 
                 item_id: str,
                 content: Dict[str, Any],
                 source: str = "unknown", 
                 priority: int = 5,
                 max_processing_time: float = 30.0,
                 routing_id: str = None,
                 target_organ: str = None):
        """
        Initialize a processing item.
        
        Args:
            item_id: Unique identifier for this item
            content: The content to be processed
            source: Where this item originated from
            priority: Processing priority (1-10, with 10 being highest)
            max_processing_time: Maximum time (seconds) this item should spend processing
        """
        self.item_id = item_id
        self.content = content
        self.source = source
        self.priority = priority
        self.max_processing_time = max_processing_time
        
        # Routing fields
        self.routing_id = routing_id or f"route-{str(uuid.uuid4())[:8]}"
        self.target_organ = target_organ  # Organ/process this item is routed to
        
        # Tracking fields
        self.creation_time = datetime.now()
        self.last_beat_time = None
        self.total_processing_time = 0.0
        self.processing_stages: list = []
        self.current_stage = None
        self.completed = False
        self.error = None
        
        # Response accumulation
        self.responses: dict = {}
        self.final_response = None
        
    def update_stage(self, stage_name: str) -> None:
        """Update the processing stage of this item."""
        if self.current_stage:
            self.processing_stages.append({
                "stage": self.current_stage,
                "duration": (datetime.now() - self.last_beat_time).total_seconds()
                if self.last_beat_time else 0
            })
            
        self.current_stage = stage_name
        self.last_beat_time = datetime.now()
    
    def add_response(self, component: str, response: Any) -> None:
        """Add a response from a component to this item."""
        self.responses[component] = response
    
    def complete(self, final_response: Any = None) -> None:
        """Mark this item as completed."""
        self.completed = True
        if final_response is not None:
            self.final_response = final_response
        
        # Calculate total processing time
        self.total_processing_time = (datetime.now() - self.creation_time).total_seconds()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert this item to a dictionary for storage or transmission."""
        return {
            "item_id": self.item_id,
            "content": self.content,
            "source": self.source,
            "priority": self.priority,
            "creation_time": self.creation_time.isoformat(),
            "processing_stages": self.processing_stages,
            "current_stage": self.current_stage,
            "completed": self.completed,
            "total_processing_time": self.total_processing_time,
            "responses": self.responses,
            "final_response": self.final_response,
            "error": str(self.error) if self.error else None,
            "routing_id": self.routing_id,
            "target_organ": self.target_organ
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'ProcessingItem':
        """Create a ProcessingItem from a dictionary."""
        item = ProcessingItem(
            item_id=data["item_id"],
            content=data["content"],
            source=data["source"],
            priority=data["priority"],
            routing_id=data.get("routing_id"),
            target_organ=data.get("target_organ")
        )
        
        # Restore tracking fields
        item.creation_time = datetime.fromisoformat(data["creation_time"])
        item.processing_stages = data["processing_stages"]
        item.current_stage = data["current_stage"]
        item.completed = data["completed"] 
        item.total_processing_time = data["total_processing_time"]
        item.responses = data["responses"]
        item.final_response = data["final_response"]
        item.error = data["error"]
        
        return item

class QueueManager:
    """
    Manages the flow of information through the system based on heartbeats.
    
    This class maintains multiple queues for different types of processing
    and controls how many items are processed per heartbeat.
    """
    
    def __init__(self, pulse_capacity: int = 10, routing_table_path: str = None):
        """
        Initialize the queue manager.
        
        Args:
            pulse_capacity: Maximum number of items to process per heartbeat
        """
        self.pulse_capacity = pulse_capacity
        self.active_items: dict = {}  # Currently processing items
        
        # Different queues for different priorities and types
        self.queues: dict = {
            "input": deque(),      # New user inputs
            "processing": deque(),  # Items being processed
            "output": deque(),     # Items ready for output
            "memory": deque(),     # Items for memory operations
            "system": deque()      # System-level operations
        }
        
        # Statistics
        self.stats: dict = {
            "enqueued": 0,
            "processed": 0,
            "completed": 0,
            "errors": 0,
            "avg_processing_time": 0.0,
            "queue_lengths": {q: 0 for q in self.queues}
        }
        
        # Registered processors and callbacks
        self.processors: dict = {}  # stage_name -> processor function
        self.completion_callbacks: list = []
        
        # Queue persistence
        self.persistence_path: Union[str, Path, None] = None
        
        # Lock for thread safety
        self.lock = threading.RLock()
        
        # Routing table and organ IDs
        self.routing_table = {}
        self.organ_ids = set()
        if routing_table_path:
            self.load_routing_table(routing_table_path)
        
        print("[QueueManager] Initialized with pulse capacity:", self.pulse_capacity)
    
    def load_routing_table(self, path: str):
        """Load routing table from a JSON file."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                self.routing_table = json.load(f)
            print(f"[QueueManager] Loaded routing table from {path}")
        except Exception as e:
            print(f"[QueueManager] Failed to load routing table: {e}")
    
    def set_pulse_capacity(self, capacity: int) -> None:
        """Set the number of items to process per heartbeat."""
        with self.lock:
            self.pulse_capacity = max(1, capacity)  # Ensure at least 1
            print(f"[QueueManager] Pulse capacity set to {self.pulse_capacity}")
    
    def enqueue(self, queue_name: str, item: ProcessingItem) -> bool:
        """Add an item to the specified queue."""
        with self.lock:
            if queue_name not in self.queues:
                print(f"[QueueManager] Error: Queue {queue_name} does not exist")
                return False
            
            self.queues[queue_name].append(item)
            self.stats["enqueued"] += 1
            self.stats["queue_lengths"][queue_name] = len(self.queues[queue_name])
            
            print(f"[QueueManager] Item {item.item_id} added to {queue_name} queue")
            return True
    
    def register_processor(self, stage_name: str, processor: Callable) -> None:
        """
        Register a processor function for a specific stage.
        
        The processor should take a ProcessingItem and return True if processing
        completed successfully, False otherwise.
        """
        self.processors[stage_name] = processor
        print(f"[QueueManager] Registered processor for stage: {stage_name}")
    
    def register_completion_callback(self, callback: Callable) -> None:
        """Register a callback to be called when an item completes processing."""
        self.completion_callbacks.append(callback)
    
    def register_organ(self, organ_id: str, processor: Callable) -> None:
        """Register an organ/process with a unique ID for routing."""
        self.organ_ids.add(organ_id)
        self.processors[organ_id] = processor
        print(f"[QueueManager] Registered organ: {organ_id}")
    
    def on_heartbeat(self, beat_data: Dict[str, Any]) -> None:
        """
        Process queues on heartbeat.
        
        This is the main method called by the heart on each beat.
        It processes up to pulse_capacity items from the queues.
        """
        beat_count = beat_data.get("beat", 0)
        start_time = datetime.now()
        
        with self.lock:
            # Update stats before processing
            for queue_name in self.queues:
                self.stats["queue_lengths"][queue_name] = len(self.queues[queue_name])
            
            # Only log on certain beats to avoid spam
            if beat_count % 10 == 0:
                total_items = sum(len(q) for q in self.queues.values())
                print(f"[QueueManager] Heartbeat {beat_count}: {total_items} items in queues, {len(self.active_items)} active")
            
            # Process items up to pulse capacity
            slots_available = self.pulse_capacity - len(self.active_items)
            
            if slots_available <= 0:
                # Process active items but don't take new ones
                self._process_active_items()
                return
            
            # Priority order of queues to process
            queue_priority = ["input", "system", "processing", "memory", "output"]
            
            # Take items from queues based on priority
            items_to_process = []
            for queue_name in queue_priority:
                queue = self.queues[queue_name]
                while slots_available > 0 and queue:
                    items_to_process.append((queue_name, queue.popleft()))
                    slots_available -= 1
            
            # Start processing the new items
            for queue_name, item in items_to_process:
                self._start_processing(item, queue_name)
            
            # Continue processing active items
            self._process_active_items()
            
            # Save state periodically
            if self.persistence_path and beat_count % 50 == 0:
                self._save_state()
        
        # Log processing time if significant
        process_duration = (datetime.now() - start_time).total_seconds()
        if process_duration > 0.1:  # Only log if significant
            print(f"[QueueManager] Queue processing took {process_duration:.3f}s")
    
    def _start_processing(self, item: ProcessingItem, from_queue: str) -> None:
        """Start processing a new item."""
        # Determine initial stage based on queue
        initial_stages = {
            "input": "input_processing",
            "system": "system_task",
            "memory": "memory_operation",
            "output": "prepare_output",
            "processing": item.current_stage or "continue_processing" 
        }
        
        stage = initial_stages.get(from_queue, "unknown")
        item.update_stage(stage)
        
        # Add to active items
        self.active_items[item.item_id] = item
        
        if from_queue != "processing":  # Don't log items continuing processing
            print(f"[QueueManager] Starting {stage} for item {item.item_id}")
    
    def _process_active_items(self) -> None:
        """Process all active items through their current stages."""
        completed_items = []
        
        for item_id, active_item in list(self.active_items.items()):
            stage = active_item.current_stage
            
            if stage not in self.processors:
                print(f"[QueueManager] Warning: No processor for stage {stage}")
                active_item.error = f"No processor for stage {stage}"
                completed_items.append(active_item)
                continue
                
            try:
                # Process the item
                processor = self.processors[stage]
                result = processor(active_item)
                
                if result or active_item.completed:
                    # Item finished this stage or is completely done
                    completed_items.append(active_item)
                    
            except Exception as e:
                print(f"[QueueManager] Error processing item {item_id} at stage {stage}: {e}")
                active_item.error = str(e)
                completed_items.append(active_item)
        
        # Handle completed items
        for completed in completed_items:
            self._handle_completed_item(completed)
    
    def _handle_completed_item(self, completed_item: ProcessingItem) -> None:
        """Handle an item that has completed its current processing stage."""
        # Remove from active items
        if completed_item.item_id in self.active_items:
            del self.active_items[completed_item.item_id]
        
        if completed_item.error:
            # Item encountered an error
            self.stats["errors"] += 1
            print(f"[QueueManager] Item {completed_item.item_id} failed with error: {completed_item.error}")
            
            # Notify callbacks of error
            for callback in self.completion_callbacks:
                try:
                    callback(completed_item, success=False)
                except Exception as cb_err:
                    print(f"[QueueManager] Error in completion callback: {cb_err}")
                    
            return
            
        if completed_item.completed:
            # Item is fully completed
            self.stats["completed"] += 1
            
            # Update average processing time
            n = self.stats["completed"]
            current_avg = self.stats["avg_processing_time"]
            self.stats["avg_processing_time"] = (
                (current_avg * (n - 1) + completed_item.total_processing_time) / n
            )
            
            print(f"[QueueManager] Item {completed_item.item_id} completed processing in {completed_item.total_processing_time:.3f}s")
            
            # Notify callbacks of completion
            for callback in self.completion_callbacks:
                try:
                    callback(completed_item, success=True)
                except Exception as cb_err:
                    print(f"[QueueManager] Error in completion callback: {cb_err}")
                    
        else:
            # Item needs further processing
            next_queue = self._determine_next_queue(completed_item)
            self.queues[next_queue].append(completed_item)
            self.stats["queue_lengths"][next_queue] = len(self.queues[next_queue])
            
            self.stats["processed"] += 1
            print(f"[QueueManager] Item {completed_item.item_id} moved to {next_queue} queue")
    
    def _determine_next_queue(self, item: ProcessingItem) -> str:
        """Determine which queue an item should go to next based on its stage."""
        current_stage = item.current_stage
        
        # Stage transitions
        transitions = {
            "input_processing": "processing",
            "brain_processing": "processing", 
            "fragment_selection": "processing",
            "llm_generation": "processing",
            "response_filtering": "output",
            "memory_operation": "processing",
            "memory_consolidation": "memory",
            "prepare_output": "output",
            "system_task": "system"
        }
        
        return transitions.get(current_stage, "processing")
    
    def set_persistence_path(self, path: Union[str, Path]) -> None:
        """Set the path for queue persistence."""
        self.persistence_path = Path(path)
        print(f"[QueueManager] Queue persistence path set to {self.persistence_path}")
        
        # Create directory if needed
        self.persistence_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _save_state(self) -> None:
        """Save the current state of all queues to disk."""
        if not self.persistence_path:
            return
            
        try:
            # Prepare data
            queue_data = {
                name: [item.to_dict() for item in queue]
                for name, queue in self.queues.items()
            }
            
            active_data = {
                item_id: item.to_dict() 
                for item_id, item in self.active_items.items()
            }
            
            state = {
                "queues": queue_data,
                "active_items": active_data,
                "stats": self.stats,
                "timestamp": datetime.now().isoformat()
            }
            
            # Save to temporary file then rename to avoid corruption
            temp_path = self.persistence_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
                
            temp_path.replace(self.persistence_path)
            
        except (OSError, json.JSONDecodeError) as e:
            print(f"[QueueManager] Error saving state: {e}")
    
    def load_state(self) -> bool:
        """Load queue state from disk if available."""
        if not self.persistence_path or not self.persistence_path.exists():
            return False
            
        try:
            with open(self.persistence_path, 'r', encoding='utf-8') as f:
                state = json.load(f)
            
            with self.lock:
                # Restore queues
                for name, items in state["queues"].items():
                    if name in self.queues:
                        self.queues[name] = deque(
                            ProcessingItem.from_dict(item) for item in items
                        )
                
                # Restore active items
                for item_id, item_data in state["active_items"].items():
                    self.active_items[item_id] = ProcessingItem.from_dict(item_data)
                
                # Restore stats
                self.stats = state["stats"]
                
                # Update queue length stats
                for name in self.queues:
                    self.stats["queue_lengths"][name] = len(self.queues[name])
                    
                print(f"[QueueManager] Loaded state from {self.persistence_path}")
                return True
                
        except (OSError, json.JSONDecodeError) as e:
            print(f"[QueueManager] Error loading state: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get current queue statistics."""
        with self.lock:
            stats = self.stats.copy()
            # Update queue lengths
            for name in self.queues:
                stats["queue_lengths"][name] = len(self.queues[name])
            stats["active_items"] = len(self.active_items)
            return stats
    
    def create_processing_item(self, 
                               content: Dict[str, Any], 
                               source: str = "user",
                               priority: int = 5) -> ProcessingItem:
        """Create a new processing item with a unique ID."""
        item_id = f"{source}-{str(uuid.uuid4())[:8]}"
        routing_id = f"route-{str(uuid.uuid4())[:8]}"
        item = ProcessingItem(
            item_id=item_id,
            content=content,
            source=source,
            priority=priority,
            routing_id=routing_id
        )
        self.assign_routing(item)
        return item
    
    def assign_routing(self, item: ProcessingItem):
        """Assign routing info to a new item from the routing table."""
        route_info = self.routing_table.get(item.routing_id)
        if route_info:
            item.target_organ = route_info.get("organ_id")
            item.final_destination = route_info.get("final_destination")
        else:
            item.target_organ = None
            item.final_destination = None
    
    def inject_routing_into_heartbeat(self, beat_data: dict, item: ProcessingItem):
        """Inject routing info into the heartbeat/pulse data for downstream processors."""
        beat_data["routing_id"] = item.routing_id
        beat_data["target_organ"] = item.target_organ
        beat_data["final_destination"] = getattr(item, "final_destination", None)
    
    def get_final_destination(self, item: ProcessingItem) -> str:
        """Get the final destination for an item from its routing info."""
        return getattr(item, "final_destination", None)
    
    def batch_process(self):
        """Group and process similar items in batches for efficiency."""
        # Example: group by target_organ
        batch_groups = {}
        for queue in self.queues.values():
            for item in queue:
                key = item.target_organ or "default"
                batch_groups.setdefault(key, []).append(item)
        for organ_id, items in batch_groups.items():
            if organ_id in self.processors:
                print(f"[QueueManager] Batch processing {len(items)} items for organ {organ_id}")
                for item in items:
                    self.processors[organ_id](item)
    
    def dynamic_update_beat_and_pulse(self, new_beat: float = None, new_pulse: int = None):
        """Dynamically update heart/river_heart beat rate and pulse capacity."""
        if self.body and hasattr(self.body, "emit_event"):
            if new_beat is not None:
                self.body.emit_event("heartbeat_control", {"type": "set_rate", "data": {"rate": new_beat}})
            if new_pulse is not None:
                self.body.emit_event("heartbeat_control", {"type": "set_pulse_capacity", "data": {"capacity": new_pulse}})
        elif hasattr(self, "heart") and self.heart:
            if new_beat is not None and hasattr(self.heart, "set_rate"):
                self.heart.set_rate(new_beat)
            if new_pulse is not None and hasattr(self.heart, "set_pulse_capacity"):
                self.heart.set_pulse_capacity(new_pulse)
        print(f"[QueueManager] Dynamic update: beat={new_beat}, pulse={new_pulse}")
    
    def process_user_input(self, text: str, metadata: Union[Dict[str, Any], None] = None) -> str:
        """
        Process a user input text through the queue system.
        Returns the ID of the created processing item.
        """
        metadata = metadata or {}
        item = self.create_processing_item(
            content={"text": text, "metadata": metadata},
            source="user",
            priority=8  # User inputs get high priority
        )
        self.enqueue("input", item)
        return item.item_id

# Direct testing
if __name__ == "__main__":
    # Create a queue manager
    qm = QueueManager(pulse_capacity=5)
    
    # Register some test processors
    def test_processor(item):
        print(f"Processing item {item.item_id} at stage {item.current_stage}")
        # Simulate processing
        time.sleep(0.1)
        
        if item.current_stage == "input_processing":
            # Move to next stage
            item.update_stage("brain_processing")
            return True
        elif item.current_stage == "brain_processing":
            # Complete processing
            item.add_response("brain", "This is a response")
            item.complete(final_response="Final response")
            return True
            
        return False
    
    qm.register_processor("input_processing", test_processor)
    qm.register_processor("brain_processing", test_processor)
    
    # Add some test items
    for i in range(10):
        item = qm.create_processing_item(
            content={"text": f"Test input {i}"},
            source="test"
        )
        qm.enqueue("input", item)
    
    # Simulate heartbeats
    for i in range(5):
        print(f"\nSimulating heartbeat {i+1}...")
        qm.on_heartbeat({"beat": i+1})
        time.sleep(0.5)
    
    # Print final stats
    print("\nFinal stats:", qm.get_stats())
