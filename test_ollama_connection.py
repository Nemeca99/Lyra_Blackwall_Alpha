#!/usr/bin/env python3
"""
Test Ollama Connection for Waiter Integration
"""

import requests
import json

def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    
    print("🔍 TESTING OLLAMA CONNECTION")
    print("=" * 40)
    
    try:
        # Test basic connection
        print("📡 Testing Ollama API connection...")
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        
        if response.status_code == 200:
            print("✅ Ollama is running!")
            
            # Get available models
            models = response.json()
            print(f"📦 Available models: {len(models.get('models', []))}")
            
            for model in models.get('models', []):
                print(f"  - {model.get('name', 'Unknown')}")
            
            # Test if qwen2.5:7b is available (used in quantum kitchen)
            model_names = [model.get('name', '') for model in models.get('models', [])]
            if 'qwen2.5:7b' in model_names:
                print("✅ qwen2.5:7b model found - Waiter ready!")
            else:
                print("⚠️  qwen2.5:7b not found - Waiter may need different model")
                
        else:
            print(f"❌ Ollama API error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Ollama not running or not accessible")
        print("💡 Start Ollama with: ollama serve")
        
    except Exception as e:
        print(f"❌ Error testing Ollama: {e}")

if __name__ == "__main__":
    test_ollama_connection() 