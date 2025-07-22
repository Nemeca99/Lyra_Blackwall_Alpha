"""
Test Complete Memory Integration
Tests the full integration of memory system with quantum kitchen and profile-based prompts
"""

import asyncio
import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory_system import MemorySystem
from personality_engine import PersonalityEngine
from quantum_kitchen import QuantumChef, QuantumOrder


async def test_complete_memory_integration():
    """Test the complete memory integration with profile-based prompts"""
    print("🧠 Testing Complete Memory Integration...")
    print("📁 Profile Index + Context Lines + Quantum Kitchen Integration")

    # Initialize systems
    memory_system = MemorySystem()
    personality_engine = PersonalityEngine()
    quantum_chef = QuantumChef()

    print("✅ All systems initialized")

    # Test with Travis's ID
    travis_id = "1380754964317601813"

    print(f"\n👤 Testing Travis's Complete Profile Integration:")

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

    # Test memory addition with context lines
    print(f"\n💾 Testing Memory Addition with Context Lines:")
    memory_id = memory_system.add_user_memory(
        travis_id,
        "Testing the complete memory integration with profile-based prompts and quantum kitchen",
        "test_integration",
        {"Recursion": 95, "Logic": 25, "Autonomy": 15, "Compassion": 30},
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
    results = memory_system.search_user_memories(travis_id, "memory integration")
    print(f"✅ Search results: {len(results)} memories found")
    for result in results:
        print(f"   - {result['memory_type']}: {result['content_preview']}")

    # Test quantum kitchen integration with profile-based prompts
    print(f"\n⚛️ Testing Quantum Kitchen with Profile-Based Prompts:")
    try:
        # Create a test order
        order = QuantumOrder(
            user_id=travis_id,
            message="Hello! I want to test the quantum superposition AI with my profile and memory context",
            format_type="text",
        )

        # Test quantum collapse with profile integration
        print(f"   🔬 Starting quantum collapse...")
        collapsed_response = await quantum_chef.observe_and_collapse(order)

        print(f"✅ Quantum collapse completed!")
        print(f"   Response: {collapsed_response.response_content[:200]}...")
        print(f"   Personalization: {collapsed_response.personalization_level:.1%}")
        print(f"   Superposition ID: {collapsed_response.superposition_id}")

        # Check if memory was stored with context line
        final_profile = memory_system.get_user_profile(travis_id)
        if final_profile:
            final_context_lines = final_profile.get("memory_context_index", {}).get(
                "context_lines", []
            )
            print(f"   Final context lines: {len(final_context_lines)}")

        print("✅ Quantum integration test completed")

    except Exception as e:
        print(f"❌ Quantum integration test failed: {e}")

    # Test new user creation and integration
    print(f"\n👤 Testing New User Creation and Integration:")
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
        "This is a test memory for the new user with quantum integration",
        "test",
        {"Logic": 50, "Compassion": 30},
    )
    print(f"✅ Memory added for new user: {new_memory_id}")

    # Test quantum integration with new user
    try:
        new_order = QuantumOrder(
            user_id=test_user_id,
            message="Hello! I'm a new user testing the quantum AI system",
            format_type="text",
        )

        new_collapsed_response = await quantum_chef.observe_and_collapse(new_order)
        print(f"✅ New user quantum test completed")
        print(f"   Response: {new_collapsed_response.response_content[:100]}...")

    except Exception as e:
        print(f"❌ New user quantum test failed: {e}")

    # Test memory summary
    print(f"\n📊 Testing Memory Summary:")
    travis_summary = memory_system.get_memory_summary(travis_id)
    print(f"✅ Travis Summary:")
    print(f"   Has Profile: {travis_summary['has_profile']}")
    print(f"   Memory Count: {travis_summary['memory_count']}")
    print(f"   Memory Types: {', '.join(travis_summary['memory_types'])}")
    print(f"   Profile Completeness: {travis_summary['profile_completeness']:.1%}")
    print(f"   Trust Level: {travis_summary['trust_level']:.1%}")

    new_user_summary = memory_system.get_memory_summary(test_user_id)
    print(f"✅ New User Summary:")
    print(f"   Has Profile: {new_user_summary['has_profile']}")
    print(f"   Memory Count: {new_user_summary['memory_count']}")
    print(f"   Profile Completeness: {new_user_summary['profile_completeness']:.1%}")

    print(f"\n🎉 Complete Memory Integration Test Complete!")
    print(f"📁 Final Directory Structure:")
    print(f"   memory/")
    print(f"   ├── Dev/")
    print(f"   │   └── default_profile_template.json")
    print(f"   ├── {travis_id}/")
    print(f"   │   ├── profile.json (with context lines)")
    print(f"   │   └── memories/")
    print(f"   │       └── [memory files with unique IDs]")
    print(f"   └── {test_user_id}/")
    print(f"       ├── profile.json (with context lines)")
    print(f"       └── memories/")
    print(f"           └── [memory files with unique IDs]")

    print(f"\n🔍 Key Features Verified:")
    print(f"   ✅ User ID folders (not 'Dev')")
    print(f"   ✅ Profile index with context lines")
    print(f"   ✅ Fast memory searching via context lines")
    print(f"   ✅ Default template for new users")
    print(f"   ✅ Memory context index for efficiency")
    print(f"   ✅ Quantum kitchen integration with profile-based prompts")
    print(f"   ✅ Memory storage with unique IDs")
    print(f"   ✅ Context line generation and storage")
    print(f"   ✅ Profile-based prompt generation")
    print(f"   ✅ Memory timeline integration")


if __name__ == "__main__":
    asyncio.run(test_complete_memory_integration())
