"""
Reminder System
Creates and manages reminders, events, and scheduled notifications
"""

import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import time
import re

logger = logging.getLogger(__name__)


@dataclass
class Reminder:
    """Reminder data structure"""

    reminder_id: str
    user_id: str
    user_name: str
    channel_id: str
    message: str
    created_at: str
    due_time: str
    is_recurring: bool = False
    recurrence_pattern: str = ""  # daily, weekly, monthly
    is_completed: bool = False
    completed_at: str = ""
    priority: str = "normal"  # low, normal, high, urgent


class ReminderSystem:
    """
    Reminder System
    - Create and manage reminders
    - Support recurring reminders
    - Priority-based notifications
    - Event scheduling
    """

    def __init__(self):
        self.reminders_file = "reminders_data.json"
        self.active_reminders: Dict[str, Reminder] = {}
        self.completed_reminders: Dict[str, Reminder] = {}

        # Load existing reminders
        self.load_reminders()

    def load_reminders(self):
        """Load reminders from file"""
        if Path(self.reminders_file).exists():
            try:
                with open(self.reminders_file, "r") as f:
                    data = json.load(f)

                    # Load active reminders
                    for reminder_id, reminder_data in data.get("active", {}).items():
                        self.active_reminders[reminder_id] = Reminder(**reminder_data)

                    # Load completed reminders
                    for reminder_id, reminder_data in data.get("completed", {}).items():
                        self.completed_reminders[reminder_id] = Reminder(
                            **reminder_data
                        )

                logger.info(
                    f"✅ Loaded {len(self.active_reminders)} active reminders, {len(self.completed_reminders)} completed"
                )
            except Exception as e:
                logger.error(f"❌ Error loading reminders: {e}")

    def save_reminders(self):
        """Save reminders to file"""
        try:
            data = {
                "active": {
                    reminder_id: asdict(reminder)
                    for reminder_id, reminder in self.active_reminders.items()
                },
                "completed": {
                    reminder_id: asdict(reminder)
                    for reminder_id, reminder in self.completed_reminders.items()
                },
                "last_updated": datetime.now().isoformat(),
            }

            with open(self.reminders_file, "w") as f:
                json.dump(data, f, indent=2)

            logger.info("✅ Saved reminders data")
        except Exception as e:
            logger.error(f"❌ Error saving reminders: {e}")

    def parse_time_string(self, time_str: str) -> Optional[datetime]:
        """Parse various time formats"""
        try:
            time_str = time_str.lower().strip()
            now = datetime.now()

            # Relative time patterns
            if "in" in time_str:
                # "in 5 minutes", "in 2 hours", "in 3 days"
                match = re.search(r"in (\d+) (\w+)", time_str)
                if match:
                    amount = int(match.group(1))
                    unit = match.group(2)

                    if unit.startswith("min"):
                        return now + timedelta(minutes=amount)
                    elif unit.startswith("hour"):
                        return now + timedelta(hours=amount)
                    elif unit.startswith("day"):
                        return now + timedelta(days=amount)
                    elif unit.startswith("week"):
                        return now + timedelta(weeks=amount)

            # Specific time patterns
            elif "at" in time_str:
                # "at 3pm", "at 15:30"
                match = re.search(r"at (\d{1,2})(?::(\d{2}))?\s*(am|pm)?", time_str)
                if match:
                    hour = int(match.group(1))
                    minute = int(match.group(2)) if match.group(2) else 0
                    ampm = match.group(3)

                    if ampm:
                        if ampm == "pm" and hour != 12:
                            hour += 12
                        elif ampm == "am" and hour == 12:
                            hour = 0

                    due_time = now.replace(
                        hour=hour, minute=minute, second=0, microsecond=0
                    )

                    # If time has passed today, schedule for tomorrow
                    if due_time <= now:
                        due_time += timedelta(days=1)

                    return due_time

            # Tomorrow patterns
            elif "tomorrow" in time_str:
                tomorrow = now + timedelta(days=1)
                # Extract time if specified
                time_match = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", time_str)
                if time_match:
                    hour = int(time_match.group(1))
                    minute = int(time_match.group(2)) if time_match.group(2) else 0
                    ampm = time_match.group(3)

                    if ampm:
                        if ampm == "pm" and hour != 12:
                            hour += 12
                        elif ampm == "am" and hour == 12:
                            hour = 0

                    return tomorrow.replace(
                        hour=hour, minute=minute, second=0, microsecond=0
                    )
                else:
                    return tomorrow.replace(
                        hour=9, minute=0, second=0, microsecond=0
                    )  # Default 9 AM

            # Today patterns
            elif "today" in time_str:
                time_match = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", time_str)
                if time_match:
                    hour = int(time_match.group(1))
                    minute = int(time_match.group(2)) if time_match.group(2) else 0
                    ampm = time_match.group(3)

                    if ampm:
                        if ampm == "pm" and hour != 12:
                            hour += 12
                        elif ampm == "am" and hour == 12:
                            hour = 0

                    due_time = now.replace(
                        hour=hour, minute=minute, second=0, microsecond=0
                    )

                    # If time has passed, schedule for tomorrow
                    if due_time <= now:
                        due_time += timedelta(days=1)

                    return due_time

            # Try parsing as ISO format
            try:
                return datetime.fromisoformat(time_str)
            except:
                pass

            # Default: 1 hour from now
            return now + timedelta(hours=1)

        except Exception as e:
            logger.error(f"❌ Error parsing time string: {e}")
            return None

    def create_reminder(
        self,
        user_id: str,
        user_name: str,
        channel_id: str,
        message: str,
        time_str: str,
        priority: str = "normal",
    ) -> str:
        """Create a new reminder"""
        try:
            # Parse time
            due_time = self.parse_time_string(time_str)
            if not due_time:
                return None

            # Generate reminder ID
            reminder_id = f"reminder_{user_id}_{int(time.time())}"

            # Create reminder
            reminder = Reminder(
                reminder_id=reminder_id,
                user_id=user_id,
                user_name=user_name,
                channel_id=channel_id,
                message=message,
                created_at=datetime.now().isoformat(),
                due_time=due_time.isoformat(),
                priority=priority,
            )

            self.active_reminders[reminder_id] = reminder
            self.save_reminders()

            logger.info(f"✅ Created reminder {reminder_id} for {user_name}")
            return reminder_id

        except Exception as e:
            logger.error(f"❌ Error creating reminder: {e}")
            return None

    def get_due_reminders(self) -> List[Reminder]:
        """Get reminders that are due"""
        current_time = datetime.now()
        due_reminders = []

        for reminder in self.active_reminders.values():
            due_time = datetime.fromisoformat(reminder.due_time)
            if due_time <= current_time:
                due_reminders.append(reminder)

        return due_reminders

    def complete_reminder(self, reminder_id: str):
        """Mark reminder as completed"""
        if reminder_id in self.active_reminders:
            reminder = self.active_reminders[reminder_id]
            reminder.is_completed = True
            reminder.completed_at = datetime.now().isoformat()

            self.completed_reminders[reminder_id] = reminder
            del self.active_reminders[reminder_id]

            self.save_reminders()
            logger.info(f"✅ Completed reminder {reminder_id}")

    def get_user_reminders(self, user_id: str) -> List[Reminder]:
        """Get reminders for specific user"""
        user_reminders = []
        for reminder in self.active_reminders.values():
            if reminder.user_id == user_id:
                user_reminders.append(reminder)
        return user_reminders

    def delete_reminder(self, reminder_id: str, user_id: str) -> bool:
        """Delete a reminder"""
        if reminder_id in self.active_reminders:
            reminder = self.active_reminders[reminder_id]
            if reminder.user_id == user_id:
                del self.active_reminders[reminder_id]
                self.save_reminders()
                logger.info(f"✅ Deleted reminder {reminder_id}")
                return True
        return False

    def handle_reminder_command(
        self, command: str, user_id: str, user_name: str, channel_id: str, content: str
    ) -> str:
        """Handle reminder commands"""
        command_lower = command.lower()

        if command_lower.startswith("!reminder"):
            return self.handle_reminder_creation(
                command, user_id, user_name, channel_id, content
            )

        elif command_lower == "!reminders":
            return self.get_user_reminders_display(user_id)

        elif command_lower.startswith("!complete_reminder"):
            return self.handle_reminder_completion(command, user_id)

        elif command_lower.startswith("!delete_reminder"):
            return self.handle_reminder_deletion(command, user_id)

        elif command_lower == "!reminder_help":
            return self.get_reminder_help()

        return None

    def handle_reminder_creation(
        self, command: str, user_id: str, user_name: str, channel_id: str, content: str
    ) -> str:
        """Handle reminder creation command"""
        try:
            # Parse: !reminder "message" "time" [priority]
            parts = content.split('"')
            if len(parts) < 5:
                return '❌ Invalid format. Use: `!reminder "message" "time" [priority]`'

            message = parts[1].strip()
            time_str = parts[3].strip()

            if not message or not time_str:
                return "❌ Please provide both message and time."

            # Parse optional priority
            priority = "normal"
            remaining_parts = content.split('"')[-1].strip().split()
            for part in remaining_parts:
                if part.lower() in ["low", "normal", "high", "urgent"]:
                    priority = part.lower()

            # Create reminder
            reminder_id = self.create_reminder(
                user_id, user_name, channel_id, message, time_str, priority
            )

            if reminder_id:
                due_time = self.parse_time_string(time_str)
                time_display = due_time.strftime("%Y-%m-%d %H:%M")

                return f"⏰ **Reminder Created!** ID: `{reminder_id}`\n\n**Message:** {message}\n**Due:** {time_display}\n**Priority:** {priority.title()}"
            else:
                return "❌ Error creating reminder. Please check the time format."

        except Exception as e:
            logger.error(f"❌ Error handling reminder creation: {e}")
            return "❌ Error creating reminder. Please check the format."

    def handle_reminder_completion(self, command: str, user_id: str) -> str:
        """Handle reminder completion command"""
        try:
            parts = command.split()
            if len(parts) < 2:
                return "❌ Please specify reminder ID. Use: `!complete_reminder reminder_id`"

            reminder_id = parts[1]
            if reminder_id in self.active_reminders:
                reminder = self.active_reminders[reminder_id]
                if reminder.user_id == user_id:
                    self.complete_reminder(reminder_id)
                    return f"✅ **Reminder completed!** {reminder.message}"
                else:
                    return "❌ You can only complete your own reminders."
            else:
                return "❌ Reminder not found."

        except Exception as e:
            logger.error(f"❌ Error handling reminder completion: {e}")
            return "❌ Error completing reminder."

    def handle_reminder_deletion(self, command: str, user_id: str) -> str:
        """Handle reminder deletion command"""
        try:
            parts = command.split()
            if len(parts) < 2:
                return (
                    "❌ Please specify reminder ID. Use: `!delete_reminder reminder_id`"
                )

            reminder_id = parts[1]
            if self.delete_reminder(reminder_id, user_id):
                return "🗑️ **Reminder deleted!**"
            else:
                return (
                    "❌ Reminder not found or you don't have permission to delete it."
                )

        except Exception as e:
            logger.error(f"❌ Error handling reminder deletion: {e}")
            return "❌ Error deleting reminder."

    def get_user_reminders_display(self, user_id: str) -> str:
        """Get user's reminders display"""
        user_reminders = self.get_user_reminders(user_id)

        if not user_reminders:
            return "⏰ You don't have any active reminders."

        # Sort by due time
        user_reminders.sort(key=lambda r: datetime.fromisoformat(r.due_time))

        response = f"⏰ **Your Reminders** ({len(user_reminders)} active):\n\n"

        for i, reminder in enumerate(user_reminders[:5], 1):
            due_time = datetime.fromisoformat(reminder.due_time)
            time_display = due_time.strftime("%m/%d %H:%M")

            priority_emoji = {"low": "🟢", "normal": "🟡", "high": "🟠", "urgent": "🔴"}

            emoji = priority_emoji.get(reminder.priority, "🟡")
            response += f"{i}. {emoji} **{reminder.message}**\n"
            response += f"   ID: `{reminder.reminder_id}` | Due: {time_display}\n"
            response += f"   Priority: {reminder.priority.title()}\n\n"

        if len(user_reminders) > 5:
            response += f"... and {len(user_reminders) - 5} more reminders"

        return response

    def get_reminder_help(self) -> str:
        """Get reminder system help"""
        help_text = "⏰ **Reminder System Help**\n\n"
        help_text += "**Creating Reminders:**\n"
        help_text += '• `!reminder "message" "time" [priority]`\n\n'
        help_text += "**Time Formats:**\n"
        help_text += "• `in 5 minutes` - Relative time\n"
        help_text += "• `in 2 hours` - Relative time\n"
        help_text += "• `at 3pm` - Specific time today\n"
        help_text += "• `tomorrow at 9am` - Specific time tomorrow\n"
        help_text += "• `2025-07-21 15:30` - ISO format\n\n"
        help_text += "**Managing Reminders:**\n"
        help_text += "• `!reminders` - View your reminders\n"
        help_text += "• `!complete_reminder reminder_id` - Mark as done\n"
        help_text += "• `!delete_reminder reminder_id` - Delete reminder\n"
        help_text += "• `!reminder_help` - Show this help\n\n"
        help_text += "**Priorities:** low, normal, high, urgent\n\n"
        help_text += "**Examples:**\n"
        help_text += '• `!reminder "Take a break" "in 30 minutes" high`\n'
        help_text += '• `!reminder "Team meeting" "tomorrow at 2pm"`\n'
        help_text += '• `!reminder "Call mom" "at 6pm" urgent`'

        return help_text
