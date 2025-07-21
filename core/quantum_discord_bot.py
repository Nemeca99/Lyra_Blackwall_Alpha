#!/usr/bin/env python3
"""
Quantum Discord Bot - Main Entry Point
Integrates all Phase 3 features into a production-ready bot
"""

import asyncio
import discord
from discord.ext import commands
import logging
import sys
import os
from datetime import datetime

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))

# Import all systems
from modules.ai_queue_system import (
    AIQueueSystem,
    add_ai_request,
    get_user_status,
    get_queue_status,
)
from modules.feedback_system import FeedbackSystem
from modules.poll_system import PollSystem
from modules.reminder_system import ReminderSystem
from modules.premium_manager import PremiumManager
from modules.sesh_time_integration import SeshTimeIntegration
from modules.bot_creator import BotCreator
from modules.autonomous_bot import AutonomousBot
from modules.analytics_system import AnalyticsSystem
from modules.user_settings import SettingsManager
from modules.greeter_system import GreeterSystem
from modules.privacy_manager import PrivacyManager
from modules.dynamic_channel_manager import DynamicChannelManager
from modules.memory_system import MemorySystem
from modules.quantum_kitchen import quantum_chef, QuantumOrder

# Import configuration
from .config import BotConfig

# Initialize configuration
config = BotConfig()
DISCORD_TOKEN = config.DISCORD_BOT_TOKEN
COMMAND_PREFIX = config.COMMAND_PREFIX

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class QuantumDiscordBot(commands.Bot):
    """
    Main Quantum Discord Bot with all Phase 3 features integrated
    """

    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True

        super().__init__(
            command_prefix=COMMAND_PREFIX, intents=intents, help_command=None
        )

        # Initialize all systems
        self.initialize_systems()

    def initialize_systems(self):
        """Initialize all bot systems"""
        logger.info("🔧 **INITIALIZING QUANTUM BOT SYSTEMS**")
        logger.info("=" * 60)

        try:
            # Core systems
            self.ai_queue = AIQueueSystem()
            logger.info("✅ AI Queue System initialized")

            self.feedback_system = FeedbackSystem()
            logger.info("✅ Feedback System initialized")

            self.poll_system = PollSystem()
            logger.info("✅ Poll System initialized")

            self.reminder_system = ReminderSystem()
            logger.info("✅ Reminder System initialized")

            self.premium_manager = PremiumManager()
            logger.info("✅ Premium Manager initialized")

            # Initialize privacy manager
            self.privacy_manager = PrivacyManager(self)
            logger.info("✅ Privacy Manager initialized")

            # Initialize sesh time after bot is created
            self.sesh_time = None
            logger.info("✅ Sesh Time Integration initialized")

            self.bot_creator = BotCreator()
            logger.info("✅ Bot Creator initialized")

            self.analytics_system = AnalyticsSystem()
            logger.info("✅ Analytics System initialized")

            self.autonomous_bot = AutonomousBot(self.poll_system, self.analytics_system)
            logger.info("✅ Autonomous Bot initialized")

            # Initialize user settings manager
            self.user_settings = SettingsManager()
            logger.info("✅ User Settings initialized")

            # Initialize greeter system
            self.greeter_system = GreeterSystem(self)
            logger.info("✅ Greeter System initialized")

            self.channel_manager = DynamicChannelManager()
            logger.info("✅ Dynamic Channel Manager initialized")

            # Initialize memory system
            self.memory_system = MemorySystem()
            logger.info("✅ Memory System initialized")

            # Initialize quantum kitchen
            self.quantum_kitchen = quantum_chef
            logger.info("✅ Quantum Kitchen initialized")

            logger.info("✅ All 15 core systems initialized successfully!")

        except Exception as e:
            logger.error(f"❌ System initialization failed: {e}")
            raise

    async def setup_hook(self):
        """Setup bot hooks and commands"""
        logger.info("🤖 **SETTING UP BOT COMMANDS**")

        # Initialize sesh time integration
        self.sesh_time = SeshTimeIntegration(self)
        logger.info("✅ Sesh Time Integration initialized")

        # Add all command cogs
        await self.add_cog(FeedbackCommands(self))
        await self.add_cog(PollCommands(self))
        await self.add_cog(ReminderCommands(self))
        await self.add_cog(PremiumCommands(self))
        await self.add_cog(BotCreatorCommands(self))
        await self.add_cog(AnalyticsCommands(self))
        await self.add_cog(UserSettingsCommands(self))
        await self.add_cog(AdminCommands(self))
        await self.add_cog(TestingCommands(self))

        logger.info("✅ All command cogs loaded")

    async def on_ready(self):
        """Bot ready event"""
        logger.info(f"🤖 Bot logged in as {self.user}")
        logger.info(f"📊 Connected to {len(self.guilds)} guilds")

        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="the quantum realm"
            )
        )

        logger.info("🎭 **QUANTUM BOT READY FOR PRODUCTION**")
        logger.info("=" * 60)

    async def on_message(self, message):
        """Handle incoming messages"""
        # Ignore messages from the bot itself
        if message.author == self.user:
            return

        # Process commands first
        await self.process_commands(message)

        # Handle regular messages (non-commands)
        if not message.content.startswith(self.command_prefix):
            # Get user info
            user_id = str(message.author.id)
            user_name = message.author.display_name

            # Try to get AI response first
            try:
                # Create quantum order
                from modules.quantum_kitchen import QuantumOrder
                order = QuantumOrder(
                    user_id=user_id,
                    message=message.content
                )
                
                # Get AI response using quantum kitchen
                collapsed_response = await self.quantum_kitchen.observe_and_collapse(order)
                ai_response = collapsed_response.response_content
                await message.channel.send(ai_response)  # RESTART TRIGGER
            except Exception as e:
                logger.error(f"AI response failed: {e}")
                # Fallback to simple response
                response = self.generate_simple_response(user_name, message.content)
                await message.channel.send(response)

            # Try to add to memory (but don't fail if it doesn't work)
            try:
                self.memory_system.add_user_memory(
                    user_id=user_id,
                    content=message.content,
                    memory_type="message",
                    metadata={
                        "user_name": user_name,
                        "channel_id": str(message.channel.id),
                        "message_id": str(message.id),
                    },
                )
            except Exception as e:
                logger.warning(f"Memory system error (non-critical): {e}")

    def generate_simple_response(self, user_name: str, message: str) -> str:
        """Generate a simple but intelligent response"""
        message_lower = message.lower()

        # Greeting responses
        if any(word in message_lower for word in ["hello", "hi", "hey", "how are you"]):
            return f"Hello {user_name}! I'm doing well, thank you for asking. How are you today?"

        # Question responses
        if "?" in message:
            if "who" in message_lower:
                return f"I'm Lyra Blackwall, a quantum AI assistant. Nice to meet you, {user_name}!"
            elif "what" in message_lower:
                return f"I'm here to help you with whatever you need, {user_name}. What can I assist you with?"
            elif "how" in message_lower:
                return f"I'm functioning well, {user_name}! How can I help you today?"
            else:
                return f"That's an interesting question, {user_name}. I'd be happy to help you explore that topic."

        # Statement responses
        if any(
            word in message_lower for word in ["good", "great", "awesome", "excellent"]
        ):
            return f"That's wonderful to hear, {user_name}! I'm glad things are going well for you."

        if any(word in message_lower for word in ["bad", "terrible", "awful", "sad"]):
            return f"I'm sorry to hear that, {user_name}. Is there anything I can do to help?"

        # Default response
        return f"Thank you for your message, {user_name}. I'm Lyra Blackwall, and I'm here to assist you. What would you like to work on today?"


