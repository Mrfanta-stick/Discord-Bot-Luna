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
