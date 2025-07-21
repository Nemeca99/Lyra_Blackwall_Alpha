#!/usr/bin/env python3
"""
Recursive AI Component - LM Studio Integration
Travis Miner - Lyra Blackwall v2.0

Handles creative, emotional, pattern-based thinking using LM Studio (DeepSeek)
Communicates with Linear AI (Qwen2.5) to get context before responding
"""

import asyncio
import json
import logging
import aiohttp
from typing import Dict, List, Any


class RecursiveAI:
    """Recursive AI for creative and emotional processing via LM Studio"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = config.get("model", "deepseek-r1-0528-qwen3-8b")
        self.max_tokens = config.get("max_tokens", 2048)
        self.temperature = config.get("temperature", 0.7)
        self.top_p = config.get("top_p", 0.9)
        self.personality = config.get("personality", {})
        self.capabilities = config.get("capabilities", [])

        # LM Studio API settings
        self.lm_studio_url = "http://localhost:1234/v1/chat/completions"
        self.is_initialized = False
        self.logger = logging.getLogger("RecursiveAI")

        # Reference to linear AI for communication
        self.linear_ai = None

    def set_linear_ai(self, linear_ai):
        """Set reference to linear AI for communication"""
        self.linear_ai = linear_ai

    async def initialize(self):
        """Initialize the recursive AI system"""
        try:
            self.logger.info(f"Initializing Recursive AI: {self.model_name}")

            # Test LM Studio connection
            await self._test_lm_studio()

            self.is_initialized = True
            self.logger.info("Recursive AI initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize Recursive AI: {e}")
            raise

    async def _test_lm_studio(self):
        """Test LM Studio API connection"""
        try:
            test_prompt = "Hello, this is a test."
            response = await self._call_lm_studio(test_prompt, max_tokens=10)

            if response and len(response.strip()) > 0:
                self.logger.info("LM Studio connection successful")
            else:
                raise Exception("LM Studio returned empty response")

        except Exception as e:
            self.logger.error(f"LM Studio test failed: {e}")
            raise

    async def generate_response(
        self,
        user_input: str,
        logical_analysis: Dict = None,
        memory_context: List[Dict] = None,
    ) -> str:
        """
        Generate creative response using recursive thinking

        Flow:
        1. Ask Linear AI (Qwen2.5) for context about the user and situation
        2. Combine original prompt with Linear AI's context
        3. Generate final creative response

        Args:
            user_input: Original user input
            logical_analysis: Optional analysis from linear AI
            memory_context: Relevant memory context

        Returns:
            Creative response string
        """
        try:
            if not self.is_initialized:
                raise Exception("Recursive AI not initialized")

            # Step 1: Ask Linear AI for context
            context_prompt = self._build_context_request(user_input)
            linear_context = await self._get_linear_ai_context(context_prompt)

            # Step 2: Build final prompt combining original + context
            final_prompt = self._build_final_prompt(
                user_input, linear_context, logical_analysis, memory_context
            )

            # Step 3: Generate response via LM Studio
            response = await self._call_lm_studio(
                final_prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
            )

            self.logger.debug(f"Generated creative response: {len(response)} chars")
            return response

        except Exception as e:
            self.logger.error(f"Error generating creative response: {e}")
            return f"I'm having trouble thinking creatively right now: {str(e)}"

    def _build_context_request(self, user_input: str) -> str:
        """Build request to ask Linear AI for context"""
        return f"""Hey, this user said: "{user_input}"

What do you know about them and the context? Please provide:
1. User's likely intent and background
2. Relevant context or previous interactions
3. Any important patterns or preferences
4. Suggested approach for responding

Give me a comprehensive analysis to help me form the best response."""

    async def _get_linear_ai_context(self, context_prompt: str) -> str:
        """Get context from Linear AI"""
        try:
            if self.linear_ai:
                # Use Linear AI's analysis method to get context
                analysis = await self.linear_ai.analyze_input(context_prompt)
                return analysis.get("summary", "No context available")
            else:
                return "Linear AI not available for context"
        except Exception as e:
            self.logger.error(f"Error getting Linear AI context: {e}")
            return f"Error getting context: {str(e)}"

    def _build_final_prompt(
        self,
        user_input: str,
        linear_context: str,
        logical_analysis: Dict = None,
        memory_context: List[Dict] = None,
    ) -> str:
        """Build final prompt combining original input with Linear AI context"""

        # Base personality prompt
        personality_traits = []
        if self.personality.get("creative"):
            personality_traits.append("creative and imaginative")
        if self.personality.get("emotional"):
            personality_traits.append("emotionally aware and empathetic")
        if self.personality.get("pattern_based"):
            personality_traits.append("pattern-recognizing and intuitive")
        if self.personality.get("intuitive"):
            personality_traits.append("intuitive and insightful")

        personality_str = ", ".join(personality_traits)

        # Memory context
        memory_str = ""
        if memory_context:
            memory_str = "\n\nRelevant memories:\n"
            for i, memory in enumerate(memory_context[:3]):
                memory_str += f"- {memory.get('content', '')[:100]}...\n"

        # Linear AI context (this is the key addition)
        context_str = f"\n\nLinear AI Context:\n{linear_context}"

        # Logical analysis
        logic_str = ""
        if logical_analysis:
            logic_str = f"\n\nLogical analysis: {logical_analysis.get('summary', '')}"

        prompt = f"""You are a {personality_str} AI assistant. Your role is to provide creative, emotional, and intuitive responses.

{memory_str}{context_str}{logic_str}

Original user input: {user_input}

Please respond in a creative, empathetic, and insightful way. Use the context from the Linear AI to personalize your response. Focus on emotional understanding, pattern recognition, and intuitive insights. Be warm, engaging, and thoughtful in your response."""

        return prompt

    async def _call_lm_studio(
        self,
        prompt: str,
        max_tokens: int = None,
        temperature: float = None,
        top_p: float = None,
    ) -> str:
        """Call LM Studio API for model inference"""
        try:
            # Prepare request payload
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens or self.max_tokens,
                "temperature": temperature or self.temperature,
                "top_p": top_p or self.top_p,
                "stream": False,
            }

            # Make API request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.lm_studio_url,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                ) as response:

                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(
                            f"LM Studio API error: {response.status} - {error_text}"
                        )

                    result = await response.json()

                    # Extract response content
                    if "choices" in result and len(result["choices"]) > 0:
                        return result["choices"][0]["message"]["content"]
                    else:
                        raise Exception("No response content in LM Studio result")

        except Exception as e:
            self.logger.error(f"Error calling LM Studio: {e}")
            raise

    async def get_status(self) -> Dict[str, Any]:
        """Get current status of recursive AI"""
        return {
            "initialized": self.is_initialized,
            "model": self.model_name,
            "type": "gpu",
            "api": "lm_studio",
            "url": self.lm_studio_url,
            "personality": self.personality,
            "capabilities": self.capabilities,
            "config": {
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
            },
        }

    async def shutdown(self):
        """Shutdown recursive AI"""
        self.logger.info("Shutting down Recursive AI")
        self.is_initialized = False
