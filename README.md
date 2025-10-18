# 🌙 Luna - Discord Bot

Luna is an AI-powered Discord bot with a moon-obsessed personality that provides interactive conversations, space facts, horoscopes, and unlimited responses powered by Ollama running on GitHub Codespaces.

## ✨ Features

- **🚀 Unlimited AI Conversations**: Powered by Ollama (Phi-3 Mini) on GitHub Codespaces - no API rate limits!
- **🕒 Smart Usage Management**: 6-hour daily limits with hour banking system to maximize free Codespace allocation
- **Interactive Commands**: 
  - `/spacefact` - Get interesting space and moon facts
  - `/horoscope` - Daily horoscopes with zodiac sign selection dropdown
  - `/usage` - Check Codespace usage status and banked hours
  - `!sync` - Sync slash commands
- **Emotional Support**: Detects emotional keywords and provides supportive responses
- **Cheerful Moon Spirit**: Luna maintains her mystical, energetic personality 24/7

## 🚀 Setup

### Prerequisites
- Python 3.8+
- Discord Bot Token
- GitHub Codespace (free with Student Pack - 180 hours/month)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Mrfanta-stick/Discord_bot_luna.git
   cd Discord_bot_luna
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your tokens:
   ```
   DISCORD_TOKEN=your_discord_bot_token_here
   OLLAMA_URL=https://your-codespace-url.github.dev/proxy/11434
   BOT_PREFIX=!
   ```

4. **Set up GitHub Codespace** (See [CODESPACE_README.md](CODESPACE_README.md))

5. **Run the bot in Codespace**
   ```bash
   python bot.py
   ```

## 🔧 Configuration

### Getting API Keys

**Discord Bot Token:**
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section
4. Copy the token

**GitHub Codespace Setup:**
See [CODESPACE_README.md](CODESPACE_README.md) for detailed instructions on setting up your free Ollama server.

### Bot Permissions
Make sure your bot has these permissions:
- Send Messages
- Use Slash Commands
- Add Reactions
- Read Message History

## 📁 Project Structure

```
Discord_bot_luna/
├── bot.py                  # Main bot file
├── ollama_client.py        # Ollama API client
├── usage_manager.py        # Smart usage tracking system
├── usage_admin.py          # Admin tools for usage management
├── ollama_manager.py       # Web UI for Ollama management
├── test_integration.py     # Integration tests
├── requirements.txt        # Python dependencies
├── .devcontainer/          # Codespace configuration
├── .env                    # Environment variables (not in repo)
├── .env.example            # Example environment file
├── CODESPACE_README.md     # Codespace setup guide
└── README.md               # This file
```

## 🤖 Commands

- `/spacefact` - Get a random space/moon fact
- `/horoscope` - Select your zodiac sign and get a daily horoscope
- `/usage` - Check Codespace usage status and banked hours
- `!sync` - Sync slash commands (admin use)

## 🌙 Luna's Personality

Luna is a cheerful moon spirit obsessed with the moon and space. She's always energized by the moon's presence somewhere in the world, maintaining her mystical, wise, and playful personality 24/7.

## 🚀 Deployment

**GitHub Codespaces (Recommended):**
- ✅ Free with Student Pack (180 hours/month)
- ✅ Unlimited AI responses
- ✅ Auto-setup with devcontainer
- ✅ Smart usage management

See [CODESPACE_README.md](CODESPACE_README.md) for full setup instructions.

## � Usage Management

Luna uses a smart usage system to maximize your free Codespace hours:
- **6 hours per day limit** (saves 60h/month)
- **Hour banking** - unused hours roll over to next day
- **Usage tracking** - Monitor via `/usage` command
- **Admin tools** - `python usage_admin.py` for manual management

## 🤝 Contributing

Feel free to contribute to Luna's development! Open issues and pull requests are welcome.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).