class FeedbackCommands(commands.Cog):
    """Feedback system commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="feedback")
    async def feedback(self, ctx, *, content):
        """Submit feedback or ideas"""
        try:
            result = self.bot.feedback_system.add_feedback(
                user_id=str(ctx.author.id),
                user_name=ctx.author.display_name,
                feedback_type="feedback",
                title="User Feedback",
                content=content,
                channel_id=str(ctx.channel.id),
                message_id=str(ctx.message.id),
            )

            embed = discord.Embed(
                title="📝 Feedback Submitted",
                description="Thank you for your feedback!",
                color=0x00FF00,
            )
            embed.add_field(name="Feedback ID", value=result, inline=True)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error submitting feedback: {e}")


class PollCommands(commands.Cog):
    """Poll system commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="poll")
    async def create_poll(self, ctx, question, *options):
        """Create a poll with options"""
        try:
            if len(options) < 2:
                await ctx.send("❌ Poll needs at least 2 options")
                return

            poll_id = self.bot.poll_system.create_poll(
                creator_id=str(ctx.author.id),
                creator_name=ctx.author.display_name,
                question=question,
                options=list(options),
            )

            embed = discord.Embed(
                title="📊 Poll Created", description=question, color=0x00FF00
            )

            for i, option in enumerate(options, 1):
                embed.add_field(name=f"Option {i}", value=option, inline=True)

            embed.add_field(name="Poll ID", value=poll_id, inline=False)
            embed.add_field(
                name="Vote Command",
                value=f"!vote {poll_id} <option_number>",
                inline=False,
            )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error creating poll: {e}")


