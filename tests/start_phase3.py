#!/usr/bin/env python3
"""
Phase 3 Startup Script
Simple startup for Discord integration testing
"""

import os
import sys
import asyncio
from phase3_discord_integration import DiscordIntegrationTester


def main():
    """Start Phase 3 Discord integration testing"""
    print("🚀 **PHASE 3: DISCORD INTEGRATION TESTING**")
    print("=" * 60)

    try:
        # Import config
        from config import config

        # Get Discord token from config
        token = config.DISCORD_BOT_TOKEN
        if not token or token == "YOUR_BOT_TOKEN_HERE":
            print("❌ Discord token not configured in config.py!")
            print("Please set your Discord bot token in config.py")
            return None

        print(f"✅ Discord token loaded from config.py")
        print(f"✅ Target channel: {config.TARGET_CHANNEL_ID}")
        print(f"✅ Heartbeat interval: {config.HEARTBEAT_INTERVAL}s")
        print(f"✅ Max response time: {config.MAX_RESPONSE_TIME}s")

        # Create tester and bot
        tester = DiscordIntegrationTester()
        bot = tester.create_test_bot()

        print("\n✅ **PHASE 3 BOT READY**")
        print("=" * 60)
        print("🤖 Bot created with all test commands")
        print("📋 Available test commands:")
        print("  !test_all - Run all integration tests")
        print("  !test_ai_queue - Test AI queue system")
        print("  !test_feedback - Test feedback system")
        print("  !test_poll - Test poll system")
        print("  !test_reminder - Test reminder system")
        print("  !test_premium - Test premium system")
        print("  !test_sesh - Test Sesh time integration")
        print("  !test_bot_creator - Test bot creator")
        print("  !test_autonomous - Test autonomous bot")
        print("  !test_analytics - Test analytics system")
        print("  !test_user_settings - Test user settings")
        print("  !test_queue_status - Test queue status")

        print(f"\n🎯 **STARTING BOT WITH CONFIG TOKEN**")
        print("Bot will connect using your config.py settings!")

        # Start the bot
        asyncio.run(bot.start(token))

    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        print("Make sure config.py exists and is properly configured")
        return None
    except Exception as e:
        print(f"❌ Phase 3 startup failed: {e}")
        return None


if __name__ == "__main__":
    main()
