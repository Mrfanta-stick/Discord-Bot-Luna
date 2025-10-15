# 🌙 Luna - Discord Bot

Luna is an AI-powered Discord bot with a moon-obsessed personality that provides interactive conversations, space facts, horoscopes, and spontaneous messaging based on day/night cycles.

## ✨ Features

- **AI Conversations**: Powered by Google Gemini AI with personality-driven responses
- **Interactive Commands**: 
  - `/spacefact` - Get interesting space and moon facts
  - `/horoscope` - Daily horoscopes with zodiac sign selection dropdown
  - `!sync` - Sync slash commands
- **Spontaneous Messaging**: Automatic messages during day/night cycles
- **Emotional Support**: Detects emotional keywords and provides supportive responses
- **Day/Night Personality**: Luna's mood changes based on time of day

## 🚀 Setup

### Prerequisites
- Python 3.8+
- Discord Bot Token
- Google Gemini API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
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
   GEMINI_API_KEY=your_gemini_api_key_here
   BOT_PREFIX=!
   ```

4. **Run the bot**
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

**Google Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key

### Bot Permissions
Make sure your bot has these permissions:
- Send Messages
- Use Slash Commands
- Add Reactions
- Read Message History

## 📁 Project Structure

```
Discord_bot_luna/
├── bot.py              # Main bot file
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not in repo)
├── .env.example       # Example environment file
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🤖 Commands

- `/spacefact` - Get a random space/moon fact
- `/horoscope` - Select your zodiac sign and get a daily horoscope
- `!sync` - Sync slash commands (admin use)

## 🌙 Luna's Personality

Luna is obsessed with the moon and space. Her personality changes based on the time:
- **Daytime**: Slightly less energetic, misses the moon
- **Nighttime**: More active and excited about the moon being visible

## 🚀 Deployment

This bot can be deployed on various platforms:
- Railway (Recommended for free hosting)
- Heroku
- DigitalOcean
- Azure
- Google Cloud Platform

## 🤝 Contributing

Feel free to contribute to Luna's development! Open issues and pull requests are welcome.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).