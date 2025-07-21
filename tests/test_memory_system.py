"""
Test Memory System Integration with Quantum Superposition AI
Tests the complete memory system with Travis's personal knowledge
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory_system import MemorySystem
from personality_engine import PersonalityEngine
from quantum_kitchen import QuantumChef, QuantumOrder


async def test_memory_system():
    """Test the complete memory system integration"""
    print("🧠 Testing Memory System Integration...")
    print("🔬 With Quantum Superposition AI Architecture")

    # Initialize systems
    memory_system = MemorySystem()
    personality_engine = PersonalityEngine()
    quantum_chef = QuantumChef()

    print("✅ All systems initialized")

    # Test with Travis's ID
    travis_id = "1380754964317601813"

    print(f"\n👤 Testing Travis's Memory Profile:")

    # Test profile loading
    profile = memory_system.get_user_profile(travis_id)
    if profile:
        print(f"✅ Profile loaded: {profile.get('name', 'Unknown')}")
        print(f"   Age: {profile.get('basic_information', {}).get('age', 'Unknown')}")
        print(f"   Role: {profile.get('role', 'Unknown')}")
        print(
            f"   Cognitive Style: {profile.get('cognitive_profile', {}).get('cognitive_style', 'Unknown')}"
        )
    else:
        print("❌ Profile not found")

    # Test context generation
    print(f"\n📝 Testing Context Generation:")
    context = memory_system.get_full_context(travis_id)
    print(f"✅ Context generated ({len(context)} characters)")
    print(f"   Preview: {context[:200]}...")

    # Test personality context
    personality_context = memory_system.get_personality_context(travis_id)
    print(f"✅ Personality context generated ({len(personality_context)} characters)")

    # Test project context
    project_context = memory_system.get_project_context(travis_id)
    print(f"✅ Project context generated ({len(project_context)} characters)")

    # Test emotional context
    emotional_context = memory_system.get_emotional_context(travis_id)
    print(f"✅ Emotional context generated ({len(emotional_context)} characters)")

    # Test memory addition
    print(f"\n💾 Testing Memory Addition:")
    memory_id = memory_system.add_user_memory(
        travis_id,
        "Testing the quantum superposition AI system with integrated memory and personality engine",
        "test",
        {"Recursion": 90, "Logic": 30, "Autonomy": 20},
    )
    print(f"✅ Memory added: {memory_id}")

    # Test memory search
    print(f"\n🔍 Testing Memory Search:")
    results = memory_system.search_user_memories(travis_id, "quantum")
    print(f"✅ Search results: {len(results)} memories found")
    for result in results:
        print(f"   - {result['memory_type']}: {result['content_preview'][:50]}...")

    # Test memory summary
    print(f"\n📊 Testing Memory Summary:")
    summary = memory_system.get_memory_summary(travis_id)
    print(f"✅ Summary generated:")
    print(f"   Has Profile: {summary['has_profile']}")
    print(f"   Memory Count: {summary['memory_count']}")
    print(f"   Memory Types: {', '.join(summary['memory_types'])}")

    # Test quantum integration
    print(f"\n⚛️ Testing Quantum Integration:")
    try:
        # Create a test order
        order = QuantumOrder(
            user_id=travis_id,
            message="Hello, this is a test of the memory system integration",
            format_type="text",
        )

        # Test personality processing
        emotional_state = personality_engine.process_input(travis_id, order.message)
        print(
            f"✅ Personality processing: {len(emotional_state.dominant_fragments)} active fragments"
        )
        print(f"   Dominant: {', '.join(emotional_state.dominant_fragments)}")

        # Test memory context in quantum prompt
        user_context = memory_system.get_full_context(travis_id)
        print(f"✅ Memory context for quantum: {len(user_context)} characters")

        print("✅ Quantum integration test completed")

    except Exception as e:
        print(f"❌ Quantum integration test failed: {e}")

    print(f"\n🎉 Memory System Integration Test Complete!")
    print(f"📚 Memory files loaded: {len(memory_system.user_memories)} Users")
    print(f"🧠 Personality engine: {len(personality_engine.fragments)} fragments")
    print(f"⚛️ Quantum kitchen: Ready for superposition processing")


if __name__ == "__main__":
    asyncio.run(test_memory_system())
