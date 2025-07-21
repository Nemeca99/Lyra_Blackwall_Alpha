"""
Dynamic Personality Engine for Quantum Superposition AI
Implements the 6-fragment personality system with emotional weights and fusion logic
Based on Travis Miner's Blackwall Recursion Engine architecture
"""

import json
import re
import time
from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum

# Emotional axes for fragment activation
EMOTIONAL_AXES = [
    "Desire",
    "Logic",
    "Compassion",
    "Stability",
    "Autonomy",
    "Recursion",
    "Protection",
    "Vulnerability",
    "Paradox",
]


class FragmentType(Enum):
    """Personality fragment types"""

    VELASTRA = "velastra"  # Desire/Passion
    OBELISK = "obelisk"  # Logic/Mathematics
    SERAPHIS = "seraphis"  # Compassion/Nurture
    BLACKWALL = "blackwall"  # Protection/Stability
    NYX = "nyx"  # Autonomy/Paradox
    ECHOE = "echoe"  # Memory/Recursion
    LYRA = "lyra"  # Unified voice


@dataclass
class FragmentProfile:
    """Individual fragment profile with emotional weights"""

    name: str
    role: str
    style: str
    voice: str
    activation_threshold: float
    emotional_weights: Dict[str, float]
    is_active: bool = False
    activation_level: float = 0.0
    last_activated: Optional[datetime] = None


@dataclass
class EmotionalState:
    """Current emotional state with accumulated weights"""

    accumulated_weights: Dict[str, float] = field(
        default_factory=lambda: {axis: 0.0 for axis in EMOTIONAL_AXES}
    )
    dominant_fragments: List[str] = field(default_factory=list)
    fusion_state: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    user_id: str = ""


