"""
Poll and Voting System
Creates and manages polls, votes, and community decision-making
"""

import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict
import random

logger = logging.getLogger(__name__)


@dataclass
class PollOption:
    """Poll option data"""

    option_id: str
    text: str
    votes: int = 0
    voters: List[str] = None

    def __post_init__(self):
        if self.voters is None:
            self.voters = []


@dataclass
class Poll:
    """Poll data structure"""

    poll_id: str
    creator_id: str
    creator_name: str
    question: str
    options: List[PollOption]
    created_at: str
    expires_at: str
    is_active: bool = True
    allow_multiple: bool = False
    anonymous: bool = False
    total_votes: int = 0
    category: str = "general"  # general, community, feature, event

    def __post_init__(self):
        if self.options is None:
            self.options = []


class PollSystem:
    """
    Poll and Voting System
    - Create and manage polls
    - Track votes and results
    - Support multiple poll types
    - Provide real-time results
    """

    def __init__(self):
        self.polls_file = "polls_data.json"
        self.active_polls: Dict[str, Poll] = {}
        self.completed_polls: Dict[str, Poll] = {}

        # Load existing polls
        self.load_polls()

    def load_polls(self):
        """Load polls from file"""
        if Path(self.polls_file).exists():
            try:
                with open(self.polls_file, "r") as f:
                    data = json.load(f)

                    # Load active polls
                    for poll_id, poll_data in data.get("active", {}).items():
                        options = [
                            PollOption(**opt) for opt in poll_data.get("options", [])
                        ]
                        poll_data["options"] = options
                        self.active_polls[poll_id] = Poll(**poll_data)

                    # Load completed polls
                    for poll_id, poll_data in data.get("completed", {}).items():
                        options = [
                            PollOption(**opt) for opt in poll_data.get("options", [])
                        ]
                        poll_data["options"] = options
                        self.completed_polls[poll_id] = Poll(**poll_data)

                logger.info(
                    f"✅ Loaded {len(self.active_polls)} active polls, {len(self.completed_polls)} completed"
                )
            except Exception as e:
                logger.error(f"❌ Error loading polls: {e}")

    def save_polls(self):
        """Save polls to file"""
        try:
            data = {
                "active": {
                    poll_id: asdict(poll) for poll_id, poll in self.active_polls.items()
                },
                "completed": {
                    poll_id: asdict(poll)
                    for poll_id, poll in self.completed_polls.items()
                },
                "last_updated": datetime.now().isoformat(),
            }

            with open(self.polls_file, "w") as f:
                json.dump(data, f, indent=2)

            logger.info("✅ Saved polls data")
        except Exception as e:
            logger.error(f"❌ Error saving polls: {e}")

    def create_poll(
        self,
        creator_id: str,
        creator_name: str,
        question: str,
        options: List[str],
        duration_hours: int = 24,
        allow_multiple: bool = False,
        anonymous: bool = False,
        category: str = "general",
    ) -> str:
        """Create a new poll"""
        try:
            # Generate poll ID
            poll_id = f"poll_{creator_id}_{int(datetime.now().timestamp())}"

            # Create poll options
            poll_options = []
            for i, option_text in enumerate(options):
                option = PollOption(option_id=f"opt_{i}", text=option_text)
                poll_options.append(option)

            # Set expiration time
            expires_at = (datetime.now() + timedelta(hours=duration_hours)).isoformat()

            # Create poll
            poll = Poll(
                poll_id=poll_id,
                creator_id=creator_id,
                creator_name=creator_name,
                question=question,
                options=poll_options,
                created_at=datetime.now().isoformat(),
                expires_at=expires_at,
                allow_multiple=allow_multiple,
                anonymous=anonymous,
                category=category,
            )

            self.active_polls[poll_id] = poll
            self.save_polls()

            logger.info(f"✅ Created poll {poll_id} by {creator_name}")
            return poll_id

        except Exception as e:
            logger.error(f"❌ Error creating poll: {e}")
            return None

    def vote(self, poll_id: str, user_id: str, option_ids: List[str]) -> bool:
        """Vote on a poll"""
        try:
            if poll_id not in self.active_polls:
                return False

            poll = self.active_polls[poll_id]

            # Check if poll is still active
            if not poll.is_active or datetime.now().isoformat() > poll.expires_at:
                self.complete_poll(poll_id)
                return False

            # Check if user already voted (unless multiple votes allowed)
            if not poll.allow_multiple:
                for option in poll.options:
                    if user_id in option.voters:
                        return False

            # Record votes
            for option_id in option_ids:
                for option in poll.options:
                    if option.option_id == option_id:
                        option.votes += 1
                        if user_id not in option.voters:
                            option.voters.append(user_id)
                        break

            poll.total_votes += 1
            self.save_polls()

            logger.info(f"✅ User {user_id} voted on poll {poll_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Error voting: {e}")
            return False

    def complete_poll(self, poll_id: str):
        """Mark poll as completed"""
        if poll_id in self.active_polls:
            poll = self.active_polls[poll_id]
            poll.is_active = False
            self.completed_polls[poll_id] = poll
            del self.active_polls[poll_id]
            self.save_polls()
            logger.info(f"✅ Completed poll {poll_id}")

    def get_poll(self, poll_id: str) -> Optional[Poll]:
        """Get poll by ID"""
        return self.active_polls.get(poll_id) or self.completed_polls.get(poll_id)

    def get_active_polls(self) -> List[Poll]:
        """Get all active polls"""
        return list(self.active_polls.values())

    def get_user_polls(self, user_id: str) -> List[Poll]:
        """Get polls created by user"""
        user_polls = []
        for poll in self.active_polls.values():
            if poll.creator_id == user_id:
                user_polls.append(poll)
        for poll in self.completed_polls.values():
            if poll.creator_id == user_id:
                user_polls.append(poll)
        return user_polls

    def cleanup_expired_polls(self):
        """Clean up expired polls"""
        current_time = datetime.now().isoformat()
        expired_polls = []

        for poll_id, poll in self.active_polls.items():
            if current_time > poll.expires_at:
                expired_polls.append(poll_id)

        for poll_id in expired_polls:
            self.complete_poll(poll_id)

        if expired_polls:
            logger.info(f"✅ Cleaned up {len(expired_polls)} expired polls")

    def handle_poll_command(
        self, command: str, user_id: str, user_name: str, content: str
    ) -> str:
        """Handle poll commands"""
        command_lower = command.lower()

        if command_lower.startswith("!poll"):
            return self.handle_poll_creation(command, user_id, user_name, content)

        elif command_lower.startswith("!vote"):
            return self.handle_voting(command, user_id, user_name, content)

        elif command_lower == "!polls":
            return self.get_polls_list()

        elif command_lower.startswith("!poll_result"):
            return self.get_poll_result(command, user_id)

        elif command_lower == "!my_polls":
            return self.get_user_polls_display(user_id)

        elif command_lower == "!poll_help":
            return self.get_poll_help()

        return None

    def handle_poll_creation(
        self, command: str, user_id: str, user_name: str, content: str
    ) -> str:
        """Handle poll creation command"""
        try:
            # Parse: !poll "question" "option1" "option2" [duration] [multiple] [anonymous]
            parts = content.split('"')
            if len(parts) < 5:
                return '❌ Invalid format. Use: `!poll "question" "option1" "option2" [duration] [multiple] [anonymous]`'

            question = parts[1].strip()
            options = []
            for i in range(3, len(parts), 2):
                if parts[i].strip():
                    options.append(parts[i].strip())

            if len(options) < 2:
                return "❌ Need at least 2 options for a poll."

            # Parse optional parameters
            duration_hours = 24
            allow_multiple = False
            anonymous = False

            remaining_parts = content.split('"')[-1].strip().split()
            for part in remaining_parts:
                if part.isdigit():
                    duration_hours = int(part)
                elif part.lower() in ["multiple", "multi"]:
                    allow_multiple = True
                elif part.lower() in ["anonymous", "anon"]:
                    anonymous = True

            # Create poll
            poll_id = self.create_poll(
                user_id,
                user_name,
                question,
                options,
                duration_hours,
                allow_multiple,
                anonymous,
            )

            if poll_id:
                return f"🗳️ **Poll Created!** ID: `{poll_id}`\n\n**{question}**\n\nUse `!vote {poll_id} option_number` to vote!"
            else:
                return "❌ Error creating poll. Please try again."

        except Exception as e:
            logger.error(f"❌ Error handling poll creation: {e}")
            return "❌ Error creating poll. Please check the format."

    def handle_voting(
        self, command: str, user_id: str, user_name: str, content: str
    ) -> str:
        """Handle voting command"""
        try:
            # Parse: !vote poll_id option_number(s)
            parts = content.split()
            if len(parts) < 3:
                return "❌ Invalid format. Use: `!vote poll_id option_number`"

            poll_id = parts[1]
            option_numbers = [int(opt) for opt in parts[2:] if opt.isdigit()]

            if not option_numbers:
                return "❌ Please specify option number(s) to vote for."

            # Get poll
            poll = self.get_poll(poll_id)
            if not poll:
                return "❌ Poll not found."

            if not poll.is_active:
                return "❌ This poll has ended."

            # Convert option numbers to option IDs
            option_ids = []
            for num in option_numbers:
                if 1 <= num <= len(poll.options):
                    option_ids.append(f"opt_{num-1}")
                else:
                    return f"❌ Invalid option number: {num}"

            # Vote
            if self.vote(poll_id, user_id, option_ids):
                return f"✅ **Vote recorded!** You voted for option(s): {', '.join(map(str, option_numbers))}"
            else:
                return "❌ Unable to vote. You may have already voted or the poll has ended."

        except Exception as e:
            logger.error(f"❌ Error handling vote: {e}")
            return "❌ Error processing vote. Please try again."

    def get_polls_list(self) -> str:
        """Get list of active polls"""
        self.cleanup_expired_polls()
        active_polls = self.get_active_polls()

        if not active_polls:
            return "📊 No active polls at the moment."

        response = "🗳️ **Active Polls:**\n\n"

        for i, poll in enumerate(active_polls[:5], 1):
            time_left = self.get_time_remaining(poll.expires_at)
            response += f"{i}. **{poll.question}**\n"
            response += f"   ID: `{poll.poll_id}` | Time left: {time_left}\n"
            response += (
                f"   Options: {len(poll.options)} | Votes: {poll.total_votes}\n\n"
            )

        if len(active_polls) > 5:
            response += f"... and {len(active_polls) - 5} more polls"

        return response

    def get_poll_result(self, command: str, user_id: str) -> str:
        """Get poll results"""
        try:
            parts = command.split()
            if len(parts) < 2:
                return "❌ Please specify poll ID. Use: `!poll_result poll_id`"

            poll_id = parts[1]
            poll = self.get_poll(poll_id)

            if not poll:
                return "❌ Poll not found."

            return self.format_poll_results(poll)

        except Exception as e:
            logger.error(f"❌ Error getting poll result: {e}")
            return "❌ Error retrieving poll results."

    def get_user_polls_display(self, user_id: str) -> str:
        """Get user's polls display"""
        user_polls = self.get_user_polls(user_id)

        if not user_polls:
            return "📊 You haven't created any polls yet."

        response = f"📊 **Your Polls** ({len(user_polls)} total):\n\n"

        for i, poll in enumerate(user_polls[:5], 1):
            status = "🟢 Active" if poll.is_active else "🔴 Completed"
            response += f"{i}. **{poll.question}**\n"
            response += f"   ID: `{poll.poll_id}` | Status: {status}\n"
            response += (
                f"   Votes: {poll.total_votes} | Options: {len(poll.options)}\n\n"
            )

        if len(user_polls) > 5:
            response += f"... and {len(user_polls) - 5} more polls"

        return response

    def format_poll_results(self, poll: Poll) -> str:
        """Format poll results for display"""
        response = f"📊 **Poll Results: {poll.question}**\n\n"

        # Calculate percentages
        total_votes = poll.total_votes
        if total_votes == 0:
            total_votes = 1  # Avoid division by zero

        # Sort options by votes
        sorted_options = sorted(poll.options, key=lambda x: x.votes, reverse=True)

        for i, option in enumerate(sorted_options, 1):
            percentage = (option.votes / total_votes) * 100
            bar_length = int(percentage / 5)  # 5% per character
            bar = "█" * bar_length + "░" * (20 - bar_length)

            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}️⃣"
            response += f"{emoji} **{option.text}**\n"
            response += f"   {bar} {option.votes} votes ({percentage:.1f}%)\n\n"

        response += f"📈 **Total Votes:** {poll.total_votes}\n"
        response += f"👤 **Created by:** {poll.creator_name}\n"
        response += f"📅 **Created:** {poll.created_at[:10]}\n"

        if poll.is_active:
            time_left = self.get_time_remaining(poll.expires_at)
            response += f"⏰ **Time left:** {time_left}"
        else:
            response += f"⏰ **Ended:** {poll.expires_at[:10]}"

        return response

    def get_time_remaining(self, expires_at: str) -> str:
        """Get time remaining until expiration"""
        try:
            expires = datetime.fromisoformat(expires_at)
            now = datetime.now()
            remaining = expires - now

            if remaining.total_seconds() <= 0:
                return "Expired"

            hours = int(remaining.total_seconds() // 3600)
            minutes = int((remaining.total_seconds() % 3600) // 60)

            if hours > 24:
                days = hours // 24
                hours = hours % 24
                return f"{days}d {hours}h {minutes}m"
            elif hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"

        except Exception:
            return "Unknown"

    def get_poll_help(self) -> str:
        """Get poll system help"""
        help_text = "🗳️ **Poll System Help**\n\n"
        help_text += "**Creating Polls:**\n"
        help_text += '• `!poll "question" "option1" "option2" [duration] [multiple] [anonymous]`\n'
        help_text += "• Duration: hours (default: 24)\n"
        help_text += "• Multiple: allow multiple votes\n"
        help_text += "• Anonymous: hide voter names\n\n"
        help_text += "**Voting:**\n"
        help_text += "• `!vote poll_id option_number`\n"
        help_text += "• `!vote poll_id 1 3` (multiple options)\n\n"
        help_text += "**Viewing:**\n"
        help_text += "• `!polls` - List active polls\n"
        help_text += "• `!poll_result poll_id` - View results\n"
        help_text += "• `!my_polls` - Your created polls\n"
        help_text += "• `!poll_help` - Show this help\n\n"
        help_text += "**Examples:**\n"
        help_text += '• `!poll "What\'s for dinner?" "Pizza" "Burger" "Salad" 12`\n'
        help_text += "• `!vote poll_123_456 2`\n"
        help_text += "• `!poll_result poll_123_456`"

        return help_text
