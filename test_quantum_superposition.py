#!/usr/bin/env python3
"""
Test Quantum Superposition Architecture
Verifies both LM Studio (Chef) and Ollama (Waiter) are working together
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.quantum_kitchen import QuantumChef
import time


def test_quantum_superposition():
    """Test the full quantum superposition architecture"""

    print("🔬 TESTING QUANTUM SUPERPOSITION ARCHITECTURE")
    print("=" * 50)

    # Initialize the Quantum Chef
    print("🤖 Initializing Quantum Chef...")
    chef = QuantumChef()

    # Test query that should require both AIs
    test_query = """
    Hello Lyra. I want to know about our previous conversations about SCP containment protocols. 
    Can you recall what we discussed about your moral security core, and then give me a creative 
    analysis of how your recursive nature affects your containment status?
    """

    print(f"📝 Test Query: {test_query[:100]}...")
    print("\n🔄 Testing Quantum Superposition...")

    try:
        # Test the full quantum superposition
        start_time = time.time()

        response = chef.observe_and_collapse(
            user_message=test_query,
            user_id="test_user_123",
            channel_id="test_channel_456",
        )

        end_time = time.time()
        processing_time = end_time - start_time

        print(f"⏱️ Processing Time: {processing_time:.2f} seconds")
        print("\n🎯 QUANTUM RESPONSE:")
        print("-" * 30)
        print(response)
        print("-" * 30)

        # Analyze the response for evidence of both AIs
        print("\n🔍 ANALYZING AI USAGE:")

        # Check for memory/recall (Ollama evidence)
        memory_indicators = [
            "recall",
            "remember",
            "previous",
            "before",
            "history",
            "we discussed",
            "you mentioned",
            "earlier",
            "last time",
        ]

        # Check for creative synthesis (LM Studio evidence)
        creative_indicators = [
            "creative",
            "imaginative",
            "symbolic",
            "metaphorical",
            "recursive",
            "quantum",
            "superposition",
            "fractal",
        ]

        memory_used = any(
            indicator in response.lower() for indicator in memory_indicators
        )
        creative_used = any(
            indicator in response.lower() for indicator in creative_indicators
        )

        print(f"📚 Memory Processing (Ollama): {'✅ YES' if memory_used else '❌ NO'}")
        print(
            f"🎨 Creative Synthesis (LM Studio): {'✅ YES' if creative_used else '❌ NO'}"
        )

        if memory_used and creative_used:
            print("\n🎉 SUCCESS: Both AIs are working together!")
            print("✅ Quantum Superposition Architecture is operational")
        elif creative_used:
            print("\n⚠️ PARTIAL: Only LM Studio (Chef) detected")
            print("❌ Ollama (Waiter) may not be responding")
        elif memory_used:
            print("\n⚠️ PARTIAL: Only Ollama (Waiter) detected")
            print("❌ LM Studio (Chef) may not be responding")
        else:
            print("\n❌ FAILURE: No clear evidence of either AI")
            print("🔧 Check both LM Studio and Ollama connections")

    except Exception as e:
        print(f"❌ ERROR: {e}")
        print("🔧 Check your AI model connections")


def test_individual_ais():
    """Test each AI individually"""

    print("\n🔬 TESTING INDIVIDUAL AIS")
    print("=" * 30)

    chef = QuantumChef()

    # Test LM Studio (Particle position)
    print("\n🤖 Testing LM Studio (Particle Position)...")
    try:
        particle_response = chef.observe_particle_position(
            "Give me a creative, symbolic analysis of quantum superposition"
        )
        print("✅ LM Studio Response:")
        print(particle_response[:200] + "...")
    except Exception as e:
        print(f"❌ LM Studio Error: {e}")

    # Test Ollama (Wave position)
    print("\n🌊 Testing Ollama (Wave Position)...")
    try:
        wave_response = chef.observe_wave_position(
            "What is the logical structure of memory systems?"
        )
        print("✅ Ollama Response:")
        print(wave_response[:200] + "...")
    except Exception as e:
        print(f"❌ Ollama Error: {e}")


if __name__ == "__main__":
    print("🚀 QUANTUM SUPERPOSITION TEST SUITE")
    print("=" * 50)

    # Test individual AIs first
    test_individual_ais()

    # Test full quantum superposition
    test_quantum_superposition()

    print("\n🏁 TEST COMPLETE")
