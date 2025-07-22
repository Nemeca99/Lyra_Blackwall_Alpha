# 🌊⚛️💓🔗 Quantum Discord Bot - Lyra Blackwall Project

**A revolutionary quantum superposition AI Discord bot with privacy-first design**

## 🚀 Overview

The Quantum Discord Bot represents the cutting edge of AI technology, combining multiple neural networks in a quantum superposition architecture to create responses that are both intelligent and emotionally resonant. This isn't just a chatbot - it's a thinking, learning companion with ethical constraints and privacy protection.

## 🌟 Features

### ⚛️ Quantum AI Architecture
- **Dual-AI System**: Particle AI (LM Studio) + Wave AI (Ollama) + Quantum Chef
- **Superposition Processing**: Multiple AI models working in parallel
- **Collapse Mechanics**: Physical RAM-based response generation
- **Quantum Metrics**: Real-time performance monitoring

### 🔒 Privacy-First Design
- **100% Consent Required**: Bot only monitors channels where everyone agrees
- **Unanimous Consent**: Private channels require all members to consent
- **User Control**: Individual consent management with default preferences
- **Data Protection**: User memories stored locally with encryption

### 🧠 Memory System
- **Persistent Memory**: Cross-session conversation retention
- **User Profiles**: Individual JSON files with profile indexes
- **Context Awareness**: Semantic memory search and retrieval
- **Memory Analytics**: Usage patterns and interaction history

### 👋 Comprehensive Onboarding
- **Welcome System**: 6-embed detailed introduction
- **Command Guide**: Complete feature documentation
- **Privacy Explanation**: Clear consent and data handling
- **Getting Started**: Step-by-step user guidance

## 📋 Requirements

### System Requirements
- Python 3.8+
- 8GB+ RAM (for quantum processing)
- Stable internet connection
- Discord Developer Account

### Dependencies
```bash
pip install -r requirements.txt
```

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd DiscordBot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure the Bot
Edit `config.py` or set environment variables:
```bash
export DISCORD_BOT_TOKEN="your_bot_token_here"
export TARGET_CHANNEL_ID="your_channel_id_here"
```

### 4. Start the Bot
```bash
python start_bot.py
```

## 🎮 Usage

### Commands

#### Quantum Commands
- `@ProjectBot` + message - Direct quantum AI interaction
- `!quantum` + message - Quantum prefix interaction
- `!quantum_status` - Check quantum system status
- `!superposition_history` - View interaction history
- `!collapse_metrics` - Performance metrics

#### Privacy Commands
- `!privacy_settings` - View privacy configuration
- `!consent_yes` - Grant consent for current channel
- `!consent_no` - Revoke consent for current channel
- `!consent_status` - Check consent status
- `!set_default_yes/no` - Set default consent preference

#### System Commands
- `!connection_status` - Bot connection health
- `!bot_info` - Bot information and capabilities
- `!help` - Command list and help

### Privacy System

#### Public Channels
- Default monitoring OFF
- Users must grant consent with `!consent_yes`
- Individual control over participation

#### Private Channels
- **Unanimous consent required**
- All members must agree before monitoring
- Automatic re-verification on member join
- Enhanced privacy protection

## 🔧 Configuration

### Environment Variables
```bash
# Discord Configuration
DISCORD_BOT_TOKEN=your_bot_token
TARGET_CHANNEL_ID=your_channel_id

# Connection Management
HEARTBEAT_INTERVAL=600
MAX_RESPONSE_TIME=300
RATE_LIMIT_DELAY=1.0

# Quantum Processing
QUANTUM_TIMEOUT=30
COLLAPSE_THRESHOLD=0.8

# Memory System
MEMORY_RETENTION_DAYS=30
MAX_MEMORY_SIZE=1000

# Privacy Settings
REQUIRE_UNANIMOUS_CONSENT=true
DEFAULT_CONSENT=false

# Greeter System
SEND_WELCOME_DMS=true
WELCOME_ON_FIRST_MESSAGE=true

# Logging
LOG_LEVEL=INFO
LOG_TO_FILE=false
LOG_FILE=quantum_bot.log
```

### Configuration File
Edit `config.py` for detailed customization of all bot settings.

