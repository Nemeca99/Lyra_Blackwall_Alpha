"""
Feedback and Idea Collection System
Collects user feedback and ideas for the quantum bot development
"""

import json
import logging
from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class FeedbackEntry:
    """Feedback/idea entry data"""

    feedback_id: str
    user_id: str
    user_name: str
    feedback_type: str  # "feedback", "idea", "bug", "feature_request"
    title: str
    content: str
    timestamp: str
    channel_id: str
    message_id: str
    status: str = "pending"  # "pending", "reviewed", "implemented", "declined"
    priority: str = "normal"  # "low", "normal", "high", "urgent"
    response_requested: bool = False
    admin_notes: str = ""


class FeedbackSystem:
    """
    Feedback and Idea Collection System
    - Collects user feedback and ideas
    - Saves to separate files for admin review
    - Optional response functionality
    """

    def __init__(self):
        self.feedback_file = "user_feedback.json"
        self.ideas_file = "user_ideas.json"
        self.bugs_file = "bug_reports.json"
        self.features_file = "feature_requests.json"

        self.feedback_entries: Dict[str, FeedbackEntry] = {}
        self.idea_entries: Dict[str, FeedbackEntry] = {}
        self.bug_entries: Dict[str, FeedbackEntry] = {}
        self.feature_entries: Dict[str, FeedbackEntry] = {}

        # Load existing feedback
        self.load_all_feedback()

    def load_all_feedback(self):
        """Load all feedback from files"""
        self.load_feedback_from_file(self.feedback_file, self.feedback_entries)
        self.load_feedback_from_file(self.ideas_file, self.idea_entries)
        self.load_feedback_from_file(self.bugs_file, self.bug_entries)
        self.load_feedback_from_file(self.features_file, self.feature_entries)

        total_entries = (
            len(self.feedback_entries)
            + len(self.idea_entries)
            + len(self.bug_entries)
            + len(self.feature_entries)
        )
        logger.info(f"✅ Loaded {total_entries} feedback entries")

    def load_feedback_from_file(
        self, filename: str, target_dict: Dict[str, FeedbackEntry]
    ):
        """Load feedback from specific file"""
        if Path(filename).exists():
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
                    for entry_id, entry_data in data.items():
                        target_dict[entry_id] = FeedbackEntry(**entry_data)
            except Exception as e:
                logger.error(f"❌ Error loading {filename}: {e}")

    def save_feedback_to_file(self, filename: str, entries: Dict[str, FeedbackEntry]):
        """Save feedback to specific file"""
        try:
            data = {}
            for entry_id, entry in entries.items():
                data[entry_id] = asdict(entry)

            with open(filename, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"✅ Saved {len(entries)} entries to {filename}")
        except Exception as e:
            logger.error(f"❌ Error saving {filename}: {e}")

    def save_all_feedback(self):
        """Save all feedback to files"""
        self.save_feedback_to_file(self.feedback_file, self.feedback_entries)
        self.save_feedback_to_file(self.ideas_file, self.idea_entries)
        self.save_feedback_to_file(self.bugs_file, self.bug_entries)
        self.save_feedback_to_file(self.features_file, self.feature_entries)

    def add_feedback(
        self,
        user_id: str,
        user_name: str,
        feedback_type: str,
        title: str,
        content: str,
        channel_id: str,
        message_id: str,
        response_requested: bool = False,
    ) -> str:
        """Add new feedback entry"""
        try:
            # Generate unique ID
            timestamp = datetime.now()
            feedback_id = (
                f"{feedback_type}_{user_id}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
            )

            # Create feedback entry
            entry = FeedbackEntry(
                feedback_id=feedback_id,
                user_id=user_id,
                user_name=user_name,
                feedback_type=feedback_type,
                title=title,
                content=content,
                timestamp=timestamp.isoformat(),
                channel_id=channel_id,
                message_id=message_id,
                response_requested=response_requested,
            )

            # Add to appropriate collection
            if feedback_type == "feedback":
                self.feedback_entries[feedback_id] = entry
            elif feedback_type == "idea":
                self.idea_entries[feedback_id] = entry
            elif feedback_type == "bug":
                self.bug_entries[feedback_id] = entry
            elif feedback_type == "feature_request":
                self.feature_entries[feedback_id] = entry

            # Save to file
            self.save_all_feedback()

            logger.info(f"✅ Added {feedback_type} from {user_name}: {title}")
            return feedback_id

        except Exception as e:
            logger.error(f"❌ Error adding feedback: {e}")
            return None

    def get_feedback_summary(self) -> Dict:
        """Get summary of all feedback"""
        return {
            "total_feedback": len(self.feedback_entries),
            "total_ideas": len(self.idea_entries),
            "total_bugs": len(self.bug_entries),
            "total_features": len(self.feature_entries),
            "total_entries": (
                len(self.feedback_entries)
                + len(self.idea_entries)
                + len(self.bug_entries)
                + len(self.feature_entries)
            ),
            "pending_feedback": len(
                [e for e in self.feedback_entries.values() if e.status == "pending"]
            ),
            "pending_ideas": len(
                [e for e in self.idea_entries.values() if e.status == "pending"]
            ),
            "pending_bugs": len(
                [e for e in self.bug_entries.values() if e.status == "pending"]
            ),
            "pending_features": len(
                [e for e in self.feature_entries.values() if e.status == "pending"]
            ),
        }

    def get_user_feedback(self, user_id: str) -> List[FeedbackEntry]:
        """Get all feedback from specific user"""
        all_entries = []
        all_entries.extend(self.feedback_entries.values())
        all_entries.extend(self.idea_entries.values())
        all_entries.extend(self.bug_entries.values())
        all_entries.extend(self.feature_entries.values())

        return [entry for entry in all_entries if entry.user_id == user_id]

    def get_recent_feedback(self, limit: int = 5) -> List[FeedbackEntry]:
        """Get most recent feedback entries"""
        all_entries = []
        all_entries.extend(self.feedback_entries.values())
        all_entries.extend(self.idea_entries.values())
        all_entries.extend(self.bug_entries.values())
        all_entries.extend(self.feature_entries.values())

        # Sort by timestamp (newest first)
        sorted_entries = sorted(all_entries, key=lambda x: x.timestamp, reverse=True)
        return sorted_entries[:limit]

    def handle_feedback_command(
        self,
        command: str,
        user_id: str,
        user_name: str,
        content: str,
        channel_id: str,
        message_id: str,
    ) -> str:
        """Handle feedback commands"""
        command_lower = command.lower()

        if command_lower.startswith("!feedback"):
            # Extract feedback content
            feedback_content = content[len("!feedback") :].strip()
            if not feedback_content:
                return "❌ Please provide feedback content. Usage: `!feedback [your feedback here]`"

            # Add feedback entry
            feedback_id = self.add_feedback(
                user_id,
                user_name,
                "feedback",
                "General Feedback",
                feedback_content,
                channel_id,
                message_id,
            )

            if feedback_id:
                return f"✅ **Feedback submitted!** ID: `{feedback_id}`\n\nYour feedback has been saved and will be reviewed. Thank you for helping improve the bot!"
            else:
                return "❌ Error submitting feedback. Please try again."

        elif command_lower.startswith("!idea"):
            # Extract idea content
            idea_content = content[len("!idea") :].strip()
            if not idea_content:
                return "❌ Please provide your idea. Usage: `!idea [your idea here]`"

            # Add idea entry
            idea_id = self.add_feedback(
                user_id,
                user_name,
                "idea",
                "User Idea",
                idea_content,
                channel_id,
                message_id,
            )

            if idea_id:
                return f"💡 **Idea submitted!** ID: `{idea_id}`\n\nYour idea has been saved and will be reviewed. Thank you for your creativity!"
            else:
                return "❌ Error submitting idea. Please try again."

        elif command_lower.startswith("!bug"):
            # Extract bug report content
            bug_content = content[len("!bug") :].strip()
            if not bug_content:
                return (
                    "❌ Please describe the bug. Usage: `!bug [bug description here]`"
                )

            # Add bug entry
            bug_id = self.add_feedback(
                user_id,
                user_name,
                "bug",
                "Bug Report",
                bug_content,
                channel_id,
                message_id,
            )

            if bug_id:
                return f"🐛 **Bug report submitted!** ID: `{bug_id}`\n\nYour bug report has been saved and will be investigated. Thank you for helping improve the bot!"
            else:
                return "❌ Error submitting bug report. Please try again."

        elif command_lower.startswith("!feature"):
            # Extract feature request content
            feature_content = content[len("!feature") :].strip()
            if not feature_content:
                return "❌ Please describe the feature. Usage: `!feature [feature description here]`"

            # Add feature entry
            feature_id = self.add_feedback(
                user_id,
                user_name,
                "feature_request",
                "Feature Request",
                feature_content,
                channel_id,
                message_id,
            )

            if feature_id:
                return f"🚀 **Feature request submitted!** ID: `{feature_id}`\n\nYour feature request has been saved and will be reviewed. Thank you for your suggestion!"
            else:
                return "❌ Error submitting feature request. Please try again."

        elif command_lower == "!my_feedback":
            # Show user's feedback history
            user_entries = self.get_user_feedback(user_id)
            if not user_entries:
                return "📝 You haven't submitted any feedback yet. Use `!feedback`, `!idea`, `!bug`, or `!feature` to submit!"

            response = (
                f"📝 **Your Feedback History** ({len(user_entries)} entries):\n\n"
            )
            for entry in user_entries[:5]:  # Show last 5 entries
                status_emoji = {
                    "pending": "⏳",
                    "reviewed": "👀",
                    "implemented": "✅",
                    "declined": "❌",
                }
                emoji = status_emoji.get(entry.status, "📝")
                response += f"{emoji} **{entry.title}** ({entry.feedback_type})\n"
                response += f"   Status: {entry.status.title()}\n"
                response += f"   Date: {entry.timestamp[:10]}\n\n"

            if len(user_entries) > 5:
                response += f"... and {len(user_entries) - 5} more entries"

            return response

        elif command_lower == "!feedback_help":
            # Show feedback help
            help_text = "📝 **Feedback System Help**\n\n"
            help_text += "**Commands:**\n"
            help_text += "• `!feedback [text]` - Submit general feedback\n"
            help_text += "• `!idea [text]` - Submit a new idea\n"
            help_text += "• `!bug [text]` - Report a bug\n"
            help_text += "• `!feature [text]` - Request a new feature\n"
            help_text += "• `!my_feedback` - View your feedback history\n"
            help_text += "• `!feedback_help` - Show this help\n\n"
            help_text += "**Note:** All feedback is saved for admin review. No automatic responses unless requested."

            return help_text

        return None

    def get_feedback_stats_embed(self) -> Dict:
        """Get feedback statistics for embed display"""
        summary = self.get_feedback_summary()

        return {
            "title": "📊 Feedback System Statistics",
            "description": "Current feedback and idea collection status",
            "color": 0x00BFFF,
            "fields": [
                {
                    "name": "📝 General Feedback",
                    "value": f"{summary['total_feedback']} total ({summary['pending_feedback']} pending)",
                    "inline": True,
                },
                {
                    "name": "💡 Ideas",
                    "value": f"{summary['total_ideas']} total ({summary['pending_ideas']} pending)",
                    "inline": True,
                },
                {
                    "name": "🐛 Bug Reports",
                    "value": f"{summary['total_bugs']} total ({summary['pending_bugs']} pending)",
                    "inline": True,
                },
                {
                    "name": "🚀 Feature Requests",
                    "value": f"{summary['total_features']} total ({summary['pending_features']} pending)",
                    "inline": True,
                },
                {
                    "name": "📊 Total Entries",
                    "value": f"{summary['total_entries']} entries collected",
                    "inline": True,
                },
                {
                    "name": "⏳ Pending Review",
                    "value": f"{summary['pending_feedback'] + summary['pending_ideas'] + summary['pending_bugs'] + summary['pending_features']} items",
                    "inline": True,
                },
            ],
        }
