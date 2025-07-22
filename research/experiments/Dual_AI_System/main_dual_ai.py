#!/usr/bin/env python3
"""
Dual-AI System Coordinator
Travis Miner - Lyra Blackwall v2.0

Manages the dual-AI architecture:
- Recursive AI (GPU/DeepSeek): Creative, emotional, pattern-based thinking
- Linear AI (CPU/Qwen2.5): Logical, structured, memory processing
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dual_ai_config import DualAIConfig
from recursive_ai import RecursiveAI
from linear_ai import LinearAI
from memory_interface import MemoryInterface


class DualAICoordinator:
    """Main coordinator for the dual-AI system"""

    def __init__(self, config_path: str = "dual_ai_config.json"):
        self.config = DualAIConfig(config_path)
        self.recursive_ai = RecursiveAI(self.config.recursive_config)
        self.linear_ai = LinearAI(self.config.linear_config)
        self.memory_interface = MemoryInterface(self.config.memory_config)

        # System state
        self.is_running = False
        self.session_id = None
        self.conversation_history = []

        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("dual_ai_system.log"),
                logging.StreamHandler(),
            ],
        )
        self.logger = logging.getLogger("DualAICoordinator")

    async def initialize(self):
        """Initialize both AI systems and memory interface"""
        try:
            self.logger.info("Initializing Dual-AI System...")

            # Initialize recursive AI (GPU-based)
            await self.recursive_ai.initialize()
            self.logger.info("Recursive AI (GPU) initialized")

            # Initialize linear AI (CPU-based)
            await self.linear_ai.initialize()
            self.logger.info("Linear AI (CPU) initialized")

            # Set up communication between AIs
            self.recursive_ai.set_linear_ai(self.linear_ai)
            self.logger.info("AI communication link established")

            # Initialize memory interface (ready for future integration)
            await self.memory_interface.initialize()
            self.logger.info("Memory interface initialized")

            self.is_running = True
            self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.logger.info(f"Dual-AI System ready - Session: {self.session_id}")

        except Exception as e:
            self.logger.error(f"Failed to initialize Dual-AI System: {e}")
            raise

    async def process_input(self, user_input: str, context: Dict = None) -> str:
        """
        Process user input through the dual-AI system

        Flow:
        1. Linear AI (Qwen2.5/Ollama) analyzes input for logical structure
        2. Memory interface searches for relevant context
        3. Recursive AI (DeepSeek/LM Studio) generates creative response
        4. Linear AI validates and structures final output

        The two AIs literally communicate with each other!
        """
        try:
            self.logger.info(f"Processing input: {user_input[:50]}...")

            # Step 1: Linear AI analysis
            logical_analysis = await self.linear_ai.analyze_input(user_input)
            self.logger.debug(f"Logical analysis: {logical_analysis}")

            # Step 2: Memory search (future integration)
            memory_context = await self.memory_interface.search_memory(user_input)
            self.logger.debug(f"Memory context found: {len(memory_context)} items")

            # Step 3: Recursive AI creative generation
            creative_response = await self.recursive_ai.generate_response(
                user_input, logical_analysis, memory_context
            )
            self.logger.debug(f"Creative response generated")

            # Step 4: Linear AI validation and structuring
            final_response = await self.linear_ai.structure_response(
                creative_response, logical_analysis
            )
            self.logger.debug(f"Response structured and validated")

            # Store in conversation history
            self.conversation_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "input": user_input,
                    "logical_analysis": logical_analysis,
                    "memory_context": memory_context,
                    "creative_response": creative_response,
                    "final_response": final_response,
                }
            )

            return final_response

        except Exception as e:
            self.logger.error(f"Error processing input: {e}")
            return f"I apologize, but I encountered an error: {str(e)}"

    async def get_system_status(self) -> Dict:
        """Get current status of all system components"""
        return {
            "session_id": self.session_id,
            "is_running": self.is_running,
            "recursive_ai_status": await self.recursive_ai.get_status(),
            "linear_ai_status": await self.linear_ai.get_status(),
            "memory_interface_status": await self.memory_interface.get_status(),
            "conversation_count": len(self.conversation_history),
            "timestamp": datetime.now().isoformat(),
        }

    async def shutdown(self):
        """Gracefully shutdown the dual-AI system"""
        try:
            self.logger.info("Shutting down Dual-AI System...")

            await self.recursive_ai.shutdown()
            await self.linear_ai.shutdown()
            await self.memory_interface.shutdown()

            self.is_running = False
            self.logger.info("Dual-AI System shutdown complete")

        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")


async def main():
    """Main entry point for testing"""
    coordinator = DualAICoordinator()

    try:
        await coordinator.initialize()

        # Test the system
        test_input = "Hello! How are you today?"
        response = await coordinator.process_input(test_input)
        print(f"Input: {test_input}")
        print(f"Response: {response}")

        # Get system status
        status = await coordinator.get_system_status()
        print(f"System Status: {json.dumps(status, indent=2)}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        await coordinator.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