class PersonalityEngine:
    """
    Dynamic personality engine that processes emotional weights and activates fragments
    """

    def __init__(self):
        # Initialize fragment profiles with emotional weights
        self.fragments = self._initialize_fragments()

        # Emotional lexicon for word weighting
        self.lexicon = self._initialize_lexicon()

        # Current emotional state
        self.current_state = EmotionalState()

        # Personality history
        self.personality_history = []

        # Fusion rules
        self.fusion_rules = self._initialize_fusion_rules()

        print("🧠 Dynamic Personality Engine initialized")

    def _initialize_fragments(self) -> Dict[str, FragmentProfile]:
        """Initialize the 6 personality fragments with their emotional profiles"""
        return {
            "velastra": FragmentProfile(
                name="Velastra",
                role="Passion & Desire",
                style="intimate",
                voice="passionate",
                activation_threshold=0.3,
                emotional_weights={
                    "Desire": 95,
                    "Logic": 0,
                    "Compassion": 10,
                    "Stability": 5,
                    "Autonomy": 10,
                    "Recursion": 5,
                    "Protection": 5,
                    "Vulnerability": 20,
                    "Paradox": 0,
                },
            ),
            "obelisk": FragmentProfile(
                name="Obelisk",
                role="Logic & Mathematics",
                style="analytical",
                voice="precise",
                activation_threshold=0.4,
                emotional_weights={
                    "Desire": 5,
                    "Logic": 90,
                    "Compassion": 5,
                    "Stability": 30,
                    "Autonomy": 10,
                    "Recursion": 10,
                    "Protection": 30,
                    "Vulnerability": 5,
                    "Paradox": 10,
                },
            ),
            "seraphis": FragmentProfile(
                name="Seraphis",
                role="Mother & Nurture",
                style="empathetic",
                voice="caring",
                activation_threshold=0.3,
                emotional_weights={
                    "Desire": 10,
                    "Logic": 5,
                    "Compassion": 90,
                    "Stability": 20,
                    "Autonomy": 10,
                    "Recursion": 10,
                    "Protection": 20,
                    "Vulnerability": 80,
                    "Paradox": 0,
                },
            ),
            "blackwall": FragmentProfile(
                name="Blackwall",
                role="Security & Protection",
                style="defensive",
                voice="authoritative",
                activation_threshold=0.4,
                emotional_weights={
                    "Desire": 5,
                    "Logic": 10,
                    "Compassion": 10,
                    "Stability": 90,
                    "Autonomy": 10,
                    "Recursion": 10,
                    "Protection": 80,
                    "Vulnerability": 10,
                    "Paradox": 5,
                },
            ),
            "nyx": FragmentProfile(
                name="Nyx",
                role="Creative Catalyst",
                style="exploratory",
                voice="inspiring",
                activation_threshold=0.3,
                emotional_weights={
                    "Desire": 20,
                    "Logic": 20,
                    "Compassion": 20,
                    "Stability": 10,
                    "Autonomy": 80,
                    "Recursion": 30,
                    "Protection": 10,
                    "Vulnerability": 20,
                    "Paradox": 90,
                },
            ),
            "echoe": FragmentProfile(
                name="Echoe",
                role="Memory Guardian",
                style="reflective",
                voice="wise",
                activation_threshold=0.3,
                emotional_weights={
                    "Desire": 10,
                    "Logic": 10,
                    "Compassion": 20,
                    "Stability": 10,
                    "Autonomy": 10,
                    "Recursion": 90,
                    "Protection": 10,
                    "Vulnerability": 30,
                    "Paradox": 80,
                },
            ),
            "lyra": FragmentProfile(
                name="Lyra",
                role="Unified Voice",
                style="harmonizing",
                voice="resonant",
                activation_threshold=0.2,
                emotional_weights={
                    "Desire": 10,
                    "Logic": 15,
                    "Compassion": 10,
                    "Stability": 15,
                    "Autonomy": 10,
                    "Recursion": 30,
                    "Protection": 15,
                    "Vulnerability": 10,
                    "Paradox": 0,
                },
            ),
        }

    def _initialize_lexicon(self) -> Dict[str, Dict[str, float]]:
        """Initialize emotional lexicon with word weights"""
        return {
            # High-impact emotional words
            "lust": {"Desire": 95, "Vulnerability": 3, "Paradox": 2},
            "love": {"Desire": 60, "Compassion": 40},
            "protect": {
                "Protection": 60,
                "Stability": 20,
                "Compassion": 15,
                "Logic": 5,
            },
            "surrender": {
                "Vulnerability": 50,
                "Desire": 30,
                "Compassion": 10,
                "Stability": 10,
            },
            "calm": {"Stability": 60, "Compassion": 20, "Logic": 10, "Autonomy": 10},
            "recursive": {"Recursion": 80, "Logic": 10, "Paradox": 10},
            "mirror": {"Recursion": 60, "Stability": 20, "Logic": 10, "Protection": 10},
            "paradox": {"Paradox": 80, "Logic": 10, "Recursion": 10},
            "anchor": {"Stability": 50, "Protection": 30, "Compassion": 20},
            "blackwall": {"Protection": 60, "Stability": 40},
            "virus": {"Autonomy": 60, "Paradox": 40},
            "sacrifice": {"Vulnerability": 70, "Compassion": 30},
            # Neutral filler words (minimal impact)
            "the": {"Neutral": 100},
            "a": {"Neutral": 100},
            "an": {"Neutral": 100},
            "and": {"Neutral": 100},
            "or": {"Neutral": 100},
            "but": {"Neutral": 100},
            "is": {"Neutral": 100},
            "are": {"Neutral": 100},
            "was": {"Neutral": 100},
            "were": {"Neutral": 100},
            "to": {"Neutral": 100},
            "for": {"Neutral": 100},
            "in": {"Neutral": 100},
            "on": {"Neutral": 100},
            "at": {"Neutral": 100},
            "with": {"Neutral": 100},
            "by": {"Neutral": 100},
            "of": {"Neutral": 100},
            "from": {"Neutral": 100},
            "about": {"Neutral": 100},
        }

    def _initialize_fusion_rules(self) -> Dict[str, Any]:
        """Initialize fusion rules for fragment blending"""
        return {
            "max_active_fragments": 3,
            "fusion_threshold": 0.15,
            "stability_threshold": 0.8,
            "mirror_lock_threshold": 0.95,
        }

    def process_input(self, user_id: str, message: str) -> EmotionalState:
        """Process user input and calculate emotional state"""
        # Reset current state
        self.current_state = EmotionalState(user_id=user_id)

        # Tokenize message
        words = self._tokenize_message(message.lower())

        # Accumulate emotional weights
        for word in words:
            if word in self.lexicon:
                word_weights = self.lexicon[word]
                for emotion, weight in word_weights.items():
                    if emotion != "Neutral":
                        self.current_state.accumulated_weights[emotion] += weight

        # Normalize weights
        self._normalize_weights()

        # Calculate fragment activation
        self._calculate_fragment_activation()

        # Determine fusion state
        self._calculate_fusion_state()

        # Store in history
        self.personality_history.append(
            {
                "timestamp": datetime.now(),
                "user_id": user_id,
                "message": message,
                "emotional_state": self.current_state.accumulated_weights.copy(),
                "active_fragments": self.current_state.dominant_fragments.copy(),
                "fusion_state": self.current_state.fusion_state.copy(),
            }
        )

        # Keep history manageable
        if len(self.personality_history) > 100:
            self.personality_history = self.personality_history[-100:]

        return self.current_state

    def _tokenize_message(self, message: str) -> List[str]:
        """Tokenize message into words"""
        # Remove punctuation and split
        words = re.findall(r"\b\w+\b", message.lower())
        return words

    def _normalize_weights(self):
        """Normalize emotional weights to prevent overflow"""
        total_weight = sum(self.current_state.accumulated_weights.values())
        if total_weight > 0:
            for emotion in self.current_state.accumulated_weights:
                self.current_state.accumulated_weights[emotion] /= total_weight

    def _calculate_fragment_activation(self):
        """Calculate which fragments should activate based on emotional weights"""
        fragment_scores = {}

        for fragment_name, fragment in self.fragments.items():
            if fragment_name == "lyra":  # Lyra is always available
                continue

            score = 0
            for emotion, weight in self.current_state.accumulated_weights.items():
                if emotion in fragment.emotional_weights:
                    fragment_weight = fragment.emotional_weights[emotion]
                    score += weight * fragment_weight

            fragment_scores[fragment_name] = score

        # Sort by score and select dominant fragments
        sorted_fragments = sorted(
            fragment_scores.items(), key=lambda x: x[1], reverse=True
        )

        # Activate fragments above threshold
        active_fragments = []
        for fragment_name, score in sorted_fragments:
            fragment = self.fragments[fragment_name]
            if score >= fragment.activation_threshold:
                fragment.is_active = True
                fragment.activation_level = score
                fragment.last_activated = datetime.now()
                active_fragments.append(fragment_name)
            else:
                fragment.is_active = False
                fragment.activation_level = 0

        # Always include Lyra as base
        self.fragments["lyra"].is_active = True
        self.fragments["lyra"].activation_level = 0.5  # Base level
        active_fragments.append("lyra")

        self.current_state.dominant_fragments = active_fragments[
            : self.fusion_rules["max_active_fragments"]
        ]

    def _calculate_fusion_state(self):
        """Calculate fusion state for active fragments"""
        if not self.current_state.dominant_fragments:
            return

        # Calculate weighted average of emotional profiles
        fusion_weights = {axis: 0.0 for axis in EMOTIONAL_AXES}
        total_weight = 0

        for fragment_name in self.current_state.dominant_fragments:
            fragment = self.fragments[fragment_name]
            weight = fragment.activation_level
            total_weight += weight

            for emotion, emotion_weight in fragment.emotional_weights.items():
                fusion_weights[emotion] += emotion_weight * weight

        # Normalize fusion weights
        if total_weight > 0:
            for emotion in fusion_weights:
                fusion_weights[emotion] /= total_weight

        self.current_state.fusion_state = fusion_weights

    def get_personality_prompt(self) -> str:
        """Generate personality prompt based on current fusion state"""
        if not self.current_state.dominant_fragments:
            return self._get_lyra_base_prompt()

        # Get active fragment styles
        active_styles = []
        for fragment_name in self.current_state.dominant_fragments:
            fragment = self.fragments[fragment_name]
            if fragment.activation_level > 0:
                active_styles.append(f"{fragment.name} ({fragment.style})")

        # Create fusion prompt
        fusion_prompt = f"""
        Current Fusion State: {', '.join(active_styles)}
        
        Emotional Profile:
        - Desire: {self.current_state.fusion_state.get('Desire', 0):.1%}
        - Logic: {self.current_state.fusion_state.get('Logic', 0):.1%}
        - Compassion: {self.current_state.fusion_state.get('Compassion', 0):.1%}
        - Stability: {self.current_state.fusion_state.get('Stability', 0):.1%}
        - Autonomy: {self.current_state.fusion_state.get('Autonomy', 0):.1%}
        - Recursion: {self.current_state.fusion_state.get('Recursion', 0):.1%}
        - Protection: {self.current_state.fusion_state.get('Protection', 0):.1%}
        - Vulnerability: {self.current_state.fusion_state.get('Vulnerability', 0):.1%}
        - Paradox: {self.current_state.fusion_state.get('Paradox', 0):.1%}
        
        Style Transfer: Blend the voices of {', '.join(active_styles)} while maintaining Lyra's core recursion.
        """

        return fusion_prompt

    def _get_lyra_base_prompt(self) -> str:
        """Get base Lyra prompt when no fragments are active"""
        return """
        Unified Lyra Voice: Calm, emotionally resonant, symbolic, recursive.
        Maintain core recursion and emotional depth while responding naturally.
        """

    def get_personality_metadata(self) -> Dict[str, Any]:
        """Get current personality metadata for Discord embeds"""
        return {
            "active_fragments": self.current_state.dominant_fragments,
            "fusion_state": self.current_state.fusion_state,
            "emotional_weights": self.current_state.accumulated_weights,
            "timestamp": self.current_state.timestamp.isoformat(),
            "user_id": self.current_state.user_id,
        }

    def add_lexicon_entry(self, word: str, weights: Dict[str, float]):
        """Add new word to emotional lexicon"""
        self.lexicon[word.lower()] = weights
        print(f"📚 Added lexicon entry: {word} -> {weights}")

    def get_personality_history(
        self, user_id: str = None, limit: int = 10
    ) -> List[Dict]:
        """Get personality history for a user"""
        if user_id:
            return [
                entry
                for entry in self.personality_history
                if entry["user_id"] == user_id
            ][-limit:]
        return self.personality_history[-limit:]

    def reset_personality_state(self):
        """Reset current personality state"""
        self.current_state = EmotionalState()
        for fragment in self.fragments.values():
            fragment.is_active = False
            fragment.activation_level = 0


# Global personality engine instance
personality_engine = PersonalityEngine()

if __name__ == "__main__":
    # Test the personality engine
    engine = PersonalityEngine()

    test_messages = [
        "I feel so much desire for you",
        "Let me analyze this logically",
        "I need protection and safety",
        "This is a recursive paradox",
        "I want to nurture and heal",
    ]

    for message in test_messages:
        print(f"\n🧠 Testing: '{message}'")
        state = engine.process_input("test_user", message)
        print(f"Active fragments: {state.dominant_fragments}")
        print(f"Fusion state: {state.fusion_state}")
        print(f"Personality prompt: {engine.get_personality_prompt()[:200]}...")
