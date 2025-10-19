#!/bin/bash
# 🌙 Luna Auto-Start Script

echo "🚀 Luna Auto-Start Script"
echo "========================"

# --- Start Ollama ---
# Use 127.0.0.1 as it's more reliable than 'localhost'
if curl -s http://127.0.0.1:11434/api/tags > /dev/null; then
    echo "✅ Ollama is already running and responsive."
else
    echo "⚠️ Ollama not responding. Starting service..."
    pkill -f "ollama serve"
    sleep 2
    nohup ollama serve > ollama.log 2>&1 &
    
    echo "⏳ Waiting for Ollama to initialize (10s)..."
    sleep 10
    
    if curl -s http://127.0.0.1:11434/api/tags > /dev/null; then
        echo "✅ Ollama started successfully."
    else
        echo "❌ CRITICAL: Ollama failed to start. Check 'ollama.log'."
        tail -n 20 ollama.log
        exit 1 # Exit if Ollama fails
    fi
fi

# --- NEW: Warm up the AI model ---
echo "🔥 Warming up Phi-3 model... (This may take a moment)"
# This sends a simple request and waits for it to complete.
# The timeout is set to 5 minutes (300s) just for this one warm-up
# to ensure the model has time to load. We send the output to /dev/null.
curl http://127.0.0.1:11434/api/generate \
     -d '{
           "model": "phi3:mini",
           "prompt": "Hello",
           "stream": false
         }' \
     --max-time 300 \
     -s -o /dev/null

echo "✅ Model is warm and ready."

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