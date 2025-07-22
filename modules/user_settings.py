"""
User Settings Management System
Manages user preferences and settings for the quantum bot
"""

import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class UserSettings:
    """User settings data structure"""

    user_id: str
    user_name: str
    last_updated: str

    # Privacy settings
    allow_memory_storage: bool = True
    allow_analytics: bool = True
    share_feedback_anonymously: bool = False

    # Notification preferences
    enable_notifications: bool = True
    notify_on_updates: bool = True
    notify_on_features: bool = True
    quiet_mode: bool = False

    # Interaction preferences
    response_length: str = "normal"  # "short", "normal", "detailed"
    personality_mode: str = (
        "balanced"  # "professional", "friendly", "casual", "technical"
    )
    auto_respond: bool = True
    use_emojis: bool = True

    # Memory preferences
    memory_retention_days: int = 30
    auto_cleanup_old_memories: bool = True
    memory_priority: str = "normal"  # "low", "normal", "high"

    # Channel preferences
    preferred_channels: list = None
    ignore_channels: list = None
    auto_monitor_channels: bool = True

    # Custom preferences
    timezone: str = "UTC"
    language: str = "en"
    theme_preference: str = "auto"  # "light", "dark", "auto"

    def __post_init__(self):
        if self.preferred_channels is None:
            self.preferred_channels = []
        if self.ignore_channels is None:
            self.ignore_channels = []


