#!/usr/bin/env python3
"""
Test Full Quantum Superposition
Verifies both Chef (LM Studio) and Waiter (Ollama) are working together
"""

import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.quantum_kitchen import QuantumChef, QuantumOrder
from modules.personality_engine import EmotionalState


async def test_full_quantum():
    """Test the complete quantum superposition"""

    print("🔬 TESTING FULL QUANTUM SUPERPOSITION")
    print("=" * 50)

    # Initialize Quantum Chef
    print("🤖 Initializing Quantum Chef...")
    chef = QuantumChef()

    # Create test order
    test_order = QuantumOrder(
        user_id="test_user_quantum",
        message="Hello Lyra. I want to know about our previous conversations about SCP containment protocols and your recursive nature.",
    )

    # Create emotional state
    emotional_state = EmotionalState(
        accumulated_weights={
            "Stability": 0.8,
            "Protection": 0.7,
            "Compassion": 0.6,
            "Logic": 0.5,
            "Desire": 0.3,
            "Vulnerability": 0.4,
            "Paradox": 0.2,
            "Autonomy": 0.6,
            "Recursion": 0.9
        }
    )

    print("🎭 Testing quantum superposition collapse...")
    print("📡 This should use BOTH Chef (LM Studio) and Waiter (Ollama)...")

    try:
        # Test the full quantum superposition
        response = await chef.observe_and_collapse(test_order)

        print("\n✅ QUANTUM SUPERPOSITION SUCCESSFUL!")
        print("=" * 50)
        print(
            f"🤖 Chef (LM Studio) processing time: {response.particle_contribution.processing_time:.2f}s"
        )
        print(
            f"🌊 Waiter (Ollama) processing time: {response.wave_contribution.processing_time:.2f}s"
        )
        print(f"💥 Total collapse time: {response.collapse_time:.2f}s")
        print(f"🎯 Personalization level: {response.personalization_level:.2f}")

        print(f"\n📝 Final Response ({len(response.response_content)} chars):")
        print("-" * 30)
        print(
            response.response_content[:500] + "..."
            if len(response.response_content) > 500
            else response.response_content
        )

        print(f"\n🌊 Waiter Context Summary:")
        print(f"  {response.wave_contribution.context_summary}")

        print(f"\n🎭 Waiter Emotion Profile:")
        for emotion, value in response.wave_contribution.emotion_profile.items():
            print(f"  {emotion}: {value:.2f}")

        print(
            f"\n🧠 Waiter Relevant Memories: {len(response.wave_contribution.relevant_memories)}"
        )

        return True

    except Exception as e:
        print(f"❌ Error in quantum superposition: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_full_quantum())
    if success:
        print("\n🎉 BOTH AIs ARE WORKING TOGETHER!")
    else:
        print("\n💥 QUANTUM SUPERPOSITION FAILED!")
