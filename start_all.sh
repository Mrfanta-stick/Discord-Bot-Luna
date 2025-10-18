#!/bin/bash
# 🌙 Luna Auto-Start Script
# This script starts Ollama and the bot automatically

echo "🚀 Luna Auto-Start Script"
echo "========================"

# Function to check if a process is running
is_running() {
    pgrep -f "$1" > /dev/null 2>&1
}

# Start Ollama if not running
if ! is_running "ollama serve"; then
    echo "🔧 Starting Ollama service..."
    ollama serve > ollama.log 2>&1 &
    sleep 5
    echo "✅ Ollama started"
else
    echo "✅ Ollama already running"
fi

# Verify Ollama is working
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama is responsive"
else
    echo "⚠️  Ollama not responding, waiting..."
    sleep 5
fi

# Start bot if not running
if ! is_running "python bot.py"; then
    echo "🌙 Starting Luna bot..."
    nohup python bot.py > bot.log 2>&1 &
    sleep 2
    echo "✅ Luna bot started"
else
    echo "✅ Luna bot already running"
fi

# Show status
echo ""
echo "📊 Current Status:"
ps aux | grep -E "ollama serve|python bot.py" | grep -v grep

echo ""
echo "🎉 All services running! Luna is live! 🌙"
echo ""
echo "📋 Useful commands:"
echo "  tail -f bot.log        # View bot logs"
echo "  tail -f ollama.log     # View Ollama logs"
echo "  ./start_all.sh         # Run this script again"