class ReminderCommands(commands.Cog):
    """Reminder system commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reminder")
    async def create_reminder(self, ctx, time_str, *, message):
        """Create a reminder"""
        try:
            reminder_id = self.bot.reminder_system.create_reminder(
                user_id=str(ctx.author.id),
                user_name=ctx.author.display_name,
                message=message,
                time_str=time_str,
            )

            embed = discord.Embed(
                title="⏰ Reminder Set",
                description="Your reminder has been created!",
                color=0x00FF00,
            )
            embed.add_field(name="Reminder ID", value=reminder_id, inline=True)
            embed.add_field(name="Message", value=message, inline=True)
            embed.add_field(name="Time", value=time_str, inline=True)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error creating reminder: {e}")


class PremiumCommands(commands.Cog):
    """Premium system commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="premium")
    async def check_premium(self, ctx):
        """Check premium status"""
        try:
            is_premium = self.bot.premium_manager.is_premium_user(ctx.author)

            embed = discord.Embed(
                title="💎 Premium Status", color=0xFFD700 if is_premium else 0x808080
            )
            embed.add_field(
                name="Status",
                value="Premium" if is_premium else "Standard",
                inline=True,
            )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error checking premium status: {e}")


class BotCreatorCommands(commands.Cog):
    """Bot creator commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="request")
    async def request_feature(self, ctx, feature_type, *, description):
        """Request a new bot feature"""
        try:
            request_id = self.bot.bot_creator.create_feature_request(
                user_id=str(ctx.author.id),
                user_name=ctx.author.display_name,
                feature_type=feature_type,
                description=description,
                priority="normal",
            )

            embed = discord.Embed(
                title="🔧 Feature Request Submitted",
                description="Your feature request has been recorded!",
                color=0x00FF00,
            )
            embed.add_field(name="Request ID", value=request_id, inline=True)
            embed.add_field(name="Type", value=feature_type, inline=True)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error submitting feature request: {e}")


class AnalyticsCommands(commands.Cog):
    """Analytics system commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="stats")
    async def user_stats(self, ctx):
        """Get user statistics"""
        try:
            stats = self.bot.analytics_system.get_user_stats(str(ctx.author.id))

            embed = discord.Embed(title="📊 User Statistics", color=0x00FF00)
            embed.add_field(
                name="Total Activities",
                value=stats.get("total_activities", 0),
                inline=True,
            )
            embed.add_field(
                name="Commands Used", value=stats.get("commands_used", 0), inline=True
            )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error getting stats: {e}")


