# 🚀 Lyra Blackwall Alpha - Advanced Setup Guide

## **🎯 Overview**

This guide covers the advanced features of Lyra Blackwall Alpha, including:
- **FAISS Vector Search** - High-performance similarity search
- **BGE Embeddings** - State-of-the-art text embeddings
- **LM Studio Integration** - Local AI model inference
- **Quantum Kitchen** - Advanced AI processing pipeline

---

## **📦 Prerequisites**

### **System Requirements**
- Python 3.8+
- 8GB+ RAM (16GB+ recommended for large models)
- 10GB+ free disk space
- NVIDIA GPU (optional, for faster inference)

### **Core Dependencies**
```bash
# Install base requirements
pip install -r requirements.txt

# Install advanced dependencies
pip install faiss-cpu==1.7.4
pip install sentence-transformers==2.2.2
pip install numpy==1.24.3
pip install aiohttp==3.9.1
```

---

## **🧠 FAISS + BGE Memory System**

### **What It Does**
- **FAISS**: Facebook's vector similarity search library
- **BGE**: BAAI's state-of-the-art text embeddings
- **Memory Storage**: Stores conversation context as vectors
- **Semantic Search**: Finds relevant memories using similarity

### **Setup Instructions**

1. **Install Dependencies**
```bash
pip install faiss-cpu sentence-transformers numpy
```

2. **Download BGE Model** (automatic on first use)
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("BAAI/bge-small-en-v1.5")
```

3. **Test Memory System**
```bash
python test_integration.py
```

### **Configuration**
```python
# In your config file
memory_config = {
    "enabled": True,
    "embedding_model": "BAAI/bge-small-en-v1.5",
    "vector_database": "faiss",
    "max_results": 10,
    "similarity_threshold": 0.7,
    "memory_path": "memory",
    "index_path": "memory/faiss_index"
}
```

### **Usage Example**
```python
from memory_interface import MemoryInterface

# Initialize
memory = MemoryInterface(config)
await memory.initialize()

# Store memory
await memory.store_memory(
    "User likes Python programming",
    {"category": "preferences", "timestamp": "2025-01-21"}
)

# Search memory
results = await memory.search_memory("What does the user like to program?")
```

---

## **🤖 LM Studio Integration**

### **What It Does**
- **Local AI Models**: Run AI models locally without cloud costs
- **API Compatibility**: OpenAI-compatible API endpoint
- **Custom Models**: Support for various model formats
- **Real-time Inference**: Fast response generation

### **Setup Instructions**

1. **Download LM Studio**
   - Visit: https://lmstudio.ai/
   - Download for your platform (Windows/Mac/Linux)

2. **Install and Launch**
```bash
# Windows
lmstudio.exe

# Mac/Linux
./lmstudio
```

3. **Download a Model**
   - Open LM Studio
   - Go to "Search" tab
   - Search for models (e.g., "llama-2-7b-chat")
   - Download a model

4. **Start Local Server**
   - Go to "Local Server" tab
   - Click "Start Server"
   - Server runs on `http://localhost:1234`

5. **Test Connection**
```bash
python test_integration.py
```

### **Configuration**
```python
# LM Studio settings
lm_studio_config = {
    "url": "http://localhost:1234/v1/chat/completions",
    "model": "local-model",
    "temperature": 0.7,
    "max_tokens": 1000,
    "timeout": 30
}
```

### **Usage Example**
```python
import aiohttp
import json

async def generate_response(prompt):
    payload = {
        "model": "local-model",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://localhost:1234/v1/chat/completions",
            json=payload
        ) as response:
            result = await response.json()
            return result["choices"][0]["message"]["content"]
```

---

## **🍽️ Quantum Kitchen System**

### **What It Does**
- **Memory Ingredient Preparation**: Analyzes user context and history
- **Executive Chef**: Generates personalized responses
- **Multi-format Output**: Text, image, video, music generation
- **Discord Integration**: Seamless delivery to Discord channels

### **Setup Instructions**

1. **Ensure Memory System is Running**
```bash
# Test memory system first
python -c "from memory_interface import MemoryInterface; print('Memory system ready')"
```

2. **Ensure LM Studio is Running**
```bash
# Test LM Studio connection
curl -X POST http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"local-model","messages":[{"role":"user","content":"Hello"}]}'
```

3. **Test Quantum Kitchen**
```bash
python test_integration.py
```

### **Configuration**
```python
# Quantum Kitchen settings
kitchen_config = {
    "discord_token": "YOUR_DISCORD_TOKEN",
    "target_channel_id": 123456789,
    "memory_enabled": True,
    "lm_studio_enabled": True,
    "max_processing_time": 30
}
```

