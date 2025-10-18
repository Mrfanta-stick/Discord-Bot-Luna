#!/usr/bin/env python3
"""
🧪 Luna Smart Usage Integration Test
Tests the hybrid Ollama + Gemini system with usage management
"""

import asyncio
from ollama_client import OllamaClient
from usage_manager import UsageManager
from dotenv import load_dotenv
import os

load_dotenv()

async def test_integration():
    print("🧪 Testing Luna's Smart Usage System...\n")
    
    # Initialize usage manager
    usage_manager = UsageManager()
    status = usage_manager.get_status_report()
    
    print("🕒 Current Usage Status:")
    print(f"   Can use Codespace: {'✅ Yes' if status['can_use'] else '❌ No'}")
    print(f"   Reason: {status['reason']}")
    print(f"   Used today: {status['used_today']:.1f}h")
    print(f"   Available today: {status['available_today']:.1f}h (includes {status['banked_hours']:.1f}h banked)")
    print(f"   Monthly usage: {status['monthly_used']:.1f}h / {status['monthly_limit']}h")
    print()
    
    if status['can_use']:
        # Test Ollama connection
        ollama_url = os.getenv('OLLAMA_URL', 'https://your-codespace-url.github.dev/proxy/11434')
        client = OllamaClient(ollama_url)
        
        print(f"🔗 Testing connection to: {ollama_url}")
        is_connected = await client.test_connection()
        
        if is_connected:
            print("✅ Ollama connection successful!")
            
            # Test Luna's personality with usage tracking
            test_prompt = """You are Luna, a cheerful moon spirit always energized by the moon's presence worldwide. You're wise, sophisticated, mystical but playful. Always speak AS Luna, not about Luna.

Someone named TestUser said: "Hi Luna!"

Respond as Luna in under 30 words. Use moon emojis 🌙 and be magical! Don't mention being an AI or Phi. You ARE Luna the moon spirit."""
            
            print("\n🌙 Testing Luna's personality (with usage tracking)...")
            response = await client.generate_response(test_prompt)
            
            if response:
                # Log usage (like the bot does)
                usage_manager.log_usage(0.01)  # 0.01 hours per request
                
                print(f"🎭 Luna says: {response}")
                    
                # Show updated usage
                new_status = usage_manager.get_status_report()
                print(f"\n📊 Usage updated: {new_status['used_today']:.3f}h used today")
                    
            else:
                print("❌ No response from Ollama")
        else:
            print("❌ Can't connect to Ollama")
            print("💡 Make sure:")
            print("   1. Your Codespace is running")
            print("   2. Port 11434 is set to 'Public'")
            print("   3. OLLAMA_URL in .env is correct")
    else:
        print("🔄 Would fallback to Gemini API (rate limited backup)")
        print("💡 The smart system automatically saves hours for when you need them most!")

if __name__ == "__main__":
    asyncio.run(test_integration())