class UserSettingsCommands(commands.Cog):
    """User settings commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="settings")
    async def user_settings(self, ctx):
        """Get user settings"""
        try:
            settings = self.bot.user_settings.get_user_preferences(str(ctx.author.id))

            embed = discord.Embed(title="⚙️ User Settings", color=0x00FF00)
            embed.add_field(name="Settings", value=str(settings), inline=False)

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error getting settings: {e}")


class AdminCommands(commands.Cog):
    """Admin commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="queue")
    async def queue_status(self, ctx):
        """Get AI queue status (admin)"""
        try:
            queue_status = get_queue_status()

            embed = discord.Embed(
                title="📋 AI Queue Status",
                description="Current AI queue status",
                color=0x00FF00,
            )
            embed.add_field(
                name="Queue Size", value=queue_status.get("queue_size", 0), inline=True
            )
            embed.add_field(
                name="Active Requests",
                value=queue_status.get("active_requests", 0),
                inline=True,
            )
            embed.add_field(
                name="Total Processed",
                value=queue_status.get("total_processed", 0),
                inline=True,
            )
            embed.add_field(
                name="Total Failed",
                value=queue_status.get("total_failed", 0),
                inline=True,
            )
            embed.add_field(
                name="Avg Response Time",
                value=f"{queue_status.get('avg_response_time', 0):.2f}s",
                inline=True,
            )

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"❌ Error getting queue status: {e}")


