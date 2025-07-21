"""
Discord Kitchen Interface - Connects Kitchen Staff to Discord (The Restaurant)
Part of the Michelin-Star AI Kitchen Architecture

Role: Interface between Discord (restaurant) and Kitchen Staff system
Handles public chat monitoring and coordinates with kitchen operations
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import discord
from discord.ext import commands, tasks

# Import our kitchen staff system
from kitchen_staff import KitchenStaffManager, MemoryIngredient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DiscordKitchenInterface:
    """
    Discord interface for the Kitchen Staff system
    Monitors public chat and coordinates with kitchen operations
    """

    def __init__(self, bot_token: str, target_channel_id: int):
        self.bot_token = bot_token
        self.target_channel_id = target_channel_id
        self.kitchen_manager = KitchenStaffManager()
        self.bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
        self.setup_bot_events()

    def setup_bot_events(self):
        """Setup Discord bot event handlers"""

        @self.bot.event
        async def on_ready():
            logger.info(
                f"🍽️ Discord Kitchen Interface ready! Logged in as {self.bot.user}"
            )
            logger.info(f"🎯 Monitoring channel: {self.target_channel_id}")

            # Start monitoring tasks
            self.monitor_public_chat.start()
            self.kitchen_status_report.start()

        @self.bot.event
        async def on_message(message):
            # Ignore bot's own messages
            if message.author == self.bot.user:
                return

            # Only process messages in target channel
            if message.channel.id == self.target_channel_id:
                await self.process_public_message(message)

            # Process commands
            await self.bot.process_commands(message)

        @self.bot.command(name="kitchen_status")
        async def kitchen_status(ctx):
            """Get current kitchen status"""
            if ctx.channel.id == self.target_channel_id:
                status = self.kitchen_manager.get_kitchen_report()
                await ctx.send(
                    f"🍳 **Kitchen Status Report:**\n```json\n{json.dumps(status, indent=2)}```"
                )

        @self.bot.command(name="prepare_ingredients")
        async def prepare_ingredients(ctx, user_id: str):
            """Prepare ingredients for a specific user"""
            if ctx.channel.id == self.target_channel_id:
                try:
                    ingredients = await self.kitchen_manager.prepare_chef_order(
                        user_id=user_id, order_details={"context": "Manual request"}
                    )
                    await ctx.send(
                        f"🥘 **Ingredients prepared for {user_id}:**\n```{ingredients.context_summary}```"
                    )
                except Exception as e:
                    await ctx.send(f"❌ Error preparing ingredients: {e}")

    async def process_public_message(self, message: discord.Message):
        """Process a public Discord message"""
        logger.info(
            f"📝 Processing message from {message.author.id}: {message.content[:50]}..."
        )

        # Extract message data
        message_data = {
            "user_id": str(message.author.id),
            "username": message.author.name,
            "content": message.content,
            "timestamp": message.created_at.isoformat(),
            "channel_id": message.channel.id,
            "message_id": message.id,
        }

        # Process through kitchen staff
        try:
            memory_id = await self.kitchen_manager.kitchen_staff.process_public_message(
                user_id=message_data["user_id"],
                message=message_data["content"],
                emotion_tags=self.detect_emotions(message_data["content"]),
            )
            logger.info(f"✅ Message processed and stored: {memory_id}")

        except Exception as e:
            logger.error(f"❌ Error processing message: {e}")

    def detect_emotions(self, text: str) -> List[str]:
        """Detect emotions in text"""
        emotions = []
        text_lower = text.lower()

        # Enhanced emotion detection
        emotion_keywords = {
            "happy": ["happy", "excited", "great", "awesome", "wonderful", "amazing"],
            "sad": ["sad", "depressed", "down", "unhappy", "miserable"],
            "angry": ["angry", "frustrated", "mad", "irritated", "annoyed"],
            "confused": ["confused", "unsure", "question", "doubt", "uncertain"],
            "surprised": ["wow", "omg", "unexpected", "shocked", "surprised"],
            "calm": ["peaceful", "relaxed", "calm", "serene", "tranquil"],
        }

        for emotion, keywords in emotion_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                emotions.append(emotion)

        return emotions

    @tasks.loop(minutes=5)
    async def monitor_public_chat(self):
        """Monitor public chat for engagement opportunities"""
        try:
            channel = self.bot.get_channel(self.target_channel_id)
            if not channel:
                logger.warning(f"❌ Target channel {self.target_channel_id} not found")
                return

            # Get recent messages (last 10 minutes)
            recent_messages = []
            async for message in channel.history(
                limit=50, after=datetime.now() - timedelta(minutes=10)
            ):
                if message.author != self.bot.user:
                    recent_messages.append(
                        {
                            "user_id": str(message.author.id),
                            "content": message.content,
                            "timestamp": message.created_at,
                        }
                    )

            # Process through kitchen manager
            if recent_messages:
                engagement_candidates = (
                    await self.kitchen_manager.handle_public_chat_monitoring(
                        recent_messages
                    )
                )

                # Log engagement opportunities
                if engagement_candidates:
                    logger.info(f"🎯 Engagement candidates: {engagement_candidates}")

        except Exception as e:
            logger.error(f"❌ Error in public chat monitoring: {e}")

    @tasks.loop(hours=1)
    async def kitchen_status_report(self):
        """Generate periodic kitchen status reports"""
        try:
            status = self.kitchen_manager.get_kitchen_report()
            logger.info(f"📊 Kitchen Status Report: {status}")

        except Exception as e:
            logger.error(f"❌ Error generating kitchen status report: {e}")

    async def start_monitoring(self):
        """Start the Discord kitchen interface"""
        logger.info("🚀 Starting Discord Kitchen Interface...")
        await self.bot.start(self.bot_token)

    async def stop_monitoring(self):
        """Stop the Discord kitchen interface"""
        logger.info("🛑 Stopping Discord Kitchen Interface...")
        await self.bot.close()


# Kitchen Interface Manager - coordinates Discord and Kitchen operations
class KitchenInterfaceManager:
    """Manages the Discord kitchen interface and coordinates operations"""

    def __init__(self, bot_token: str, target_channel_id: int):
        self.interface = DiscordKitchenInterface(bot_token, target_channel_id)
        self.is_running = False

    async def start(self):
        """Start the kitchen interface"""
        if not self.is_running:
            self.is_running = True
            await self.interface.start_monitoring()

    async def stop(self):
        """Stop the kitchen interface"""
        if self.is_running:
            self.is_running = False
            await self.interface.stop_monitoring()

    def get_kitchen_status(self) -> Dict:
        """Get kitchen status"""
        return self.interface.kitchen_manager.get_kitchen_report()

    async def prepare_ingredients_for_user(
        self, user_id: str, context: str = None
    ) -> MemoryIngredient:
        """Prepare ingredients for a specific user"""
        return await self.interface.kitchen_manager.prepare_chef_order(
            user_id=user_id, order_details={"context": context or "General context"}
        )


# Configuration
KITCHEN_CONFIG = {
    "bot_token": "YOUR_DISCORD_BOT_TOKEN_HERE",  # Replace with actual token
    "target_channel_id": 123456789,  # Replace with actual channel ID
    "monitoring_interval": 300,  # 5 minutes
    "status_report_interval": 3600,  # 1 hour
}

# Main kitchen interface instance
kitchen_interface = KitchenInterfaceManager(
    KITCHEN_CONFIG["bot_token"], KITCHEN_CONFIG["target_channel_id"]
)

if __name__ == "__main__":
    # Test the kitchen interface
    async def test_kitchen_interface():
        print("🍽️ Testing Discord Kitchen Interface...")

        # Test kitchen status
        status = kitchen_interface.get_kitchen_status()
        print(f"📊 Kitchen Status: {status}")

        # Test ingredient preparation
        try:
            ingredients = await kitchen_interface.prepare_ingredients_for_user(
                user_id="test_user_123", context="Test context"
            )
            print(f"🥘 Prepared ingredients for user: {ingredients.user_id}")
        except Exception as e:
            print(f"❌ Error preparing ingredients: {e}")

        print("🎉 Discord Kitchen Interface test completed!")

    asyncio.run(test_kitchen_interface())
