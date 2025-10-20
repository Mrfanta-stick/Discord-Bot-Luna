# 🌙 Luna - Discord Bot

Luna is an AI-powered Discord bot with a cheerful moon spirit personality. She provides interactive conversations, space facts, horoscopes, and emotional support powered by Google's Gemini 2.0 Flash Lite.

## ✨ Features

- **🤖 AI Conversations**: Powered by Gemini 2.5 Flash Lite (1000 RPD, 15 RPM)
- **🌙 Moon Spirit Personality**: Cheerful, wise, mystical, and playful
- **Interactive Commands**: 
  - `/spacefact` - Get interesting space and moon facts
  - `/horoscope` - Daily horoscopes with zodiac sign selection
  - `!sync` - Sync slash commands (admin)
- **💬 Smart Interactions**: Detects greetings, emotional support needs, and disrespectful behavior
- **🎭 Mood Variations**: Sassy responses to disrespect, supportive for emotional needs

## 🚀 Quick Deploy to Railway

### Prerequisites
- Discord Bot Token
- Google Gemini API Key (2.5 Flash Lite model)

### One-Click Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. Click "Deploy on Railway"
2. Add environment variables:
   - `DISCORD_TOKEN` - Your Discord bot token
   - `GEMINI_API_KEY` - Your Gemini API key
   - `BOT_PREFIX` - Command prefix (default: `!`)
3. Deploy and enjoy!

## 🔧 Manual Setup

### 1. Clone Repository
```bash
git clone https://github.com/Mrfanta-stick/Discord_bot_luna.git
cd Discord_bot_luna
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` and add your tokens:
```env
DISCORD_TOKEN=your_discord_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
BOT_PREFIX=!
```

### 4. Run the Bot
```bash
python bot.py
```

## 🔑 Getting API Keys

### Discord Bot Token
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" section → Create bot
4. Copy the token
5. Enable "Message Content Intent" under Bot settings

### Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key

**Model**: Gemini 2.5 Flash Lite
- **1000 requests per day (RPD)**
- **15 requests per minute (RPM)**
- Perfect for Discord bot usage!

## 📋 Bot Permissions

Make sure your bot has these Discord permissions:
- ✅ Send Messages
- ✅ Use Slash Commands
- ✅ Add Reactions
- ✅ Read Message History
- ✅ Mention Everyone (for user tagging)

## 🤖 Commands

### Slash Commands
- `/spacefact` - Get a random space/moon fact from Luna
- `/horoscope` - Select your zodiac sign and get a daily horoscope

### Text Commands
- `!sync` - Sync slash commands with Discord (admin/bot owner only)

### Natural Interactions
- **Greetings**: Luna responds to hi, hello, hey, etc.
- **Emotional Support**: Detects when you're feeling down and offers support
- **Space Topics**: Ask about space, moon, planets, stars, etc.
- **Advice Requests**: Ask Luna for advice or opinions
- **Welfare Checks**: Ask how Luna is doing

## 🌙 Luna's Personality

Luna is a **cheerful moon spirit** who:
- 🌕 Is always energized by the moon's presence worldwide
- ✨ Speaks mystically with moon emojis
- 💫 Offers wisdom and playful banter
- 🎭 Gets sassy when disrespected (but stays sophisticated)
- 💖 Provides emotional support when needed

## 📊 Rate Limits

**Gemini 2.5 Flash Lite:**
- 1000 requests per day (RPD)
- 15 requests per minute (RPM)

Luna automatically handles rate limiting and falls back to pre-written responses when limits are reached.

## 🛠️ Project Structure

```
Discord_bot_luna/
├── bot.py              # Main bot file
├── requirements.txt    # Python dependencies
├── Procfile           # Railway/Heroku deployment
├── railway.json       # Railway configuration
├── runtime.txt        # Python version
├── .env               # Environment variables (not in repo)
├── .env.example       # Example environment file
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## 🚀 Deployment Options

### Railway (Recommended - Free Tier)
- Free $5/month credit
- Always-on deployment
- Automatic restarts
- Easy environment variables

### Heroku
- Free tier available
- Easy deployment
- Good documentation

### Self-Hosted
- Run on your own server
- Full control
- Use `nohup python bot.py &` for background process

## 🤝 Contributing

Feel free to contribute to Luna's development! Open issues and pull requests are welcome.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

**Made with 🌙 by the Luna development team**