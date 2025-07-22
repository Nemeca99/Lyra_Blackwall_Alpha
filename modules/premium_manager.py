"""
Premium Manager for Ethical Monetization
$2.99 forever - No token pricing, no corporate greed
"""

import json
import logging
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class UserLimits:
    """User limitation data"""

    user_id: str
    is_premium: bool
    max_memory_files: int
    max_storage_mb: int
    current_memory_files: int
    current_storage_mb: float
    upgrade_date: Optional[str] = None
    payment_method: str = "discord_role"


class PremiumManager:
    """
    Ethical Premium Management System
    - $2.99 forever pricing
    - Memory-based limitations only
    - No token pricing, no corporate greed
    """

    def __init__(self):
        self.premium_data_file = "premium_users.json"
        self.memory_limits_file = "memory_usage.json"
        self.premium_users: Dict[str, UserLimits] = {}
        self.memory_usage: Dict[str, Dict] = {}

        # Free tier limits (infrastructure-based)
        self.FREE_MAX_FILES = 100
        self.FREE_MAX_STORAGE_MB = 50

        # Premium tier (unlimited)
        self.PREMIUM_MAX_FILES = float("inf")
        self.PREMIUM_MAX_STORAGE_MB = float("inf")

        # Load existing data
        self.load_premium_data()
        self.load_memory_usage()

    def load_premium_data(self):
        """Load premium user data"""
        if Path(self.premium_data_file).exists():
            try:
                with open(self.premium_data_file, "r") as f:
                    data = json.load(f)
                    for user_id, user_data in data.items():
                        self.premium_users[user_id] = UserLimits(**user_data)
                logger.info(f"✅ Loaded {len(self.premium_users)} premium users")
            except Exception as e:
                logger.error(f"❌ Error loading premium data: {e}")

    def save_premium_data(self):
        """Save premium user data"""
        try:
            data = {}
            for user_id, limits in self.premium_users.items():
                data[user_id] = asdict(limits)

            with open(self.premium_data_file, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"✅ Saved {len(self.premium_users)} premium users")
        except Exception as e:
            logger.error(f"❌ Error saving premium data: {e}")

    def load_memory_usage(self):
        """Load memory usage data"""
        if Path(self.memory_limits_file).exists():
            try:
                with open(self.memory_limits_file, "r") as f:
                    self.memory_usage = json.load(f)
                logger.info(
                    f"✅ Loaded memory usage for {len(self.memory_usage)} users"
                )
            except Exception as e:
                logger.error(f"❌ Error loading memory usage: {e}")

    def save_memory_usage(self):
        """Save memory usage data"""
        try:
            with open(self.memory_limits_file, "w") as f:
                json.dump(self.memory_usage, f, indent=2)
            logger.info(f"✅ Saved memory usage data")
        except Exception as e:
            logger.error(f"❌ Error saving memory usage: {e}")

    def is_premium_user(self, user_id: str, member_roles: List[str] = None) -> bool:
        """Check if user has premium access (including admin/mod roles)"""
        # Check if user has admin/mod roles (free premium)
        if member_roles:
            admin_roles = ["admin", "administrator", "mod", "moderator", "moderator+", "admin+"]
            for role in member_roles:
                if role.lower() in admin_roles:
                    return True
        
        # Check paid premium status
        return user_id in self.premium_users and self.premium_users[user_id].is_premium

    def add_premium_user(
        self, user_id: str, payment_method: str = "discord_role"
    ) -> bool:
        """Add user to premium tier"""
        try:
            limits = UserLimits(
                user_id=user_id,
                is_premium=True,
                max_memory_files=self.PREMIUM_MAX_FILES,
                max_storage_mb=self.PREMIUM_MAX_STORAGE_MB,
                current_memory_files=0,
                current_storage_mb=0.0,
                upgrade_date=datetime.now().isoformat(),
                payment_method=payment_method,
            )

            self.premium_users[user_id] = limits
            self.save_premium_data()
            logger.info(f"✅ Added premium user: {user_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Error adding premium user: {e}")
            return False

    def remove_premium_user(self, user_id: str) -> bool:
        """Remove user from premium tier"""
        if user_id in self.premium_users:
            self.premium_users[user_id].is_premium = False
            self.premium_users[user_id].max_memory_files = self.FREE_MAX_FILES
            self.premium_users[user_id].max_storage_mb = self.FREE_MAX_STORAGE_MB
            self.save_premium_data()
            logger.info(f"✅ Removed premium user: {user_id}")
            return True
        return False

    def get_user_limits(self, user_id: str, member_roles: List[str] = None) -> UserLimits:
        """Get user's current limits (including admin/mod roles)"""
        # Check if user has admin/mod roles (free premium)
        is_admin_mod = False
        if member_roles:
            admin_roles = ["admin", "administrator", "mod", "moderator", "moderator+", "admin+"]
            for role in member_roles:
                if role.lower() in admin_roles:
                    is_admin_mod = True
                    break
        
        if user_id in self.premium_users:
            limits = self.premium_users[user_id]
            # Override with admin/mod status if applicable
            if is_admin_mod:
                limits.is_premium = True
                limits.max_memory_files = self.PREMIUM_MAX_FILES
                limits.max_storage_mb = self.PREMIUM_MAX_STORAGE_MB
            return limits
        
        # Create user limits (free or admin/mod)
        if is_admin_mod:
            limits = UserLimits(
                user_id=user_id,
                is_premium=True,
                max_memory_files=self.PREMIUM_MAX_FILES,
                max_storage_mb=self.PREMIUM_MAX_STORAGE_MB,
                current_memory_files=0,
                current_storage_mb=0.0,
                payment_method="admin_mod_role"
            )
        else:
            limits = UserLimits(
                user_id=user_id,
                is_premium=False,
                max_memory_files=self.FREE_MAX_FILES,
                max_storage_mb=self.FREE_MAX_STORAGE_MB,
                current_memory_files=0,
                current_storage_mb=0.0
            )

        # Initialize memory usage tracking
        if user_id not in self.memory_usage:
            self.memory_usage[user_id] = {
                "files": 0,
                "storage_mb": 0.0,
                "last_updated": datetime.now().isoformat(),
            }

        # Update current usage
        limits.current_memory_files = self.memory_usage[user_id]["files"]
        limits.current_storage_mb = self.memory_usage[user_id]["storage_mb"]

        return limits

    def can_add_memory(
        self, user_id: str, file_size_mb: float = 0.1
    ) -> Tuple[bool, str]:
        """Check if user can add more memory"""
        limits = self.get_user_limits(user_id)

        if limits.is_premium:
            return True, "Unlimited storage available"

        # Check file count limit
        if limits.current_memory_files >= limits.max_memory_files:
            return (
                False,
                f"Memory file limit reached ({limits.current_memory_files}/{limits.max_memory_files})",
            )

        # Check storage limit
        if limits.current_storage_mb + file_size_mb > limits.max_storage_mb:
            return (
                False,
                f"Storage limit reached ({limits.current_storage_mb:.1f}/{limits.max_storage_mb}MB)",
            )

        return True, "Memory can be added"

    def add_memory_usage(self, user_id: str, file_size_mb: float = 0.1) -> bool:
        """Track memory usage for user"""
        try:
            if user_id not in self.memory_usage:
                self.memory_usage[user_id] = {
                    "files": 0,
                    "storage_mb": 0.0,
                    "last_updated": datetime.now().isoformat(),
                }

            self.memory_usage[user_id]["files"] += 1
            self.memory_usage[user_id]["storage_mb"] += file_size_mb
            self.memory_usage[user_id]["last_updated"] = datetime.now().isoformat()

            self.save_memory_usage()
            logger.info(f"✅ Updated memory usage for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Error updating memory usage: {e}")
            return False

    def get_upgrade_prompt(self, user_id: str) -> str:
        """Generate upgrade prompt for user"""
        limits = self.get_user_limits(user_id)

        if limits.is_premium:
            return "🌟 **Premium User** - Unlimited storage available!"

        usage_percent_files = (
            limits.current_memory_files / limits.max_memory_files
        ) * 100
        usage_percent_storage = (
            limits.current_storage_mb / limits.max_storage_mb
        ) * 100

        prompt = f"📊 **Memory Usage:**\n"
        prompt += f"📁 Files: {limits.current_memory_files}/{limits.max_memory_files} ({usage_percent_files:.1f}%)\n"
        prompt += f"💾 Storage: {limits.current_storage_mb:.1f}/{limits.max_storage_mb}MB ({usage_percent_storage:.1f}%)\n\n"

        if usage_percent_files > 80 or usage_percent_storage > 80:
            prompt += "⚠️ **Approaching limits!**\n\n"

        prompt += "💎 **Upgrade to Premium for $2.99:**\n"
        prompt += "• Unlimited memory files\n"
        prompt += "• Unlimited storage\n"
        prompt += "• Advanced mycelium network features\n"
        prompt += "• Priority processing\n"
        prompt += "• Support the project\n\n"
        prompt += "🎯 **No token pricing, no corporate greed - just $2.99 forever!**"

        return prompt

    def get_premium_status_embed(self, user_id: str, member_roles: List[str] = None) -> Dict:
        """Get premium status for embed display (including admin/mod roles)"""
        limits = self.get_user_limits(user_id, member_roles)

        if limits.is_premium:
            return {
                "title": "💎 Premium User",
                "description": "Unlimited access to all features!",
                "color": 0xFFD700,  # Gold
                "fields": [
                    {"name": "Status", "value": "✅ Premium Active", "inline": True},
                    {"name": "Memory Files", "value": "∞ Unlimited", "inline": True},
                    {"name": "Storage", "value": "∞ Unlimited", "inline": True},
                    {
                        "name": "Upgraded",
                        "value": (
                            limits.upgrade_date[:10]
                            if limits.upgrade_date
                            else "Unknown"
                        ),
                        "inline": True,
                    },
                ],
            }
        else:
            usage_percent_files = (
                limits.current_memory_files / limits.max_memory_files
            ) * 100
            usage_percent_storage = (
                limits.current_storage_mb / limits.max_storage_mb
            ) * 100

            return {
                "title": "🆓 Free User",
                "description": "Upgrade to unlock unlimited features!",
                "color": 0x00BFFF,  # Blue
                "fields": [
                    {
                        "name": "Memory Files",
                        "value": f"{limits.current_memory_files}/{limits.max_memory_files} ({usage_percent_files:.1f}%)",
                        "inline": True,
                    },
                    {
                        "name": "Storage",
                        "value": f"{limits.current_storage_mb:.1f}/{limits.max_storage_mb}MB ({usage_percent_storage:.1f}%)",
                        "inline": True,
                    },
                    {"name": "Upgrade Cost", "value": "$2.99 forever", "inline": True},
                    {
                        "name": "Features",
                        "value": "Unlimited memory, advanced features",
                        "inline": True,
                    },
                ],
            }

    def get_ethical_pricing_info(self) -> str:
        """Get information about ethical pricing"""
        info = "🎯 **Our Ethical Pricing Philosophy:**\n\n"
        info += "✅ **$2.99 forever** - No price increases, no hidden fees\n"
        info += "✅ **No token pricing** - No per-message charges\n"
        info += "✅ **No corporate greed** - Fair, transparent pricing\n"
        info += "✅ **Infrastructure-based limits** - Only limited by actual costs\n"
        info += "✅ **Free API access** - When we launch, our API will be free\n\n"
        info += "🆓 **Free Tier:** Full functionality, 100 files, 50MB storage\n"
        info += "💎 **Premium Tier:** Everything from free + unlimited storage\n\n"
        info += "🌟 **Support innovation, not corporate greed!**"

        return info
