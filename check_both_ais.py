#!/usr/bin/env python3
"""
Check Both AIs Are Accessible
Simple test to verify LM Studio and Ollama are running
"""

import requests
import json


def check_both_ais():
    """Check if both LM Studio and Ollama are accessible"""

    print("🔍 CHECKING BOTH AIs")
    print("=" * 30)

    # Check LM Studio (Chef)
    print("🤖 Checking LM Studio (Chef)...")
    try:
        lm_response = requests.get("http://169.254.83.107:1234/v1/models", timeout=10)
        if lm_response.status_code == 200:
            print("✅ LM Studio is running!")
            models = lm_response.json()
            print(f"📦 Available models: {len(models.get('data', []))}")
        else:
            print(f"❌ LM Studio error: {lm_response.status_code}")
    except Exception as e:
        print(f"❌ LM Studio connection failed: {e}")

    # Check Ollama (Waiter)
    print("\n🌊 Checking Ollama (Waiter)...")
    try:
        ollama_response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if ollama_response.status_code == 200:
            print("✅ Ollama is running!")
            models = ollama_response.json()
            print(f"📦 Available models: {len(models.get('models', []))}")

            # Check for qwen2.5:3b
            model_names = [m.get("name", "") for m in models.get("models", [])]
            if "qwen2.5:3b" in model_names:
                print("✅ qwen2.5:3b model found - Waiter ready!")
            else:
                print("⚠️  qwen2.5:3b not found")
        else:
            print(f"❌ Ollama error: {ollama_response.status_code}")
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")

    print("\n🎯 SUMMARY:")
    print("Both AIs should be accessible for quantum superposition!")


if __name__ == "__main__":
    check_both_ais()