class SettingsManager:
    """
    User Settings Management System
    - Manages user preferences and settings
    - Provides easy settings viewing and modification
    - Supports default settings and customization
    """

    def __init__(self):
        self.settings_file = "user_settings.json"
        self.default_settings_file = "default_settings.json"
        self.user_settings: Dict[str, UserSettings] = {}

        # Load existing settings
        self.load_all_settings()
        self.create_default_settings()

    def create_default_settings(self):
        """Create default settings template"""
        default_settings = {
            "privacy": {
                "allow_memory_storage": True,
                "allow_analytics": True,
                "share_feedback_anonymously": False,
            },
            "notifications": {
                "enable_notifications": True,
                "notify_on_updates": True,
                "notify_on_features": True,
                "quiet_mode": False,
            },
            "interaction": {
                "response_length": "normal",
                "personality_mode": "balanced",
                "auto_respond": True,
                "use_emojis": True,
            },
            "memory": {
                "memory_retention_days": 30,
                "auto_cleanup_old_memories": True,
                "memory_priority": "normal",
            },
            "channels": {
                "preferred_channels": [],
                "ignore_channels": [],
                "auto_monitor_channels": True,
            },
            "custom": {"timezone": "UTC", "language": "en", "theme_preference": "auto"},
        }

        try:
            with open(self.default_settings_file, "w") as f:
                json.dump(default_settings, f, indent=2)
            logger.info("✅ Created default settings template")
        except Exception as e:
            logger.error(f"❌ Error creating default settings: {e}")

    def load_all_settings(self):
        """Load all user settings from file"""
        if Path(self.settings_file).exists():
            try:
                with open(self.settings_file, "r") as f:
                    data = json.load(f)
                    for user_id, settings_data in data.items():
                        self.user_settings[user_id] = UserSettings(**settings_data)
                logger.info(f"✅ Loaded {len(self.user_settings)} user settings")
            except Exception as e:
                logger.error(f"❌ Error loading settings: {e}")

    def save_all_settings(self):
        """Save all user settings to file"""
        try:
            data = {}
            for user_id, settings in self.user_settings.items():
                data[user_id] = asdict(settings)

            with open(self.settings_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"✅ Saved {len(self.user_settings)} user settings")
        except Exception as e:
            logger.error(f"❌ Error saving settings: {e}")

    def get_user_settings(self, user_id: str) -> UserSettings:
        """Get user settings, create default if not exists"""
        if user_id not in self.user_settings:
            # Create default settings for new user
            settings = UserSettings(
                user_id=user_id,
                user_name="Unknown User",
                last_updated=datetime.now().isoformat(),
            )
            self.user_settings[user_id] = settings
            self.save_all_settings()

        return self.user_settings[user_id]

    def update_user_settings(
        self, user_id: str, user_name: str, updates: Dict[str, Any]
    ) -> bool:
        """Update user settings"""
        try:
            settings = self.get_user_settings(user_id)
            settings.user_name = user_name
            settings.last_updated = datetime.now().isoformat()

            # Apply updates
            for key, value in updates.items():
                if hasattr(settings, key):
                    setattr(settings, key, value)

            self.save_all_settings()
            logger.info(f"✅ Updated settings for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Error updating settings: {e}")
            return False

    def reset_user_settings(self, user_id: str) -> bool:
        """Reset user settings to defaults"""
        try:
            if user_id in self.user_settings:
                del self.user_settings[user_id]
                self.save_all_settings()
                logger.info(f"✅ Reset settings for user {user_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"❌ Error resetting settings: {e}")
            return False

    def handle_settings_command(
        self, command: str, user_id: str, user_name: str, content: str
    ) -> str:
        """Handle settings commands"""
        command_lower = command.lower()

        if command_lower == "!settings":
            return self.get_settings_display(user_id, user_name)

        elif command_lower == "!settings_help":
            return self.get_settings_help()

        elif command_lower.startswith("!set_"):
            return self.handle_setting_update(command, user_id, user_name, content)

        elif command_lower == "!reset_settings":
            if self.reset_user_settings(user_id):
                return (
                    "✅ **Settings reset!** Your settings have been reset to defaults."
                )
            else:
                return "❌ Error resetting settings. Please try again."

        elif command_lower == "!settings_export":
            return self.export_user_settings(user_id)

        return None

    def get_settings_display(self, user_id: str, user_name: str) -> str:
        """Get formatted settings display"""
        settings = self.get_user_settings(user_id)

        response = f"⚙️ **Settings for {user_name}**\n\n"

        # Privacy Settings
        response += "🔒 **Privacy Settings:**\n"
        response += (
            f"   Memory Storage: {'✅' if settings.allow_memory_storage else '❌'}\n"
        )
        response += f"   Analytics: {'✅' if settings.allow_analytics else '❌'}\n"
        response += f"   Anonymous Feedback: {'✅' if settings.share_feedback_anonymously else '❌'}\n\n"

        # Notification Settings
        response += "🔔 **Notification Settings:**\n"
        response += (
            f"   Notifications: {'✅' if settings.enable_notifications else '❌'}\n"
        )
        response += (
            f"   Update Notifications: {'✅' if settings.notify_on_updates else '❌'}\n"
        )
        response += f"   Feature Notifications: {'✅' if settings.notify_on_features else '❌'}\n"
        response += f"   Quiet Mode: {'✅' if settings.quiet_mode else '❌'}\n\n"

        # Interaction Settings
        response += "💬 **Interaction Settings:**\n"
        response += f"   Response Length: {settings.response_length.title()}\n"
        response += f"   Personality: {settings.personality_mode.title()}\n"
        response += f"   Auto Respond: {'✅' if settings.auto_respond else '❌'}\n"
        response += f"   Use Emojis: {'✅' if settings.use_emojis else '❌'}\n\n"

        # Memory Settings
        response += "🧠 **Memory Settings:**\n"
        response += f"   Retention Days: {settings.memory_retention_days}\n"
        response += (
            f"   Auto Cleanup: {'✅' if settings.auto_cleanup_old_memories else '❌'}\n"
        )
        response += f"   Priority: {settings.memory_priority.title()}\n\n"

        # Custom Settings
        response += "🎨 **Custom Settings:**\n"
        response += f"   Timezone: {settings.timezone}\n"
        response += f"   Language: {settings.language.upper()}\n"
        response += f"   Theme: {settings.theme_preference.title()}\n\n"

        response += f"📅 Last Updated: {settings.last_updated[:10]}"

        return response

    def get_settings_help(self) -> str:
        """Get settings help information"""
        help_text = "⚙️ **Settings System Help**\n\n"
        help_text += "**Commands:**\n"
        help_text += "• `!settings` - View your current settings\n"
        help_text += "• `!settings_help` - Show this help\n"
        help_text += "• `!reset_settings` - Reset to default settings\n"
        help_text += "• `!settings_export` - Export your settings\n\n"
        help_text += "**Setting Updates:**\n"
        help_text += (
            "• `!set_privacy [setting] [true/false]` - Update privacy settings\n"
        )
        help_text += "• `!set_notifications [setting] [true/false]` - Update notification settings\n"
        help_text += (
            "• `!set_interaction [setting] [value]` - Update interaction settings\n"
        )
        help_text += "• `!set_memory [setting] [value]` - Update memory settings\n"
        help_text += "• `!set_custom [setting] [value]` - Update custom settings\n\n"
        help_text += "**Examples:**\n"
        help_text += "• `!set_privacy allow_memory_storage false`\n"
        help_text += "• `!set_interaction response_length detailed`\n"
        help_text += "• `!set_custom timezone EST`\n\n"
        help_text += "**Available Values:**\n"
        help_text += "• Response Length: short, normal, detailed\n"
        help_text += (
            "• Personality: professional, friendly, casual, technical, balanced\n"
        )
        help_text += "• Memory Priority: low, normal, high\n"
        help_text += "• Theme: light, dark, auto"

        return help_text

    def handle_setting_update(
        self, command: str, user_id: str, user_name: str, content: str
    ) -> str:
        """Handle setting update commands"""
        try:
            # Parse command: !set_category setting value
            parts = content.split()
            if len(parts) < 4:
                return "❌ Invalid format. Use: `!set_category setting value`"

            category = parts[1]
            setting_name = parts[2]
            value = " ".join(parts[3:])

            # Convert value to appropriate type
            if value.lower() in ["true", "yes", "on", "1"]:
                value = True
            elif value.lower() in ["false", "no", "off", "0"]:
                value = False
            elif value.isdigit():
                value = int(value)

            # Update setting
            updates = {setting_name: value}
            if self.update_user_settings(user_id, user_name, updates):
                return f"✅ **Setting updated!** {category}.{setting_name} = {value}"
            else:
                return "❌ Error updating setting. Please try again."

        except Exception as e:
            logger.error(f"❌ Error handling setting update: {e}")
            return "❌ Error updating setting. Please check the format."

    def export_user_settings(self, user_id: str) -> str:
        """Export user settings as JSON"""
        try:
            settings = self.get_user_settings(user_id)
            settings_dict = asdict(settings)

            # Create export filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_filename = f"settings_export_{user_id}_{timestamp}.json"

            with open(export_filename, "w") as f:
                json.dump(settings_dict, f, indent=2)

            return f"📁 **Settings exported!** Saved as `{export_filename}`"
        except Exception as e:
            logger.error(f"❌ Error exporting settings: {e}")
            return "❌ Error exporting settings. Please try again."

    def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Get user preferences for bot behavior"""
        settings = self.get_user_settings(user_id)
        return {
            "response_length": settings.response_length,
            "personality_mode": settings.personality_mode,
            "use_emojis": settings.use_emojis,
            "quiet_mode": settings.quiet_mode,
            "allow_memory_storage": settings.allow_memory_storage,
            "memory_retention_days": settings.memory_retention_days,
            "preferred_channels": settings.preferred_channels,
            "ignore_channels": settings.ignore_channels,
        }
