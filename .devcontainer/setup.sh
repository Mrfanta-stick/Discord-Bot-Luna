#!/bin/bash

echo "🌙 Setting up Luna's Ollama Server..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Ollama
echo "📦 Installing Ollama..."
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service in background
echo "🚀 Starting Ollama service..."
nohup ollama serve > ollama.log 2>&1 &

# Wait for Ollama to start
echo "⏳ Waiting for Ollama to initialize..."
sleep 10

# Download a lightweight model
echo "🤖 Downloading Phi-3 Mini model (lightweight but capable)..."
ollama pull phi3:mini

# Install Python dependencies for Luna
echo "🐍 Installing Python dependencies..."
pip install -r requirements.txt

# Create a simple API test script
cat > test_ollama.py << 'EOF'
import requests
import json

def test_ollama():
    try:
        response = requests.post('http://localhost:11434/api/generate', 
            json={
                "model": "phi3:mini",
                "prompt": "Hello! I'm Luna, a cheerful moon spirit. How are you today?",
                "stream": False
            })
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Ollama is working!")
            print("🌙 Luna says:", result['response'])
            return True
        else:
            print("❌ Ollama error:", response.status_code)
            return False
    except Exception as e:
        print("❌ Connection error:", e)
        return False

if __name__ == "__main__":
    test_ollama()
EOF

echo "✅ Setup complete!"
echo ""
echo "🌙 Luna's Ollama server is ready!"
echo "📋 Next steps:"
echo "   1. Test Ollama: python test_ollama.py"
echo "   2. Check logs: tail -f ollama.log"
echo "   3. API endpoint: http://localhost:11434"
echo ""
echo "🎯 Available models:"
ollama list