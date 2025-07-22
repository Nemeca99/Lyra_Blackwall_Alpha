#!/usr/bin/env python3
"""
Quick Start Script for Lyra Blackwall Alpha
Helps users get the system running with all advanced features
"""

import asyncio
import logging
import sys
import os
import subprocess
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("❌ Python 3.8+ required")
        logger.info(f"Current version: {sys.version}")
        return False
    logger.info(f"✅ Python version: {sys.version.split()[0]}")
    return True


def install_dependencies():
    """Install required dependencies"""
    logger.info("📦 Installing dependencies...")

    try:
        # Install base requirements
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        logger.info("✅ Base dependencies installed")

        # Install advanced dependencies
        advanced_deps = [
            "faiss-cpu==1.7.4",
            "sentence-transformers==2.2.2",
            "numpy==1.24.3",
            "aiohttp==3.9.1",
        ]

        for dep in advanced_deps:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])

        logger.info("✅ Advanced dependencies installed")
        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install dependencies: {e}")
        return False


def check_config():
    """Check if configuration is set up"""
    config_file = Path("core/config.py")

    if not config_file.exists():
        logger.error("❌ Configuration file not found")
        logger.info("💡 Copy core/config.example.py to core/config.py and configure it")
        return False

    # Check if Discord token is configured
    try:
        with open(config_file, "r") as f:
            content = f.read()
            if "YOUR_BOT_TOKEN_HERE" in content:
                logger.warning("⚠️ Discord token not configured")
                logger.info("💡 Set DISCORD_BOT_TOKEN in core/config.py")
                return False
    except Exception as e:
        logger.error(f"❌ Error reading config: {e}")
        return False

    logger.info("✅ Configuration looks good")
    return True


async def test_memory_system():
    """Test FAISS and BGE memory system"""
    logger.info("🧠 Testing memory system...")

    try:
        # Test import
        from research.experiments.Dual_AI_System.memory_interface import MemoryInterface

        # Test configuration
        config = {
            "enabled": True,
            "embedding_model": "BAAI/bge-small-en-v1.5",
            "vector_database": "faiss",
            "max_results": 5,
            "similarity_threshold": 0.7,
            "memory_path": "test_memory",
            "index_path": "test_memory/faiss_index",
        }

        # Initialize
        memory = MemoryInterface(config)
        await memory.initialize()

        # Test storage
        success = await memory.store_memory(
            "Test memory for quick start", {"test": True}
        )

        # Test search
        results = await memory.search_memory("test memory")

        # Cleanup
        await memory.shutdown()

        if success and len(results) > 0:
            logger.info("✅ Memory system working")
            return True
        else:
            logger.warning("⚠️ Memory system test incomplete")
            return False

    except ImportError as e:
        logger.warning(f"⚠️ Memory system not available: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Memory system test failed: {e}")
        return False


async def test_lm_studio():
    """Test LM Studio connection"""
    logger.info("🤖 Testing LM Studio...")

    try:
        import aiohttp

        timeout = aiohttp.ClientTimeout(total=5)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get("http://localhost:1234/v1/models") as response:
                if response.status == 200:
                    logger.info("✅ LM Studio is running")
                    return True
                else:
                    logger.warning("⚠️ LM Studio not responding")
                    return False

    except aiohttp.ClientError:
        logger.warning("⚠️ LM Studio not running")
        logger.info("💡 Start LM Studio and run 'lmstudio serve'")
        return False
    except ImportError:
        logger.warning("⚠️ aiohttp not available")
        return False
    except Exception as e:
        logger.error(f"❌ LM Studio test failed: {e}")
        return False


def check_lm_studio_installation():
    """Check if LM Studio is installed"""
    logger.info("🔍 Checking LM Studio installation...")

    # Check common installation paths
    possible_paths = [
        "C:\\Users\\%USERNAME%\\AppData\\Local\\LM Studio\\lmstudio.exe",
        "/Applications/LM Studio.app/Contents/MacOS/LM Studio",
        "~/.local/bin/lmstudio",
    ]

    for path in possible_paths:
        expanded_path = os.path.expanduser(os.path.expandvars(path))
        if os.path.exists(expanded_path):
            logger.info("✅ LM Studio found")
            return True

    logger.warning("⚠️ LM Studio not found")
    logger.info("💡 Download from: https://lmstudio.ai/")
    return False