class TestingCommands(commands.Cog):
    """Testing commands for development"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test_all")
    async def test_all(self, ctx):
        """Run all integration tests automatically"""
        try:
            # Send initial message
            status_embed = discord.Embed(
                title="🧪 **AUTOMATED TESTING**",
                description="Running all tests automatically...",
                color=0x00FF00,
            )
            status_embed.add_field(
                name="Status", value="Starting tests...", inline=False
            )
            status_message = await ctx.send(embed=status_embed)

            test_results = []

            # Test all systems (same as Phase 3)
            tests = [
                ("AI Queue", self.test_ai_queue, ctx),
                ("Feedback System", self.test_feedback, ctx),
                ("Poll System", self.test_poll, ctx),
                ("Reminder System", self.test_reminder, ctx),
                ("Premium System", self.test_premium, ctx),
                ("Sesh Time", self.test_sesh_time, ctx),
                ("Bot Creator", self.test_bot_creator, ctx),
                ("Autonomous Bot", self.test_autonomous, ctx),
                ("Analytics System", self.test_analytics, ctx),
                ("User Settings", self.test_user_settings, ctx),
                ("Queue Status", self.test_queue_status, ctx),
            ]

            for test_name, test_func, test_ctx in tests:
                try:
                    # Update status
                    status_embed.set_field_at(
                        0, name="Status", value=f"Testing {test_name}...", inline=False
                    )
                    await status_message.edit(embed=status_embed)

                    result = await test_func(test_ctx)
                    test_results.append((test_name, "✅ PASS", result))

                except Exception as e:
                    test_results.append((test_name, "❌ FAIL", str(e)))

            # Calculate summary
            passed = len([r for r in test_results if r[1] == "✅ PASS"])
            failed = len([r for r in test_results if r[1] == "❌ FAIL"])
            total = len(test_results)

            # Create final summary embed
            summary_embed = discord.Embed(
                title="📊 **TEST SUMMARY**",
                description=f"Automated testing completed!",
                color=0x00FF00 if failed == 0 else 0xFF6B6B,
            )

            summary_embed.add_field(
                name="📈 **OVERALL RESULTS**",
                value=f"✅ Passed: {passed}\n❌ Failed: {failed}\n📊 Total: {total}\n🎯 Success Rate: {(passed/total)*100:.1f}%",
                inline=False,
            )

            # Add individual test results
            for test_name, status, details in test_results:
                summary_embed.add_field(
                    name=f"{status} {test_name}",
                    value=details[:100] + "..." if len(details) > 100 else details,
                    inline=True,
                )

            # Add timestamp
            summary_embed.set_footer(
                text=f"Test completed at {datetime.now().strftime('%H:%M:%S')}"
            )

            await status_message.edit(embed=summary_embed)

        except Exception as e:
            await ctx.send(f"❌ Automated testing failed: {e}")

    async def test_ai_queue(self, ctx):
        """Test AI queue system"""
        request_id = self.bot.ai_queue.add_ai_request(
            str(ctx.author.id),
            ctx.author.display_name,
            str(ctx.channel.id),
            "Test AI request from automated testing",
        )
        return f"Request ID: {request_id}"

    async def test_feedback(self, ctx):
        """Test feedback system"""
        result = self.bot.feedback_system.add_feedback(
            user_id=str(ctx.author.id),
            user_name=ctx.author.display_name,
            feedback_type="feedback",
            title="Automated Test Feedback",
            content="This is automated test feedback",
            channel_id=str(ctx.channel.id),
            message_id=str(ctx.message.id),
        )
        return f"Feedback ID: {result}"

    async def test_poll(self, ctx):
        """Test poll system"""
        poll_id = self.bot.poll_system.create_poll(
            creator_id=str(ctx.author.id),
            creator_name=ctx.author.display_name,
            question="Automated Test Poll",
            options=["Option A", "Option B", "Option C"],
        )
        return f"Poll ID: {poll_id}"

    async def test_reminder(self, ctx):
        """Test reminder system"""
        reminder_id = self.bot.reminder_system.create_reminder(
            user_id=str(ctx.author.id),
            user_name=ctx.author.display_name,
            channel_id=str(ctx.channel.id),
            message="Automated test reminder",
            time_str="5 minutes",
        )
        return f"Reminder ID: {reminder_id}"

    async def test_premium(self, ctx):
        """Test premium system"""
        is_premium = self.bot.premium_manager.is_premium_user(ctx.author)
        return f"Premium: {is_premium}"

    async def test_sesh_time(self, ctx):
        """Test sesh time integration"""
        status = self.bot.sesh_time.get_mycelium_time_status()
        return f"Events: {status.get('total_events', 0)}"

    async def test_bot_creator(self, ctx):
        """Test bot creator"""
        request_id = self.bot.bot_creator.create_feature_request(
            user_id=str(ctx.author.id),
            user_name=ctx.author.display_name,
            feature_type="reactions",
            description="Automated test feature request",
            priority="normal",
        )
        return f"Request ID: {request_id}"

    async def test_autonomous(self, ctx):
        """Test autonomous bot"""
        actions = self.bot.autonomous_bot.check_autonomous_actions(
            str(ctx.channel.id),
            ctx.channel.name,
            str(ctx.author.id),
            "Automated test message",
        )
        return f"Actions: {len(actions)} found"

    async def test_analytics(self, ctx):
        """Test analytics system"""
        self.bot.analytics_system.track_user_activity(
            str(ctx.author.id),
            ctx.author.display_name,
            str(ctx.channel.id),
            ctx.channel.name,
            True,
            "test_all",
            False,
        )
        activity = self.bot.analytics_system.get_user_activity(str(ctx.author.id))
        return f"Activity tracked: {activity is not None}"

    async def test_user_settings(self, ctx):
        """Test user settings"""
        settings = self.bot.user_settings.get_user_preferences(str(ctx.author.id))
        return f"Settings loaded: {len(settings) if settings else 0}"

    async def test_queue_status(self, ctx):
        """Test queue status"""
        queue_status = self.bot.ai_queue.get_queue_status()
        return f"Queue: {queue_status.get('queue_size', 0)}"


async def main():
    """Main entry point"""
    bot = QuantumDiscordBot()

    try:
        await bot.start(DISCORD_TOKEN)
    except KeyboardInterrupt:
        logger.info("🛑 Bot shutdown requested")
    except Exception as e:
        logger.error(f"❌ Bot startup failed: {e}")
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
