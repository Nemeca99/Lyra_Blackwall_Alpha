"""
Greeter System for Quantum Discord Bot
Sends comprehensive welcome messages to new users
"""

import discord
from discord.ext import commands
from datetime import datetime
from typing import Dict, Set
import json
import os


class GreeterSystem:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.welcomed_users = set()  # Track users who have been welcomed
        self.greeter_data_file = "greeter_data.json"
        self.load_greeter_data()

    def load_greeter_data(self):
        """Load greeter data from file"""
        if os.path.exists(self.greeter_data_file):
            try:
                with open(self.greeter_data_file, "r") as f:
                    data = json.load(f)
                    self.welcomed_users = set(data.get("welcomed_users", []))
            except Exception as e:
                print(f"❌ Error loading greeter data: {e}")

    def save_greeter_data(self):
        """Save greeter data to file"""
        try:
            data = {
                "welcomed_users": list(self.welcomed_users),
                "last_updated": datetime.now().isoformat(),
            }
            with open(self.greeter_data_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"❌ Error saving greeter data: {e}")

    def has_been_welcomed(self, user_id: int) -> bool:
        """Check if user has already been welcomed"""
        return user_id in self.welcomed_users

    def mark_as_welcomed(self, user_id: int):
        """Mark user as welcomed"""
        self.welcomed_users.add(user_id)
        self.save_greeter_data()

    async def send_welcome_message(self, user: discord.User):
        """Send comprehensive welcome message to new user"""
        try:
            # Main welcome embed
            welcome_embed = discord.Embed(
                title="🌊 Welcome to Quantum AI!",
                description="You've encountered **ProjectBot**, a revolutionary quantum superposition AI system. This bot uses advanced AI architecture to provide personalized, intelligent responses.",
                color=0x00FFFF,
                timestamp=datetime.now(),
            )

            welcome_embed.add_field(
                name="🤖 What is ProjectBot?",
                value="ProjectBot is a **quantum superposition AI** that combines multiple AI models to create responses that are both intelligent and emotionally resonant. It's not just a chatbot - it's a thinking, learning companion.",
                inline=False,
            )

            welcome_embed.add_field(
                name="⚛️ How Does It Work?",
                value="The bot uses a **dual-AI architecture**:\n• **Particle AI** (LM Studio) - Handles logical processing\n• **Wave AI** (Ollama) - Manages emotional context\n• **Quantum Chef** - Coordinates and collapses responses\n\nThink of it like having two specialized brains working together!",
                inline=False,
            )

            welcome_embed.add_field(
                name="🔒 Privacy First",
                value="Your privacy is our top priority:\n• **100% consent required** - Bot only monitors channels where everyone agrees\n• **Personal memories** - Your conversations are stored privately\n• **Revoke anytime** - Use `!consent_no` to stop monitoring\n• **Default privacy** - Bot starts with monitoring OFF",
                inline=False,
            )

            await user.send(embed=welcome_embed)

            # Commands guide embed
            commands_embed = discord.Embed(
                title="📋 How to Use ProjectBot",
                description="Here are all the commands and features available:",
                color=0x00BFFF,
            )

            commands_embed.add_field(
                name="🌊 Quantum Commands",
                value="• **Mention the bot** - `@ProjectBot` + your message\n• **Quantum prefix** - `!quantum` + your message\n• **Status check** - `!quantum_status`\n• **History** - `!superposition_history`\n• **Metrics** - `!collapse_metrics`",
                inline=False,
            )

            commands_embed.add_field(
                name="🔒 Privacy Commands",
                value="• **Settings** - `!privacy_settings`\n• **Grant consent** - `!consent_yes`\n• **Revoke consent** - `!consent_no`\n• **Check status** - `!consent_status`\n• **Set defaults** - `!set_default_yes` / `!set_default_no`",
                inline=False,
            )

            commands_embed.add_field(
                name="🔗 System Commands",
                value="• **Connection status** - `!connection_status`\n• **Bot info** - `!bot_info`\n• **Help** - `!help`",
                inline=False,
            )

            await user.send(embed=commands_embed)

            # Features and capabilities embed
            features_embed = discord.Embed(
                title="🚀 What ProjectBot Can Do",
                description="Advanced capabilities that set this bot apart:",
                color=0x32CD32,
            )

            features_embed.add_field(
                name="🧠 Memory & Learning",
                value="• **Personal memory** - Remembers your conversations\n• **Context awareness** - Understands conversation history\n• **Emotional intelligence** - Responds with appropriate emotion\n• **Learning adaptation** - Improves responses over time",
                inline=False,
            )

            features_embed.add_field(
                name="⚛️ Quantum Processing",
                value="• **Superposition responses** - Multiple AI models working together\n• **Collapse mechanics** - Physical RAM-based response generation\n• **Parallel processing** - Simultaneous logical and emotional analysis\n• **Real-time adaptation** - Dynamic response adjustment",
                inline=False,
            )

            features_embed.add_field(
                name="🔒 Privacy & Security",
                value="• **User-owned data** - Your memories stay on your hardware\n• **Consent-based monitoring** - Only listens when you allow\n• **Encrypted storage** - Secure memory protection\n• **Individual control** - You control your data",
                inline=False,
            )

            await user.send(embed=features_embed)

            # Limitations and expectations embed
            limitations_embed = discord.Embed(
                title="⚠️ What ProjectBot Cannot Do",
                description="Important limitations to understand:",
                color=0xFF6B6B,
            )

            limitations_embed.add_field(
                name="🚫 Technical Limitations",
                value="• **No voice processing** - Text only\n• **No image generation** - Cannot create images\n• **No file uploads** - Cannot process uploaded files\n• **No external APIs** - Cannot access external services\n• **No persistent connections** - Cannot maintain long-term connections",
                inline=False,
            )

            limitations_embed.add_field(
                name="🚫 Ethical Boundaries",
                value="• **No harmful content** - Will not generate harmful responses\n• **No personal data sharing** - Cannot share your information\n• **No unauthorized access** - Cannot access private channels without consent\n• **No manipulation** - Designed to be honest and transparent",
                inline=False,
            )

            limitations_embed.add_field(
                name="🚫 Usage Boundaries",
                value="• **No commercial use** - Personal use only\n• **No mass messaging** - Cannot spam or mass message\n• **No automated actions** - Cannot perform automated tasks\n• **No data export** - Cannot export your data",
                inline=False,
            )

            await user.send(embed=limitations_embed)

            # Getting started embed
            getting_started_embed = discord.Embed(
                title="🎯 Getting Started",
                description="Ready to begin your quantum AI journey?",
                color=0xFFD700,
            )

            getting_started_embed.add_field(
                name="Step 1: Privacy Setup",
                value="1. Go to any channel where ProjectBot is present\n2. Type `!privacy_settings` to see your options\n3. Use `!consent_yes` to allow monitoring in that channel\n4. Set your default preference with `!set_default_yes` or `!set_default_no`",
                inline=False,
            )

            getting_started_embed.add_field(
                name="Step 2: First Interaction",
                value="1. Mention the bot: `@ProjectBot Hello!`\n2. Or use the quantum prefix: `!quantum Tell me about yourself`\n3. The bot will process your request through quantum superposition\n4. You'll receive a personalized, intelligent response",
                inline=False,
            )

            getting_started_embed.add_field(
                name="Step 3: Explore Features",
                value="• Try `!quantum_status` to see the bot's current state\n• Use `!superposition_history` to see your interaction history\n• Check `!connection_status` for system health\n• Ask the bot about itself or any topic you're curious about",
                inline=False,
            )

            getting_started_embed.add_field(
                name="💡 Pro Tips",
                value="• **Be specific** - Detailed questions get better responses\n• **Use context** - Reference previous conversations\n• **Be patient** - Quantum processing takes time\n• **Respect privacy** - Only use in consented channels",
                inline=False,
            )

            await user.send(embed=getting_started_embed)

            # Final embed with contact info
            final_embed = discord.Embed(
                title="🎉 Welcome to the Future!",
                description="You're now part of a revolutionary AI experience. ProjectBot represents the cutting edge of quantum AI technology, combining multiple AI models to create something truly unique.",
                color=0x9932CC,
            )

            final_embed.add_field(
                name="🌟 What Makes This Special",
                value="• **First quantum superposition AI** - Unique dual-AI architecture\n• **Privacy-first design** - Your data stays yours\n• **Emotional intelligence** - Responds with genuine understanding\n• **Continuous learning** - Improves with every interaction",
                inline=False,
            )

            final_embed.add_field(
                name="🔬 Technical Innovation",
                value="• **Recursive sync engines** - Advanced processing architecture\n• **Memory integration** - Seamless conversation memory\n• **Quantum collapse mechanics** - Physical RAM-based responses\n• **Hemispheric lexicon system** - Personalized language understanding",
                inline=False,
            )

            final_embed.add_field(
                name="📞 Need Help?",
                value="• Use `!help` in any channel for command list\n• Check `!connection_status` for system health\n• Ask the bot directly: `@ProjectBot How do I use you?`\n• The bot is designed to be intuitive and helpful!",
                inline=False,
            )

            final_embed.set_footer(text="Welcome to the quantum revolution! 🌊⚛️")

            await user.send(embed=final_embed)

            # Mark user as welcomed
            self.mark_as_welcomed(user.id)

            print(f"✅ Welcome message sent to {user.display_name} ({user.id})")

        except Exception as e:
            print(f"❌ Error sending welcome message to {user.id}: {e}")

    async def check_and_welcome_user(self, user: discord.User):
        """Check if user needs welcome message and send if needed"""
        if not self.has_been_welcomed(user.id):
            await self.send_welcome_message(user)

    async def handle_new_member(self, member: discord.Member):
        """Handle new member joining server"""
        await self.check_and_welcome_user(member)

    async def handle_message_from_new_user(self, message: discord.Message):
        """Handle first message from a user"""
        await self.check_and_welcome_user(message.author)
