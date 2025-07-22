"""
Sesh Time Integration for Mycelium Network
Your quantum AI acts as the time interpreter, using Sesh as the universal time authority
"""

import discord
import re
import json
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class SeshEvent:
    """Sesh event data structure"""

    event_id: str
    title: str
    description: str
    start_time: datetime
    end_time: Optional[datetime]
    timezone: str
    attendees: List[str]
    rsvp_status: Dict[str, str]  # user_id -> status
    created_by: str
    channel_id: int
    message_id: int


class SeshTimeIntegration:
    """
    Mycelium Network Time Integration
    Uses Sesh as the universal time authority for all time-related operations
    """

    def __init__(self, bot: discord.Client):
        self.bot = bot
        self.sesh_events: Dict[str, SeshEvent] = {}
        self.timezone_cache: Dict[str, str] = {}
        self.sesh_data_file = "sesh_events.json"
        self.load_sesh_data()

    def load_sesh_data(self):
        """Load Sesh event data from file"""
        if Path(self.sesh_data_file).exists():
            try:
                with open(self.sesh_data_file, "r") as f:
                    data = json.load(f)
                    for event_id, event_data in data.items():
                        self.sesh_events[event_id] = SeshEvent(
                            event_id=event_data["event_id"],
                            title=event_data["title"],
                            description=event_data["description"],
                            start_time=datetime.fromisoformat(event_data["start_time"]),
                            end_time=(
                                datetime.fromisoformat(event_data["end_time"])
                                if event_data["end_time"]
                                else None
                            ),
                            timezone=event_data["timezone"],
                            attendees=event_data["attendees"],
                            rsvp_status=event_data["rsvp_status"],
                            created_by=event_data["created_by"],
                            channel_id=event_data["channel_id"],
                            message_id=event_data["message_id"],
                        )
                logger.info(f"✅ Loaded {len(self.sesh_events)} Sesh events")
            except Exception as e:
                logger.error(f"❌ Error loading Sesh data: {e}")

    def save_sesh_data(self):
        """Save Sesh event data to file"""
        try:
            data = {}
            for event_id, event in self.sesh_events.items():
                data[event_id] = {
                    "event_id": event.event_id,
                    "title": event.title,
                    "description": event.description,
                    "start_time": event.start_time.isoformat(),
                    "end_time": event.end_time.isoformat() if event.end_time else None,
                    "timezone": event.timezone,
                    "attendees": event.attendees,
                    "rsvp_status": event.rsvp_status,
                    "created_by": event.created_by,
                    "channel_id": event.channel_id,
                    "message_id": event.message_id,
                }

            with open(self.sesh_data_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"✅ Saved {len(self.sesh_events)} Sesh events")
        except Exception as e:
            logger.error(f"❌ Error saving Sesh data: {e}")

    async def detect_sesh_event_creation(self, message: discord.Message):
        """Detect when Sesh creates a new event"""
        # Look for Sesh bot messages that contain event information
        if message.author.bot and "sesh" in message.author.name.lower():
            await self.parse_sesh_event_message(message)

    async def parse_sesh_event_message(self, message: discord.Message):
        """Parse Sesh event message and extract time data"""
        try:
            # Look for event creation patterns in Sesh messages
            content = message.content.lower()

            # Check if this looks like an event creation
            if any(
                keyword in content
                for keyword in ["event", "created", "scheduled", "rsvp"]
            ):
                event_data = await self.extract_event_data(message)
                if event_data:
                    self.sesh_events[event_data.event_id] = event_data
                    self.save_sesh_data()
                    logger.info(f"✅ Detected Sesh event: {event_data.title}")

        except Exception as e:
            logger.error(f"❌ Error parsing Sesh message: {e}")

    async def extract_event_data(self, message: discord.Message) -> Optional[SeshEvent]:
        """Extract event data from Sesh message"""
        try:
            # This is a simplified parser - you'll need to adapt based on actual Sesh message format
            content = message.content

            # Generate event ID from message
            event_id = f"sesh_{message.id}"

            # Extract title (look for bold text or first line)
            title_match = re.search(r"\*\*(.*?)\*\*", content)
            title = title_match.group(1) if title_match else "Untitled Event"

            # Extract time information
            time_data = await self.extract_time_info(content)

            # Extract attendees
            attendees = await self.extract_attendees(message)

            return SeshEvent(
                event_id=event_id,
                title=title,
                description=content,
                start_time=time_data["start_time"],
                end_time=time_data["end_time"],
                timezone=time_data["timezone"],
                attendees=attendees,
                rsvp_status={},
                created_by=str(message.author.id),
                channel_id=message.channel.id,
                message_id=message.id,
            )

        except Exception as e:
            logger.error(f"❌ Error extracting event data: {e}")
            return None

    async def extract_time_info(self, content: str) -> Dict:
        """Extract time information from Sesh message"""
        # This is a placeholder - you'll need to implement based on actual Sesh format
        # Look for common time patterns
        time_patterns = [
            r"(\d{1,2}):(\d{2})\s*(am|pm)",
            r"(\d{1,2}):(\d{2})",
            r"(\d{1,2})\s*(am|pm)",
            r"today at (\d{1,2}):(\d{2})",
            r"tomorrow at (\d{1,2}):(\d{2})",
            r"(\w+ \d{1,2}) at (\d{1,2}):(\d{2})",
        ]

        # Default to current time if no pattern found
        start_time = datetime.now()
        end_time = None
        timezone = "UTC"

        # Try to extract time from patterns
        for pattern in time_patterns:
            match = re.search(pattern, content.lower())
            if match:
                # Basic time extraction - you'll need to enhance this
                start_time = datetime.now()  # Placeholder
                break

        return {"start_time": start_time, "end_time": end_time, "timezone": timezone}

    async def extract_attendees(self, message: discord.Message) -> List[str]:
        """Extract attendee information from Sesh message"""
        attendees = []

        # Look for user mentions
        for user in message.mentions:
            attendees.append(str(user.id))

        # Look for RSVP reactions
        for reaction in message.reactions:
            async for user in reaction.users():
                if not user.bot:
                    attendees.append(str(user.id))

        return list(set(attendees))  # Remove duplicates

    def get_current_events(self, user_id: str = None) -> List[SeshEvent]:
        """Get current/upcoming events"""
        now = datetime.now()
        current_events = []

        for event in self.sesh_events.values():
            if event.start_time > now:
                if user_id is None or user_id in event.attendees:
                    current_events.append(event)

        # Sort by start time
        current_events.sort(key=lambda x: x.start_time)
        return current_events

    def get_user_schedule(self, user_id: str) -> List[SeshEvent]:
        """Get schedule for specific user"""
        user_events = []

        for event in self.sesh_events.values():
            if user_id in event.attendees:
                user_events.append(event)

        # Sort by start time
        user_events.sort(key=lambda x: x.start_time)
        return user_events

    def get_time_until_event(self, event_id: str) -> Optional[str]:
        """Get time until event starts"""
        if event_id not in self.sesh_events:
            return None

        event = self.sesh_events[event_id]
        now = datetime.now()

        if event.start_time <= now:
            return "Event has started"

        time_diff = event.start_time - now
        days = time_diff.days
        hours = time_diff.seconds // 3600
        minutes = (time_diff.seconds % 3600) // 60

        if days > 0:
            return f"{days} days, {hours} hours"
        elif hours > 0:
            return f"{hours} hours, {minutes} minutes"
        else:
            return f"{minutes} minutes"

    async def create_time_aware_response(self, user_id: str, query: str) -> str:
        """Create time-aware response using Sesh data"""
        try:
            # Check if user is asking about time/schedule
            query_lower = query.lower()

            if any(
                word in query_lower
                for word in ["when", "time", "schedule", "event", "meeting"]
            ):
                user_events = self.get_user_schedule(user_id)

                if user_events:
                    response = "📅 **Your upcoming events:**\n\n"
                    for event in user_events[:5]:  # Show next 5 events
                        time_until = self.get_time_until_event(event.event_id)
                        response += f"• **{event.title}** - {time_until}\n"
                        response += (
                            f"  📍 {event.start_time.strftime('%Y-%m-%d %H:%M')}\n\n"
                        )
                else:
                    response = "📅 You have no upcoming events scheduled."

                return response

            elif any(word in query_lower for word in ["next", "upcoming", "soon"]):
                current_events = self.get_current_events()

                if current_events:
                    next_event = current_events[0]
                    time_until = self.get_time_until_event(next_event.event_id)
                    response = f"⏰ **Next event:** {next_event.title}\n"
                    response += f"🕐 Starts in: {time_until}\n"
                    response += (
                        f"📅 Date: {next_event.start_time.strftime('%Y-%m-%d %H:%M')}"
                    )
                else:
                    response = "📅 No upcoming events found."

                return response

            # Default response if no time-related query
            return None

        except Exception as e:
            logger.error(f"❌ Error creating time-aware response: {e}")
            return None

    def get_timezone_info(self, user_id: str) -> str:
        """Get user's timezone information"""
        # This would integrate with your memory system
        # For now, return default
        return "UTC"

    async def format_event_embed(self, event: SeshEvent) -> discord.Embed:
        """Format Sesh event as Discord embed"""
        embed = discord.Embed(
            title=f"📅 {event.title}",
            description=event.description[:2000],  # Discord limit
            color=0x00BFFF,
            timestamp=event.start_time,
        )

        # Add time information
        time_until = self.get_time_until_event(event.event_id)
        embed.add_field(
            name="⏰ Time",
            value=f"Starts in: {time_until}\n{event.start_time.strftime('%Y-%m-%d %H:%M')}",
            inline=True,
        )

        # Add attendee information
        attendee_count = len(event.attendees)
        embed.add_field(
            name="👥 Attendees", value=f"{attendee_count} people attending", inline=True
        )

        # Add timezone
        embed.add_field(name="🌍 Timezone", value=event.timezone, inline=True)

        embed.set_footer(text="Powered by Sesh Time Integration")
        return embed

    def get_mycelium_time_status(self) -> Dict:
        """Get mycelium network time integration status"""
        return {
            "total_events": len(self.sesh_events),
            "upcoming_events": len(self.get_current_events()),
            "timezone_cache_size": len(self.timezone_cache),
            "sesh_integration": "active",
            "last_updated": datetime.now().isoformat(),
        }
