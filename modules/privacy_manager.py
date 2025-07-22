"""
Privacy Manager for Quantum Discord Bot
Handles consent tracking, channel monitoring, and privacy settings
"""

import json
import os
from datetime import datetime
from typing import Dict, Set, Optional
import discord
from discord.ext import commands


class PrivacyManager:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.consent_channels = {}  # channel_id -> {user_id: consent_status}
        self.user_privacy_settings = {}  # user_id -> privacy_preferences
        self.monitored_channels = set()  # channels currently being monitored
        self.privacy_data_file = "privacy_data.json"
        self.load_privacy_data()

    def load_privacy_data(self):
        """Load privacy settings from file"""
        if os.path.exists(self.privacy_data_file):
            try:
                with open(self.privacy_data_file, "r") as f:
                    data = json.load(f)
                    self.consent_channels = data.get("consent_channels", {})
                    self.user_privacy_settings = data.get("user_settings", {})
                    self.monitored_channels = set(data.get("monitored_channels", []))
            except Exception as e:
                print(f"❌ Error loading privacy data: {e}")

    def save_privacy_data(self):
        """Save privacy settings to file"""
        try:
            data = {
                "consent_channels": self.consent_channels,
                "user_settings": self.user_privacy_settings,
                "monitored_channels": list(self.monitored_channels),
                "last_updated": datetime.now().isoformat(),
            }
            with open(self.privacy_data_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving privacy data: {e}")

    async def check_channel_consent(self, channel_id: int) -> bool:
        """Check if all members in a channel have consented"""
        if str(channel_id) not in self.consent_channels:
            return False

        channel = self.bot.get_channel(channel_id)
        if not channel:
            return False

        # Get all members in the channel
        members = set()
        if hasattr(channel, "members"):
            members = set(member.id for member in channel.members)
        else:
            # For DM channels, just check the user
            members = {channel.recipient.id} if hasattr(channel, "recipient") else set()

        # Check if all members have consented
        channel_consent = self.consent_channels[str(channel_id)]
        for member_id in members:
            if (
                str(member_id) not in channel_consent
                or not channel_consent[str(member_id)]
            ):
                return False

        return True

    async def handle_member_join(self, channel_id: int, user_id: int):
        """Handle when a new member joins a monitored channel"""
        if str(channel_id) not in self.consent_channels:
            return

        # Pause monitoring temporarily
        self.monitored_channels.discard(channel_id)

        # Check user's default privacy setting
        user_setting = self.user_privacy_settings.get(str(user_id), {}).get(
            "default_consent", False
        )

        if user_setting:
            # Auto-consent based on user preference
            self.consent_channels[str(channel_id)][str(user_id)] = True
            await self.resume_monitoring(channel_id)
        else:
            # Request explicit consent
            await self.request_consent(channel_id, user_id)

    async def request_consent(self, channel_id: int, user_id: int):
        """Request consent from a new member"""
        channel = self.bot.get_channel(channel_id)
        if not channel:
            return

        user = self.bot.get_user(user_id)
        username = user.display_name if user else f"User {user_id}"

        embed = discord.Embed(
            title="🔒 Privacy Consent Required",
            description=f"**{username}** has joined this channel. The AI bot requires consent from all members to monitor conversations.",
            color=0xFF6B6B,
        )
        embed.add_field(
            name="What this means:",
            value="• The AI will remember conversations in this channel\n• Memories are stored securely and privately\n• You can revoke consent at any time",
            inline=False,
        )
        embed.add_field(
            name="Your options:",
            value="• `!consent_yes` - Allow monitoring\n• `!consent_no` - Decline monitoring\n• `!privacy_settings` - Set default preferences",
            inline=False,
        )

        await channel.send(embed=embed)

    async def resume_monitoring(self, channel_id: int):
        """Resume monitoring if all members have consented"""
        if await self.check_channel_consent(channel_id):
            self.monitored_channels.add(channel_id)
            channel = self.bot.get_channel(channel_id)
            if channel:
                await channel.send(
                    "✅ **Privacy consent confirmed. AI monitoring resumed.**"
                )

    async def revoke_consent(self, channel_id: int, user_id: int):
        """Revoke consent and stop monitoring"""
        if str(channel_id) in self.consent_channels:
            self.consent_channels[str(channel_id)][str(user_id)] = False
            self.monitored_channels.discard(channel_id)
            self.save_privacy_data()

            channel = self.bot.get_channel(channel_id)
            if channel:
                user = self.bot.get_user(user_id)
                username = user.display_name if user else f"User {user_id}"
                await channel.send(
                    f"🔒 **{username} has revoked consent. AI monitoring stopped.**"
                )

    async def grant_consent(self, channel_id: int, user_id: int):
        """Grant consent for channel monitoring"""
        if str(channel_id) not in self.consent_channels:
            self.consent_channels[str(channel_id)] = {}

        self.consent_channels[str(channel_id)][str(user_id)] = True
        self.save_privacy_data()

        # Check if we can resume monitoring
        await self.resume_monitoring(channel_id)

    def set_user_privacy_setting(self, user_id: int, setting: str, value: bool):
        """Set user's privacy preferences"""
        if str(user_id) not in self.user_privacy_settings:
            self.user_privacy_settings[str(user_id)] = {}

        self.user_privacy_settings[str(user_id)][setting] = value
        self.save_privacy_data()

    def get_user_privacy_setting(self, user_id: int, setting: str) -> bool:
        """Get user's privacy preference"""
        return self.user_privacy_settings.get(str(user_id), {}).get(setting, False)

    def is_channel_monitored(self, channel_id: int) -> bool:
        """Check if a channel is currently being monitored"""
        return channel_id in self.monitored_channels

    async def get_consent_status(self, channel_id: int) -> Dict:
        """Get detailed consent status for a channel"""
        channel = self.bot.get_channel(channel_id)
        if not channel:
            return {"error": "Channel not found"}

        members = []
        if hasattr(channel, "members"):
            for member in channel.members:
                consent = self.consent_channels.get(str(channel_id), {}).get(
                    str(member.id), False
                )
                members.append(
                    {
                        "user_id": member.id,
                        "username": member.display_name,
                        "consent": consent,
                    }
                )

        total_members = len(members)
        consented_members = sum(1 for m in members if m["consent"])

        return {
            "channel_id": channel_id,
            "channel_name": channel.name,
            "total_members": total_members,
            "consented_members": consented_members,
            "consent_percentage": (
                (consented_members / total_members * 100) if total_members > 0 else 0
            ),
            "monitored": self.is_channel_monitored(channel_id),
            "members": members,
        }
