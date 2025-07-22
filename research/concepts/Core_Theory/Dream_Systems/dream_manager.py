"""
DreamManager - Memory Consolidation and Dream Cycle Management

This module implements the Dream Cycle for the BlackwallV2 architecture,
providing memory consolidation, symbolic compression, and insight generation
during "sleep" periods.
"""

import time
import random
import json
import os
from pathlib import Path
from datetime import datetime
import logging
from typing import List, Dict, Any, Optional, Union, Tuple, Callable

# Constants
SLEEP_TRIGGER_THRESHOLD = 0.8  # Threshold for memory fragmentation score
MIN_CONSOLIDATION_INTERVAL = 3600  # Minimum time (seconds) between dream cycles
DREAM_DURATION_BASE = 30  # Base duration of dream cycle in seconds
CONSOLIDATION_CHUNK_SIZE = 20  # Maximum memories to process in one cycle


class DreamManager:
    """
    Manages the dream cycle for the BlackwallV2 system, handling memory
    consolidation, symbolic compression, and insight generation.
    """
    
    def __init__(self, 
                 long_term_memory=None, 
                 heart=None,
                 body=None,
                 logger=None):
        """
        Initialize the DreamManager.
        
        Args:
            long_term_memory: The LongTermMemory instance
            heart: The Heart instance for managing system rhythms
            body: The Body instance for system-wide signaling
            logger: Optional logger for recording dream activities
        """
        self.ltm = long_term_memory
        self.heart = heart
        self.body = body
        self.logger = logger or logging.getLogger("DreamManager")
        self.is_dreaming = False
        self.last_dream_time = time.time() - (MIN_CONSOLIDATION_INTERVAL + 100)  # Allow immediate dreaming on first check
        self.consolidation_stats = {
            "total_cycles": 0,
            "total_memories_processed": 0,
            "total_consolidations": 0,
            "insights_generated": 0,
            "last_cycle_duration": 0,
            "memory_usage": {
                "before_cycle": {},
                "after_cycle": {},
                "savings_history": []
            }
        }
        self.dream_log_path = os.path.join(Path(__file__).resolve().parent.parent, "log", "dream_log.txt")
        self._ensure_log_file()
        
        # Try to load previous stats
        self._load_stats()
        
    def _ensure_log_file(self):
        """Create dream log file if it doesn't exist."""
        os.makedirs(os.path.dirname(self.dream_log_path), exist_ok=True)
        if not os.path.exists(self.dream_log_path):
            with open(self.dream_log_path, "w", encoding="utf-8") as f:
                f.write(f"# BlackwallV2 Dream Log\nInitialized: {datetime.now().isoformat()}\n\n")
                
    def _load_stats(self):
        """Load previous consolidation stats if available."""
        stats_path = os.path.join(os.path.dirname(self.dream_log_path), "dream_stats.json")
        if os.path.exists(stats_path):
            try:
                with open(stats_path, "r", encoding="utf-8") as f:
                    self.consolidation_stats = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.logger.error("Failed to load dream stats, using defaults")
                
    def _save_stats(self):
        """Save consolidation statistics."""
        stats_path = os.path.join(os.path.dirname(self.dream_log_path), "dream_stats.json")
        try:
            with open(stats_path, "w", encoding="utf-8") as f:
                json.dump(self.consolidation_stats, f, indent=2)
        except IOError:
            self.logger.error("Failed to save dream stats")
            
    def log_dream_activity(self, message: str, level: str = "INFO"):
        """Log dream cycle activities to the dream log file."""
        timestamp = datetime.now().isoformat()
        with open(self.dream_log_path, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {level}: {message}\n")
            
        if self.logger:
            # Check if the logger has specific level methods or a generic log method
            if hasattr(self.logger, level.lower()):
                # Standard logging module style
                getattr(self.logger, level.lower())(message)
            elif hasattr(self.logger, 'log'):
                # Custom logger with log method
                self.logger.log(message, level)
                
    def check_sleep_conditions(self) -> Tuple[bool, Dict[str, float]]:
        """
        Determine if the system should enter dream mode based on memory
        fragmentation and system load.
        
        Returns:
            Tuple[bool, Dict]: (should_sleep, condition_scores)
        """
        # Don't dream if we recently had a dream cycle
        time_since_last_dream = time.time() - self.last_dream_time
        if time_since_last_dream < MIN_CONSOLIDATION_INTERVAL:
            return False, {"time_remaining": MIN_CONSOLIDATION_INTERVAL - time_since_last_dream}
        
        # Check memory fragmentation if LTM available
        fragmentation_score = 0.0
        if self.ltm:
            try:
                fragmentation_score = self._calculate_memory_fragmentation()
            except Exception as e:
                self.logger.error(f"Error calculating fragmentation: {e}")
        
        # Check system load if Heart available
        system_load = 0.0
        if self.heart:
            try:
                system_load = self._get_system_load()
            except Exception as e:
                self.logger.error(f"Error getting system load: {e}")
                
        # Decide if we should sleep
        should_sleep = (fragmentation_score > SLEEP_TRIGGER_THRESHOLD or 
                        system_load > SLEEP_TRIGGER_THRESHOLD)
        
        condition_scores = {
            "fragmentation": fragmentation_score,
            "system_load": system_load,
            "time_since_last_dream": time_since_last_dream
        }
        
        return should_sleep, condition_scores
    
    def _calculate_memory_fragmentation(self) -> float:
        """
        Calculate memory fragmentation score from 0.0 to 1.0.
        
        Returns:
            float: Fragmentation score where higher values indicate more fragmentation
        """
        if not self.ltm or not hasattr(self.ltm, 'memory'):
            return 0.0
            
        # Safety check if memory is not initialized
        if not self.ltm.memory:
            return 0.0
            
        # Simple fragmentation metrics:
        # 1. Number of separate memory entries vs consolidation potential
        # 2. Lack of connections between related memories
        
        # Count total memories and tagged clusters
        try:
            total_memories = len(self.ltm.memory)
            if total_memories == 0:
                return 0.0
                
            # Count unique tags/topics
            tags = set()
            for mem in self.ltm.memory:
                if isinstance(mem, dict) and 'tag' in mem:
                    tags.add(mem['tag'])
                    
            # Calculate potential consolidation ratio
            tag_ratio = len(tags) / max(1, total_memories)
            
            # More tags with fewer memories indicates higher fragmentation
            if len(tags) == 0:
                return 0.5  # No tags means moderate fragmentation
            
            # Calculate fragmentation based on memory distribution across tags
            tag_counts = {}
            for mem in self.ltm.memory:
                if isinstance(mem, dict) and 'tag' in mem:
                    tag_counts[mem['tag']] = tag_counts.get(mem['tag'], 0) + 1
                    
            # More even distribution = more fragmentation
            # High std deviation = less fragmentation (some topics consolidated)
            if len(tag_counts) > 0:
                values = list(tag_counts.values())
                mean = sum(values) / len(values)
                variance = sum((x - mean) ** 2 for x in values) / len(values)
                std_dev = variance ** 0.5
                normalized_std = std_dev / (mean if mean > 0 else 1)
                
                # Lower std deviation = higher fragmentation
                uniformity = 1.0 - min(1.0, normalized_std)
                  # Combine metrics
                fragmentation = (0.5 * tag_ratio) + (0.5 * uniformity)
            else:
                fragmentation = 0.5
            return min(1.0, fragmentation)
        except Exception as e:
            self.logger.error(f"Error in fragmentation calculation: {e}")
            return 0.5  # Default to moderate fragmentation on error
            
    def _get_system_load(self) -> float:
        """
        Get system load from Heart's queue status.
        
        Returns:
            float: System load from 0.0 to 1.0
        """
        if not self.heart:
            return 0.0
            
        # If Heart has queue and queue manager
        if hasattr(self.heart, 'queue_manager'):
            try:
                queue_size = len(self.heart.queue_manager.queue)
                capacity = self.heart.queue_manager.max_queue_size or 100
                return min(1.0, queue_size / capacity)
            except Exception:
                return 0.0
        return 0.0
        
    def enter_dream_cycle(self) -> bool:
        """
        Enter dream cycle mode, consolidate memories, and generate insights.
        
        Returns:
            bool: True if dream cycle completed successfully
        """
        if self.is_dreaming:
            return False
        self.is_dreaming = True
        self.last_dream_time = time.time()
        start_time = time.time()
        
        # Track memory usage before consolidation
        try:
            self._track_memory_usage("before")
        except ImportError:
            self.log_dream_activity("Memory monitoring requires psutil package. Install with 'pip install psutil'", "WARNING")
        except Exception as e:
            self.log_dream_activity(f"Failed to track memory usage: {e}", "ERROR")
        
        try:
            # Announce entering dream cycle
            self.log_dream_activity("Entering dream cycle...", "INFO")
              # Signal body if available
            if self.body:
                self.body.route_signal("dream_manager", "brainstem", {
                    "type": "system_event",
                    "event": "dream_cycle_start",
                    "timestamp": datetime.now().isoformat()
                })
            
            # Slow down heart rate if heart is available
            original_interval = None
            if self.heart and hasattr(self.heart, 'heartbeat_interval'):
                original_interval = self.heart.heartbeat_interval
                self.heart.heartbeat_interval = original_interval * 2
                self.log_dream_activity(f"Slowing heart rate from {original_interval}s to {self.heart.heartbeat_interval}s", "INFO")
            
            # Track memory usage before consolidation
            self._track_memory_usage(phase="before")
            
            # Perform memory consolidation if LTM available
            if self.ltm and hasattr(self.ltm, 'memory'):
                self._consolidate_memories()
                
            # Generate insights based on consolidated memories
            insights = self._generate_insights()
            
            # Track memory usage after consolidation
            self._track_memory_usage(phase="after")
            
            # Restore heart rate
            if self.heart and original_interval is not None:
                self.heart.heartbeat_interval = original_interval
                self.log_dream_activity(f"Restoring heart rate to {original_interval}s", "INFO")
              # Signal dream cycle completion
            if self.body:
                self.body.route_signal("dream_manager", "brainstem", {
                    "type": "system_event",
                    "event": "dream_cycle_end",
                    "timestamp": datetime.now().isoformat(),
                    "data": {
                        "duration": time.time() - start_time,
                        "insights_generated": len(insights)
                    }
                })
                  # Track memory usage after consolidation
            try:
                self._track_memory_usage("after")
            except ImportError:
                pass  # Already warned about psutil requirement
            except Exception as e:
                self.log_dream_activity(f"Failed to track memory usage after cycle: {e}", "ERROR")
            
            # Update stats
            self.consolidation_stats["total_cycles"] += 1
            self.consolidation_stats["last_cycle_duration"] = time.time() - start_time
            self._save_stats()
            
            self.log_dream_activity(f"Dream cycle completed in {time.time() - start_time:.2f} seconds", "INFO")
            return True
            
        except Exception as e:
            self.log_dream_activity(f"Error in dream cycle: {e}", "ERROR")
            return False
        finally:
            self.is_dreaming = False
            
    def _consolidate_memories(self) -> List[Dict[str, Any]]:
        """
        Consolidate related memories to reduce fragmentation.
        
        Returns:
            List[Dict]: List of consolidated memory entries
        """
        if not self.ltm or not hasattr(self.ltm, 'memory') or not self.ltm.memory:
            return []
            
        # Safety check
        if not isinstance(self.ltm.memory, list):
            self.log_dream_activity("LTM memory is not a list, cannot consolidate", "ERROR")
            return []
            
        # Get a subset of memories to process in this cycle
        memories_to_process = self.ltm.memory[:CONSOLIDATION_CHUNK_SIZE]
        
        # Group memories by tag
        memory_clusters = {}
        for mem in memories_to_process:
            if not isinstance(mem, dict):
                continue
                
            tag = mem.get('tag', 'untagged')
            if tag not in memory_clusters:
                memory_clusters[tag] = []
            memory_clusters[tag].append(mem)
            
        # Process clusters with multiple memories
        consolidations = []
        processed_indices = set()
        
        for tag, cluster in memory_clusters.items():
            if len(cluster) < 2:
                continue
                
            # Sort by timestamp if available
            cluster.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            
            # Create consolidated memory
            consolidated = {
                'tag': tag,
                'type': 'consolidated_memory',
                'timestamp': datetime.now().isoformat(),
                'source_count': len(cluster),
                'content': self._merge_memory_content(cluster),
                'sources': [mem.get('id', i) for i, mem in enumerate(cluster)]
            }
            
            # Track original memory indices
            for mem in cluster:
                if 'id' in mem and isinstance(mem['id'], int):
                    processed_indices.add(mem['id'])
            
            consolidations.append(consolidated)
            
            self.log_dream_activity(
                f"Consolidated {len(cluster)} memories with tag '{tag}'", 
                "INFO"
            )
            
        # Update statistics
        self.consolidation_stats["total_memories_processed"] += len(memories_to_process)
        self.consolidation_stats["total_consolidations"] += len(consolidations)
        
        # Update LTM: add consolidations and potentially remove processed memories
        if hasattr(self.ltm, 'add_memory'):
            for cons in consolidations:
                self.ltm.add_memory(cons)
                
        return consolidations
    
    def _merge_memory_content(self, memories: List[Dict[str, Any]]) -> str:
        """
        Merge the content of multiple related memories.
        
        Args:
            memories: List of memory dictionaries to merge
            
        Returns:
            str: Consolidated content
        """
        if not memories:
            return ""
            
        # Extract content from each memory
        contents = []
        for mem in memories:
            if isinstance(mem, dict) and 'content' in mem:
                if isinstance(mem['content'], str):
                    contents.append(mem['content'])
                elif isinstance(mem['content'], dict):
                    # Handle summary dictionaries
                    summary = mem['content'].get('summary', '')
                    if summary:
                        contents.append(summary)
        
        # Simple concatenation for now - in real implementation, 
        # this would use more sophisticated NLP techniques
        if contents:
            merged = f"Consolidated memory ({len(contents)} sources):\n\n"
            merged += "\n---\n".join(contents[:3])  # Limit to prevent huge consolidations
            if len(contents) > 3:
                merged += f"\n\n[+{len(contents)-3} more related memories]"
            return merged
        else:
            return "Empty consolidated memory"
            
    def _generate_insights(self) -> List[Dict[str, Any]]:
        """
        Generate insights from consolidated memories.
        
        Returns:
            List[Dict]: Generated insights
        """
        # Simplified placeholder - in production, this would use 
        # more sophisticated pattern recognition or LLM integration
        insights = []
        
        if not self.ltm or not hasattr(self.ltm, 'memory') or not self.ltm.memory:
            return insights
            
        # Find consolidated memories
        consolidated = [m for m in self.ltm.memory if isinstance(m, dict) and 
                        m.get('type') == 'consolidated_memory']
                        
        if not consolidated:
            return insights
            
        # Simple insight generation
        insight = {
            'type': 'dream_insight',
            'timestamp': datetime.now().isoformat(),
            'content': f"Generated insight connecting {len(consolidated)} memory clusters",
            'sources': [m.get('id', i) for i, m in enumerate(consolidated)]
        }
        
        if len(consolidated) >= 2:
            # Generate a metaphorical "dream" connecting two random consolidations
            c1 = random.choice(consolidated)
            c2 = random.choice(consolidated)
            if c1 != c2:
                t1 = c1.get('tag', 'unknown')
                t2 = c2.get('tag', 'unknown')
                insight['content'] = f"Dream connection: '{t1}' and '{t2}' are linked through shared patterns"
                
        insights.append(insight)
        self.consolidation_stats["insights_generated"] += 1
        
        # Add to LTM if available
        if hasattr(self.ltm, 'add_memory'):
            self.ltm.add_memory(insight)
            
        self.log_dream_activity(f"Generated insight: {insight['content']}", "INFO")
        return insights
        
    def receive_signal(self, signal):
        """Handle signals from other components."""
        if isinstance(signal, dict):
            if signal.get('command') == 'check_dream_conditions':
                should_sleep, conditions = self.check_sleep_conditions()
                return {
                    'should_sleep': should_sleep, 
                    'conditions': conditions
                }
            elif signal.get('command') == 'force_dream_cycle':
                self.last_dream_time = 0  # Reset timer to allow immediate dreaming
                success = self.enter_dream_cycle()
                return {'success': success}
        return {'status': 'unknown_signal'}

    def register_with_body(self, body):
        """Register this module with the Body system."""
        if body:
            self.body = body
            result = body.register_module("dream_manager", self)
            print("[DreamManager] Registered with body system")
            return result
        return False
    
    def check_dream_cycle(self):
        """
        Check if it's time for a dream cycle based on memory state and time elapsed.
        
        Returns:
            bool: True if a dream cycle should be initiated, False otherwise
        """
        # Don't run if already dreaming
        if self.is_dreaming:
            return False
            
        # Check if minimum time has passed since last dream
        current_time = time.time()
        if current_time - self.last_dream_time < MIN_CONSOLIDATION_INTERVAL:
            return False
            
        # Check memory fragmentation (normally would analyze memory)
        if self.ltm:
            memories = self.ltm.get_all()[-50:]  # Look at last 50 memories
            if len(memories) > 20:  # Need enough memories to consider consolidation
                # In a real system, we would analyze memory coherence and fragmentation
                # For this simulation, just use a time and random threshold
                fragmentation_score = random.uniform(0.4, 1.0)
                if fragmentation_score > SLEEP_TRIGGER_THRESHOLD:
                    self.logger.info(f"Memory fragmentation detected ({fragmentation_score:.2f}), initiating dream cycle")
                    return True
                    
        # Fallback - initiate dream cycle every 4-5 hours of uptime
        if current_time - self.last_dream_time > 14400 + random.uniform(0, 3600):
            self.logger.info("Time-based dream cycle triggered")
            return True
            
        return False
        
    def cluster_memories(self, memories):
        """
        Cluster memories by topic, theme, or conceptual similarity.
        
        Args:
            memories: List of memory items to cluster
            
        Returns:
            Dict of cluster labels to lists of memory indices
        """
        # This is a simple implementation that clusters based on tags
        clusters = {}
        
        # Group by tags
        for i, memory in enumerate(memories):
            tags = memory.get("tags", [])
            
            # Assign to a primary cluster based on first tag
            if tags:
                primary_tag = tags[0]
                if primary_tag not in clusters:
                    clusters[primary_tag] = []
                clusters[primary_tag].append(i)
            else:
                # Handle untagged memories
                if "untagged" not in clusters:
                    clusters["untagged"] = []
                clusters["untagged"].append(i)
                
        return clusters

    def _track_memory_usage(self, phase: str = "before") -> Dict[str, Any]:
        """
        Track memory usage statistics for the dream cycle.
        
        Args:
            phase: Either "before" or "after" the dream cycle
            
        Returns:
            Dict[str, Any]: Memory usage statistics
        """
        import sys
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        
        # Get memory stats
        usage_stats = {
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "process_memory_info": {
                "rss": process.memory_info().rss / (1024 * 1024),  # MB
                "vms": process.memory_info().vms / (1024 * 1024),  # MB
            },
            "system_memory": {
                "total": psutil.virtual_memory().total / (1024 * 1024),  # MB
                "available": psutil.virtual_memory().available / (1024 * 1024),  # MB
                "percent_used": psutil.virtual_memory().percent
            }
        }
        
        # Get BlackwallV2 memory structures size
        if self.ltm and hasattr(self.ltm, "memory"):
            # Estimate memory size of LTM
            try:
                ltm_size = sys.getsizeof(self.ltm.memory) / (1024 * 1024)  # MB
                usage_stats["blackwall_memory"] = {
                    "ltm_object_size": ltm_size,
                    "ltm_entry_count": len(self.ltm.memory) if isinstance(self.ltm.memory, list) else 0
                }
            except Exception as e:
                self.logger.error(f"Error calculating LTM memory size: {e}")
                usage_stats["blackwall_memory"] = {
                    "ltm_object_size": -1,
                    "ltm_entry_count": -1
                }
        
        # Store the stats in the appropriate place
        if phase.lower() == "before":
            self.consolidation_stats["memory_usage"]["before_cycle"] = usage_stats
        elif phase.lower() == "after":
            self.consolidation_stats["memory_usage"]["after_cycle"] = usage_stats
            
            # Calculate memory savings if we have both before and after stats
            before = self.consolidation_stats["memory_usage"].get("before_cycle", {})
            if before:
                try:
                    before_entries = before.get("blackwall_memory", {}).get("ltm_entry_count", 0)
                    after_entries = usage_stats.get("blackwall_memory", {}).get("ltm_entry_count", 0)
                    
                    before_size = before.get("blackwall_memory", {}).get("ltm_object_size", 0)
                    after_size = usage_stats.get("blackwall_memory", {}).get("ltm_object_size", 0)
                    
                    savings = {
                        "timestamp": datetime.now().isoformat(),
                        "entries_before": before_entries,
                        "entries_after": after_entries,
                        "entries_diff": before_entries - after_entries,
                        "size_before_mb": before_size,
                        "size_after_mb": after_size,
                        "size_diff_mb": before_size - after_size,
                        "percent_reduction_entries": ((before_entries - after_entries) / max(1, before_entries)) * 100,
                        "percent_reduction_size": ((before_size - after_size) / max(0.001, before_size)) * 100
                    }
                    
                    # Add to history
                    self.consolidation_stats["memory_usage"]["savings_history"].append(savings)
                    
                    # Keep history to a reasonable size
                    max_history = 100
                    if len(self.consolidation_stats["memory_usage"]["savings_history"]) > max_history:
                        self.consolidation_stats["memory_usage"]["savings_history"] = \
                            self.consolidation_stats["memory_usage"]["savings_history"][-max_history:]
                            
                    # Log the savings
                    self.log_dream_activity(
                        f"Memory consolidation: {savings['percent_reduction_entries']:.1f}% reduction in entries, "
                        f"{savings['percent_reduction_size']:.1f}% reduction in size",
                        "INFO"
                    )
                    
                except Exception as e:
                    self.logger.error(f"Error calculating memory savings: {e}")
        
        return usage_stats

    def generate_memory_usage_report(self) -> Dict[str, Any]:
        """
        Generate a comprehensive report on memory usage and consolidation statistics.
        
        Returns:
            Dict[str, Any]: Memory usage report
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "dream_cycles": {
                "total": self.consolidation_stats.get("total_cycles", 0),
                "last_cycle_time": datetime.fromtimestamp(
                    self.last_dream_time).isoformat() if self.last_dream_time else "Never",
                "last_cycle_duration": self.consolidation_stats.get("last_cycle_duration", 0)
            },
            "memory_metrics": {
                "current_usage": self._track_memory_usage("current"),
                "last_cycle": {
                    "before": self.consolidation_stats.get("memory_usage", {}).get("before_cycle", {}),
                    "after": self.consolidation_stats.get("memory_usage", {}).get("after_cycle", {})
                }
            },
            "consolidation_metrics": {
                "total_memories_processed": self.consolidation_stats.get("total_memories_processed", 0),
                "total_consolidations": self.consolidation_stats.get("total_consolidations", 0),
                "insights_generated": self.consolidation_stats.get("insights_generated", 0)
            }
        }
        
        # Add savings history metrics if available
        savings_history = self.consolidation_stats.get("memory_usage", {}).get("savings_history", [])
        if savings_history:
            # Calculate averages
            avg_entry_reduction = sum(s.get("percent_reduction_entries", 0) for s in savings_history) / max(1, len(savings_history))
            avg_size_reduction = sum(s.get("percent_reduction_size", 0) for s in savings_history) / max(1, len(savings_history))
            
            report["consolidation_efficiency"] = {
                "average_entry_reduction_percent": avg_entry_reduction,
                "average_size_reduction_percent": avg_size_reduction,
                "cycles_with_metrics": len(savings_history),
                "recent_savings": savings_history[-5:] if len(savings_history) >= 5 else savings_history
            }
        
        return report

    def generate_memory_visualization(self, output_path: Optional[str] = None) -> str:
        """
        Generate an HTML visualization of memory usage and dream cycle metrics.
        
        Args:
            output_path: Optional path to save the HTML report. If None, uses default path.
            
        Returns:
            str: Path to the generated HTML file
        """
        if output_path is None:
            # Create a file in the log directory
            os.makedirs(os.path.join(Path(__file__).resolve().parent.parent, "log"), exist_ok=True)
            output_path = os.path.join(
                Path(__file__).resolve().parent.parent, 
                "log", 
                f"memory_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            )
        
        # Get the report data
        report = self.generate_memory_usage_report()
        
        # Create the HTML content
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>BlackwallV2 Memory Usage Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                h1, h2, h3 {{ color: #333; }}
                .metrics-card {{ background-color: white; border: 1px solid #ddd; border-radius: 5px; padding: 15px; margin-bottom: 20px; }}
                .metrics-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
                .metric {{ margin-bottom: 10px; }}
                .metric-label {{ font-weight: bold; color: #555; }}
                .metric-value {{ color: #333; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
                th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f2f2f2; }}
                .chart-container {{ height: 300px; margin: 20px 0; }}
                @media (max-width: 768px) {{ .metrics-grid {{ grid-template-columns: 1fr; }} }}
            </style>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        </head>
        <body>
            <div class="container">
                <h1>BlackwallV2 Memory Usage Report</h1>
                <p>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                <div class="metrics-grid">
                    <div class="metrics-card">
                        <h2>Dream Cycle Summary</h2>
                        <div class="metric">
                            <span class="metric-label">Total Cycles:</span>
                            <span class="metric-value">{report['dream_cycles']['total']}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Last Cycle Time:</span>
                            <span class="metric-value">{report['dream_cycles']['last_cycle_time']}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Last Cycle Duration:</span>
                            <span class="metric-value">{report['dream_cycles']['last_cycle_duration']:.2f} seconds</span>
                        </div>
                    </div>
                    
                    <div class="metrics-card">
                        <h2>Consolidation Metrics</h2>
                        <div class="metric">
                            <span class="metric-label">Total Memories Processed:</span>
                            <span class="metric-value">{report['consolidation_metrics']['total_memories_processed']}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Total Consolidations:</span>
                            <span class="metric-value">{report['consolidation_metrics']['total_consolidations']}</span>
                        </div>
                        <div class="metric">
                            <span class="metric-label">Insights Generated:</span>
                            <span class="metric-value">{report['consolidation_metrics']['insights_generated']}</span>
                        </div>
                    </div>
                </div>
                
                <div class="metrics-card">
                    <h2>Current Memory Usage</h2>
                    <div class="metrics-grid">
                        <div>
                            <h3>Process Memory</h3>
                            <div class="metric">
                                <span class="metric-label">RSS:</span>
                                <span class="metric-value">
                                    {report['memory_metrics']['current_usage'].get('process_memory_info', {}).get('rss', 0):.2f} MB
                                </span>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Virtual Memory:</span>
                                <span class="metric-value">
                                    {report['memory_metrics']['current_usage'].get('process_memory_info', {}).get('vms', 0):.2f} MB
                                </span>
                            </div>
                        </div>
                        
                        <div>
                            <h3>BlackwallV2 Memory</h3>
                            <div class="metric">
                                <span class="metric-label">LTM Object Size:</span>
                                <span class="metric-value">
                                    {report['memory_metrics']['current_usage'].get('blackwall_memory', {}).get('ltm_object_size', 0):.2f} MB
                                </span>
                            </div>
                            <div class="metric">
                                <span class="metric-label">LTM Entry Count:</span>
                                <span class="metric-value">
                                    {report['memory_metrics']['current_usage'].get('blackwall_memory', {}).get('ltm_entry_count', 0)}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
        """
        
        # Add consolidation efficiency section if available
        if 'consolidation_efficiency' in report:
            html += f"""
                <div class="metrics-card">
                    <h2>Consolidation Efficiency</h2>
                    <div class="metrics-grid">
                        <div>
                            <div class="metric">
                                <span class="metric-label">Average Entry Reduction:</span>
                                <span class="metric-value">
                                    {report['consolidation_efficiency']['average_entry_reduction_percent']:.2f}%
                                </span>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Average Size Reduction:</span>
                                <span class="metric-value">
                                    {report['consolidation_efficiency']['average_size_reduction_percent']:.2f}%
                                </span>
                            </div>
                            <div class="metric">
                                <span class="metric-label">Cycles with Metrics:</span>
                                <span class="metric-value">
                                    {report['consolidation_efficiency']['cycles_with_metrics']}
                                </span>
                            </div>
                        </div>
                        
                        <div>
                            <div class="chart-container">
                                <canvas id="efficiencyChart"></canvas>
                            </div>
                        </div>
                    </div>
                </div>
            """
        
        # Add savings history table if available
        if report.get('consolidation_efficiency', {}).get('recent_savings'):
            html += """
                <div class="metrics-card">
                    <h2>Recent Consolidation Savings</h2>
                    <table>
                        <tr>
                            <th>Timestamp</th>
                            <th>Entries Before</th>
                            <th>Entries After</th>
                            <th>Entries Reduction</th>
                            <th>Size Before (MB)</th>
                            <th>Size After (MB)</th>
                            <th>Size Reduction</th>
                        </tr>
            """
            
            for saving in report['consolidation_efficiency']['recent_savings']:
                html += f"""
                        <tr>
                            <td>{saving.get('timestamp', '')}</td>
                            <td>{saving.get('entries_before', 0)}</td>
                            <td>{saving.get('entries_after', 0)}</td>
                            <td>{saving.get('percent_reduction_entries', 0):.2f}%</td>
                            <td>{saving.get('size_before_mb', 0):.2f}</td>
                            <td>{saving.get('size_after_mb', 0):.2f}</td>
                            <td>{saving.get('percent_reduction_size', 0):.2f}%</td>
                        </tr>
                """
            
            html += """
                    </table>
                </div>
            """
        
        # Add JavaScript for chart if data is available
        if report.get('consolidation_efficiency', {}).get('recent_savings'):
            savings = report['consolidation_efficiency']['recent_savings']
            
            timestamps = [s.get('timestamp', '').split('T')[0] + ' ' + 
                          s.get('timestamp', '').split('T')[1].split('.')[0] 
                          for s in savings]
            entry_reductions = [s.get('percent_reduction_entries', 0) for s in savings]
            size_reductions = [s.get('percent_reduction_size', 0) for s in savings]
            
            html += f"""
                <script>
                    document.addEventListener('DOMContentLoaded', function() {{
                        const ctx = document.getElementById('efficiencyChart').getContext('2d');
                        new Chart(ctx, {{
                            type: 'line',
                            data: {{
                                labels: {str(timestamps).replace("'", '"')},
                                datasets: [
                                    {{
                                        label: 'Entry Reduction (%)',
                                        data: {entry_reductions},
                                        borderColor: 'rgba(75, 192, 192, 1)',
                                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                        tension: 0.1
                                    }},
                                    {{
                                        label: 'Size Reduction (%)',
                                        data: {size_reductions},
                                        borderColor: 'rgba(153, 102, 255, 1)',
                                        backgroundColor: 'rgba(153, 102, 255, 0.2)',
                                        tension: 0.1
                                    }}
                                ]
                            }},
                            options: {{
                                responsive: true,
                                maintainAspectRatio: false,
                                scales: {{
                                    y: {{
                                        beginAtZero: true,
                                        title: {{
                                            display: true,
                                            text: 'Reduction Percentage'
                                        }}
                                    }}
                                }}
                            }}
                        }});
                    }});
                </script>
            """
        
        # Close the HTML
        html += """
            </div>
        </body>
        </html>
        """
        
        # Write to file
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html)
            self.log_dream_activity(f"Memory visualization report generated at {output_path}", "INFO")
            return output_path
        except Exception as e:
            self.log_dream_activity(f"Error generating memory visualization: {e}", "ERROR")
            return ""