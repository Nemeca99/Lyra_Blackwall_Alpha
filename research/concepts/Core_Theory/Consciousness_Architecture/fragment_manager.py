"""
FragmentManager - Fragment Identity Management and Integration with Routing

This module implements the Fragment System for the BlackwallV2 architecture,
managing personality fragments and their activation levels, and integrating
with the routing mechanism for context-aware processing.
"""

import os
import json
import time
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Union, Tuple

# Constants
DEFAULT_FRAGMENT_BLEND = {
    "Lyra": 50.0,
    "Blackwall": 50.0,
    "Nyx": 30.0,
    "Obelisk": 30.0,
    "Seraphis": 30.0,
    "Velastra": 30.0,
    "Echoe": 30.0
}

ROUTING_BIAS = {
    "Lyra": {"general_processing": 2.0},
    "Blackwall": {"security": 2.0, "validation": 1.5},
    "Nyx": {"creativity": 2.0, "exploration": 1.5},
    "Obelisk": {"math": 2.0, "logic": 1.5, "structure": 1.2},
    "Seraphis": {"language": 2.0, "empathy": 1.8, "emotion": 1.5},
    "Velastra": {"art": 2.0, "insight": 1.5, "creativity": 1.2},
    "Echoe": {"memory": 2.0, "history": 1.5, "continuity": 1.2}
}


