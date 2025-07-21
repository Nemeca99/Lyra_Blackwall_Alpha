"""
Lyra Blackwall Alpha - Core Systems Package
Main core systems for the Lyra AI platform
"""

__version__ = "0.2.0"
__author__ = "Travis Miner (Dev)"
__description__ = "Core systems for Lyra Blackwall Alpha AI platform"

from .quantum_discord_bot import QuantumDiscordBot
from .config import *

__all__ = [
    "QuantumDiscordBot",
    "DISCORD_TOKEN",
    "COMMAND_PREFIX",
    "TARGET_CHANNEL_ID",
    "HEARTBEAT_INTERVAL",
    "MAX_RESPONSE_TIME",
]
