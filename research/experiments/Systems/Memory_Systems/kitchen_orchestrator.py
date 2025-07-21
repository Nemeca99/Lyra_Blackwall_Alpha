"""
Kitchen Orchestrator - Coordinates Kitchen Staff and Executive Chef
Part of the Michelin-Star AI Kitchen Architecture

Role: Central coordinator that manages communication between:
- Kitchen Staff (Ollama) - manages public memory and ingredients
- Executive Chef (LM Studio) - creates personalized responses
- Discord (Restaurant) - customer interface and delivery
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass

# Import our kitchen components
from kitchen_staff import KitchenStaffManager, MemoryIngredient
from discord_kitchen_interface import KitchenInterfaceManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ChefOrder:
    """Order from Discord to the Executive Chef"""

    user_id: str
    message_content: str
    format_type: str  # 'text', 'image', 'video', 'music'
    context: Optional[str] = None
    priority: str = "normal"  # 'low', 'normal', 'high', 'urgent'
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class ChefResponse:
    """Response from Executive Chef back to Discord"""

    user_id: str
    response_content: str
    format_type: str
    ingredients_used: MemoryIngredient
    response_metadata: Dict
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class KitchenOrchestrator:
    """
    Main orchestrator for the Michelin-Star AI Kitchen
    Coordinates all operations between Kitchen Staff and Executive Chef
    """

    def __init__(self, discord_token: str, target_channel_id: int):
        self.kitchen_staff = KitchenStaffManager()
        self.discord_interface = KitchenInterfaceManager(
            discord_token, target_channel_id
        )
        self.active_orders = {}
        self.order_queue = asyncio.Queue()
        self.is_running = False

        logger.info("🎭 Kitchen Orchestrator initialized")

    async def start_kitchen(self):
        """Start the complete kitchen system"""
        logger.info("🚀 Starting Michelin-Star AI Kitchen...")

        self.is_running = True

        # Start Discord interface
        await self.discord_interface.start()

        # Start order processing
        asyncio.create_task(self.process_order_queue())

        # Start kitchen monitoring
        asyncio.create_task(self.monitor_kitchen_health())

        logger.info("✅ Kitchen system started successfully")

    async def stop_kitchen(self):
        """Stop the complete kitchen system"""
        logger.info("🛑 Stopping Michelin-Star AI Kitchen...")

        self.is_running = False

        # Stop Discord interface
        await self.discord_interface.stop()

        logger.info("✅ Kitchen system stopped")

    async def submit_order(self, order: ChefOrder) -> str:
        """
        Submit an order to the kitchen

        Args:
            order: ChefOrder with user request

        Returns:
            Order ID for tracking
        """
        order_id = f"order_{order.user_id}_{int(order.timestamp.timestamp())}"

        # Add to active orders
        self.active_orders[order_id] = order

        # Add to processing queue
        await self.order_queue.put((order_id, order))

        logger.info(f"📋 Order submitted: {order_id} for user {order.user_id}")
        return order_id

    async def process_order_queue(self):
        """Process orders from the queue"""
        logger.info("🔄 Starting order queue processor")

        while self.is_running:
            try:
                # Get next order from queue
                order_id, order = await asyncio.wait_for(
                    self.order_queue.get(), timeout=1.0
                )

                # Process the order
                await self.process_order(order_id, order)

                # Mark order as complete
                self.order_queue.task_done()

            except asyncio.TimeoutError:
                # No orders in queue, continue monitoring
                continue
            except Exception as e:
                logger.error(f"❌ Error processing order: {e}")

    async def process_order(self, order_id: str, order: ChefOrder):
        """
        Process a single order through the kitchen

        Args:
            order_id: Unique order identifier
            order: ChefOrder to process
        """
        logger.info(f"👨‍🍳 Processing order {order_id}")

        try:
            # Step 1: Kitchen Staff prepares ingredients
            ingredients = await self.kitchen_staff.prepare_chef_order(
                user_id=order.user_id,
                order_details={
                    "context": order.context,
                    "format_type": order.format_type,
                    "priority": order.priority,
                },
            )

            logger.info(f"🥘 Ingredients prepared for order {order_id}")

            # Step 2: Executive Chef creates response
            chef_response = await self.create_chef_response(order, ingredients)

            logger.info(f"🎨 Chef response created for order {order_id}")

            # Step 3: Deliver response to Discord
            await self.deliver_response(chef_response)

            # Step 4: Update order status
            self.active_orders[order_id] = {
                "status": "completed",
                "response": chef_response,
                "completed_at": datetime.now(),
            }

            logger.info(f"✅ Order {order_id} completed successfully")

        except Exception as e:
            logger.error(f"❌ Error processing order {order_id}: {e}")

            # Update order status to failed
            self.active_orders[order_id] = {
                "status": "failed",
                "error": str(e),
                "failed_at": datetime.now(),
            }

    async def create_chef_response(
        self, order: ChefOrder, ingredients: MemoryIngredient
    ) -> ChefResponse:
        """
        Create response using Executive Chef (LM Studio)

        Args:
            order: Original order
            ingredients: Prepared ingredients from Kitchen Staff

        Returns:
            ChefResponse with personalized content
        """
        # TODO: Implement actual LM Studio integration
        # For now, create a mock response

        # Prepare context for the chef
        context_prompt = self.prepare_chef_context(order, ingredients)

        # Generate response (mock for now)
        response_content = await self.generate_chef_response(
            context_prompt, order.format_type
        )

        # Create response metadata
        response_metadata = {
            "ingredients_used": {
                "context_summary": ingredients.context_summary,
                "emotion_profile": ingredients.emotion_profile,
                "relevant_memories_count": len(ingredients.relevant_memories),
            },
            "processing_time": datetime.now() - order.timestamp,
            "format_type": order.format_type,
            "priority": order.priority,
        }

        return ChefResponse(
            user_id=order.user_id,
            response_content=response_content,
            format_type=order.format_type,
            ingredients_used=ingredients,
            response_metadata=response_metadata,
        )

    def prepare_chef_context(
        self, order: ChefOrder, ingredients: MemoryIngredient
    ) -> str:
        """Prepare context prompt for the Executive Chef"""

        context = f"""
        EXECUTIVE CHEF CONTEXT:
        
        Customer: {order.user_id}
        Order: {order.message_content}
        Format: {order.format_type}
        Priority: {order.priority}
        
        INGREDIENTS FROM KITCHEN STAFF:
        Context Summary: {ingredients.context_summary}
        Emotion Profile: {ingredients.emotion_profile}
        Recent Interactions: {ingredients.interaction_history[-3:]}
        
        TASK: Create a personalized response that:
        1. Addresses the customer's specific request
        2. Uses the provided context and emotion profile
        3. Maintains the customer's preferred interaction style
        4. Delivers in the requested format ({order.format_type})
        
        RESPONSE:
        """

        return context

    async def generate_chef_response(
        self, context_prompt: str, format_type: str
    ) -> str:
        """
        Generate response using Executive Chef (LM Studio)

        Args:
            context_prompt: Prepared context for the chef
            format_type: Desired output format

        Returns:
            Generated response content
        """
        # TODO: Replace with actual LM Studio API call
        # For now, return a mock response

        mock_responses = {
            "text": f"Thank you for your order! Based on your preferences and our conversation history, here's your personalized response: [Generated content would go here]",
            "image": "Image generation request processed. [Image would be generated here]",
            "video": "Video creation request processed. [Video would be generated here]",
            "music": "Music composition request processed. [Music would be generated here]",
        }

        # Simulate processing time
        await asyncio.sleep(0.5)

        return mock_responses.get(format_type, mock_responses["text"])

    async def deliver_response(self, response: ChefResponse):
        """
        Deliver response back to Discord

        Args:
            response: ChefResponse to deliver
        """
        # TODO: Implement actual Discord delivery
        # For now, just log the response

        logger.info(f"📤 Delivering response to user {response.user_id}")
        logger.info(f"📝 Response content: {response.response_content[:100]}...")
        logger.info(f"🎨 Format: {response.format_type}")

    async def monitor_kitchen_health(self):
        """Monitor overall kitchen health and performance"""
        logger.info("🏥 Starting kitchen health monitor")

        while self.is_running:
            try:
                # Get kitchen status
                kitchen_status = self.kitchen_staff.get_kitchen_report()

                # Check for issues
                if kitchen_status["kitchen_status"]["total_memories"] > 10000:
                    logger.warning("⚠️ High memory usage detected")

                if len(self.active_orders) > 50:
                    logger.warning("⚠️ High order queue detected")

                # Log health status
                logger.info(f"🏥 Kitchen Health: {kitchen_status['system_health']}")

                # Wait before next check
                await asyncio.sleep(60)  # Check every minute

            except Exception as e:
                logger.error(f"❌ Error in kitchen health monitoring: {e}")
                await asyncio.sleep(60)

    def get_kitchen_status(self) -> Dict:
        """Get comprehensive kitchen status"""
        kitchen_status = self.kitchen_staff.get_kitchen_report()

        return {
            "kitchen_status": kitchen_status,
            "active_orders": len(self.active_orders),
            "queue_size": self.order_queue.qsize(),
            "system_running": self.is_running,
            "last_updated": datetime.now().isoformat(),
        }

    async def handle_discord_message(
        self, user_id: str, message: str, format_type: str = "text"
    ) -> str:
        """
        Handle incoming Discord message and create order

        Args:
            user_id: Discord user ID
            message: Message content
            format_type: Desired response format

        Returns:
            Order ID for tracking
        """
        # Create order from Discord message
        order = ChefOrder(
            user_id=user_id,
            message_content=message,
            format_type=format_type,
            context="Discord message",
        )

        # Submit order to kitchen
        order_id = await self.submit_order(order)

        return order_id


# Main kitchen orchestrator instance
kitchen_orchestrator = None


def initialize_kitchen(discord_token: str, target_channel_id: int):
    """Initialize the kitchen orchestrator"""
    global kitchen_orchestrator

    kitchen_orchestrator = KitchenOrchestrator(discord_token, target_channel_id)

    return kitchen_orchestrator


async def start_kitchen_system(discord_token: str, target_channel_id: int):
    """Start the complete kitchen system"""
    global kitchen_orchestrator

    if kitchen_orchestrator is None:
        kitchen_orchestrator = initialize_kitchen(discord_token, target_channel_id)

    await kitchen_orchestrator.start_kitchen()
    return kitchen_orchestrator


async def stop_kitchen_system():
    """Stop the complete kitchen system"""
    global kitchen_orchestrator

    if kitchen_orchestrator:
        await kitchen_orchestrator.stop_kitchen()


if __name__ == "__main__":
    # Test the kitchen orchestrator
    async def test_orchestrator():
        print("🎭 Testing Kitchen Orchestrator...")

        # Initialize kitchen
        orchestrator = initialize_kitchen("test_token", 123456789)

        # Test order submission
        order = ChefOrder(
            user_id="test_user_123",
            message_content="Hello, I need help with my project!",
            format_type="text",
        )

        order_id = await orchestrator.submit_order(order)
        print(f"📋 Order submitted: {order_id}")

        # Get kitchen status
        status = orchestrator.get_kitchen_status()
        print(f"📊 Kitchen Status: {status}")

        print("🎉 Kitchen Orchestrator test completed!")

    asyncio.run(test_orchestrator())
