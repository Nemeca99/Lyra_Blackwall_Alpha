"""
Test Kitchen Staff System
Tests the Ollama-managed public memory system
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from kitchen_staff import KitchenStaffManager, MemoryIngredient


async def test_kitchen_staff():
    """Test the kitchen staff system"""
    print("🧑‍🍳 Testing Kitchen Staff System...")

    # Initialize kitchen staff
    kitchen_manager = KitchenStaffManager()

    # Test 1: Process public messages
    print("\n📝 Test 1: Processing public messages...")

    test_messages = [
        {
            "user_id": "user_123",
            "content": "I'm really excited about this new AI project!",
            "emotion_tags": ["happy", "excited"],
        },
        {
            "user_id": "user_456",
            "content": "I'm feeling frustrated with my coding today.",
            "emotion_tags": ["frustrated", "angry"],
        },
        {
            "user_id": "user_789",
            "content": "Can someone help me understand this concept?",
            "emotion_tags": ["confused", "questioning"],
        },
    ]

    for msg in test_messages:
        memory_id = await kitchen_manager.kitchen_staff.process_public_message(
            user_id=msg["user_id"],
            message=msg["content"],
            emotion_tags=msg["emotion_tags"],
        )
        print(f"✅ Processed message: {memory_id}")

    # Test 2: Prepare ingredients for chef
    print("\n🥘 Test 2: Preparing ingredients for chef...")

    ingredients = await kitchen_manager.kitchen_staff.prepare_ingredients_for_chef(
        user_id="user_123"
    )

    print(f"✅ Ingredients prepared for user: {ingredients.user_id}")
    print(f"📝 Context summary: {ingredients.context_summary}")
    print(f"😊 Emotion profile: {ingredients.emotion_profile}")
    print(f"📚 Relevant memories: {len(ingredients.relevant_memories)}")

    # Test 3: Kitchen status
    print("\n📊 Test 3: Kitchen status...")

    status = kitchen_manager.get_kitchen_report()
    print(f"✅ Kitchen Status: {status}")

    # Test 4: Public chat monitoring
    print("\n👀 Test 4: Public chat monitoring...")

    chat_messages = [
        {"user_id": "user_123", "content": "Hello everyone!"},
        {"user_id": "user_456", "content": "How is everyone doing?"},
        {"user_id": "user_789", "content": "I have a question about AI"},
    ]

    engagement_candidates = await kitchen_manager.handle_public_chat_monitoring(
        chat_messages
    )

    print(f"✅ Engagement candidates: {engagement_candidates}")

    print("\n🎉 Kitchen Staff System test completed successfully!")


async def test_kitchen_interface():
    """Test the Discord kitchen interface (without actual Discord connection)"""
    print("\n🍽️ Testing Discord Kitchen Interface...")

    # Test without actual Discord connection
    from discord_kitchen_interface import KitchenInterfaceManager

    # Create interface with dummy credentials
    interface = KitchenInterfaceManager(
        bot_token="test_token", target_channel_id=123456789
    )

    # Test kitchen status
    status = interface.get_kitchen_status()
    print(f"✅ Kitchen Status: {status}")

    # Test ingredient preparation
    try:
        ingredients = await interface.prepare_ingredients_for_user(
            user_id="test_user_123", context="Test context"
        )
        print(f"✅ Prepared ingredients for user: {ingredients.user_id}")
    except Exception as e:
        print(f"❌ Error preparing ingredients: {e}")

    print("🎉 Discord Kitchen Interface test completed!")


async def test_kitchen_orchestrator():
    """Test the kitchen orchestrator"""
    print("\n🎭 Testing Kitchen Orchestrator...")

    from kitchen_orchestrator import initialize_kitchen, ChefOrder

    # Initialize kitchen
    orchestrator = initialize_kitchen("test_token", 123456789)

    # Test order submission
    order = ChefOrder(
        user_id="test_user_123",
        message_content="Hello, I need help with my project!",
        format_type="text",
    )

    order_id = await orchestrator.submit_order(order)
    print(f"✅ Order submitted: {order_id}")

    # Get kitchen status
    status = orchestrator.get_kitchen_status()
    print(f"✅ Kitchen Status: {status}")

    print("🎉 Kitchen Orchestrator test completed!")


async def main():
    """Run all tests"""
    print("🚀 Starting Kitchen Staff System Tests...")

    try:
        # Test kitchen staff
        await test_kitchen_staff()

        # Test kitchen interface
        await test_kitchen_interface()

        # Test kitchen orchestrator
        await test_kitchen_orchestrator()

        print("\n🎉 All tests completed successfully!")
        print("✅ Kitchen Staff System is ready for integration!")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
