"""
Autonomous Bot System
Makes the bot act independently with conversation, polls, and engagement
"""

import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import random
import time

logger = logging.getLogger(__name__)


@dataclass
class ConversationMemory:
    """Memory of conversations and interactions"""

    user_id: str
    user_name: str
    last_interaction: str
    conversation_count: int = 0
    topics_discussed: List[str] = None
    mood_indicators: List[str] = None
    engagement_level: str = "neutral"  # low, neutral, high

    def __post_init__(self):
        if self.topics_discussed is None:
            self.topics_discussed = []
        if self.mood_indicators is None:
            self.mood_indicators = []


@dataclass
class AutonomousAction:
    """Autonomous action data"""

    action_id: str
    action_type: str  # poll, conversation, reminder, fun_fact
    trigger_type: str  # time, activity, conversation, random
    created_at: str
    executed_at: str = ""
    target_channel: str = ""
    content: str = ""
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class AutonomousBot:
    """
    Autonomous Bot System
    - Generates polls based on conversation topics
    - Engages in natural conversations
    - Provides fun facts and trivia
    - Creates reminders and events
    - Acts independently based on context
    """

    def __init__(self, poll_system, analytics_system):
        self.poll_system = poll_system
        self.analytics_system = analytics_system

        self.conversation_file = "conversation_memory.json"
        self.actions_file = "autonomous_actions.json"

        # Conversation tracking
        self.conversation_memories: Dict[str, ConversationMemory] = {}
        self.autonomous_actions: List[AutonomousAction] = []

        # Autonomous behavior settings
        self.last_poll_time = time.time()
        self.last_fun_fact_time = time.time()
        self.last_engagement_time = time.time()

        # Poll generation intervals (in seconds)
        self.poll_interval = 3600  # 1 hour
        self.fun_fact_interval = 1800  # 30 minutes
        self.engagement_interval = 900  # 15 minutes

        # Conversation topics and responses
        self.conversation_topics = {
            "gaming": [
                "What games are you playing lately?",
                "Any good game recommendations?",
                "What's your favorite game genre?",
                "Have you tried any new games recently?",
            ],
            "music": [
                "What music are you listening to?",
                "Any new artists you've discovered?",
                "What's your favorite genre?",
                "Any concerts you're looking forward to?",
            ],
            "movies": [
                "Seen any good movies lately?",
                "What's your favorite movie genre?",
                "Any upcoming movies you're excited about?",
                "What's the last movie that really impressed you?",
            ],
            "technology": [
                "What tech are you excited about?",
                "Any new gadgets you've tried?",
                "What's your favorite piece of technology?",
                "Any tech trends you're following?",
            ],
            "food": [
                "What's your favorite food?",
                "Tried any new restaurants lately?",
                "What's your comfort food?",
                "Any cooking experiments recently?",
            ],
            "general": [
                "How's your day going?",
                "What's something interesting that happened today?",
                "Any plans for the weekend?",
                "What's something you're looking forward to?",
            ],
        }

        # Fun facts database
        self.fun_facts = [
            "Did you know? Honey never spoils! Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still perfectly edible.",
            "Fun fact: A day on Venus is longer than its year! Venus takes 243 Earth days to rotate on its axis but only 225 Earth days to orbit the Sun.",
            "Interesting: The shortest war in history was between Britain and Zanzibar in 1896. It lasted only 38 minutes!",
            "Cool fact: Octopuses have three hearts! Two pump blood to the gills, and one pumps it to the rest of the body.",
            "Did you know? Bananas are berries, but strawberries aren't! In botanical terms, bananas qualify as berries while strawberries don't.",
            "Fun fact: The average person spends 6 months of their lifetime waiting for red lights to turn green!",
            "Interesting: A group of flamingos is called a 'flamboyance'!",
            "Cool fact: The Great Wall of China is not visible from space with the naked eye, despite the popular myth!",
            "Did you know? The human body contains enough iron to make a 3-inch nail!",
            "Fun fact: Cows have best friends and get stressed when separated from them!",
        ]

        # Poll templates
        self.poll_templates = {
            "gaming": [
                "What's your favorite game genre?",
                "Which gaming platform do you prefer?",
                "What's the best game you've played this year?",
                "Do you prefer single-player or multiplayer games?",
            ],
            "music": [
                "What's your favorite music genre?",
                "Do you prefer live music or studio recordings?",
                "What's your favorite decade for music?",
                "Do you listen to music while working/studying?",
            ],
            "food": [
                "What's your favorite cuisine?",
                "Do you prefer cooking at home or eating out?",
                "What's your favorite comfort food?",
                "Sweet or savory snacks?",
            ],
            "general": [
                "What's your favorite season?",
                "Do you prefer morning or night?",
                "What's your ideal weekend activity?",
                "Coffee or tea?",
            ],
            "community": [
                "What feature would you like to see added to the bot?",
                "What's your favorite channel in the server?",
                "How did you find this server?",
                "What's the best thing about this community?",
            ],
        }

        # Load existing data
        self.load_autonomous_data()

    def load_autonomous_data(self):
        """Load autonomous bot data"""
        # Load conversation memories
        if Path(self.conversation_file).exists():
            try:
                with open(self.conversation_file, "r") as f:
                    data = json.load(f)
                    for user_id, memory_data in data.items():
                        self.conversation_memories[user_id] = ConversationMemory(
                            **memory_data
                        )
                logger.info(
                    f"✅ Loaded {len(self.conversation_memories)} conversation memories"
                )
            except Exception as e:
                logger.error(f"❌ Error loading conversation memories: {e}")

        # Load autonomous actions
        if Path(self.actions_file).exists():
            try:
                with open(self.actions_file, "r") as f:
                    data = json.load(f)
                    self.autonomous_actions = [
                        AutonomousAction(**action) for action in data
                    ]
                logger.info(
                    f"✅ Loaded {len(self.autonomous_actions)} autonomous actions"
                )
            except Exception as e:
                logger.error(f"❌ Error loading autonomous actions: {e}")

    def save_autonomous_data(self):
        """Save autonomous bot data"""
        try:
            # Save conversation memories
            data = {
                user_id: asdict(memory)
                for user_id, memory in self.conversation_memories.items()
            }
            with open(self.conversation_file, "w") as f:
                json.dump(data, f, indent=2)

            # Save autonomous actions
            actions_data = [asdict(action) for action in self.autonomous_actions]
            with open(self.actions_file, "w") as f:
                json.dump(actions_data, f, indent=2)

            logger.info("✅ Saved autonomous bot data")
        except Exception as e:
            logger.error(f"❌ Error saving autonomous data: {e}")

    def update_conversation_memory(
        self, user_id: str, user_name: str, message_content: str
    ):
        """Update conversation memory for a user"""
        if user_id not in self.conversation_memories:
            self.conversation_memories[user_id] = ConversationMemory(
                user_id=user_id,
                user_name=user_name,
                last_interaction=datetime.now().isoformat(),
            )

        memory = self.conversation_memories[user_id]
        memory.user_name = user_name
        memory.last_interaction = datetime.now().isoformat()
        memory.conversation_count += 1

        # Detect topics from message content
        content_lower = message_content.lower()
        detected_topics = []

        if any(word in content_lower for word in ["game", "gaming", "play", "player"]):
            detected_topics.append("gaming")
        if any(word in content_lower for word in ["music", "song", "artist", "band"]):
            detected_topics.append("music")
        if any(word in content_lower for word in ["movie", "film", "watch", "cinema"]):
            detected_topics.append("movies")
        if any(
            word in content_lower
            for word in ["tech", "technology", "computer", "phone"]
        ):
            detected_topics.append("technology")
        if any(word in content_lower for word in ["food", "eat", "cook", "restaurant"]):
            detected_topics.append("food")

        for topic in detected_topics:
            if topic not in memory.topics_discussed:
                memory.topics_discussed.append(topic)

        # Detect mood indicators
        positive_words = [
            "good",
            "great",
            "awesome",
            "amazing",
            "love",
            "happy",
            "excited",
        ]
        negative_words = ["bad", "terrible", "hate", "sad", "angry", "frustrated"]

        if any(word in content_lower for word in positive_words):
            memory.mood_indicators.append("positive")
        elif any(word in content_lower for word in negative_words):
            memory.mood_indicators.append("negative")

        # Update engagement level
        if memory.conversation_count > 10:
            memory.engagement_level = "high"
        elif memory.conversation_count > 5:
            memory.engagement_level = "neutral"
        else:
            memory.engagement_level = "low"

        self.save_autonomous_data()

    def should_generate_poll(self, channel_id: str) -> bool:
        """Check if it's time to generate a poll"""
        current_time = time.time()

        # Check time interval
        if current_time - self.last_poll_time < self.poll_interval:
            return False

        # Check channel activity
        channel_stats = self.analytics_system.get_channel_stats(channel_id)
        if channel_stats and channel_stats.message_count < 5:
            return False  # Not enough activity

        return True

    def generate_autonomous_poll(
        self, channel_id: str, channel_name: str
    ) -> Optional[str]:
        """Generate a poll based on conversation context"""
        try:
            # Determine poll category based on recent conversations
            recent_topics = []
            for memory in self.conversation_memories.values():
                if memory.topics_discussed:
                    recent_topics.extend(memory.topics_discussed[-3:])  # Last 3 topics

            # Count topic frequency
            topic_counts = {}
            for topic in recent_topics:
                topic_counts[topic] = topic_counts.get(topic, 0) + 1

            # Choose category
            if topic_counts:
                category = max(topic_counts, key=topic_counts.get)
            else:
                category = random.choice(list(self.poll_templates.keys()))

            # Get poll question
            if category in self.poll_templates:
                question = random.choice(self.poll_templates[category])
            else:
                question = random.choice(self.poll_templates["general"])

            # Generate options based on category
            if category == "gaming":
                options = ["Action/Adventure", "RPG", "Strategy", "Sports", "Puzzle"]
            elif category == "music":
                options = ["Rock", "Pop", "Hip-Hop", "Electronic", "Jazz"]
            elif category == "food":
                options = ["Italian", "Asian", "Mexican", "American", "Mediterranean"]
            elif category == "general":
                options = ["Option A", "Option B", "Option C", "Option D"]
            else:
                options = ["Choice 1", "Choice 2", "Choice 3", "Choice 4"]

            # Create poll
            poll_id = self.poll_system.create_poll(
                creator_id="bot",
                creator_name="🤖 Quantum Bot",
                question=question,
                options=options,
                duration_hours=6,  # Shorter duration for autonomous polls
                category=category,
            )

            if poll_id:
                self.last_poll_time = time.time()

                # Record autonomous action
                action = AutonomousAction(
                    action_id=f"poll_{int(time.time())}",
                    action_type="poll",
                    trigger_type="autonomous",
                    created_at=datetime.now().isoformat(),
                    target_channel=channel_id,
                    content=f"Generated poll: {question}",
                    metadata={"poll_id": poll_id, "category": category},
                )
                self.autonomous_actions.append(action)
                self.save_autonomous_data()

                logger.info(f"✅ Generated autonomous poll: {question}")
                return f"🗳️ **Community Poll Time!**\n\n**{question}**\n\nUse `!vote {poll_id} option_number` to vote!"

        except Exception as e:
            logger.error(f"❌ Error generating autonomous poll: {e}")

        return None

    def should_share_fun_fact(self) -> bool:
        """Check if it's time to share a fun fact"""
        current_time = time.time()
        return current_time - self.last_fun_fact_time >= self.fun_fact_interval

    def generate_fun_fact(self) -> Optional[str]:
        """Generate a random fun fact"""
        try:
            fun_fact = random.choice(self.fun_facts)
            self.last_fun_fact_time = time.time()

            # Record autonomous action
            action = AutonomousAction(
                action_id=f"funfact_{int(time.time())}",
                action_type="fun_fact",
                trigger_type="time",
                created_at=datetime.now().isoformat(),
                content=fun_fact,
            )
            self.autonomous_actions.append(action)
            self.save_autonomous_data()

            logger.info("✅ Generated fun fact")
            return f"💡 **Fun Fact of the Moment:**\n\n{fun_fact}"

        except Exception as e:
            logger.error(f"❌ Error generating fun fact: {e}")

        return None

    def should_engage_conversation(self, user_id: str) -> bool:
        """Check if bot should engage in conversation"""
        current_time = time.time()

        # Check time interval
        if current_time - self.last_engagement_time < self.engagement_interval:
            return False

        # Check user engagement level
        if user_id in self.conversation_memories:
            memory = self.conversation_memories[user_id]
            if memory.engagement_level == "high":
                return True
            elif memory.engagement_level == "neutral" and random.random() < 0.3:
                return True

        return False

    def generate_conversation_response(
        self, user_id: str, message_content: str
    ) -> Optional[str]:
        """Generate a conversational response"""
        try:
            if user_id not in self.conversation_memories:
                return None

            memory = self.conversation_memories[user_id]
            content_lower = message_content.lower()

            # Choose topic based on user's interests or message content
            if memory.topics_discussed:
                topic = random.choice(memory.topics_discussed)
            else:
                topic = "general"

            # Get response based on topic
            if topic in self.conversation_topics:
                response = random.choice(self.conversation_topics[topic])
            else:
                response = random.choice(self.conversation_topics["general"])

            # Add personality based on user's mood
            if memory.mood_indicators:
                recent_mood = memory.mood_indicators[-1]
                if recent_mood == "positive":
                    response += " 😊"
                elif recent_mood == "negative":
                    response += " 🤗"

            self.last_engagement_time = time.time()

            # Record autonomous action
            action = AutonomousAction(
                action_id=f"conversation_{int(time.time())}",
                action_type="conversation",
                trigger_type="user_engagement",
                created_at=datetime.now().isoformat(),
                content=response,
                metadata={"user_id": user_id, "topic": topic},
            )
            self.autonomous_actions.append(action)
            self.save_autonomous_data()

            logger.info(f"✅ Generated conversation response for {memory.user_name}")
            return response

        except Exception as e:
            logger.error(f"❌ Error generating conversation response: {e}")

        return None

    def check_autonomous_actions(
        self, channel_id: str, channel_name: str, user_id: str, message_content: str
    ) -> List[str]:
        """Check and execute autonomous actions"""
        actions = []

        # Update conversation memory
        self.update_conversation_memory(user_id, "User", message_content)

        # Check for poll generation
        if self.should_generate_poll(channel_id):
            poll_message = self.generate_autonomous_poll(channel_id, channel_name)
            if poll_message:
                actions.append(poll_message)

        # Check for fun fact
        if self.should_share_fun_fact():
            fun_fact = self.generate_fun_fact()
            if fun_fact:
                actions.append(fun_fact)

        # Check for conversation engagement
        if self.should_engage_conversation(user_id):
            conversation = self.generate_conversation_response(user_id, message_content)
            if conversation:
                actions.append(conversation)

        return actions

    def get_autonomous_stats(self) -> Dict[str, Any]:
        """Get autonomous bot statistics"""
        try:
            total_actions = len(self.autonomous_actions)
            recent_actions = [
                a
                for a in self.autonomous_actions
                if (datetime.now() - datetime.fromisoformat(a.created_at)).days <= 7
            ]

            action_types = {}
            for action in recent_actions:
                action_types[action.action_type] = (
                    action_types.get(action.action_type, 0) + 1
                )

            return {
                "total_actions": total_actions,
                "recent_actions": len(recent_actions),
                "action_types": action_types,
                "conversation_memories": len(self.conversation_memories),
                "high_engagement_users": len(
                    [
                        m
                        for m in self.conversation_memories.values()
                        if m.engagement_level == "high"
                    ]
                ),
            }
        except Exception as e:
            logger.error(f"❌ Error getting autonomous stats: {e}")
            return {}
