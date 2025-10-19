#!/bin/bash

# Start the Ollama server in the background
echo "🌙 Starting Ollama service..."
ollama serve &

# Wait 5 seconds for Ollama to be ready
sleep 5

# Start your Discord bot in the background
echo "🌙 Starting Luna bot (bot.py)..."
python3 bot.py &

# Start your web manager in the FOREGROUND
echo "🌐 Starting web manager (ollama_manager.py) on port 8000..."
python3 ollama_manager.py