### **Usage Example**
```python
from kitchen_orchestrator import KitchenOrchestrator, ChefOrder

# Initialize kitchen
kitchen = KitchenOrchestrator(discord_token, channel_id)
await kitchen.start_kitchen()

# Create order
order = ChefOrder(
    user_id="user123",
    message_content="Tell me about AI",
    format_type="text",
    priority="normal"
)

# Submit order
order_id = await kitchen.submit_order(order)
```

---

## **🔧 Advanced Configuration**

### **Memory System Tuning**
```python
# For better performance
memory_config = {
    "embedding_model": "BAAI/bge-large-en-v1.5",  # Larger, more accurate
    "similarity_threshold": 0.8,  # Higher threshold = more relevant
    "max_results": 20,  # More results
    "index_type": "faiss.IndexIVFFlat"  # Faster for large datasets
}
```

### **LM Studio Optimization**
```python
# For faster inference
lm_config = {
    "temperature": 0.5,  # Lower = more focused
    "max_tokens": 500,   # Shorter responses
    "top_p": 0.9,        # Nucleus sampling
    "frequency_penalty": 0.1  # Reduce repetition
}
```

### **Discord Integration**
```python
# For better Discord experience
discord_config = {
    "embed_color": 0x00ff00,
    "max_message_length": 2000,
    "typing_indicator": True,
    "reaction_confirmations": True
}
```

---

## **🧪 Testing and Validation**

### **Run All Tests**
```bash
python test_integration.py
```

### **Individual Component Tests**
```bash
# Test memory system only
python -c "
import asyncio
from test_integration import test_memory_interface
asyncio.run(test_memory_interface())
"

# Test LM Studio only
python -c "
import asyncio
from test_integration import test_lm_studio_integration
asyncio.run(test_lm_studio_integration())
"
```

### **Performance Benchmarks**
```bash
# Memory search performance
python -c "
import asyncio
import time
from memory_interface import MemoryInterface

async def benchmark():
    memory = MemoryInterface({'enabled': True})
    await memory.initialize()
    
    start = time.time()
    results = await memory.search_memory('test query')
    end = time.time()
    
    print(f'Search time: {end - start:.3f}s')
    print(f'Results: {len(results)}')

asyncio.run(benchmark())
"
```

---

## **🚨 Troubleshooting**

### **Common Issues**

1. **FAISS Import Error**
```bash
# Solution: Install correct version
pip uninstall faiss
pip install faiss-cpu==1.7.4
```

2. **BGE Model Download Fails**
```bash
# Solution: Manual download
python -c "
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('BAAI/bge-small-en-v1.5')
model.save('local_bge_model')
"
```

3. **LM Studio Connection Failed**
```bash
# Check if server is running
curl http://localhost:1234/v1/models

# Restart LM Studio server
# Check firewall settings
```

4. **Memory System Slow**
```python
# Use smaller model
"embedding_model": "BAAI/bge-small-en-v1.5"  # Instead of large

# Reduce search scope
"max_results": 5  # Instead of 20
```

### **Performance Optimization**

1. **For Large Memory Sets**
```python
# Use IVF index for better performance
import faiss
index = faiss.IndexIVFFlat(quantizer, dimension, nlist)
```

2. **For Faster Inference**
```python
# Use smaller models
"embedding_model": "BAAI/bge-small-en-v1.5"
"max_tokens": 500
```

3. **For Better Search Quality**
```python
# Use larger models
"embedding_model": "BAAI/bge-large-en-v1.5"
"similarity_threshold": 0.8
```

---

## **📈 Monitoring and Maintenance**

### **Memory System Health**
```python
# Check memory stats
stats = await memory.get_memory_stats()
print(f"Total memories: {stats['total_memories']}")
print(f"Index size: {stats['index_size']}")
```

### **LM Studio Performance**
```python
# Monitor response times
import time
start = time.time()
response = await generate_response("test")
end = time.time()
print(f"Response time: {end - start:.3f}s")
```

### **Discord Bot Status**
```python
# Check bot health
bot_status = bot.get_kitchen_status()
print(f"Bot running: {bot_status['is_running']}")
print(f"Active orders: {bot_status['active_orders']}")
```

---

## **🎯 Next Steps**

1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Configure LM Studio**: Download and start local server
3. **Test Integration**: `python test_integration.py`
4. **Start Bot**: `python start.py`
5. **Monitor Performance**: Use built-in monitoring tools

---

**🎉 Congratulations!** You now have a fully functional advanced AI system with vector search, local inference, and personalized responses! 