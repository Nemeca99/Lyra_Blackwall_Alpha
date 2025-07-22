#!/usr/bin/env python3
"""
Linear AI Component
Travis Miner - Lyra Blackwall v2.0

Handles logical, structured, systematic thinking using CPU-based models
"""

import asyncio
import json
import logging
from typing import Dict, List, Any


class LinearAI:
    """Linear AI for logical and structured processing"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = config.get("model", "qwen2.5:0.5b")
        self.max_tokens = config.get("max_tokens", 1024)
        self.temperature = config.get("temperature", 0.3)
        self.top_p = config.get("top_p", 0.8)
        self.personality = config.get("personality", {})
        self.capabilities = config.get("capabilities", [])

        self.is_initialized = False
        self.logger = logging.getLogger("LinearAI")

    async def initialize(self):
        """Initialize the linear AI system"""
        try:
            self.logger.info(f"Initializing Linear AI: {self.model_name}")

            # Test model availability
            await self._test_model()

            self.is_initialized = True
            self.logger.info("Linear AI initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize Linear AI: {e}")
            raise

    async def _test_model(self):
        """Test if the model is available and working"""
        try:
            test_prompt = "What is 2+2? Answer with just the number."
            response = await self._call_ollama(test_prompt, max_tokens=10)

            if response and len(response.strip()) > 0:
                self.logger.info("Model test successful")
            else:
                raise Exception("Model returned empty response")

        except Exception as e:
            self.logger.error(f"Model test failed: {e}")
            raise

    async def analyze_input(self, user_input: str) -> Dict[str, Any]:
        """
        Analyze user input for logical structure

        Args:
            user_input: User's input text

        Returns:
            Dictionary with logical analysis
        """
        try:
            if not self.is_initialized:
                raise Exception("Linear AI not initialized")

            # Build analysis prompt
            prompt = self._build_analysis_prompt(user_input)

            # Get analysis
            response = await self._call_ollama(
                prompt,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
            )

            # Parse analysis
            analysis = self._parse_analysis(response)

            self.logger.debug(f"Input analysis completed")
            return analysis

        except Exception as e:
            self.logger.error(f"Error analyzing input: {e}")
            return {
                "summary": "Analysis failed",
                "intent": "unknown",
                "structure": "unstructured",
                "confidence": 0.0,
            }

    def _build_analysis_prompt(self, user_input: str) -> str:
        """Build prompt for logical analysis"""

        # Base personality prompt
        personality_traits = []
        if self.personality.get("logical"):
            personality_traits.append("logical and analytical")
        if self.personality.get("structured"):
            personality_traits.append("structured and organized")
        if self.personality.get("systematic"):
            personality_traits.append("systematic and methodical")
        if self.personality.get("analytical"):
            personality_traits.append("analytical and precise")

        personality_str = ", ".join(personality_traits)

        prompt = f"""You are a {personality_str} AI assistant. You work with a Recursive AI (DeepSeek) that handles creative responses. Analyze the following input and provide a structured analysis.

User input: {user_input}

Please analyze this input and respond with a JSON object containing:
- "summary": Brief summary of the input
- "intent": User's intent (question, statement, request, etc.)
- "structure": Logical structure (structured, unstructured, etc.)
- "confidence": Confidence level (0.0 to 1.0)
- "key_points": List of key points or topics
- "suggested_approach": How to best respond to this input
- "creative_direction": Suggestions for the Recursive AI's creative response

Respond with only the JSON object."""

        return prompt

    def _parse_analysis(self, response: str) -> Dict[str, Any]:
        """Parse analysis response from model"""
        try:
            # Try to extract JSON from response
            response_clean = response.strip()
            if response_clean.startswith("{") and response_clean.endswith("}"):
                analysis = json.loads(response_clean)
            else:
                # Fallback parsing
                analysis = {
                    "summary": response_clean[:100],
                    "intent": "unknown",
                    "structure": "unstructured",
                    "confidence": 0.5,
                    "key_points": [],
                    "suggested_approach": "direct_response",
                }

            return analysis

        except Exception as e:
            self.logger.error(f"Error parsing analysis: {e}")
            return {
                "summary": response[:100],
                "intent": "unknown",
                "structure": "unstructured",
                "confidence": 0.0,
                "key_points": [],
                "suggested_approach": "direct_response",
            }

    async def structure_response(
        self, creative_response: str, logical_analysis: Dict
    ) -> str:
        """
        Structure and validate creative response

        Args:
            creative_response: Response from recursive AI
            logical_analysis: Original input analysis

        Returns:
            Structured and validated response
        """
        try:
            if not self.is_initialized:
                return creative_response

            # Build structuring prompt
            prompt = self._build_structuring_prompt(creative_response, logical_analysis)

            # Get structured response
            structured_response = await self._call_ollama(
                prompt,
                max_tokens=self.max_tokens,
                temperature=0.1,  # Low temperature for consistency
                top_p=0.9,
            )

            self.logger.debug(f"Response structured successfully")
            return structured_response.strip()

        except Exception as e:
            self.logger.error(f"Error structuring response: {e}")
            return creative_response

    def _build_structuring_prompt(
        self, creative_response: str, logical_analysis: Dict
    ) -> str:
        """Build prompt for response structuring"""

        prompt = f"""You are a logical AI assistant. Review and structure the following creative response to ensure it is clear, coherent, and appropriate.

Original analysis: {logical_analysis.get('summary', '')}
User intent: {logical_analysis.get('intent', '')}

Creative response: {creative_response}

Please review this response and provide a final, well-structured version that:
1. Maintains the creative and empathetic tone
2. Ensures logical coherence and clarity
3. Addresses the user's intent appropriately
4. Is well-formatted and easy to read

Provide only the final response, no additional commentary."""

        return prompt

    async def _call_ollama(
        self,
        prompt: str,
        max_tokens: int = None,
        temperature: float = None,
        top_p: float = None,
    ) -> str:
        """Call Ollama API for model inference"""
        try:
            # Build command
            cmd = ["ollama", "run", self.model_name]

            # Add parameters if provided (Ollama doesn't support all flags)
            # For now, just use basic command without parameters

            # Run command
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate(input=prompt.encode())

            if process.returncode != 0:
                raise Exception(f"Ollama error: {stderr.decode()}")

            return stdout.decode().strip()

        except Exception as e:
            self.logger.error(f"Error calling Ollama: {e}")
            raise

    async def get_status(self) -> Dict[str, Any]:
        """Get current status of linear AI"""
        return {
            "initialized": self.is_initialized,
            "model": self.model_name,
            "type": "cpu",
            "personality": self.personality,
            "capabilities": self.capabilities,
            "config": {
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "top_p": self.top_p,
            },
        }

    async def shutdown(self):
        """Shutdown linear AI"""
        self.logger.info("Shutting down Linear AI")
        self.is_initialized = False
