#!/bin/bash
# 🌙 Luna Auto-Start Script

echo "🚀 Luna Auto-Start Script"
echo "========================"

# --- Start Ollama ---
# Check if Ollama API is responsive
if curl -s http://localhost:11434/api/tags > /dev/null; then
    echo "✅ Ollama is already running and responsive."
else
    echo "⚠️ Ollama not responding. Starting service..."
    # Kill any old, broken processes first
    pkill -f "ollama serve"
    sleep 2
    # Start fresh in the background
    nohup ollama serve > ollama.log 2>&1 &
    
    echo "⏳ Waiting for Ollama to initialize (10s)..."
    sleep 10
    
    # Final check
    if curl -s http://localhost:11434/api/tags > /dev/null; then
        echo "✅ Ollama started successfully."
    else
        echo "❌ CRITICAL: Ollama failed to start. Check 'ollama.log'."
        tail -n 20 ollama.log
    fi
fi

# --- Start the Bot ---
if ! pgrep -f "python bot.py" > /dev/null; then
    echo "🌙 Starting Luna bot..."
    nohup python bot.py > bot.log 2>&1 &
    sleep 2
    echo "✅ Luna bot started."
else
    echo "✅ Luna bot already running."
fi

echo ""
echo "📊 Current Status:"
ps aux | grep -E "ollama serve|python bot.py" | grep -v grep

echo ""
echo "🎉 All services running! Luna is live! 🌙"
echo "  (Note: Codespace will sleep after 30 mins of inactivity)"
echo "  tail -f bot.log        # View bot logs"
echo "  tail -f ollama.log     # View Ollama logs"