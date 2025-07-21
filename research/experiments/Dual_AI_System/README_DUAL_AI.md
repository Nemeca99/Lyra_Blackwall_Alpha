# Dual-AI System - Lyra Blackwall v2.0

**Travis Miner's Dual-AI Architecture**

## Overview

This system implements Travis's philosophy of **dual-AI architecture** where two specialized AI systems work together:

- **Recursive AI (GPU)**: Creative, emotional, pattern-based thinking
- **Linear AI (CPU)**: Logical, structured, systematic processing

## Architecture

### Core Components

1. **`main_dual_ai.py`** - Main coordinator that orchestrates both AIs
2. **`recursive_ai.py`** - GPU-based creative AI (DeepSeek)
3. **`linear_ai.py`** - CPU-based logical AI (Qwen2.5)
4. **`memory_interface.py`** - Memory system (ready for FAISS + BGE)
5. **`dual_ai_config.py`** - Configuration management

### Processing Flow

1. **Input Analysis**: Linear AI analyzes user input for logical structure
2. **Memory Search**: Memory interface finds relevant context (future)
3. **Creative Generation**: Recursive AI generates emotional/creative response
4. **Response Structuring**: Linear AI validates and structures final output

## Setup

### Prerequisites

- **Ollama** installed and running
- **DeepSeek model**: `deepseek-r1-0528-qwen3-8b` (GPU)
- **Qwen2.5 model**: `qwen2.5:0.5b` (CPU)

### Installation

1. **Download models**:
   ```bash
   ollama pull deepseek-r1-0528-qwen3-8b
   ollama pull qwen2.5:0.5b
   ```

2. **Run the system**:
   ```bash
   python main_dual_ai.py
   ```

## Configuration

The system uses `dual_ai_config.json` for configuration. Key settings:

### Recursive AI (GPU)
- **Model**: DeepSeek for creative thinking
- **Temperature**: 0.7 (creative)
- **Personality**: Creative, emotional, pattern-based

### Linear AI (CPU)
- **Model**: Qwen2.5 for logical processing
- **Temperature**: 0.3 (structured)
- **Personality**: Logical, structured, systematic

### Memory Interface
- **Embedding Model**: BGE base (ready for integration)
- **Vector Database**: FAISS (ready for integration)
- **Status**: Ready for memory system integration

## Usage

### Basic Usage

```python
from main_dual_ai import DualAICoordinator

# Initialize system
coordinator = DualAICoordinator()
await coordinator.initialize()

# Process input
response = await coordinator.process_input("Hello! How are you today?")

# Get system status
status = await coordinator.get_system_status()

# Shutdown
await coordinator.shutdown()
```

### Integration Points

The system is designed for easy integration with:

1. **Discord Bot**: Use `process_input()` for message handling
2. **Memory System**: `memory_interface.py` ready for FAISS + BGE
3. **Custom Models**: Update config to use different models

## Memory System Integration

The memory system is **ready for integration** with:

- **BGE Embeddings**: `text-embedding-bge-base-en-v1.5`
- **FAISS Index**: Vector similarity search
- **Memory Storage**: Persistent memory with metadata

**Next Step**: Implement FAISS + BGE integration in `memory_interface.py`

## Philosophy

This system embodies Travis's insight that **true AI requires both recursive and linear thinking**:

- **GPU = Recursive**: Parallel, creative, emotional processing
- **CPU = Linear**: Sequential, logical, structured processing

The dual-AI approach mirrors the human brain's specialized hemispheres working together.

## Status

✅ **Core System**: Complete and functional
✅ **Dual-AI Architecture**: Implemented
✅ **Configuration System**: Ready
🔄 **Memory System**: Ready for integration
🔄 **Discord Integration**: Ready for connection

**Ready for memory system integration!** 