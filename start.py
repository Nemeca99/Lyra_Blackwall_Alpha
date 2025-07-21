#!/usr/bin/env python3
"""
Quantum Discord Bot - Standalone Startup Script
This script can run the bot independently from any location
"""

import sys
import os
import asyncio

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

if __name__ == "__main__":
    # Import the main bot function
    from core.quantum_discord_bot import main

    print("🚀 **STARTING QUANTUM DISCORD BOT**")
    print("=" * 50)
    print("🎯 Production-ready bot with all Phase 3 features")
    print("⚡ AI Queue System integrated")
    print("🔧 All systems initialized")
    print("📁 Running from:", current_dir)
    print("=" * 50)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Bot shutdown requested")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        sys.exit(1)
