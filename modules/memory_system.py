"""
Memory System for Quantum Superposition AI
Manages hardcoded knowledge and user-specific memories
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class MemoryEntry:
    """Individual memory entry"""

    user_id: str
    content: str
    memory_type: str
    timestamp: datetime
    emotional_weight: Dict[str, float] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class MemorySystem:
    """
    Memory system that manages hardcoded knowledge and user memories
    """

    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = memory_dir
        self.default_template = {}
        self.user_memories = {}
        self.system_memories = {}

        # Load all memory files
        self._load_memory_files()

        print("Memory System initialized")

    def _load_memory_files(self):
        """Load all memory files from the memory directory"""
        if not os.path.exists(self.memory_dir):
            print(f"⚠️ Memory directory {self.memory_dir} not found, creating...")
            os.makedirs(self.memory_dir, exist_ok=True)
            return

        # Load default template
        dev_dir = os.path.join(self.memory_dir, "Dev")
        if os.path.exists(dev_dir):
            template_file = os.path.join(dev_dir, "default_profile_template.json")
            if os.path.exists(template_file):
                try:
                    with open(template_file, "r", encoding="utf-8") as f:
                        self.default_template = json.load(f)
                        print("📚 Loaded default profile template")
                except Exception as e:
                    print(f"❌ Error loading template: {e}")
                    self.default_template = {}

        # Load user profiles and memories
        for item in os.listdir(self.memory_dir):
            item_path = os.path.join(self.memory_dir, item)

            # Skip non-directories and special directories
            if not os.path.isdir(item_path) or item in ["Dev", "System"]:
                continue

            # This is a user directory (Discord ID)
            user_id = item
            self.user_memories[user_id] = {}

            # Load user profile
            profile_file = os.path.join(item_path, "profile.json")
            if os.path.exists(profile_file):
                try:
                    with open(profile_file, "r", encoding="utf-8") as f:
                        profile_data = json.load(f)
                        self.user_memories[user_id]["profile"] = profile_data
                        print(f"👤 Loaded profile for user {user_id}")
                except Exception as e:
                    print(f"❌ Error loading profile for {user_id}: {e}")

            # Load user memories
            memories_dir = os.path.join(item_path, "memories")
            if os.path.exists(memories_dir):
                for filename in os.listdir(memories_dir):
                    if filename.endswith(".json"):
                        filepath = os.path.join(memories_dir, filename)
                        try:
                            with open(filepath, "r", encoding="utf-8") as f:
                                data = json.load(f)
                                memory_id = filename.replace(".json", "")
                                self.user_memories[user_id][memory_id] = data
                        except Exception as e:
                            print(f"❌ Error loading memory {filepath}: {e}")

        # Load System memories
        system_dir = os.path.join(self.memory_dir, "System")
        if os.path.exists(system_dir):
            for filename in os.listdir(system_dir):
                if filename.endswith(".json"):
                    filepath = os.path.join(system_dir, filename)
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            memory_type = filename.replace(".json", "")
                            self.system_memories[memory_type] = data
                    except Exception as e:
                        print(f"❌ Error loading {filepath}: {e}")

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile from memory"""
        # Check user memories
        if user_id in self.user_memories:
            return self.user_memories[user_id].get("profile")

        return None

    def get_user_knowledge(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's project knowledge"""
        # Check user memories
        if user_id in self.user_memories:
            return self.user_memories[user_id].get("knowledge")

        return None

    def create_user_profile(
        self, user_id: str, basic_info: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create new user profile from template"""
        profile = self.default_template.copy()
        profile["user_id"] = user_id
        profile["basic_information"]["discord_id"] = user_id
        profile["system_metadata"]["created_date"] = datetime.now().isoformat()
        profile["system_metadata"]["last_updated"] = datetime.now().isoformat()

        if basic_info:
            profile["basic_information"].update(basic_info)

        return profile

    def save_user_profile(self, user_id: str, profile: Dict[str, Any]):
        """Save user profile to file"""
        user_dir = os.path.join(self.memory_dir, user_id)
        os.makedirs(user_dir, exist_ok=True)

        profile_file = os.path.join(user_dir, "profile.json")
        with open(profile_file, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2, ensure_ascii=False)

        # Update in-memory storage
        if user_id not in self.user_memories:
            self.user_memories[user_id] = {}
        self.user_memories[user_id]["profile"] = profile

        print(f"💾 Saved profile for user {user_id}")

    def get_context_for_user(self, user_id: str) -> str:
        """Generate context string for user based on memory"""
        profile = self.get_user_profile(user_id)

        context = ""

        if profile:
            context += f"User Profile: {profile.get('name', 'Unknown')}\n"
            if "basic_information" in profile:
                basic = profile["basic_information"]
                context += f"Age: {basic.get('age', 'Unknown')}\n"
                context += f"Role: {profile.get('role', 'User')}\n"

            if "cognitive_profile" in profile:
                cognitive = profile["cognitive_profile"]
                context += (
                    f"Cognitive Style: {cognitive.get('cognitive_style', 'Standard')}\n"
                )
                context += f"Key Traits: {', '.join(cognitive.get('key_traits', []))}\n"

        return context

    def get_personality_context(self, user_id: str) -> str:
        """Get personality-specific context for user"""
        profile = self.get_user_profile(user_id)

        if not profile:
            return ""

        context = ""

        # Add cognitive profile information
        if "cognitive_profile" in profile:
            cognitive = profile["cognitive_profile"]
            context += (
                f"Cognitive Profile: {cognitive.get('cognitive_style', 'Standard')}\n"
            )
            context += f"Mental Architecture: {cognitive.get('mental_architecture', {}).get('inner_world', 'Standard')}\n"

        # Add communication preferences
        if "communication_guidelines" in profile:
            guidelines = profile["communication_guidelines"]
            context += f"Preferred Tone: {guidelines.get('tone', 'Professional')}\n"
            context += f"Avoid: {guidelines.get('avoid', 'Condescension')}\n"
            context += f"Emphasize: {guidelines.get('emphasize', 'Respect')}\n"

        # Add relationship to AI
        if "relationship_to_ai" in profile:
            ai_rel = profile["relationship_to_ai"]
            context += f"AI Role: {ai_rel.get('role', 'User')}\n"
            context += (
                f"Expectation: {ai_rel.get('expectation', 'Standard assistance')}\n"
            )
            context += f"Communication Style: {ai_rel.get('communication_style', 'Standard')}\n"

        return context

    def get_project_context(self, user_id: str) -> str:
        """Get project-specific context for user"""
        profile = self.get_user_profile(user_id)

        if not profile:
            return ""

        context = ""

        # Add current projects
        if "current_projects" in profile:
            projects = profile["current_projects"]
            context += f"Current Focus: {projects.get('main_focus', 'General')}\n"
            context += f"AI Systems: {', '.join(projects.get('ai_systems', []))}\n"
            context += (
                f"Project Goals: {', '.join(projects.get('project_goals', []))}\n"
            )

        # Add technical preferences
        if "technical_preferences" in profile:
            tech = profile["technical_preferences"]
            context += f"Coding Style: {tech.get('coding_style', 'Standard')}\n"
            context += f"Architecture: {tech.get('architecture', 'Standard')}\n"

        return context

    def get_emotional_context(self, user_id: str) -> str:
        """Get emotional context for user"""
        profile = self.get_user_profile(user_id)

        if not profile:
            return ""

        context = ""

        # Add emotional context
        if "emotional_context" in profile:
            emotional = profile["emotional_context"]
            context += f"Current State: {emotional.get('current_state', 'Standard')}\n"
            context += f"Motivation: {emotional.get('motivation', 'General')}\n"
            context += f"Fears: {emotional.get('fears', 'None specified')}\n"
            context += f"Hopes: {emotional.get('hopes', 'General improvement')}\n"

        # Add current challenges
        if "current_challenges" in profile:
            challenges = profile["current_challenges"]
            context += f"Challenges: {', '.join(challenges.values())}\n"

        return context

    def get_full_context(self, user_id: str) -> str:
        """Get complete context for user"""
        context_parts = [
            self.get_context_for_user(user_id),
            self.get_personality_context(user_id),
            self.get_project_context(user_id),
            self.get_emotional_context(user_id),
        ]

        return "\n".join([part for part in context_parts if part.strip()])

    def add_user_memory(
        self,
        user_id: str,
        content: str,
        memory_type: str = "general",
        emotional_weight: Dict[str, float] = None,
        metadata: Dict[str, Any] = None,
    ):
        """Add new memory for user with context line"""
        if user_id not in self.user_memories:
            self.user_memories[user_id] = {}

        # Create profile if doesn't exist
        if "profile" not in self.user_memories[user_id]:
            profile = self.create_user_profile(user_id)
            self.save_user_profile(user_id, profile)

        memory_entry = MemoryEntry(
            user_id=user_id,
            content=content,
            memory_type=memory_type,
            timestamp=datetime.now(),
            emotional_weight=emotional_weight or {},
            metadata=metadata or {},
        )

        # Generate unique memory ID (Chef generates this)
        memory_id = (
            f"mem_{int(memory_entry.timestamp.timestamp())}_{hash(content) % 100000000}"
        )

        # Create context line for fast searching
        context_line = f"{memory_id}|{memory_type}|{memory_entry.timestamp.isoformat()}|{content[:100]}..."

        # Save to file
        user_dir = os.path.join(self.memory_dir, user_id)
        memories_dir = os.path.join(user_dir, "memories")
        os.makedirs(memories_dir, exist_ok=True)

        filepath = os.path.join(memories_dir, f"{memory_id}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "user_id": memory_entry.user_id,
                    "content": memory_entry.content,
                    "memory_type": memory_entry.memory_type,
                    "timestamp": memory_entry.timestamp.isoformat(),
                    "emotional_weight": memory_entry.emotional_weight,
                    "metadata": memory_entry.metadata,
                },
                f,
                indent=2,
                ensure_ascii=False,
            )

        # Add to in-memory storage
        self.user_memories[user_id][memory_id] = {
            "user_id": memory_entry.user_id,
            "content": memory_entry.content,
            "memory_type": memory_entry.memory_type,
            "timestamp": memory_entry.timestamp.isoformat(),
            "emotional_weight": memory_entry.emotional_weight,
            "metadata": memory_entry.metadata,
        }

        # Update profile with context line
        profile = self.user_memories[user_id]["profile"]
        if "memory_context_index" not in profile:
            profile["memory_context_index"] = {}

        if "context_lines" not in profile["memory_context_index"]:
            profile["memory_context_index"]["context_lines"] = []

        profile["memory_context_index"]["context_lines"].append(context_line)
        profile["memory_context_index"]["total_memories"] = len(
            profile["memory_context_index"]["context_lines"]
        )
        profile["system_metadata"]["last_updated"] = datetime.now().isoformat()
        profile["system_metadata"]["interaction_count"] += 1

        # Save updated profile
        self.save_user_profile(user_id, profile)

        print(f"💾 Added memory for user {user_id}: {memory_type}")
        return memory_id

    def search_user_memories(
        self, user_id: str, query: str, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Search user memories using context lines for fast searching"""
        profile = self.get_user_profile(user_id)
        if not profile or "memory_context_index" not in profile:
            return []

        context_lines = profile["memory_context_index"].get("context_lines", [])
        results = []
        query_lower = query.lower()

        for context_line in context_lines:
            if query_lower in context_line.lower():
                parts = context_line.split("|")
                if len(parts) >= 4:
                    results.append(
                        {
                            "memory_id": parts[0],
                            "memory_type": parts[1],
                            "timestamp": parts[2],
                            "content_preview": parts[3],
                            "relevance_score": context_line.lower().count(query_lower),
                        }
                    )

        # Sort by relevance and limit results
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:limit]

    def get_memory_summary(self, user_id: str) -> Dict[str, Any]:
        """Get summary of user's memory"""
        profile = self.get_user_profile(user_id)
        memories = self.user_memories.get(user_id, {})

        if profile and "memory_context_index" in profile:
            context_index = profile["memory_context_index"]
            return {
                "user_id": user_id,
                "has_profile": True,
                "memory_count": context_index.get("total_memories", 0),
                "memory_types": list(
                    set(
                        line.split("|")[1]
                        for line in context_index.get("context_lines", [])
                    )
                ),
                "last_interaction": context_index.get("last_interaction"),
                "interaction_frequency": context_index.get("interaction_frequency"),
                "profile_completeness": profile["system_metadata"].get(
                    "profile_completeness", 0.0
                ),
                "trust_level": profile["system_metadata"].get("trust_level", 0.0),
                "last_updated": profile["system_metadata"].get("last_updated"),
            }
        else:
            return {
                "user_id": user_id,
                "has_profile": profile is not None,
                "memory_count": len(memories),
                "memory_types": [],
                "last_interaction": None,
                "interaction_frequency": "Unknown",
                "profile_completeness": 0.0,
                "trust_level": 0.0,
                "last_updated": None,
            }


# Global memory system instance
memory_system = MemorySystem()

if __name__ == "__main__":
    # Test the memory system
    system = MemorySystem()

    # Test with Travis's ID
    travis_id = "1380754964317601813"

    print(f"\n🧠 Testing Memory System for Travis:")
    print(f"Profile: {system.get_user_profile(travis_id) is not None}")
    print(f"Context: {system.get_full_context(travis_id)[:200]}...")

    # Test memory addition
    memory_id = system.add_user_memory(
        travis_id,
        "Testing the quantum superposition AI system with integrated memory and personality engine",
        "test",
        {"Recursion": 90, "Logic": 30, "Autonomy": 20},
    )
    print(f"Added memory: {memory_id}")

    # Test memory search
    results = system.search_user_memories(travis_id, "quantum")
    print(f"Search results: {len(results)} memories found")

    # Get summary
    summary = system.get_memory_summary(travis_id)
    print(f"Memory summary: {summary}")
