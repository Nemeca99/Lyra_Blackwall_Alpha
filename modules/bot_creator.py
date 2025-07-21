"""
Bot Creator System
Allows users to request bot features and integrations
"""

import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
import random

logger = logging.getLogger(__name__)


@dataclass
class BotRequest:
    """Bot feature request data"""

    request_id: str
    user_id: str
    user_name: str
    feature_type: str  # reaction, webhook, cooldown, permission, custom
    description: str
    created_at: str
    status: str = "pending"  # pending, approved, implemented, declined
    priority: str = "normal"  # low, normal, high, urgent
    complexity: str = "medium"  # easy, medium, hard
    estimated_time: str = ""
    admin_notes: str = ""


class BotCreator:
    """
    Bot Creator System
    - Handles feature requests and bot enhancements
    - Provides templates and examples
    - Manages implementation priorities
    - Generates code snippets and integrations
    """

    def __init__(self):
        self.requests_file = "bot_requests.json"
        self.templates_file = "bot_templates.json"
        self.bot_requests: Dict[str, BotRequest] = {}

        # Load existing data
        self.load_creator_data()
        self.create_templates()

    def load_creator_data(self):
        """Load bot creator data"""
        if Path(self.requests_file).exists():
            try:
                with open(self.requests_file, "r") as f:
                    data = json.load(f)
                    for request_id, request_data in data.items():
                        self.bot_requests[request_id] = BotRequest(**request_data)
                logger.info(f"✅ Loaded {len(self.bot_requests)} bot requests")
            except Exception as e:
                logger.error(f"❌ Error loading bot requests: {e}")

    def save_creator_data(self):
        """Save bot creator data"""
        try:
            data = {
                request_id: asdict(request)
                for request_id, request in self.bot_requests.items()
            }
            with open(self.requests_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.info("✅ Saved bot creator data")
        except Exception as e:
            logger.error(f"❌ Error saving bot creator data: {e}")

    def create_templates(self):
        """Create bot feature templates"""
        templates = {
            "reactions": {
                "name": "Reaction System",
                "description": "Add reaction-based interactions to messages",
                "features": [
                    "Basic emoji reactions",
                    "Custom emoji reactions",
                    "Reaction menus",
                    "Reaction-based polls",
                    "Reaction role assignment",
                ],
                "complexity": "easy",
                "estimated_time": "30 minutes",
            },
            "webhooks": {
                "name": "Webhook System",
                "description": "Integrate external services and notifications",
                "features": [
                    "External service integration",
                    "Notification webhooks",
                    "Custom webhook messages",
                    "Webhook management",
                    "Multi-service support",
                ],
                "complexity": "medium",
                "estimated_time": "1 hour",
            },
            "cooldowns": {
                "name": "Cooldown System",
                "description": "Add rate limiting and cooldowns to commands",
                "features": [
                    "Command cooldowns",
                    "User-based rate limiting",
                    "Global cooldowns",
                    "Custom cooldown messages",
                    "Cooldown bypass for admins",
                ],
                "complexity": "easy",
                "estimated_time": "45 minutes",
            },
            "permissions": {
                "name": "Permission System",
                "description": "Advanced permission management and role control",
                "features": [
                    "Role-based permissions",
                    "Channel-specific permissions",
                    "Permission checking",
                    "Role management",
                    "Permission inheritance",
                ],
                "complexity": "medium",
                "estimated_time": "1.5 hours",
            },
            "moderation": {
                "name": "Moderation System",
                "description": "Server moderation and management tools",
                "features": [
                    "User warnings",
                    "Temporary mutes",
                    "Kick/ban functionality",
                    "Moderation logs",
                    "Auto-moderation",
                ],
                "complexity": "hard",
                "estimated_time": "2 hours",
            },
            "welcome": {
                "name": "Welcome System",
                "description": "Welcome new members with custom messages",
                "features": [
                    "Custom welcome messages",
                    "Welcome images",
                    "Role assignment",
                    "Welcome channels",
                    "Welcome DMs",
                ],
                "complexity": "medium",
                "estimated_time": "1 hour",
            },
            "logging": {
                "name": "Logging System",
                "description": "Comprehensive server activity logging",
                "features": [
                    "Message logging",
                    "Member join/leave logs",
                    "Channel activity logs",
                    "Moderation logs",
                    "Custom log channels",
                ],
                "complexity": "medium",
                "estimated_time": "1.5 hours",
            },
            "games": {
                "name": "Game System",
                "description": "Fun games and entertainment features",
                "features": [
                    "Trivia games",
                    "Word games",
                    "Mini-games",
                    "Leaderboards",
                    "Game rewards",
                ],
                "complexity": "hard",
                "estimated_time": "2.5 hours",
            },
            "music": {
                "name": "Music System",
                "description": "Music playback and queue management",
                "features": [
                    "YouTube/SoundCloud integration",
                    "Music queue",
                    "Playlist support",
                    "Volume control",
                    "Music commands",
                ],
                "complexity": "hard",
                "estimated_time": "3 hours",
            },
            "economy": {
                "name": "Economy System",
                "description": "Virtual currency and economy features",
                "features": [
                    "Virtual currency",
                    "Daily rewards",
                    "Shop system",
                    "Gambling games",
                    "Economy leaderboards",
                ],
                "complexity": "hard",
                "estimated_time": "2.5 hours",
            },
        }

        try:
            with open(self.templates_file, "w") as f:
                json.dump(templates, f, indent=2)
            logger.info("✅ Created bot feature templates")
        except Exception as e:
            logger.error(f"❌ Error creating templates: {e}")

    def create_feature_request(
        self,
        user_id: str,
        user_name: str,
        feature_type: str,
        description: str,
        priority: str = "normal",
    ) -> str:
        """Create a new feature request"""
        try:
            # Generate request ID
            request_id = f"request_{user_id}_{int(datetime.now().timestamp())}"

            # Determine complexity and estimated time
            complexity = "medium"
            estimated_time = "1 hour"

            if feature_type in ["reactions", "cooldowns"]:
                complexity = "easy"
                estimated_time = "30-45 minutes"
            elif feature_type in ["moderation", "games", "music", "economy"]:
                complexity = "hard"
                estimated_time = "2-3 hours"

            # Create request
            request = BotRequest(
                request_id=request_id,
                user_id=user_id,
                user_name=user_name,
                feature_type=feature_type,
                description=description,
                created_at=datetime.now().isoformat(),
                priority=priority,
                complexity=complexity,
                estimated_time=estimated_time,
            )

            self.bot_requests[request_id] = request
            self.save_creator_data()

            logger.info(f"✅ Created feature request {request_id} by {user_name}")
            return request_id

        except Exception as e:
            logger.error(f"❌ Error creating feature request: {e}")
            return None

    def get_available_features(self) -> Dict[str, Any]:
        """Get available feature templates"""
        try:
            with open(self.templates_file, "r") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ Error loading templates: {e}")
            return {}

    def handle_creator_command(
        self, command: str, user_id: str, user_name: str, content: str
    ) -> str:
        """Handle bot creator commands"""
        command_lower = command.lower()

        if command_lower == "!bot_features":
            return self.get_features_display()

        elif command_lower.startswith("!request_feature"):
            return self.handle_feature_request(command, user_id, user_name, content)

        elif command_lower == "!my_requests":
            return self.get_user_requests_display(user_id)

        elif command_lower.startswith("!feature_info"):
            return self.get_feature_info(command)

        elif command_lower == "!bot_help":
            return self.get_creator_help()

        return None

    def get_features_display(self) -> str:
        """Get available features display"""
        features = self.get_available_features()

        response = "🤖 **Available Bot Features**\n\n"

        for feature_type, info in features.items():
            complexity_emoji = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}

            emoji = complexity_emoji.get(info["complexity"], "🟡")
            response += f"{emoji} **{info['name']}**\n"
            response += f"   Type: `{feature_type}`\n"
            response += f"   Complexity: {info['complexity'].title()}\n"
            response += f"   Time: {info['estimated_time']}\n"
            response += f"   {info['description']}\n\n"

        response += 'Use `!request_feature "type" "description" [priority]` to request a feature!'

        return response

    def handle_feature_request(
        self, command: str, user_id: str, user_name: str, content: str
    ) -> str:
        """Handle feature request command"""
        try:
            # Parse: !request_feature "type" "description" [priority]
            parts = content.split('"')
            if len(parts) < 5:
                return '❌ Invalid format. Use: `!request_feature "type" "description" [priority]`'

            feature_type = parts[1].strip().lower()
            description = parts[3].strip()

            if not feature_type or not description:
                return "❌ Please provide both feature type and description."

            # Check if feature type is valid
            features = self.get_available_features()
            if feature_type not in features:
                valid_types = ", ".join(features.keys())
                return f"❌ Invalid feature type. Available types: {valid_types}"

            # Parse optional priority
            priority = "normal"
            remaining_parts = content.split('"')[-1].strip().split()
            for part in remaining_parts:
                if part.lower() in ["low", "normal", "high", "urgent"]:
                    priority = part.lower()

            # Create request
            request_id = self.create_feature_request(
                user_id, user_name, feature_type, description, priority
            )

            if request_id:
                feature_info = features[feature_type]
                return f"✅ **Feature Request Created!** ID: `{request_id}`\n\n**Feature:** {feature_info['name']}\n**Type:** {feature_type}\n**Description:** {description}\n**Priority:** {priority.title()}\n**Complexity:** {feature_info['complexity'].title()}\n**Estimated Time:** {feature_info['estimated_time']}\n\nYour request has been submitted and will be reviewed!"
            else:
                return "❌ Error creating feature request. Please try again."

        except Exception as e:
            logger.error(f"❌ Error handling feature request: {e}")
            return "❌ Error creating feature request. Please check the format."

    def get_user_requests_display(self, user_id: str) -> str:
        """Get user's feature requests display"""
        user_requests = []
        for request in self.bot_requests.values():
            if request.user_id == user_id:
                user_requests.append(request)

        if not user_requests:
            return "🤖 You haven't submitted any feature requests yet."

        # Sort by creation date (newest first)
        user_requests.sort(key=lambda r: r.created_at, reverse=True)

        response = f"🤖 **Your Feature Requests** ({len(user_requests)} total):\n\n"

        for i, request in enumerate(user_requests[:5], 1):
            status_emoji = {
                "pending": "⏳",
                "approved": "✅",
                "implemented": "🚀",
                "declined": "❌",
            }

            emoji = status_emoji.get(request.status, "📝")
            response += f"{i}. {emoji} **{request.feature_type.title()}**\n"
            response += f"   ID: `{request.request_id}`\n"
            response += f"   Status: {request.status.title()}\n"
            response += f"   Priority: {request.priority.title()}\n"
            response += f"   Description: {request.description[:50]}...\n\n"

        if len(user_requests) > 5:
            response += f"... and {len(user_requests) - 5} more requests"

        return response

    def get_feature_info(self, command: str) -> str:
        """Get detailed feature information"""
        try:
            parts = command.split()
            if len(parts) < 2:
                return "❌ Please specify feature type. Use: `!feature_info type`"

            feature_type = parts[1].lower()
            features = self.get_available_features()

            if feature_type not in features:
                valid_types = ", ".join(features.keys())
                return f"❌ Invalid feature type. Available types: {valid_types}"

            info = features[feature_type]

            response = f"🤖 **{info['name']}**\n\n"
            response += f"**Type:** {feature_type}\n"
            response += f"**Complexity:** {info['complexity'].title()}\n"
            response += f"**Estimated Time:** {info['estimated_time']}\n"
            response += f"**Description:** {info['description']}\n\n"

            response += "**Features Included:**\n"
            for feature in info["features"]:
                response += f"• {feature}\n"

            response += f'\n**Request Command:**\n`!request_feature "{feature_type}" "your description"`'

            return response

        except Exception as e:
            logger.error(f"❌ Error getting feature info: {e}")
            return "❌ Error retrieving feature information."

    def get_creator_help(self) -> str:
        """Get bot creator help"""
        help_text = "🤖 **Bot Creator System Help**\n\n"
        help_text += "**Commands:**\n"
        help_text += "• `!bot_features` - View available features\n"
        help_text += (
            '• `!request_feature "type" "description" [priority]` - Request a feature\n'
        )
        help_text += "• `!my_requests` - View your feature requests\n"
        help_text += "• `!feature_info type` - Get detailed feature information\n"
        help_text += "• `!bot_help` - Show this help\n\n"
        help_text += "**Available Feature Types:**\n"
        help_text += "• reactions - Reaction-based interactions\n"
        help_text += "• webhooks - External service integration\n"
        help_text += "• cooldowns - Rate limiting and cooldowns\n"
        help_text += "• permissions - Advanced permission management\n"
        help_text += "• moderation - Server moderation tools\n"
        help_text += "• welcome - Welcome system for new members\n"
        help_text += "• logging - Comprehensive activity logging\n"
        help_text += "• games - Fun games and entertainment\n"
        help_text += "• music - Music playback system\n"
        help_text += "• economy - Virtual currency system\n\n"
        help_text += "**Priorities:** low, normal, high, urgent\n\n"
        help_text += "**Examples:**\n"
        help_text += (
            '• `!request_feature "reactions" "Add reaction menus for polls" high`\n'
        )
        help_text += (
            '• `!request_feature "welcome" "Custom welcome messages with images"`\n'
        )
        help_text += "• `!feature_info moderation`"

        return help_text
