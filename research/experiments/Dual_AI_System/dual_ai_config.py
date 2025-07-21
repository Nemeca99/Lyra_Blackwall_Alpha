#!/usr/bin/env python3
"""
Dual-AI Configuration System
Travis Miner - Lyra Blackwall v2.0

Manages configuration for both recursive and linear AI systems
"""

import json
import os
from typing import Dict, Any


class DualAIConfig:
    """Configuration manager for dual-AI system"""

    def __init__(self, config_path: str = "dual_ai_config.json"):
        self.config_path = config_path
        self.config = self._load_config()

        # Extract component configs
        self.recursive_config = self.config.get("recursive_ai", {})
        self.linear_config = self.config.get("linear_ai", {})
        self.memory_config = self.config.get("memory_interface", {})
        self.system_config = self.config.get("system", {})

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
                return self._create_default_config()
        else:
            return self._create_default_config()

    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration"""
        default_config = {
            "system": {
                "name": "Lyra Blackwall v2.0",
                "version": "2.0.0",
                "session_timeout": 3600,
                "max_conversation_history": 1000,
                "log_level": "INFO",
            },
            "recursive_ai": {
                "name": "DeepSeek Recursive",
                "model": "deepseek-r1-0528-qwen3-8b",
                "type": "gpu",
                "api": "lm_studio",
                "max_tokens": 2048,
                "temperature": 0.7,
                "top_p": 0.9,
                "personality": {
                    "creative": True,
                    "emotional": True,
                    "pattern_based": True,
                    "intuitive": True,
                },
                "capabilities": [
                    "creative_writing",
                    "emotional_analysis",
                    "pattern_recognition",
                    "intuitive_leaps",
                ],
            },
            "linear_ai": {
                "name": "Qwen2.5 Linear",
                "model": "qwen2.5:0.5b",
                "type": "cpu",
                "max_tokens": 1024,
                "temperature": 0.3,
                "top_p": 0.8,
                "personality": {
                    "logical": True,
                    "structured": True,
                    "systematic": True,
                    "analytical": True,
                },
                "capabilities": [
                    "logical_analysis",
                    "structure_validation",
                    "memory_organization",
                    "factual_processing",
                ],
            },
            "memory_interface": {
                "enabled": True,
                "embedding_model": "text-embedding-bge-base-en-v1.5",
                "vector_database": "faiss",
                "max_results": 10,
                "similarity_threshold": 0.7,
                "memory_path": "./memory/",
                "index_path": "./memory/faiss_index/",
            },
        }

        # Save default config
        self._save_config(default_config)
        return default_config

    def _save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")

    def update_config(self, section: str, key: str, value: Any):
        """Update a specific configuration value"""
        if section in self.config:
            self.config[section][key] = value
            self._save_config(self.config)

            # Update component configs
            if section == "recursive_ai":
                self.recursive_config = self.config["recursive_ai"]
            elif section == "linear_ai":
                self.linear_config = self.config["linear_ai"]
            elif section == "memory_interface":
                self.memory_config = self.config["memory_interface"]

    def get_config(self, section: str = None) -> Dict[str, Any]:
        """Get configuration for a section or entire config"""
        if section:
            return self.config.get(section, {})
        return self.config

    def validate_config(self) -> bool:
        """Validate configuration integrity"""
        required_sections = ["system", "recursive_ai", "linear_ai", "memory_interface"]

        for section in required_sections:
            if section not in self.config:
                print(f"Missing required config section: {section}")
                return False

        return True