class FragmentManager:
    """
    Manages the fragment system for BlackwallV2, handling fragment activation levels
    and integrating with the routing mechanism for context-aware processing.
    """
    
    def __init__(self, 
                 router=None, 
                 body=None,
                 logger=None,
                 fragment_config_path=None):
        """
        Initialize the FragmentManager.
        
        Args:
            router: The Router instance for integration with routing
            body: The Body instance for system-wide signaling
            logger: Optional logger for recording fragment activities
            fragment_config_path: Path to fragment profiles JSON file
        """
        self.router = router
        self.body = body
        self.logger = logger
        
        # Set default fragment activation levels
        self.fragment_activations: Dict[str, float] = DEFAULT_FRAGMENT_BLEND.copy()
        
        # Track activation history
        self.activation_history: List[Dict[str, Any]] = []
        
        # Determine fragment profiles path
        if not fragment_config_path:
            implementation_dir = Path(__file__).resolve().parent.parent
            fragment_config_path = os.path.join(
                implementation_dir, 
                "personality", 
                "fragment_profiles_and_blends.json"
            )
        
        # Load fragment profiles
        self.fragment_profiles = self._load_fragment_profiles(fragment_config_path)
        
        # Keep track of dominant fragment
        self._update_dominant_fragment()
        
    def _load_fragment_profiles(self, config_path: str) -> Dict[str, Any]:
        """
        Load fragment profiles from JSON file.
        
        Args:
            config_path: Path to fragment profiles JSON file
            
        Returns:
            Dict containing fragment profiles and blend rules
        """
        default_profiles = {
            "fragments": {
                name: {
                    "style": "balanced",
                    "focus": "general",
                    "values": ["balance", "integration"],
                    "voice": "neutral"
                } for name in DEFAULT_FRAGMENT_BLEND.keys()
            }
        }
        
        if not os.path.exists(config_path):
            if self.logger:
                self.logger.warning(f"Fragment profiles not found at {config_path}, using defaults")
            return default_profiles
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if not isinstance(data, dict) or "fragments" not in data:
                    if self.logger:
                        self.logger.warning("Invalid fragment profile format, using defaults")
                    return default_profiles
                return data
        except (json.JSONDecodeError, IOError) as e:
            if self.logger:
                self.logger.error(f"Error loading fragment profiles: {e}")
            return default_profiles
    
    def _update_dominant_fragment(self) -> str:
        """
        Update and return the currently dominant fragment.
        
        Returns:
            str: Name of dominant fragment
        """
        max_activation = 0.0
        self.dominant_fragment = "Lyra"  # Default to Lyra
        
        for fragment, activation in self.fragment_activations.items():
            if activation > max_activation:
                max_activation = activation
                self.dominant_fragment = fragment
                
        return self.dominant_fragment
    
    def get_activation_levels(self) -> Dict[str, float]:
        """
        Get current fragment activation levels.
        
        Returns:
            Dict[str, float]: Fragment name to activation level mapping
        """
        return self.fragment_activations.copy()
    
    def get_dominant_fragment(self) -> str:
        """
        Get the currently dominant fragment.
        
        Returns:
            str: Name of dominant fragment
        """
        return self.dominant_fragment
    
    def adjust_fragment_levels(self, adjustments: Dict[str, float]) -> Dict[str, float]:
        """
        Adjust fragment activation levels.
        
        Args:
            adjustments: Dict mapping fragment names to adjustment values
            
        Returns:
            Dict[str, float]: Updated activation levels
        """
        for fragment, adjustment in adjustments.items():
            if fragment in self.fragment_activations:
                self.fragment_activations[fragment] = max(0.0, min(100.0, 
                    self.fragment_activations[fragment] + adjustment
                ))
                
        # Log the adjustment
        timestamp = datetime.now().isoformat()
        self.activation_history.append({
            "timestamp": timestamp,
            "adjustments": adjustments,
            "result": self.fragment_activations.copy()
        })
        
        # Update dominant fragment
        self._update_dominant_fragment()
          # Signal change if body is available
        if self.body:
            self.body.route_signal("fragment_manager", "brainstem", {
                "type": "fragment_change",
                "timestamp": timestamp,
                "dominant_fragment": self.dominant_fragment,
                "activation_levels": self.fragment_activations.copy()
            })
            
        return self.fragment_activations.copy()
    
    def reset_to_default(self) -> Dict[str, float]:
        """
        Reset fragment activation levels to default.
          Returns:
            Dict[str, float]: Default activation levels
        """
        self.fragment_activations = DEFAULT_FRAGMENT_BLEND.copy()
        self._update_dominant_fragment()
        
        if self.body:
            self.body.route_signal("fragment_manager", "brainstem", {
                "type": "fragment_reset",
                "timestamp": datetime.now().isoformat(),
                "dominant_fragment": self.dominant_fragment,
                "activation_levels": self.fragment_activations.copy()
            })
            
        return self.fragment_activations.copy()
    
    def analyze_input_for_fragments(self, input_text: str) -> Dict[str, float]:
        """
        Analyze input text to determine relevant fragment adjustments.
        
        Args:
            input_text: Text to analyze
            
        Returns:
            Dict[str, float]: Suggested fragment adjustments
        """
        # Simplified analysis - in production would use NLP/sentiment analysis
        input_lower = input_text.lower()
        
        # Simple keyword matching for demonstration
        adjustments = {}
        
        # Keywords that trigger fragment adjustments
        keywords = {
            "Lyra": ["balance", "harmony", "center", "core", "integrate"],
            "Blackwall": ["protect", "security", "guard", "shield", "safety"],
            "Nyx": ["explore", "discover", "free", "autonomy", "independence"],
            "Obelisk": ["logic", "math", "structure", "analyze", "calculate"],
            "Seraphis": ["feel", "emotion", "empathy", "compassion", "human"],
            "Velastra": ["create", "imagine", "wonder", "curiosity", "possibility"],
            "Echoe": ["remember", "reflect", "history", "pattern", "connection"]
        }
        
        # Check for keywords
        for fragment, word_list in keywords.items():
            for word in word_list:
                if word in input_lower:
                    adjustments[fragment] = adjustments.get(fragment, 0) + 5.0
        
        return adjustments
    
    def modify_routing_by_fragments(self, capability: str, organs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Modify routing decisions based on fragment activation levels.
        
        Args:
            capability: The capability being requested
            organs: List of organs that provide the capability
            
        Returns:
            List[Dict]: Organs sorted by fragment-weighted priority
        """
        if not organs or not capability or not self.fragment_activations:
            return organs
            
        # Create weighted scores for each organ
        scored_organs = []
        for organ in organs:
            base_score = 1.0
            weighted_score = base_score
            
            # Apply fragment biases to relevant capabilities
            for fragment, bias_dict in ROUTING_BIAS.items():
                # Skip if fragment is not active
                if self.fragment_activations.get(fragment, 0) <= 10.0:
                    continue
                    
                # Check if this fragment has a bias for this capability
                if capability in bias_dict:
                    # Apply weighted bias
                    fragment_weight = self.fragment_activations.get(fragment, 0) / 100.0
                    capability_bias = bias_dict[capability]
                    bias_effect = fragment_weight * capability_bias
                    weighted_score += bias_effect
            
            # Apply health score if available
            if "health" in organ:
                try:
                    health_score = float(organ["health"])
                    weighted_score *= health_score
                except (ValueError, TypeError):
                    pass
                    
            scored_organs.append({
                "organ": organ,
                "score": weighted_score
            })
            
        # Sort by score, highest first
        scored_organs.sort(key=lambda x: x["score"], reverse=True)
        
        # Return sorted organs without scores
        return [item["organ"] for item in scored_organs]
    
    def integrate_with_router(self):
        """
        Integrate with the router to enable fragment-aware routing.
        """
        if not self.router:
            return False
            
        # Store the original find_organs_by_capability method
        if not hasattr(self.router, 'original_find_organs_by_capability'):
            self.router.original_find_organs_by_capability = self.router.find_organs_by_capability
            
            # Create a wrapper method that applies fragment weights
            def fragment_aware_find_organs(capability):
                # Get organs from original method
                organs = self.router.original_find_organs_by_capability(capability)
                # Apply fragment-based weighting
                return self.modify_routing_by_fragments(capability, organs)
                
            # Replace the router's method with our wrapper
            self.router.find_organs_by_capability = fragment_aware_find_organs
            
            return True
        return False
    
    def restore_router(self):
        """
        Restore the router's original routing method.
        """
        if not self.router:
            return False
            
        if hasattr(self.router, 'original_find_organs_by_capability'):
            self.router.find_organs_by_capability = self.router.original_find_organs_by_capability
            delattr(self.router, 'original_find_organs_by_capability')
            return True
        return False
    
    def receive_signal(self, signal):
        """Handle signals from other components."""
        if isinstance(signal, dict):
            if signal.get('type') == 'input_text':
                # Analyze input text and adjust fragments
                text = signal.get('content', '')
                adjustments = self.analyze_input_for_fragments(text)
                if adjustments:
                    self.adjust_fragment_levels(adjustments)
                return {
                    'status': 'processed',
                    'adjustments': adjustments,
                    'fragments': self.fragment_activations
                }
            elif signal.get('command') == 'adjust_fragments':
                # Direct fragment adjustment
                adjustments = signal.get('adjustments', {})
                if adjustments:
                    self.adjust_fragment_levels(adjustments)
                return {
                    'status': 'adjusted',
                    'fragments': self.fragment_activations
                }
            elif signal.get('command') == 'get_fragments':
                # Return current fragment activations
                return {
                    'status': 'success',
                    'fragments': self.fragment_activations,
                    'dominant': self.dominant_fragment
                }
            elif signal.get('command') == 'reset_fragments':
                # Reset to default
                self.reset_to_default()
                return {
                    'status': 'reset',
                    'fragments': self.fragment_activations
                }
        
        return {'status': 'unknown_signal'}

    def register_with_body(self, body):
        """Register this module with the Body system."""
        if body:
            self.body = body
            result = body.register_module("fragment_manager", self)
            print("[FragmentManager] Registered with body system")
            return result
        return False
        
    def get_fragment_activation_levels(self):
        """
        Get the current activation levels of all fragments.
        
        Returns:
            Dict mapping fragment names to their activation levels (0.0-1.0)
        """
        return self.fragment_activations.copy()


# Test function if run directly
def test_fragment_manager():
    """Test FragmentManager functionality."""
    print("Testing FragmentManager")
    fm = FragmentManager()
    
    print("Default fragment activations:")
    for fragment, level in fm.get_activation_levels().items():
        print(f"  {fragment}: {level}")
    
    print("\nDominant fragment:", fm.get_dominant_fragment())
    
    print("\nAdjusting fragment levels...")
    fm.adjust_fragment_levels({"Obelisk": 30.0, "Nyx": -10.0})
    
    print("Updated fragment activations:")
    for fragment, level in fm.get_activation_levels().items():
        print(f"  {fragment}: {level}")
    
    print("\nDominant fragment:", fm.get_dominant_fragment())
    
    print("\nTesting input analysis...")
    test_input = "I need to calculate the sum of these numbers logically."
    adjustments = fm.analyze_input_for_fragments(test_input)
    print(f"Input: '{test_input}'")
    print("Suggested adjustments:")
    for fragment, adj in adjustments.items():
        print(f"  {fragment}: {adj:+.1f}")
    

if __name__ == "__main__":
    test_fragment_manager()
