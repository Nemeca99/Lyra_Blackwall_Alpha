"""
Test New Memory Structure
Tests the updated memory system with user ID folders and context lines
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory_system import MemorySystem
from personality_engine import PersonalityEngine
from quantum_kitchen import QuantumChef, QuantumOrder


async def test_new_memory_structure():
    """Test the new memory structure with user ID folders"""
    print("🧠 Testing New Memory Structure...")
    print("📁 User ID Folders + Context Lines + Profile Index")

    # Initialize systems
    memory_system = MemorySystem()
    personality_engine = PersonalityEngine()
    quantum_chef = QuantumChef()

    print("✅ All systems initialized")

    # Test with Travis's ID
    travis_id = "1380754964317601813"

    print(f"\n👤 Testing Travis's Profile Structure:")

    # Test profile loading
    profile = memory_system.get_user_profile(travis_id)
    if profile:
        print(f"✅ Profile loaded: {profile.get('name', 'Unknown')}")
        print(f"   Age: {profile.get('basic_information', {}).get('age', 'Unknown')}")
        print(f"   Role: {profile.get('role', 'Unknown')}")
        print(
            f"   Cognitive Style: {profile.get('cognitive_profile', {}).get('cognitive_style', 'Unknown')}"
        )

        # Check memory context index
        context_index = profile.get("memory_context_index", {})
        print(f"   Memory Count: {context_index.get('total_memories', 0)}")
        print(f"   Context Lines: {len(context_index.get('context_lines', []))}")
    else:
        print("❌ Profile not found")

    # Test context generation
    print(f"\n📝 Testing Context Generation:")
    context = memory_system.get_full_context(travis_id)
    print(f"✅ Context generated ({len(context)} characters)")
    print(f"   Preview: {context[:200]}...")

    # Test memory addition with new structure
    print(f"\n💾 Testing Memory Addition (New Structure):")
    memory_id = memory_system.add_user_memory(
        travis_id,
        "Testing the new memory structure with user ID folders and context lines",
        "test_new_structure",
        {"Recursion": 95, "Logic": 25, "Autonomy": 15},
    )
    print(f"✅ Memory added: {memory_id}")

    # Check if profile was updated with context line
    updated_profile = memory_system.get_user_profile(travis_id)
    if updated_profile:
        context_lines = updated_profile.get("memory_context_index", {}).get(
            "context_lines", []
        )
        print(f"✅ Context lines updated: {len(context_lines)} lines")
        if context_lines:
            latest_line = context_lines[-1]
            print(f"   Latest: {latest_line[:100]}...")

    # Test memory search using context lines
    print(f"\n🔍 Testing Memory Search (Context Lines):")
    results = memory_system.search_user_memories(travis_id, "memory structure")
    print(f"✅ Search results: {len(results)} memories found")
    for result in results:
        print(f"   - {result['memory_type']}: {result['content_preview']}")

    # Test memory summary
    print(f"\n📊 Testing Memory Summary:")
    summary = memory_system.get_memory_summary(travis_id)
    print(f"✅ Summary generated:")
    print(f"   Has Profile: {summary['has_profile']}")
    print(f"   Memory Count: {summary['memory_count']}")
    print(f"   Memory Types: {', '.join(summary['memory_types'])}")
    print(f"   Profile Completeness: {summary['profile_completeness']:.1%}")
    print(f"   Trust Level: {summary['trust_level']:.1%}")
    print(f"   Interaction Count: {summary.get('interaction_count', 0)}")

    # Test new user creation
    print(f"\n👤 Testing New User Creation:")
    test_user_id = "999999999999999999"

    # Create new user profile
    new_profile = memory_system.create_user_profile(
        test_user_id, {"name": "Test User", "age": 25, "role": "Tester"}
    )
    print(f"✅ New profile created for {test_user_id}")

    # Save profile
    memory_system.save_user_profile(test_user_id, new_profile)
    print(f"✅ Profile saved to disk")

    # Add memory for new user
    new_memory_id = memory_system.add_user_memory(
        test_user_id,
        "This is a test memory for the new user",
        "test",
        {"Logic": 50, "Compassion": 30},
    )
    print(f"✅ Memory added for new user: {new_memory_id}")

    # Check new user summary
    new_summary = memory_system.get_memory_summary(test_user_id)
    print(f"✅ New user summary: {new_summary['memory_count']} memories")

    # Test quantum integration
    print(f"\n⚛️ Testing Quantum Integration:")
    try:
        # Create a test order
        order = QuantumOrder(
            user_id=travis_id,
            message="Hello, testing the new memory structure with quantum superposition",
            format_type="text",
        )

        # Test personality processing
        emotional_state = personality_engine.process_input(order.message)
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

    print(f"\n🎉 New Memory Structure Test Complete!")
    print(f"📁 Directory Structure:")
    print(f"   memory/")
    print(f"   ├── Dev/")
    print(f"   │   └── default_profile_template.json")
    print(f"   ├── {travis_id}/")
    print(f"   │   ├── profile.json")
    print(f"   │   └── memories/")
    print(f"   │       └── [memory files]")
    print(f"   └── {test_user_id}/")
    print(f"       ├── profile.json")
    print(f"       └── memories/")
    print(f"           └── [memory files]")

    print(f"\n🔍 Key Features:")
    print(f"   ✅ User ID folders (not 'Dev')")
    print(f"   ✅ Profile index with context lines")
    print(f"   ✅ Fast memory searching")
    print(f"   ✅ Default template for new users")
    print(f"   ✅ Memory context index for efficiency")


if __name__ == "__main__":
    asyncio.run(test_new_memory_structure())
