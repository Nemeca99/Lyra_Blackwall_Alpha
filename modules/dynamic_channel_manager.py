"""
Dynamic Channel Manager for Mycelium Network
Manages channel monitoring based on categories and user commands
"""

import json
import logging
from typing import Dict, List, Set, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class ChannelConfig:
    """Channel configuration data"""

    channel_id: int
    channel_name: str
    category_name: str
    is_public: bool
    requires_consent: bool
    added_by: str
    added_at: str
    active: bool = True


class DynamicChannelManager:
    """
    Dynamic channel management system
    - Automatically monitors all Public category channels
    - Allows manual addition/removal of private channels
    - Manages consent requirements per channel
    """

    def __init__(self):
        self.channels_file = "dynamic_channels.json"
        self.channels: Dict[int, ChannelConfig] = {}
        self.public_category_names = ["Public", "public", "PUBLIC"]
        self.private_category_names = ["Private", "private", "PRIVATE"]

        # Load existing channel configurations
        self.load_channels()

    def load_channels(self):
        """Load channel configurations from file"""
        if Path(self.channels_file).exists():
            try:
                with open(self.channels_file, "r") as f:
                    data = json.load(f)
                    for channel_id_str, channel_data in data.items():
                        channel_id = int(channel_id_str)
                        self.channels[channel_id] = ChannelConfig(**channel_data)
                logger.info(f"✅ Loaded {len(self.channels)} channel configurations")
            except Exception as e:
                logger.error(f"❌ Error loading channel configurations: {e}")

    def save_channels(self):
        """Save channel configurations to file"""
        try:
            data = {}
            for channel_id, config in self.channels.items():
                data[str(channel_id)] = asdict(config)

            with open(self.channels_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"✅ Saved {len(self.channels)} channel configurations")
        except Exception as e:
            logger.error(f"❌ Error saving channel configurations: {e}")

    def is_public_category(self, category_name: str) -> bool:
        """Check if category is considered public"""
        return category_name in self.public_category_names

    def is_private_category(self, category_name: str) -> bool:
        """Check if category is considered private"""
        return category_name in self.private_category_names

    def should_monitor_channel(
        self, channel_id: int, category_name: str, channel_name: str
    ) -> bool:
        """
        Determine if a channel should be monitored
        - Always monitor public category channels
        - Only monitor private channels if explicitly added
        """
        # Check if channel is already configured
        if channel_id in self.channels:
            return self.channels[channel_id].active

        # Auto-monitor public category channels
        if self.is_public_category(category_name):
            # Add to configuration automatically
            self.add_channel_auto(channel_id, channel_name, category_name, True)
            return True

        # Don't monitor private channels unless explicitly added
        return False

    def add_channel_auto(
        self, channel_id: int, channel_name: str, category_name: str, is_public: bool
    ):
        """Automatically add channel to monitoring (for public channels)"""
        if channel_id not in self.channels:
            config = ChannelConfig(
                channel_id=channel_id,
                channel_name=channel_name,
                category_name=category_name,
                is_public=is_public,
                requires_consent=not is_public,  # Private channels require consent
                added_by="system",
                added_at=datetime.now().isoformat(),
            )
            self.channels[channel_id] = config
            self.save_channels()
            logger.info(f"✅ Auto-added channel: {channel_name} ({category_name})")

    def add_private_channel(
        self, channel_id: int, channel_name: str, category_name: str, added_by: str
    ) -> bool:
        """Manually add a private channel to monitoring"""
        if channel_id in self.channels:
            # Update existing configuration
            self.channels[channel_id].active = True
            self.channels[channel_id].added_by = added_by
            self.channels[channel_id].added_at = datetime.now().isoformat()
            logger.info(f"✅ Re-activated private channel: {channel_name}")
        else:
            # Add new private channel
            config = ChannelConfig(
                channel_id=channel_id,
                channel_name=channel_name,
                category_name=category_name,
                is_public=False,
                requires_consent=True,  # Private channels always require consent
                added_by=added_by,
                added_at=datetime.now().isoformat(),
            )
            self.channels[channel_id] = config
            logger.info(f"✅ Added private channel: {channel_name}")

        self.save_channels()
        return True

    def remove_private_channel(self, channel_id: int, removed_by: str) -> bool:
        """Remove a private channel from monitoring"""
        if channel_id in self.channels:
            config = self.channels[channel_id]
            if config.is_public:
                logger.warning(f"⚠️ Cannot remove public channel: {config.channel_name}")
                return False

            config.active = False
            config.added_by = f"{removed_by} (removed)"
            self.save_channels()
            logger.info(f"✅ Removed private channel: {config.channel_name}")
            return True

        return False

    def get_monitored_channels(self) -> List[ChannelConfig]:
        """Get all actively monitored channels"""
        return [config for config in self.channels.values() if config.active]

    def get_public_channels(self) -> List[ChannelConfig]:
        """Get all public channels"""
        return [
            config
            for config in self.channels.values()
            if config.active and config.is_public
        ]

    def get_private_channels(self) -> List[ChannelConfig]:
        """Get all private channels"""
        return [
            config
            for config in self.channels.values()
            if config.active and not config.is_public
        ]

    def get_channel_config(self, channel_id: int) -> Optional[ChannelConfig]:
        """Get configuration for specific channel"""
        return self.channels.get(channel_id)

    def requires_consent(self, channel_id: int) -> bool:
        """Check if channel requires consent for monitoring"""
        config = self.get_channel_config(channel_id)
        return config.requires_consent if config else True

    def is_channel_monitored(self, channel_id: int) -> bool:
        """Check if channel is actively monitored"""
        config = self.get_channel_config(channel_id)
        return config.active if config else False

    def get_channel_status_embed(self) -> Dict:
        """Get channel status for embed display"""
        monitored = self.get_monitored_channels()
        public = self.get_public_channels()
        private = self.get_private_channels()

        return {
            "total_monitored": len(monitored),
            "public_channels": len(public),
            "private_channels": len(private),
            "public_list": [f"#{c.channel_name}" for c in public[:5]],  # Show first 5
            "private_list": [f"#{c.channel_name}" for c in private[:5]],  # Show first 5
        }

    def handle_channel_command(
        self,
        command: str,
        channel_id: int,
        channel_name: str,
        category_name: str,
        user_id: str,
    ) -> str:
        """Handle channel management commands"""
        command_lower = command.lower()

        if command_lower in ["!add_channel", "!monitor_channel"]:
            if self.is_public_category(category_name):
                return "✅ This public channel is already monitored automatically!"
            else:
                success = self.add_private_channel(
                    channel_id, channel_name, category_name, user_id
                )
                return (
                    "✅ Private channel added to monitoring!"
                    if success
                    else "❌ Failed to add channel"
                )

        elif command_lower in ["!remove_channel", "!stop_monitoring"]:
            success = self.remove_private_channel(channel_id, user_id)
            return (
                "✅ Private channel removed from monitoring!"
                if success
                else "❌ Failed to remove channel"
            )

        elif command_lower == "!channel_status":
            return self.get_channel_status_text()

        return None

    def get_channel_status_text(self) -> str:
        """Get channel status as text"""
        status = self.get_channel_status_embed()

        text = f"📊 **Channel Monitoring Status**\n\n"
        text += f"🔍 **Total Monitored:** {status['total_monitored']}\n"
        text += f"🌐 **Public Channels:** {status['public_channels']}\n"
        text += f"🔒 **Private Channels:** {status['private_channels']}\n\n"

        if status["public_list"]:
            text += "🌐 **Public Channels:**\n"
            text += "\n".join(status["public_list"]) + "\n\n"

        if status["private_list"]:
            text += "🔒 **Private Channels:**\n"
            text += "\n".join(status["private_list"]) + "\n\n"

        text += "💡 **Commands:**\n"
        text += "• `!add_channel` - Add private channel to monitoring\n"
        text += "• `!remove_channel` - Remove private channel from monitoring\n"
        text += "• `!channel_status` - Show current monitoring status"

        return text
