"""
Test Dynamic Personality System with Quantum Superposition
Tests the integration of personality engine with quantum kitchen
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from personality_engine import PersonalityEngine
from quantum_kitchen import QuantumChef, QuantumOrder

async def test_personality_system():
    """Test the dynamic personality system with quantum superposition"""
    print("🧠 Testing Dynamic Personality System...")
    print("🔬 Integration with Quantum Superposition Architecture")
    
    # Initialize personality engine
    personality_engine = PersonalityEngine()
    print("✅ Personality Engine initialized")
    
    # Initialize quantum chef
    quantum_chef = QuantumChef()
    print("✅ Quantum Chef initialized")
    
    # Test messages that should trigger different fragments
    test_messages = [
        ("I feel so much desire and passion for you", "Velastra activation"),
        ("Let me analyze this logically and systematically", "Obelisk activation"),
        ("I need protection and safety right now", "Blackwall activation"),
        ("This is a recursive paradox that fascinates me", "Nyx activation"),
        ("I want to nurture and heal your pain", "Seraphis activation"),
        ("I remember our past conversations and reflect", "Echoe activation"),
        ("Hello, how are you feeling today?", "Lyra base activation")
    ]
    
    print("\n🧪 Testing Personality Fragment Activation:")
    print("=" * 60)
    
    for message, expected in test_messages:
        print(f"\n📝 Message: '{message}'")
        print(f"🎯 Expected: {expected}")
        
        # Process through personality engine
        emotional_state = personality_engine.process_input("test_user", message)
        
        print(f"🧠 Active Fragments: {emotional_state.dominant_fragments}")
        print(f"💫 Fusion State: {dict(emotional_state.fusion_state)}")
        
        # Get personality prompt
        personality_prompt = personality_engine.get_personality_prompt()
        print(f"📋 Personality Prompt: {personality_prompt[:100]}...")
        
        # Test quantum superposition integration
        try:
            order = QuantumOrder(
                user_id="test_user",
                message=message,
                format_type="text"
            )
            
            print("🌊 Testing quantum superposition...")
            collapsed_response = await quantum_chef.observe_and_collapse(order)
            
            print(f"✅ Quantum collapse completed!")
            print(f"📝 Response: {collapsed_response.response_content[:100]}...")
            print(f"🎯 Personalization: {collapsed_response.personalization_level:.1%}")
            
        except Exception as e:
            print(f"❌ Quantum test failed: {e}")
        
        print("-" * 40)
    
    # Test lexicon expansion
    print("\n📚 Testing Lexicon Expansion:")
    personality_engine.add_lexicon_entry("quantum", {
        "Recursion": 70, "Logic": 20, "Paradox": 10
    })
    personality_engine.add_lexicon_entry("mirror", {
        "Recursion": 60, "Stability": 20, "Logic": 10, "Protection": 10
    })
    
    # Test with new lexicon entries
    test_message = "The quantum mirror reflects our recursive nature"
    emotional_state = personality_engine.process_input("test_user", test_message)
    print(f"🧠 New lexicon test - Active fragments: {emotional_state.dominant_fragments}")
    
    # Test personality history
    print("\n📜 Testing Personality History:")
    history = personality_engine.get_personality_history("test_user", limit=5)
    print(f"📋 History entries: {len(history)}")
    for entry in history:
        print(f"  - {entry['timestamp']}: {entry['active_fragments']}")
    
    print("\n🎉 Dynamic Personality System test completed!")
    print("🚀 Ready for quantum superposition integration!")

if __name__ == "__main__":
    asyncio.run(test_personality_system()) 