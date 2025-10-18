import aiohttp
import asyncio
import json

class OllamaClient:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/api/generate"
    
    async def test_connection(self):
        """Test if Ollama server is reachable"""
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                async with session.get(f"{self.base_url}/api/tags") as response:
                    return response.status == 200
        except:
            return False
    
    async def generate_response(self, prompt, model="phi3:mini"):
        """Generate AI response using Ollama"""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "top_k": 40,
                }
            }
            
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
                async with session.post(self.api_url, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('response', '').strip()
                    else:
                        print(f"Ollama API error: {response.status}")
                        return None
                        
        except asyncio.TimeoutError:
            print("Ollama timeout error")
            return None
        except Exception as e:
            print(f"Ollama error: {e}")
            return None