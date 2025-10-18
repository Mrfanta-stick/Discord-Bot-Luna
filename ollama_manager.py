#!/usr/bin/env python3
"""
Luna's Ollama Management Server
Simple web interface to manage the Ollama service in Codespace
"""

import asyncio
import aiohttp
from aiohttp import web
import json
import subprocess
import os

class OllamaManager:
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
    
    async def test_connection(self):
        """Test if Ollama is running"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.ollama_url}/api/tags") as response:
                    return response.status == 200
        except:
            return False
    
    async def list_models(self):
        """Get list of installed models"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.ollama_url}/api/tags") as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('models', [])
        except:
            pass
        return []
    
    async def generate_response(self, model, prompt):
        """Generate AI response"""
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                }
                async with session.post(f"{self.ollama_url}/api/generate", json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('response', 'No response')
        except Exception as e:
            return f"Error: {e}"
        return "Failed to generate response"

# Initialize manager
manager = OllamaManager()

async def home(request):
    """Home page with status and controls"""
    is_running = await manager.test_connection()
    models = await manager.list_models()
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🌙 Luna's Ollama Manager</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #1a1a2e; color: #eee; }}
            .status {{ padding: 20px; border-radius: 10px; margin: 20px 0; }}
            .running {{ background: #16213e; border: 2px solid #0f3460; }}
            .stopped {{ background: #2e1a1a; border: 2px solid #604040; }}
            .models {{ background: #1e2a1e; border: 2px solid #404060; padding: 20px; border-radius: 10px; }}
            input, textarea {{ width: 100%; padding: 10px; margin: 10px 0; background: #2a2a3e; color: #eee; border: 1px solid #555; }}
            button {{ padding: 12px 24px; background: #0f3460; color: white; border: none; border-radius: 5px; cursor: pointer; }}
            button:hover {{ background: #16213e; }}
            .response {{ background: #2e2a1e; padding: 15px; border-radius: 5px; margin: 10px 0; border-left: 4px solid #ffd700; }}
        </style>
    </head>
    <body>
        <h1>🌙 Luna's Ollama Management Center</h1>
        
        <div class="status {'running' if is_running else 'stopped'}">
            <h2>Status: {'🟢 Running' if is_running else '🔴 Stopped'}</h2>
            <p>Ollama API: {manager.ollama_url}</p>
        </div>
        
        <div class="models">
            <h2>📦 Installed Models</h2>
            {f'<ul>{"".join([f"<li>🤖 {m.get('name', 'Unknown')} ({m.get('size', 'Unknown size')})</li>" for m in models])}</ul>' if models else '<p>No models installed</p>'}
        </div>
        
        <div class="models">
            <h2>💬 Test Luna's AI</h2>
            <form action="/test" method="post">
                <select name="model" style="width: 100%; padding: 10px; margin: 10px 0; background: #2a2a3e; color: #eee;">
                    {f'{"".join([f"<option value='{m.get('name', '')}'>{m.get('name', 'Unknown')}</option>" for m in models])}' if models else '<option>No models available</option>'}
                </select>
                <textarea name="prompt" placeholder="Ask Luna something..." rows="3">Hello Luna! Tell me something interesting about the moon!</textarea>
                <button type="submit">🚀 Generate Response</button>
            </form>
        </div>
        
        <div class="models">
            <h2>🔧 Quick Actions</h2>
            <button onclick="window.location.reload()">🔄 Refresh Status</button>
            <button onclick="downloadModel()">📥 Download Model</button>
        </div>
        
        <script>
            function downloadModel() {{
                const model = prompt("Enter model name (e.g., 'llama3.2:3b', 'phi3:mini'):");
                if (model) {{
                    fetch('/download', {{
                        method: 'POST',
                        headers: {{'Content-Type': 'application/json'}},
                        body: JSON.stringify({{model: model}})
                    }}).then(() => location.reload());
                }}
            }}
        </script>
    </body>
    </html>
    """
    return web.Response(text=html, content_type='text/html')

async def test_ai(request):
    """Test AI generation"""
    data = await request.post()
    model = data.get('model')
    prompt = data.get('prompt')
    
    if not model or not prompt:
        return web.Response(text="Missing model or prompt", status=400)
    
    response = await manager.generate_response(model, prompt)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🌙 Luna's Response</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #1a1a2e; color: #eee; }}
            .response {{ background: #2e2a1e; padding: 20px; border-radius: 10px; border-left: 4px solid #ffd700; }}
            button {{ padding: 12px 24px; background: #0f3460; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <h1>🌙 Luna's Response</h1>
        <div class="response">
            <h3>📝 Your prompt:</h3>
            <p><em>{prompt}</em></p>
            <h3>🤖 Luna says:</h3>
            <p>{response}</p>
        </div>
        <button onclick="history.back()">← Back</button>
    </body>
    </html>
    """
    return web.Response(text=html, content_type='text/html')

async def download_model(request):
    """Download a new model"""
    data = await request.json()
    model = data.get('model')
    
    if model:
        try:
            # Run ollama pull in background
            subprocess.Popen(['ollama', 'pull', model])
            return web.json_response({"status": "downloading", "model": model})
        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)
    
    return web.json_response({"error": "No model specified"}, status=400)

# Create web app
app = web.Application()
app.router.add_get('/', home)
app.router.add_post('/test', test_ai)
app.router.add_post('/download', download_model)

if __name__ == '__main__':
    print("🌙 Starting Luna's Ollama Manager...")
    print("🌐 Open: http://localhost:8000")
    web.run_app(app, host='0.0.0.0', port=8000)