async def run_integration_tests():
    """Run comprehensive integration tests"""
    logger.info("🧪 Running integration tests...")

    try:
        # Import test module
        from test_integration import run_all_tests

        # Run tests
        success = await run_all_tests()

        if success:
            logger.info("✅ All integration tests passed")
        else:
            logger.warning("⚠️ Some integration tests failed")

        return success

    except ImportError as e:
        logger.warning(f"⚠️ Integration tests not available: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Integration tests failed: {e}")
        return False


def start_bot():
    """Start the Discord bot"""
    logger.info("🚀 Starting Discord bot...")

    try:
        # Import and start bot
        from core.quantum_discord_bot import main

        logger.info("✅ Bot starting...")
        logger.info("💡 Use Ctrl+C to stop the bot")

        # Run the bot
        asyncio.run(main())

    except ImportError as e:
        logger.error(f"❌ Failed to import bot: {e}")
        return False
    except KeyboardInterrupt:
        logger.info("⏹️ Bot stopped by user")
        return True
    except Exception as e:
        logger.error(f"❌ Bot failed to start: {e}")
        return False


async def quick_start():
    """Main quick start function"""
    logger.info("🚀 **LYRA BLACKWALL ALPHA QUICK START**")
    logger.info("=" * 60)

    # Step 1: Check Python version
    if not check_python_version():
        return False

    # Step 2: Install dependencies
    if not install_dependencies():
        return False

    # Step 3: Check configuration
    if not check_config():
        return False

    # Step 4: Check LM Studio installation
    lm_studio_installed = check_lm_studio_installation()

    # Step 5: Test memory system
    memory_working = await test_memory_system()

    # Step 6: Test LM Studio (if installed)
    lm_studio_working = False
    if lm_studio_installed:
        lm_studio_working = await test_lm_studio()

    # Step 7: Run integration tests
    tests_passed = await run_integration_tests()

    # Summary
    logger.info("\n📊 **QUICK START SUMMARY**")
    logger.info("=" * 60)

    status_items = [
        ("Python Version", True),
        ("Dependencies", True),
        ("Configuration", True),
        ("LM Studio Installed", lm_studio_installed),
        ("Memory System", memory_working),
        ("LM Studio Running", lm_studio_working),
        ("Integration Tests", tests_passed),
    ]

    for item, status in status_items:
        icon = "✅" if status else "❌"
        logger.info(f"{icon} {item}")

    # Determine if ready to start
    core_ready = all([status for _, status in status_items[:3]])
    advanced_ready = memory_working and (lm_studio_working or not lm_studio_installed)

    if core_ready and advanced_ready:
        logger.info("\n🎉 **SYSTEM READY!**")
        logger.info("=" * 60)

        # Ask user if they want to start the bot
        try:
            response = input("\n🤖 Start Discord bot now? (y/n): ").lower().strip()
            if response in ["y", "yes"]:
                return start_bot()
            else:
                logger.info("💡 Run 'python start.py' to start the bot later")
                return True
        except KeyboardInterrupt:
            logger.info("\n⏹️ Quick start interrupted")
            return True

    else:
        logger.warning("\n⚠️ **SYSTEM NOT FULLY READY**")
        logger.info("=" * 60)

        if not core_ready:
            logger.error("❌ Core systems not ready. Please fix configuration issues.")

        if not advanced_ready:
            logger.warning("⚠️ Advanced features not ready:")
            if not memory_working:
                logger.info("  - Memory system needs attention")
            if not lm_studio_working and lm_studio_installed:
                logger.info("  - LM Studio needs to be started")

        logger.info("\n💡 Check SETUP_ADVANCED.md for detailed setup instructions")
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(quick_start())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\n⏹️ Quick start interrupted")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Quick start failed: {e}")
        sys.exit(1)