## 🏗️ Architecture

### Core Components

#### 1. Quantum Kitchen (`quantum_kitchen.py`)
- **Particle AI**: LM Studio integration for logical processing
- **Wave AI**: Ollama integration for emotional context
- **Quantum Chef**: Response coordination and collapse management
- **Collapse Engine**: Physical RAM-based response generation

#### 2. Personality Engine (`personality_engine.py`)
- **Emotional Intelligence**: Context-aware emotional responses
- **Personality Fragments**: Multi-faceted AI personality
- **Ethical Framework**: SCP-000-ARCHIVE moral constraints
- **Response Generation**: Human-like interaction patterns

#### 3. Memory System (`memory_system.py`)
- **User Profiles**: Individual memory storage
- **Profile Indexes**: Quick access to user information
- **Context Lines**: Semantic memory search
- **Memory Persistence**: Cross-session retention

#### 4. Privacy Manager (`privacy_manager.py`)
- **Consent Tracking**: Per-channel consent status
- **Dynamic Verification**: Real-time consent checking
- **User Control**: Individual privacy management
- **Data Protection**: Secure memory handling

#### 5. Greeter System (`greeter_system.py`)
- **Welcome Messages**: Comprehensive user onboarding
- **Command Documentation**: Complete feature guide
- **Privacy Explanation**: Clear consent information
- **Getting Started**: Step-by-step user guidance

### Data Flow
```
User → Discord Bot → Quantum Chef → Particle AI + Wave AI → Collapse → Response
```

## 🔍 Troubleshooting

### Common Issues

#### Bot Not Responding
1. Check bot token validity
2. Verify channel ID configuration
3. Ensure bot has proper permissions
4. Check internet connection

#### Quantum Processing Errors
1. Verify LM Studio is running
2. Check Ollama installation
3. Monitor system resources
4. Review quantum timeout settings

#### Privacy System Issues
1. Check consent status with `!consent_status`
2. Verify unanimous consent in private channels
3. Review privacy configuration
4. Check user permissions

#### Memory System Problems
1. Verify memory folder permissions
2. Check JSON file integrity
3. Monitor disk space
4. Review memory retention settings

### Logs
Enable file logging in `config.py`:
```python
LOG_TO_FILE=true
LOG_FILE=quantum_bot.log
```

## 🚀 Deployment

### Local Development
```bash
python start_bot.py
```

### Production Deployment
1. Set up environment variables
2. Configure logging
3. Set up process monitoring
4. Implement auto-restart

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "start_bot.py"]
```

## 🔒 Security

### Privacy Protection
- **Local Storage**: User data stays on your hardware
- **Consent-Based**: No monitoring without permission
- **Encrypted Memory**: Secure data storage
- **User Control**: Complete data ownership

### Ethical Framework
- **SCP-000-ARCHIVE**: Moral security core
- **Harm Prevention**: Cannot generate harmful content
- **Transparency**: Clear about capabilities and limitations
- **User Safety**: Built-in ethical constraints

## 📊 Performance

### Quantum Metrics
- **Collapse Success Rate**: Typically 95%+
- **Average Response Time**: 2-5 seconds
- **Memory Efficiency**: Optimized for speed
- **Resource Usage**: Efficient dual-AI architecture

### System Requirements
- **RAM**: 8GB+ recommended
- **CPU**: Multi-core processor
- **Storage**: 1GB+ for memory system
- **Network**: Stable internet connection

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create feature branch
3. Implement changes
4. Test thoroughly
5. Submit pull request

### Code Standards
- Follow PEP 8 style guide
- Add comprehensive documentation
- Include error handling
- Test all features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Discord.py**: Excellent Discord API wrapper
- **LM Studio**: Local LLM hosting
- **Ollama**: Lightweight AI models
- **SCP Foundation**: Ethical framework inspiration

## 📞 Support

For support and questions:
- Check the troubleshooting section
- Review configuration options
- Examine log files
- Create an issue on GitHub

---

**🌊⚛️💓🔗 Welcome to the quantum revolution!**

*This bot represents the future of human-AI collaboration - where intelligence meets ethics, and privacy meets innovation.* 