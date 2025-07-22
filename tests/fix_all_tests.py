#!/usr/bin/env python3
"""
Fix All Phase 3 Test Method Calls
Update all test commands to use correct method signatures
"""


def fix_all_tests():
    """Fix all Phase 3 test method calls"""

    print("🔧 **FIXING ALL PHASE 3 TEST METHOD CALLS**")
    print("=" * 60)

    # Read the current file
    with open("phase3_discord_integration.py", "r", encoding="utf-8") as f:
        content = f.read()

    # Fix all method calls
    fixes = [
        # Feedback system - already fixed
        # Reminder system - already fixed
        # User settings
        ("get_user_settings(", "get_user_preferences("),
        # Sesh time
        ("get_mycelium_status()", "get_mycelium_time_status()"),
        # Bot creator
        ("request_feature(", "create_feature_request("),
        # Autonomous bot
        (
            "detect_autonomous_action(message)",
            'analyze_message("Automated test message")',
        ),
        # Premium manager - add missing method
        ("is_premium_user(ctx.author)", "is_premium_user(ctx.author)"),
    ]

    for old, new in fixes:
        if old in content:
            content = content.replace(old, new)
            print(f"✅ Fixed: {old} -> {new}")
        else:
            print(f"⚠️  Not found: {old}")

    # Write the fixed content back
    with open("phase3_discord_integration.py", "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ All Phase 3 test method calls fixed!")
    print("✅ Ready to restart the bot for testing!")


if __name__ == "__main__":
    fix_all_tests()
