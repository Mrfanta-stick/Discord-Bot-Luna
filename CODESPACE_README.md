# 🚀 GitHub Codespace Setup for Luna

This guide helps you set up Luna with **unlimited AI responses** using Ollama on GitHub Codespaces (free with Student Pack!).

## 🎯 Why Codespaces?

- **✅ Free**: 180 hours/month with GitHub Student Pack
- **✅ Unlimited AI**: No API rate limits with local Ollama
- **✅ Auto-setup**: Everything installs automatically
- **✅ Always online**: Runs independently from your PC

## 🛠️ Setup Steps

### 1. Create the Codespace

1. Go to your GitHub repository
2. Click the **Code** button (green)
3. Go to **Codespaces** tab
4. Click **Create codespace on master**
5. Wait ~5 minutes for automatic setup

### 2. Verify Installation

The devcontainer automatically:
- ✅ Installs Ollama
- ✅ Downloads Phi-3 Mini model (~2.3GB)
- ✅ Starts Ollama service
- ✅ Installs Python dependencies

Check it worked:
```bash
python test_integration.py
```

You should see:
```
✅ Ollama connection successful!
🎭 Luna says: [mystical response]
✅ Luna sounds mystical!
```

### 3. Configure Environment

Create your `.env` file in Codespace:
```bash
nano .env
```

Add your Discord token and Codespace URL:
```env
DISCORD_TOKEN=your_discord_bot_token_here
OLLAMA_URL=https://your-codespace-url.github.dev/proxy/11434
BOT_PREFIX=!
```

**To get your Codespace URL:**
1. Go to **Ports** tab in Codespace
2. Find port **11434** (Ollama API)
3. Right-click → **Port Visibility** → **Public**
4. Copy the forwarded address

### 4. Run Luna

```bash
python bot.py
```

Luna is now live with unlimited responses! 🌙✨

## 🕒 Smart Usage Management

Luna includes a 6-hour daily limit system to maximize your 180h/month:

- **Daily Limit**: 6 hours/day
- **Hour Banking**: Unused hours roll over
- **Max Banked**: Up to 60 hours
- **Monitoring**: Use `/usage` command in Discord

### Check Usage Status
```bash
python usage_admin.py --status
```

### Manually Bank Hours
```bash
python usage_admin.py --bank 2.5
```

## 🌐 Web Management Interface

Start the Ollama web UI:
```bash
python ollama_manager.py
```

Access at: `http://localhost:8000`

Features:
- ✅ Test model responses
- ✅ View model info
- ✅ Check service status

## 🤖 Available Models

The setup automatically downloads `phi3:mini` (lightweight, fast). You can add more:

```bash
# Download additional models
ollama pull llama3.2:3b      # Better reasoning
ollama pull codellama:7b     # Code specialist
ollama pull mistral:7b       # Fast and capable
```

## 🔧 Troubleshooting

**Ollama not responding?**
```bash
# Check if Ollama is running
ps aux | grep ollama

# Restart Ollama
pkill ollama
ollama serve &
```

**Port not accessible?**
- Make sure port 11434 is set to **Public** in Ports tab
- Check firewall settings

**Model not found?**
```bash
# Download Phi-3 Mini
ollama pull phi3:mini
```

## 💡 Tips

- **Keep Codespace alive**: Activity keeps it running
- **Stop when not needed**: Saves hours for busier days
- **Monitor usage**: Check `/usage` in Discord regularly
- **Update code**: Run `git pull origin master` for updates

## 📊 Expected Performance

- **Response Time**: 2-5 seconds
- **Concurrency**: Handles multiple users
- **Uptime**: As long as Codespace is running
- **Cost**: $0 with Student Pack

## 🎉 You're Done!

Luna now has:
- ✅ Unlimited AI responses
- ✅ Smart hour management
- ✅ Free hosting on Codespaces
- ✅ No API rate limits

Enjoy your mystical moon spirit bot! 🌙✨