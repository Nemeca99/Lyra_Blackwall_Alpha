# Lyra Core Theory

This directory contains the core theoretical components of the Lyra Blackwall biomimetic AI system, organized into logical subdirectories.

## Directory Structure

### Consciousness_Architecture/
Contains the core consciousness and cognitive architecture components:

- **brainstem.py** - Central orchestrator for the Lyra Blackwall system
- **Left_Hemisphere.py** - Short-term memory system
- **Right_Hemisphere.py** - Long-term memory system
- **soul.py** - Identity verification and core principles
- **body.py** - System coordination and module registration
- **heart.py** - Rhythm management and system timing
- **queue_manager.py** - Task management and processing queues
- **fragment_manager.py** - Personality fragment management
- **simple_router.py** - Message routing and communication (lightweight, no external dependencies)

### Dream_Systems/
Contains the dream cycle and memory consolidation systems:

- **dream_manager.py** - Dream cycle management, memory consolidation, and insight generation

## Usage

### Importing from Consciousness_Architecture
```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Consciousness_Architecture'))

import brainstem
import Left_Hemisphere
import Right_Hemisphere
import simple_router
# ... other imports
```

### Importing from Dream_Systems
```python
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Dream_Systems'))

import dream_manager
```

### Running the Brainstem
```python
# Initialize the brainstem
brainstem = brainstem.Brainstem()

# Process input
response = brainstem.process_input("Hello, how are you?")

# Handle system pulses
brainstem.pulse(interval=1.0)
```

## Key Features

### Consciousness Architecture
- **Dual-hemisphere memory system** with short-term and long-term components
- **Fragment-based personality system** with dynamic blending
- **Heart-driven timing system** for system rhythms
- **Queue-based task management** for processing efficiency
- **Identity verification** through the soul component

### Dream Systems
- **Memory consolidation** during dream cycles
- **Symbolic compression** of related memories
- **Insight generation** through pattern recognition
- **Sleep condition monitoring** based on memory fragmentation
- **Dream cycle logging** and statistics tracking

## Dependencies

The system requires the following Python packages:
- Standard library modules (os, json, sys, time, pathlib)
- No external dependencies required

## Notes

- The brainstem.py file has been updated to use relative imports for the new directory structure
- The dream_manager.py was copied from the Jetbrains_Pycharm directory to ensure compatibility
- A simple_router.py was created to replace the complex LiteLLM router dependency
- All files maintain their original functionality while being organized into logical groups
- No external dependencies required - all components use only Python standard library 