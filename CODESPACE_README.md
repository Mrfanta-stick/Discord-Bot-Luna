# 🌙 Luna's Ollama Codespace Setup

This Codespace is configured to run Ollama with Luna's Discord bot for unlimited AI responses!

## 🚀 Quick Start

1. **Launch Codespace**: Click "Code" → "Codespaces" → "Create codespace on main"
2. **Wait for setup**: The setup script will automatically install Ollama and download models
3. **Test the setup**: Run `python test_ollama.py`
4. **Start manager**: Run `python ollama_manager.py` and open port 8000

## 🌐 Access Points

- **Ollama API**: `http://localhost:11434`
- **Management Web UI**: `http://localhost:8000`
- **Model Downloads**: Use the web UI or command line

## 🤖 Available Models

The setup automatically downloads `phi3:mini` (lightweight, fast). You can add more:

```bash
# Download additional models
ollama pull llama3.2:3b      # Better reasoning
ollama pull codellama:7b     # Code specialist
ollama pull mistral:7b       # Fast and capable
```

## 🔧 Management Commands

```bash
# Check Ollama status
ollama list

# Test a model
ollama run phi3:mini "Hello from Luna!"

# View logs
tail -f ollama.log

# Restart Ollama
pkill ollama && ollama serve &
```

## 🌙 Integration with Luna

To use this Ollama instance with your Discord bot:

1. Get the Codespace URL (changes each time)
2. Update Luna's code to use: `https://your-codespace-url.github.dev:11434`
3. Add fallback to Gemini API for when Codespace is sleeping

## 💡 Tips

- **Keep active**: Codespaces sleep after 30 min of inactivity
- **Bookmark URL**: The Codespace URL changes, so save it when active
- **Monitor usage**: Student pack gives 180 hours/month
- **Use ngrok**: For permanent URL (optional)

## 🔄 Auto-restart Script

Create `keep_alive.sh` for auto-restart:

```bash
#!/bin/bash
while true; do
    if ! pgrep -x "ollama" > /dev/null; then
        echo "Restarting Ollama..."
        ollama serve &
    fi
    sleep 60
done
```

Run with: `nohup bash keep_alive.sh &`