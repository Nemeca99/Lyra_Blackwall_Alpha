"""
Kitchen Staff System - Ollama-Managed Public Memory Management
Part of the Michelin-Star AI Kitchen Architecture

Role: The Kitchen Staff/Waiters who manage all raw ingredients (memory indexing), 
keep inventory (public memory pool), and handle kitchen logistics.

Location: D:\Books\.Material\Implementation\05_Lyra\Systems\Memory_Systems
"""

import json
import sqlite3
import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import ollama
import faiss
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class PublicMemory:
    """Public memory entry for chat interactions"""

    user_id: str
    message_content: str
    emotion_tags: List[str]
    timestamp: datetime
    context_tags: List[str]
    interaction_type: str  # 'passive', 'active', 'response'
    memory_id: Optional[str] = None


@dataclass
class MemoryIngredient:
    """Ingredient package for the Executive Chef"""

    user_id: str
    context_summary: str
    relevant_memories: List[PublicMemory]
    emotion_profile: Dict[str, float]
    interaction_history: List[str]
    timestamp: datetime


class KitchenStaff:
    """
    The Kitchen Staff system - manages public memory, indexing, and provides
    ingredients to the Executive Chef (LM Studio)
    """

    def __init__(self, db_path: str = "public_memory.db"):
        self.db_path = db_path
        self.vector_index = None
        self.ollama_client = None
        self.public_memory_pool = []
        self.initialize_system()

    def initialize_system(self):
        """Initialize the kitchen staff system"""
        logger.info("🧑‍🍳 Initializing Kitchen Staff System...")

        # Initialize database
        self.setup_database()

        # Initialize Ollama client
        self.ollama_client = ollama.Client()

        # Initialize vector index for memory search
        self.setup_vector_index()

        logger.info("✅ Kitchen Staff System initialized successfully")

    def setup_database(self):
        """Setup SQLite database for public memory storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS public_memories (
                memory_id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                message_content TEXT NOT NULL,
                emotion_tags TEXT,
                context_tags TEXT,
                interaction_type TEXT,
                timestamp TEXT,
                embedding_vector BLOB
            )
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_user_id ON public_memories(user_id)
        """
        )

        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_timestamp ON public_memories(timestamp)
        """
        )

        conn.commit()
        conn.close()
        logger.info("📊 Public memory database initialized")

    def setup_vector_index(self):
        """Initialize FAISS vector index for memory search"""
        # Initialize with 128-dimensional vectors (adjust based on your embedding model)
        dimension = 128
        self.vector_index = faiss.IndexFlatL2(dimension)
        logger.info("🔍 Vector index initialized for memory search")

    async def process_public_message(
        self, user_id: str, message: str, emotion_tags: List[str] = None
    ) -> str:
        """
        Process a public message and store it in public memory pool

        Args:
            user_id: Discord user ID
            message: Message content
            emotion_tags: Emotional context tags

        Returns:
            Memory ID of stored message
        """
        logger.info(f"📝 Processing public message from user {user_id}")

        # Create memory entry
        memory = PublicMemory(
            user_id=user_id,
            message_content=message,
            emotion_tags=emotion_tags or [],
            timestamp=datetime.now(),
            context_tags=self.extract_context_tags(message),
            interaction_type="passive",
        )

        # Generate embedding
        embedding = await self.generate_embedding(message)

        # Store in database
        memory_id = self.store_memory(memory, embedding)
        memory.memory_id = memory_id

        # Add to public memory pool
        self.public_memory_pool.append(memory)

        logger.info(f"✅ Public message stored with ID: {memory_id}")
        return memory_id

    def extract_context_tags(self, message: str) -> List[str]:
        """Extract context tags from message content"""
        # Simple keyword extraction - can be enhanced with NLP
        keywords = []
        message_lower = message.lower()

        # Basic context detection
        if any(word in message_lower for word in ["help", "question", "ask"]):
            keywords.append("question")
        if any(word in message_lower for word in ["happy", "excited", "great"]):
            keywords.append("positive")
        if any(word in message_lower for word in ["sad", "angry", "frustrated"]):
            keywords.append("negative")
        if any(word in message_lower for word in ["work", "job", "career"]):
            keywords.append("work")
        if any(word in message_lower for word in ["game", "play", "fun"]):
            keywords.append("entertainment")

        return keywords

    async def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding using Ollama"""
        try:
            response = self.ollama_client.embeddings(
                model="qwen2.5:3b", prompt=text  # Using Qwen2.5 for embeddings
            )
            return np.array(response["embedding"], dtype=np.float32)
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            # Return zero vector as fallback
            return np.zeros(128, dtype=np.float32)

    def store_memory(self, memory: PublicMemory, embedding: np.ndarray) -> str:
        """Store memory in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        memory_id = f"pub_{memory.user_id}_{int(memory.timestamp.timestamp())}"

        cursor.execute(
            """
            INSERT INTO public_memories 
            (memory_id, user_id, message_content, emotion_tags, context_tags, 
             interaction_type, timestamp, embedding_vector)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                memory_id,
                memory.user_id,
                memory.message_content,
                json.dumps(memory.emotion_tags),
                json.dumps(memory.context_tags),
                memory.interaction_type,
                memory.timestamp.isoformat(),
                embedding.tobytes(),
            ),
        )

        conn.commit()
        conn.close()

        return memory_id

    async def prepare_ingredients_for_chef(
        self, user_id: str, context_query: str = None
    ) -> MemoryIngredient:
        """
        Prepare ingredients package for the Executive Chef (LM Studio)

        Args:
            user_id: Target user ID
            context_query: Optional context query for filtering

        Returns:
            MemoryIngredient package with all relevant context
        """
        logger.info(f"🥘 Preparing ingredients for user {user_id}")

        # Get user's public memory history
        user_memories = self.get_user_public_memories(user_id)

        # Get relevant memories based on context
        relevant_memories = self.find_relevant_memories(user_id, context_query)

        # Generate emotion profile
        emotion_profile = self.generate_emotion_profile(user_memories)

        # Create interaction history
        interaction_history = [
            mem.message_content for mem in user_memories[-10:]
        ]  # Last 10 interactions

        # Generate context summary
        context_summary = await self.generate_context_summary(
            user_memories, context_query
        )

        # Create ingredient package
        ingredients = MemoryIngredient(
            user_id=user_id,
            context_summary=context_summary,
            relevant_memories=relevant_memories,
            emotion_profile=emotion_profile,
            interaction_history=interaction_history,
            timestamp=datetime.now(),
        )

        logger.info(f"✅ Ingredients prepared for user {user_id}")
        return ingredients

    def get_user_public_memories(self, user_id: str) -> List[PublicMemory]:
        """Get all public memories for a specific user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT memory_id, user_id, message_content, emotion_tags, 
                   context_tags, interaction_type, timestamp
            FROM public_memories 
            WHERE user_id = ?
            ORDER BY timestamp DESC
        """,
            (user_id,),
        )

        memories = []
        for row in cursor.fetchall():
            memory = PublicMemory(
                memory_id=row[0],
                user_id=row[1],
                message_content=row[2],
                emotion_tags=json.loads(row[3]) if row[3] else [],
                context_tags=json.loads(row[4]) if row[4] else [],
                interaction_type=row[5],
                timestamp=datetime.fromisoformat(row[6]),
            )
            memories.append(memory)

        conn.close()
        return memories

    def find_relevant_memories(
        self, user_id: str, context_query: str = None
    ) -> List[PublicMemory]:
        """Find memories relevant to current context"""
        if not context_query:
            # Return recent memories if no specific query
            return self.get_user_public_memories(user_id)[:5]

        # TODO: Implement semantic search using vector index
        # For now, return recent memories
        return self.get_user_public_memories(user_id)[:5]

    def generate_emotion_profile(
        self, memories: List[PublicMemory]
    ) -> Dict[str, float]:
        """Generate emotion profile from user's memory history"""
        emotion_counts = {}
        total_memories = len(memories)

        for memory in memories:
            for emotion in memory.emotion_tags:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

        # Convert to percentages
        emotion_profile = {}
        for emotion, count in emotion_counts.items():
            emotion_profile[emotion] = (
                count / total_memories if total_memories > 0 else 0
            )

        return emotion_profile

    async def generate_context_summary(
        self, memories: List[PublicMemory], context_query: str = None
    ) -> str:
        """Generate context summary using Ollama"""
        if not memories:
            return "No previous interaction history available."

        # Prepare context for summary
        recent_messages = [
            mem.message_content for mem in memories[-5:]
        ]  # Last 5 messages
        context_text = "\n".join(recent_messages)

        prompt = f"""
        Based on the following recent messages from a user, provide a brief context summary:
        
        {context_text}
        
        Context query: {context_query or 'General context'}
        
        Summary:
        """

        try:
            response = self.ollama_client.chat(
                model="qwen2.5:3b", messages=[{"role": "user", "content": prompt}]
            )
            return response["message"]["content"]
        except Exception as e:
            logger.error(f"Error generating context summary: {e}")
            return f"User has {len(memories)} previous interactions. Recent focus: {', '.join(memories[-1].context_tags) if memories else 'None'}"

    def get_kitchen_status(self) -> Dict:
        """Get current kitchen status and inventory"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get total memories
        cursor.execute("SELECT COUNT(*) FROM public_memories")
        total_memories = cursor.fetchone()[0]

        # Get unique users
        cursor.execute("SELECT COUNT(DISTINCT user_id) FROM public_memories")
        unique_users = cursor.fetchone()[0]

        # Get recent activity
        cursor.execute(
            """
            SELECT COUNT(*) FROM public_memories 
            WHERE timestamp > datetime('now', '-1 hour')
        """
        )
        recent_activity = cursor.fetchone()[0]

        conn.close()

        return {
            "total_memories": total_memories,
            "unique_users": unique_users,
            "recent_activity": recent_activity,
            "memory_pool_size": len(self.public_memory_pool),
            "system_status": "operational",
        }


# Kitchen Staff Manager - coordinates all kitchen operations
class KitchenStaffManager:
    """Manages the kitchen staff and coordinates with the Executive Chef"""

    def __init__(self):
        self.kitchen_staff = KitchenStaff()
        self.active_orders = {}
        logger.info("👨‍🍳 Kitchen Staff Manager initialized")

    async def handle_public_chat_monitoring(
        self, chat_messages: List[Dict]
    ) -> List[str]:
        """
        Monitor public chat and process messages

        Args:
            chat_messages: List of chat messages from Discord

        Returns:
            List of user IDs to potentially engage with
        """
        logger.info(f"👀 Monitoring {len(chat_messages)} public chat messages")

        processed_users = []

        for message in chat_messages:
            user_id = message.get("user_id")
            content = message.get("content")

            if user_id and content:
                # Process public message
                memory_id = await self.kitchen_staff.process_public_message(
                    user_id=user_id,
                    message=content,
                    emotion_tags=self.detect_emotions(content),
                )

                processed_users.append(user_id)

        # Return users who might be good candidates for engagement
        return self.select_users_for_engagement(processed_users)

    def detect_emotions(self, text: str) -> List[str]:
        """Simple emotion detection - can be enhanced with NLP"""
        emotions = []
        text_lower = text.lower()

        # Basic emotion detection
        if any(word in text_lower for word in ["happy", "excited", "great", "awesome"]):
            emotions.append("happy")
        if any(word in text_lower for word in ["sad", "depressed", "down"]):
            emotions.append("sad")
        if any(word in text_lower for word in ["angry", "frustrated", "mad"]):
            emotions.append("angry")
        if any(word in text_lower for word in ["confused", "unsure", "question"]):
            emotions.append("confused")

        return emotions

    def select_users_for_engagement(self, user_ids: List[str]) -> List[str]:
        """Select users who should be engaged with based on activity patterns"""
        # Simple selection logic - can be enhanced
        # For now, return users who have been active recently
        return user_ids[:3]  # Limit to 3 users for demo

    async def prepare_chef_order(
        self, user_id: str, order_details: Dict
    ) -> MemoryIngredient:
        """
        Prepare a complete order for the Executive Chef

        Args:
            user_id: Target user
            order_details: Order details from Discord

        Returns:
            Complete ingredient package for the chef
        """
        logger.info(f"📋 Preparing chef order for user {user_id}")

        # Get ingredients from kitchen staff
        ingredients = await self.kitchen_staff.prepare_ingredients_for_chef(
            user_id=user_id, context_query=order_details.get("context")
        )

        # Add order details to ingredients
        ingredients.order_details = order_details

        logger.info(f"✅ Chef order prepared for user {user_id}")
        return ingredients

    def get_kitchen_report(self) -> Dict:
        """Get comprehensive kitchen status report"""
        status = self.kitchen_staff.get_kitchen_status()

        return {
            "kitchen_status": status,
            "active_orders": len(self.active_orders),
            "system_health": "excellent",
            "last_updated": datetime.now().isoformat(),
        }


# Main kitchen staff system instance
kitchen_manager = KitchenStaffManager()

if __name__ == "__main__":
    # Test the kitchen staff system
    async def test_kitchen():
        print("🧑‍🍳 Testing Kitchen Staff System...")

        # Test public message processing
        memory_id = await kitchen_manager.kitchen_staff.process_public_message(
            user_id="test_user_123",
            message="I'm really excited about this new project!",
            emotion_tags=["happy", "excited"],
        )
        print(f"✅ Processed message: {memory_id}")

        # Test ingredient preparation
        ingredients = await kitchen_manager.kitchen_staff.prepare_ingredients_for_chef(
            user_id="test_user_123"
        )
        print(f"✅ Prepared ingredients for user: {ingredients.user_id}")

        # Get kitchen status
        status = kitchen_manager.get_kitchen_report()
        print(f"📊 Kitchen Status: {status}")

        print("🎉 Kitchen Staff System test completed!")

    asyncio.run(test_kitchen())
