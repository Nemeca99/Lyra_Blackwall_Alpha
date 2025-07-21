"""
Configuration file for Quantum Discord Bot
Easy customization of bot settings and behavior

COPY THIS FILE TO config.py AND ADD YOUR ACTUAL TOKENS
"""

import os
from typing import Dict, Any


class BotConfig:
    """Configuration management for Quantum Discord Bot"""

    def __init__(self):
        # Discord Bot Configuration
        self.DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
        if (
            not self.DISCORD_BOT_TOKEN
            or self.DISCORD_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE"
        ):
            raise ValueError("DISCORD_BOT_TOKEN environment variable is required")

        self.TARGET_CHANNEL_ID = int(
            os.getenv("TARGET_CHANNEL_ID", "YOUR_CHANNEL_ID_HERE")
        )

        # Command Configuration
        self.COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "!")

        # Connection Management
        self.HEARTBEAT_INTERVAL = int(
            os.getenv("HEARTBEAT_INTERVAL", "600")
        )  # 10 minutes
        self.MAX_RESPONSE_TIME = int(os.getenv("MAX_RESPONSE_TIME", "300"))  # 5 minutes
        self.RATE_LIMIT_DELAY = float(os.getenv("RATE_LIMIT_DELAY", "1.0"))  # 1 second

        # Quantum Processing
        self.QUANTUM_TIMEOUT = int(os.getenv("QUANTUM_TIMEOUT", "30"))  # 30 seconds
        self.COLLAPSE_THRESHOLD = float(os.getenv("COLLAPSE_THRESHOLD", "0.8"))  # 80%

        # Memory System
        self.MEMORY_RETENTION_DAYS = int(os.getenv("MEMORY_RETENTION_DAYS", "30"))
        self.MAX_MEMORY_SIZE = int(
            os.getenv("MAX_MEMORY_SIZE", "1000")
        )  # 1000 entries per user

        # Privacy Settings
        self.REQUIRE_UNANIMOUS_CONSENT = (
            os.getenv("REQUIRE_UNANIMOUS_CONSENT", "true").lower() == "true"
        )
        self.DEFAULT_CONSENT = os.getenv("DEFAULT_CONSENT", "false").lower() == "true"

        # Greeter System
        self.SEND_WELCOME_DMS = os.getenv("SEND_WELCOME_DMS", "true").lower() == "true"
        self.WELCOME_ON_FIRST_MESSAGE = (
            os.getenv("WELCOME_ON_FIRST_MESSAGE", "true").lower() == "true"
        )

        # Logging
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.LOG_TO_FILE = os.getenv("LOG_TO_FILE", "false").lower() == "true"
        self.LOG_FILE = os.getenv("LOG_FILE", "quantum_bot.log")

        # Bot Status
        self.BOT_STATUS = os.getenv("BOT_STATUS", "quantum superposition collapse")
        self.BOT_ACTIVITY_TYPE = os.getenv("BOT_ACTIVITY_TYPE", "watching")

    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return {
            "discord": {
                "bot_token": (
                    self.DISCORD_BOT_TOKEN[:20] + "..."
                    if len(self.DISCORD_BOT_TOKEN) > 20
                    else self.DISCORD_BOT_TOKEN
                ),
                "target_channel_id": self.TARGET_CHANNEL_ID,
            },
            "connection": {
                "heartbeat_interval": self.HEARTBEAT_INTERVAL,
                "max_response_time": self.MAX_RESPONSE_TIME,
                "rate_limit_delay": self.RATE_LIMIT_DELAY,
            },
            "quantum": {
                "timeout": self.QUANTUM_TIMEOUT,
                "collapse_threshold": self.COLLAPSE_THRESHOLD,
            },
            "memory": {
                "retention_days": self.MEMORY_RETENTION_DAYS,
                "max_size": self.MAX_MEMORY_SIZE,
            },
            "privacy": {
                "require_unanimous_consent": self.REQUIRE_UNANIMOUS_CONSENT,
                "default_consent": self.DEFAULT_CONSENT,
            },
            "greeter": {
                "send_welcome_dms": self.SEND_WELCOME_DMS,
                "welcome_on_first_message": self.WELCOME_ON_FIRST_MESSAGE,
            },
            "logging": {
                "level": self.LOG_LEVEL,
                "log_to_file": self.LOG_TO_FILE,
                "log_file": self.LOG_FILE,
            },
            "bot_status": {
                "status": self.BOT_STATUS,
                "activity_type": self.BOT_ACTIVITY_TYPE,
            },
        }

    def print_config(self):
        """Print current configuration (safe version)"""
        config = self.get_all_config()
        print("🤖 Quantum Discord Bot Configuration:")
        print("=" * 50)
        for section, settings in config.items():
            print(f"\n📋 {section.upper()}:")
            for key, value in settings.items():
                print(f"  {key}: {value}")
        print("\n" + "=" * 50)


# Global config instance
config = BotConfig()
