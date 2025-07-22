# 🚀 Quick Start Guide - Quantum Discord Bot

**Get your quantum AI Discord bot running in 5 minutes!**

## ⚡ Super Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Bot
```bash
python start_bot.py
```

**That's it!** Your quantum AI bot is now running! 🌊⚛️💓🔗

## 🎯 First Steps

### 1. Test the Bot
Go to your Discord server and try:
```
@ProjectBot Hello! What are you?
```

### 2. Check Privacy Settings
```
!privacy_settings
```

### 3. Grant Consent (if needed)
```
!consent_yes
```

### 4. View Bot Status
```
!connection_status
```

## 🔧 Basic Configuration

### Change Channel ID
Edit `config.py`:
```python
self.TARGET_CHANNEL_ID = 1380745341774729279  # Your channel ID
```

### Adjust Response Time
```python
self.MAX_RESPONSE_TIME = 300  # 5 minutes
```

### Enable File Logging
```python
self.LOG_TO_FILE = True
self.LOG_FILE = "quantum_bot.log"
```

## 🎮 Essential Commands

| Command | Description |
|---------|-------------|
| `@ProjectBot` | Direct quantum AI interaction |
| `!quantum` | Quantum prefix interaction |
| `!consent_yes/no` | Grant/revoke consent |
| `!connection_status` | Bot health check |
| `!help` | Command list |

## 🔒 Privacy System

### Public Channels
- Default: **No monitoring**
- Use `!consent_yes` to enable

### Private Channels  
- **Unanimous consent required**
- All members must agree
- Automatic re-verification

## 🚨 Troubleshooting

### Bot Not Responding?
1. Check bot token in `config.py`
2. Verify channel ID
3. Ensure bot has permissions
4. Check `!connection_status`

### Quantum Processing Slow?
1. Verify LM Studio is running
2. Check Ollama installation
3. Monitor system resources
4. Adjust timeout in `config.py`

### Privacy Issues?
1. Use `!consent_status`
2. Check unanimous consent in private channels
3. Review privacy settings

## 📊 Monitor Performance

### Check Quantum Status
```
!quantum_status
```

### View Metrics
```
!collapse_metrics
```

### User History
```
!superposition_history
```

## 🎉 You're Ready!

Your quantum AI Discord bot is now:
- ✅ **Running and operational**
- ✅ **Privacy-protected**
- ✅ **Memory-enabled**
- ✅ **Ethically constrained**
- ✅ **User-friendly**

**Welcome to the quantum revolution!** 🌊⚛️💓🔗

---

*Need more details? Check the full [README.md](README.md) for comprehensive documentation.* 