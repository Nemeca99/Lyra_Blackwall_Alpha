"""
Analytics and Statistics System
Tracks server usage, user engagement, and bot performance metrics
"""

import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import time

logger = logging.getLogger(__name__)


@dataclass
class UserActivity:
    """User activity tracking data"""

    user_id: str
    user_name: str
    message_count: int = 0
    command_count: int = 0
    feedback_count: int = 0
    first_seen: str = ""
    last_seen: str = ""
    total_interactions: int = 0
    favorite_commands: List[str] = None

    def __post_init__(self):
        if self.favorite_commands is None:
            self.favorite_commands = []


@dataclass
class ChannelStats:
    """Channel activity statistics"""

    channel_id: str
    channel_name: str
    message_count: int = 0
    command_count: int = 0
    active_users: int = 0
    last_activity: str = ""
    peak_hour: str = ""
    average_daily_messages: float = 0.0


@dataclass
class BotPerformance:
    """Bot performance metrics"""

    uptime_seconds: int = 0
    total_commands_processed: int = 0
    average_response_time: float = 0.0
    error_count: int = 0
    memory_usage_mb: float = 0.0
    active_channels: int = 0
    total_users: int = 0
    premium_users: int = 0


class AnalyticsSystem:
    """
    Analytics and Statistics System
    - Tracks user activity and engagement
    - Monitors channel performance
    - Measures bot performance metrics
    - Provides insights and trends
    """

    def __init__(self):
        self.analytics_file = "analytics_data.json"
        self.daily_stats_file = "daily_statistics.json"
        self.performance_file = "performance_metrics.json"

        # Data storage
        self.user_activities: Dict[str, UserActivity] = {}
        self.channel_stats: Dict[str, ChannelStats] = {}
        self.bot_performance = BotPerformance()
        self.daily_stats: Dict[str, Dict] = {}

        # Real-time tracking
        self.command_times: List[float] = []
        self.error_log: List[Dict] = []
        self.start_time = time.time()

        # Load existing data
        self.load_analytics_data()

    def load_analytics_data(self):
        """Load analytics data from files"""
        # Load user activities
        if Path(self.analytics_file).exists():
            try:
                with open(self.analytics_file, "r") as f:
                    data = json.load(f)
                    for user_id, user_data in data.get("users", {}).items():
                        self.user_activities[user_id] = UserActivity(**user_data)
                    for channel_id, channel_data in data.get("channels", {}).items():
                        self.channel_stats[channel_id] = ChannelStats(**channel_data)
                    if "performance" in data:
                        self.bot_performance = BotPerformance(**data["performance"])
                logger.info(
                    f"✅ Loaded analytics data: {len(self.user_activities)} users, {len(self.channel_stats)} channels"
                )
            except Exception as e:
                logger.error(f"❌ Error loading analytics: {e}")

        # Load daily statistics
        if Path(self.daily_stats_file).exists():
            try:
                with open(self.daily_stats_file, "r") as f:
                    self.daily_stats = json.load(f)
                logger.info(f"✅ Loaded {len(self.daily_stats)} days of statistics")
            except Exception as e:
                logger.error(f"❌ Error loading daily stats: {e}")

    def save_analytics_data(self):
        """Save analytics data to files"""
        try:
            # Prepare data
            data = {
                "users": {
                    user_id: asdict(activity)
                    for user_id, activity in self.user_activities.items()
                },
                "channels": {
                    channel_id: asdict(stats)
                    for channel_id, stats in self.channel_stats.items()
                },
                "performance": asdict(self.bot_performance),
                "last_updated": datetime.now().isoformat(),
            }

            with open(self.analytics_file, "w") as f:
                json.dump(data, f, indent=2)

            # Save daily statistics
            with open(self.daily_stats_file, "w") as f:
                json.dump(self.daily_stats, f, indent=2)

            logger.info("✅ Saved analytics data")
        except Exception as e:
            logger.error(f"❌ Error saving analytics: {e}")

    def track_user_activity(
        self,
        user_id: str,
        user_name: str,
        channel_id: str,
        channel_name: str,
        is_command: bool = False,
        command_name: str = "",
        is_feedback: bool = False,
    ):
        """Track user activity and interactions"""
        try:
            current_time = datetime.now().isoformat()

            # Update user activity
            if user_id not in self.user_activities:
                self.user_activities[user_id] = UserActivity(
                    user_id=user_id, user_name=user_name, first_seen=current_time
                )

            user_activity = self.user_activities[user_id]
            user_activity.user_name = user_name
            user_activity.last_seen = current_time
            user_activity.message_count += 1
            user_activity.total_interactions += 1

            if is_command:
                user_activity.command_count += 1
                if command_name and command_name not in user_activity.favorite_commands:
                    user_activity.favorite_commands.append(command_name)

            if is_feedback:
                user_activity.feedback_count += 1

            # Update channel stats
            if channel_id not in self.channel_stats:
                self.channel_stats[channel_id] = ChannelStats(
                    channel_id=channel_id, channel_name=channel_name
                )

            channel_stat = self.channel_stats[channel_id]
            channel_stat.channel_name = channel_name
            channel_stat.message_count += 1
            channel_stat.last_activity = current_time

            if is_command:
                channel_stat.command_count += 1

            # Track unique users per channel
            if not hasattr(channel_stat, "unique_users"):
                channel_stat.unique_users = set()
            channel_stat.unique_users.add(user_id)
            channel_stat.active_users = len(channel_stat.unique_users)

            # Update daily statistics
            self.update_daily_stats(current_time, is_command, is_feedback)

        except Exception as e:
            logger.error(f"❌ Error tracking user activity: {e}")

    def track_command_performance(
        self,
        command_name: str,
        response_time: float,
        success: bool = True,
        error_message: str = "",
    ):
        """Track command performance metrics"""
        try:
            self.command_times.append(response_time)

            # Keep only last 1000 command times for average calculation
            if len(self.command_times) > 1000:
                self.command_times = self.command_times[-1000:]

            self.bot_performance.total_commands_processed += 1
            self.bot_performance.average_response_time = sum(self.command_times) / len(
                self.command_times
            )

            if not success:
                self.bot_performance.error_count += 1
                self.error_log.append(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "command": command_name,
                        "error": error_message,
                    }
                )

                # Keep only last 100 errors
                if len(self.error_log) > 100:
                    self.error_log = self.error_log[-100:]

        except Exception as e:
            logger.error(f"❌ Error tracking command performance: {e}")

    def update_daily_stats(self, timestamp: str, is_command: bool, is_feedback: bool):
        """Update daily statistics"""
        try:
            date_key = timestamp[:10]  # YYYY-MM-DD

            if date_key not in self.daily_stats:
                self.daily_stats[date_key] = {
                    "total_messages": 0,
                    "total_commands": 0,
                    "total_feedback": 0,
                    "active_users": set(),
                    "active_channels": set(),
                    "hourly_activity": defaultdict(int),
                }

            daily = self.daily_stats[date_key]
            daily["total_messages"] += 1

            if is_command:
                daily["total_commands"] += 1

            if is_feedback:
                daily["total_feedback"] += 1

            # Track hourly activity
            hour = timestamp[11:13]
            daily["hourly_activity"][hour] += 1

        except Exception as e:
            logger.error(f"❌ Error updating daily stats: {e}")

    def get_server_stats(self) -> Dict[str, Any]:
        """Get comprehensive server statistics"""
        try:
            total_users = len(self.user_activities)
            total_channels = len(self.channel_stats)

            # Calculate engagement metrics
            active_users_7d = 0
            active_users_24h = 0
            current_time = datetime.now()

            for user_activity in self.user_activities.values():
                if user_activity.last_seen:
                    last_seen = datetime.fromisoformat(user_activity.last_seen)
                    if (current_time - last_seen).days <= 7:
                        active_users_7d += 1
                    if (current_time - last_seen).days <= 1:
                        active_users_24h += 1

            # Get top channels
            top_channels = sorted(
                self.channel_stats.values(), key=lambda x: x.message_count, reverse=True
            )[:5]

            # Get top users
            top_users = sorted(
                self.user_activities.values(),
                key=lambda x: x.message_count,
                reverse=True,
            )[:5]

            # Get most used commands
            all_commands = []
            for user_activity in self.user_activities.values():
                all_commands.extend(user_activity.favorite_commands)
            command_counts = Counter(all_commands)
            top_commands = command_counts.most_common(5)

            return {
                "total_users": total_users,
                "total_channels": total_channels,
                "active_users_7d": active_users_7d,
                "active_users_24h": active_users_24h,
                "total_messages": sum(
                    u.message_count for u in self.user_activities.values()
                ),
                "total_commands": sum(
                    u.command_count for u in self.user_activities.values()
                ),
                "total_feedback": sum(
                    u.feedback_count for u in self.user_activities.values()
                ),
                "top_channels": [
                    (c.channel_name, c.message_count) for c in top_channels
                ],
                "top_users": [(u.user_name, u.message_count) for u in top_users],
                "top_commands": top_commands,
                "bot_uptime_hours": (time.time() - self.start_time) / 3600,
                "average_response_time": self.bot_performance.average_response_time,
                "error_rate": (
                    self.bot_performance.error_count
                    / max(self.bot_performance.total_commands_processed, 1)
                )
                * 100,
            }

        except Exception as e:
            logger.error(f"❌ Error getting server stats: {e}")
            return {}

    def get_user_activity(self, user_id: str) -> Optional[UserActivity]:
        """Get activity data for specific user"""
        return self.user_activities.get(user_id)

    def get_channel_stats(self, channel_id: str) -> Optional[ChannelStats]:
        """Get statistics for specific channel"""
        return self.channel_stats.get(channel_id)

    def get_trends(self, days: int = 7) -> Dict[str, Any]:
        """Get trends over specified days"""
        try:
            trends = {
                "daily_messages": [],
                "daily_commands": [],
                "daily_feedback": [],
                "peak_hours": [],
                "growth_rate": 0.0,
            }

            # Get recent daily stats
            current_time = datetime.now()
            recent_days = []

            for i in range(days):
                date = current_time - timedelta(days=i)
                date_key = date.strftime("%Y-%m-%d")
                if date_key in self.daily_stats:
                    recent_days.append((date_key, self.daily_stats[date_key]))

            recent_days.reverse()  # Oldest first

            for date_key, daily_data in recent_days:
                trends["daily_messages"].append(
                    (date_key, daily_data["total_messages"])
                )
                trends["daily_commands"].append(
                    (date_key, daily_data["total_commands"])
                )
                trends["daily_feedback"].append(
                    (date_key, daily_data["total_feedback"])
                )

                # Find peak hour
                if daily_data["hourly_activity"]:
                    peak_hour = max(
                        daily_data["hourly_activity"].items(), key=lambda x: x[1]
                    )
                    trends["peak_hours"].append((date_key, peak_hour[0], peak_hour[1]))

            # Calculate growth rate
            if len(trends["daily_messages"]) >= 2:
                first_day = trends["daily_messages"][0][1]
                last_day = trends["daily_messages"][-1][1]
                if first_day > 0:
                    trends["growth_rate"] = ((last_day - first_day) / first_day) * 100

            return trends

        except Exception as e:
            logger.error(f"❌ Error getting trends: {e}")
            return {}

    def handle_analytics_command(
        self, command: str, user_id: str, user_name: str
    ) -> str:
        """Handle analytics commands"""
        command_lower = command.lower()

        if command_lower == "!stats":
            return self.get_stats_display()

        elif command_lower == "!activity":
            return self.get_activity_display(user_id)

        elif command_lower == "!trends":
            return self.get_trends_display()

        elif command_lower == "!leaderboard":
            return self.get_leaderboard_display()

        elif command_lower == "!bot_health":
            return self.get_bot_health_display()

        elif command_lower == "!analytics_help":
            return self.get_analytics_help()

        return None

    def get_stats_display(self) -> str:
        """Get formatted server statistics display"""
        stats = self.get_server_stats()
        if not stats:
            return "❌ Error retrieving server statistics."

        response = "📊 **Server Statistics**\n\n"

        # Overview
        response += "🌍 **Overview:**\n"
        response += f"   Total Users: {stats['total_users']}\n"
        response += f"   Active (7d): {stats['active_users_7d']}\n"
        response += f"   Active (24h): {stats['active_users_24h']}\n"
        response += f"   Total Channels: {stats['total_channels']}\n\n"

        # Activity
        response += "💬 **Activity:**\n"
        response += f"   Total Messages: {stats['total_messages']:,}\n"
        response += f"   Total Commands: {stats['total_commands']:,}\n"
        response += f"   Total Feedback: {stats['total_feedback']:,}\n\n"

        # Top channels
        response += "📢 **Top Channels:**\n"
        for i, (channel, count) in enumerate(stats["top_channels"][:3], 1):
            response += f"   {i}. #{channel}: {count:,} messages\n"

        response += "\n"

        # Top users
        response += "👥 **Top Users:**\n"
        for i, (user, count) in enumerate(stats["top_users"][:3], 1):
            response += f"   {i}. {user}: {count:,} messages\n"

        response += "\n"

        # Bot performance
        response += "🤖 **Bot Performance:**\n"
        response += f"   Uptime: {stats['bot_uptime_hours']:.1f} hours\n"
        response += f"   Avg Response: {stats['average_response_time']:.2f}s\n"
        response += f"   Error Rate: {stats['error_rate']:.1f}%\n"

        return response

    def get_activity_display(self, user_id: str) -> str:
        """Get user activity display"""
        user_activity = self.get_user_activity(user_id)
        if not user_activity:
            return "📝 No activity data found for you yet."

        response = f"📈 **Activity for {user_activity.user_name}**\n\n"

        response += "💬 **Messages:**\n"
        response += f"   Total Messages: {user_activity.message_count:,}\n"
        response += f"   Commands Used: {user_activity.command_count:,}\n"
        response += f"   Feedback Given: {user_activity.feedback_count:,}\n"
        response += f"   Total Interactions: {user_activity.total_interactions:,}\n\n"

        response += "📅 **Timeline:**\n"
        response += f"   First Seen: {user_activity.first_seen[:10]}\n"
        response += f"   Last Active: {user_activity.last_seen[:10]}\n\n"

        if user_activity.favorite_commands:
            response += "⭐ **Favorite Commands:**\n"
            for cmd in user_activity.favorite_commands[:5]:
                response += f"   • {cmd}\n"

        return response

    def get_trends_display(self) -> str:
        """Get trends display"""
        trends = self.get_trends(7)
        if not trends:
            return "❌ Error retrieving trends data."

        response = "📈 **7-Day Trends**\n\n"

        # Growth rate
        response += f"📊 **Growth Rate:** {trends['growth_rate']:+.1f}%\n\n"

        # Recent activity
        if trends["daily_messages"]:
            response += "📅 **Recent Activity:**\n"
            for date, count in trends["daily_messages"][-3:]:
                response += f"   {date}: {count} messages\n"

        response += "\n"

        # Peak hours
        if trends["peak_hours"]:
            response += "⏰ **Peak Activity Hours:**\n"
            for date, hour, count in trends["peak_hours"][-3:]:
                response += f"   {date} {hour}:00 - {count} messages\n"

        return response

    def get_leaderboard_display(self) -> str:
        """Get leaderboard display"""
        stats = self.get_server_stats()
        if not stats:
            return "❌ Error retrieving leaderboard data."

        response = "🏆 **Leaderboard**\n\n"

        # Top users
        response += "👥 **Top Users:**\n"
        for i, (user, count) in enumerate(stats["top_users"][:5], 1):
            emoji = (
                "🥇"
                if i == 1
                else "🥈" if i == 2 else "🥉" if i == 3 else "4️⃣" if i == 4 else "5️⃣"
            )
            response += f"   {emoji} {user}: {count:,} messages\n"

        response += "\n"

        # Top channels
        response += "📢 **Top Channels:**\n"
        for i, (channel, count) in enumerate(stats["top_channels"][:5], 1):
            emoji = (
                "🥇"
                if i == 1
                else "🥈" if i == 2 else "🥉" if i == 3 else "4️⃣" if i == 4 else "5️⃣"
            )
            response += f"   {emoji} #{channel}: {count:,} messages\n"

        response += "\n"

        # Top commands
        response += "⚡ **Most Used Commands:**\n"
        for i, (cmd, count) in enumerate(stats["top_commands"][:5], 1):
            emoji = (
                "🥇"
                if i == 1
                else "🥈" if i == 2 else "🥉" if i == 3 else "4️⃣" if i == 4 else "5️⃣"
            )
            response += f"   {emoji} {cmd}: {count} uses\n"

        return response

    def get_bot_health_display(self) -> str:
        """Get bot health display"""
        stats = self.get_server_stats()
        if not stats:
            return "❌ Error retrieving bot health data."

        response = "🤖 **Bot Health Report**\n\n"

        # Performance metrics
        response += "⚡ **Performance:**\n"
        response += f"   Uptime: {stats['bot_uptime_hours']:.1f} hours\n"
        response += f"   Avg Response Time: {stats['average_response_time']:.2f}s\n"
        response += f"   Commands Processed: {stats['total_commands']:,}\n"
        response += f"   Error Rate: {stats['error_rate']:.1f}%\n\n"

        # Health indicators
        health_status = (
            "🟢 Excellent"
            if stats["error_rate"] < 1
            else "🟡 Good" if stats["error_rate"] < 5 else "🔴 Needs Attention"
        )
        response += f"🏥 **Health Status:** {health_status}\n\n"

        # Recommendations
        response += "💡 **Recommendations:**\n"
        if stats["error_rate"] > 5:
            response += "   • Check error logs for issues\n"
        if stats["average_response_time"] > 2.0:
            response += "   • Consider performance optimization\n"
        if stats["bot_uptime_hours"] < 24:
            response += "   • Monitor uptime stability\n"
        else:
            response += "   • All systems operational\n"

        return response

    def get_analytics_help(self) -> str:
        """Get analytics help information"""
        help_text = "📊 **Analytics System Help**\n\n"
        help_text += "**Commands:**\n"
        help_text += "• `!stats` - Server statistics overview\n"
        help_text += "• `!activity` - Your personal activity data\n"
        help_text += "• `!trends` - 7-day activity trends\n"
        help_text += "• `!leaderboard` - Top users and channels\n"
        help_text += "• `!bot_health` - Bot performance metrics\n"
        help_text += "• `!analytics_help` - Show this help\n\n"
        help_text += "**Privacy:** All analytics respect user privacy settings and are anonymized where possible."

        return help_text
