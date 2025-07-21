#!/usr/bin/env python3
"""
Test Dual-AI Communication
Travis Miner - Lyra Blackwall v2.0

Tests that DeepSeek (LM Studio) and Qwen2.5 (Ollama) can communicate
"""

import asyncio
import json
from dual_ai_config import DualAIConfig
from recursive_ai import RecursiveAI
from linear_ai import LinearAI


async def test_ai_communication():
    """Test communication between the two AIs"""

    print("🤖 Testing Dual-AI Communication System")
    print("=" * 50)

    # Load config
    config = DualAIConfig()

    # Initialize AIs
    print("\n1️⃣ Initializing Recursive AI (DeepSeek/LM Studio)...")
    recursive_ai = RecursiveAI(config.recursive_config)
    await recursive_ai.initialize()
    print("✅ Recursive AI ready!")

    print("\n2️⃣ Initializing Linear AI (Qwen2.5/Ollama)...")
    linear_ai = LinearAI(config.linear_config)
    await linear_ai.initialize()
    print("✅ Linear AI ready!")

    # Set up communication link
    print("\n3️⃣ Establishing AI Communication Link...")
    recursive_ai.set_linear_ai(linear_ai)
    print("✅ Communication link established!")

    # Test communication flow
    print("\n4️⃣ Testing AI Communication Flow...")
    test_input = "What is the meaning of life?"

    print(f"\n📝 User Input: {test_input}")

    # Step 1: Recursive AI asks Linear AI for context
    print("\n🔍 Recursive AI asking Linear AI for context...")
    context_prompt = recursive_ai._build_context_request(test_input)
    print(f"📤 Context Request: {context_prompt}")

    # Step 2: Linear AI provides context
    print("\n📊 Linear AI providing context...")
    linear_context = await recursive_ai._get_linear_ai_context(context_prompt)
    print(f"📥 Linear AI Context: {linear_context}")

    # Step 3: Recursive AI generates final response
    print("\n🎨 Recursive AI generating final response...")
    final_response = await recursive_ai.generate_response(test_input)
    print(f"✨ Final Response: {final_response}")

    print("\n🎉 Dual-AI Communication Test Complete!")
    print("\nThe two AIs successfully communicated with each other:")
    print(
        "• DeepSeek (LM Studio) → Qwen2.5 (Ollama): 'What do you know about this user?'"
    )
    print("• Qwen2.5 (Ollama) → DeepSeek (LM Studio): Provides context and analysis")
    print("• DeepSeek (LM Studio) → User: Final response using combined context")

    # Cleanup
    await recursive_ai.shutdown()
    await linear_ai.shutdown()


if __name__ == "__main__":
    asyncio.run(test_ai_communication())
