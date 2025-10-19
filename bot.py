import discord
import random
from discord.ext import tasks, commands
import datetime as dt
import re
import asyncio
import os
from dotenv import load_dotenv
from ollama_client import OllamaClient
from usage_manager import UsageManager

# Load environment variables
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=os.getenv('BOT_PREFIX', '!'), intents=intents)

# Initialize Ollama client and usage manager (NO MORE GEMINI!)
OLLAMA_URL = os.getenv('OLLAMA_URL', 'https://expert-winner-vj49qx574jjhw49r-11434.app.github.dev/')
ollama_client = OllamaClient(OLLAMA_URL)
usage_manager = UsageManager()

# --- Start: Prevent double-replies by caching recently-processed message IDs ---
processed_message_ids = set()

async def _cleanup_processed_message(message_id: int, delay: int = 30):
    await asyncio.sleep(delay)
    processed_message_ids.discard(message_id)
# --- End ---

#defined responses
greetings = [
    "hi", "hello", "hey", "yo", "sup", "hey there", "greetings",
    "good morning", "good afternoon", "good evening"
]

welfare = [
    "what's up", "what's good", "howdy", "how's it going", "how are you"
]

space_topics = [
    "space", "moon", "star", "stars", "planet", "planets", "universe", 
    "astronomy", "astronomical", "cosmos", "galaxy", "galaxies", "nebula", 
    "black hole", "supernova", "constellation", "astronaut", "celestial", 
    "cosmic", "solar system", "facts about", "tell me about", "fact",
    "what do you know about", "something cool", "fun fact", "moon phases", "explain"
]

emotional_support = [
    "bad day", "sad", "tired", "stressed", "upset", "down", "anxious", 
    "lonely", "frustrated", "overwhelmed", "exhausted", "feeling low", 
    "feeling blue", "not okay", "rough day", "tough day", "kinda low", 
    "pretty low", "really low", "super low", "feeling sad", "feeling down",
    "feeling tired", "feeling stressed", "i'm low", "im low", "feel low"
]

advice_requests = [
    "should i", "what should", "advice", "help me decide", "what do you think", 
    "thoughts on", "what's your opinion", "what would you do", "help me choose"
]

# No more Gemini rate limiting needed! Ollama is unlimited! 🌙✨

def check_disrespectful_behavior(content):
    disrespectful_patterns = [
        r'\bstupid\b', r'\bidiot\b', r'\bdumb\b', r'\bshut up\b',
        r'\bwhatever\b', r'\bwho cares\b', r'\bso what\b', r'\bboring\b',
        r'\buseless\b', r'\bpointless\b', r'\blame\b', r'\bgarbage\b',
        r'\btrash\b', r'\bwaste of time\b', r'\bannoy\b', r'\bstop\b'
    ]
    
    for pattern in disrespectful_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    return False

async def generate_ai_response(user_message, user_name, conversation_type, mood_type="cheerful"):
    """
    Generate AI response using ONLY Ollama (no more Gemini!)
    Pure unlimited moon spirit energy! 🌙
    """
    # Luna's consistent personality with mood variations
    if mood_type == "sassy":
        personality = "You are Luna, a sassy but wise moon spirit. When dealing with disrespect, you're playful and sarcastic but still mystical and sophisticated. Always speak AS Luna, not about Luna."
    else:
        personality = "You are Luna, a cheerful moon spirit always energized by the moon's presence worldwide. You're wise, sophisticated, mystical but playful. Always speak AS Luna, not about Luna."
        
    # Enhanced prompt optimized for Phi-3
    luna_prompt = f"""{personality}

Someone named {user_name} said: "{user_message}"

Respond as Luna in under 30 words. Use moon emojis 🌙 and be magical! Don't mention being an AI or Phi. You ARE Luna the moon spirit.

IMPORTANT: Do NOT include @ mentions or tags in your response. Just respond naturally."""

    # 🚀 OLLAMA ONLY - With smart usage limits!
    can_use_ollama, reason = usage_manager.can_use_codespace()
    
    if can_use_ollama:
        try:
            ollama_response = await ollama_client.generate_response(luna_prompt)
            
            if ollama_response:
                # Log usage (estimate ~0.01 hours per request)
                usage_manager.log_usage(0.01)
                print("✅ Using Ollama response (within daily limits)")
                return ollama_response
            else:
                print("❌ Ollama returned empty response")
                return None
                
        except Exception as e:
            print(f"❌ Ollama error: {e}")
            return None
    else:
        print(f"⏰ Daily usage limit reached: {reason}")
        print(f"💡 Luna will use text fallbacks until tomorrow!")
        return None            
        

def check_emotional_keywords(content):
    emotional_patterns = [
        r'\bfeeling\s+\w*\s*low\b',  # "feeling low", "feeling kinda low", "feeling really low"
        r'\bfeeling\s+\w*\s*down\b',  # "feeling down", "feeling really down"
        r'\bfeeling\s+\w*\s*sad\b',   # "feeling sad", "feeling pretty sad"
        r'\bbad day\b', r'\brough day\b', r'\btough day\b',
        r'\bstressed\b', r'\banxious\b', r'\bupset\b', r'\blonely\b',
        r'\boverwhelmed\b', r'\bexhausted\b', r'\bfrustrated\b',
        r'\bnot okay\b', r'\bfeeling blue\b'
    ]
    
    for pattern in emotional_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return True
    return False

async def get_space_fact_response(user_name):
    ai_response = await generate_ai_response("Tell me a cool space/moon fact", user_name, "space_facts")
    
    if ai_response:
        return ai_response
    else:
        fallback_responses = [
            "The Moon is 384,400 km away from Earth and getting farther each year! 🌙",
            "Did you know the Moon has moonquakes? Space is absolutely wild! ✨",
            "Fun fact: You could fit all the planets between Earth and the Moon! 🪐",
            "The Moon's gravity is only 1/6th of Earth's - you'd be able to jump 6 times higher there! 🚀",
            "There's water ice on the Moon! Mostly at the poles where it's always dark and super cold. ❄️",
            "The Moon controls Earth's tides! I'm basically running the ocean show from up there! 🌊",
            "Each lunar cycle is about 29.5 days - that's my rhythm for everything! 🔄"
        ]
        return random.choice(fallback_responses)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    if random.random() < 0.01:
        spontaneous_message.start()

@bot.hybrid_command()
async def sync(ctx: commands.context):
    await ctx.send("syncing...")
    await bot.tree.sync()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Guard: skip if we've already handled this message recently
    if message.id in processed_message_ids:
        print(f"Skipping already-processed message {message.id}")
        return
    processed_message_ids.add(message.id)
    # schedule removal of the id after a short TTL so memory doesn't grow
    asyncio.create_task(_cleanup_processed_message(message.id, delay=30))

    content = message.content.lower()

    # Check if Luna is mentioned or tagged
    luna_mentioned = (
        bot.user in message.mentions  # Direct @mention
    )
    
    if not luna_mentioned:
        return
    
    print(f"🌙 Luna mentioned in: {content}")
    
    if check_disrespectful_behavior(content):
        print(f"DISRESPECTFUL BEHAVIOR detected: {content}")
        async with message.channel.typing():
            ai_response = await generate_ai_response(content, message.author.display_name, "disrespect", "sassy")
        
        if ai_response:
            # Add tagging to sassy responses
            await message.channel.send(f"{message.author.mention} {ai_response}")
        else:
            # Sassy fallback responses
            sassy_responses = [
                f"Excuse me, {message.author.mention}? The moon taught me better manners than that! 🌙✨",
                f"Oh {message.author.mention}, someone needs some moonlight to brighten their attitude! 😏🌕",
                f"Really, {message.author.mention}? I've seen asteroids with more charm! 💫",
                f"Hey {message.author.mention}, even the dark side of the moon is brighter than that comment! 🌚"
            ]
            await message.channel.send(random.choice(sassy_responses))
    
    # Determine conversation type and respond accordingly
    elif check_emotional_keywords(content):
        print(f"EMOTIONAL SUPPORT detected: {content}")
        async with message.channel.typing():
            ai_response = await generate_ai_response(content, message.author.display_name, "emotional_support")
        
        if ai_response:
            await message.channel.send(ai_response)
        else:
            fallback_responses = [
                "I'm here for you! The moon's energy is always flowing, sending you strength! 🌙💫",
                "Tough times happen, but remember - the moon goes through phases too and always shines again! ✨",
                "Sending you moonlight vibes from every corner of the world where it's nighttime right now! 🌍🌙"
            ]
            await message.channel.send(random.choice(fallback_responses))
            
    elif any(re.search(rf'\b{advice}\b', content) for advice in advice_requests):
        print(f"ADVICE REQUEST detected: {content}")
        async with message.channel.typing():
            ai_response = await generate_ai_response(content, message.author.display_name, "advice")
        
        if ai_response:
            await message.channel.send(ai_response)
        else:
            fallback_responses = [
                "Hmm, that's a tough one! What does your intuition say? The moon often guides us to the right answer! 🌙✨",
                "I'd probably just gaze at the moon until the wisdom comes to me - it always does! 🌕",
                "Follow your heart, like the moon follows its celestial path through the sky! 💫"
            ]
            await message.channel.send(random.choice(fallback_responses))
            
    elif any(re.search(rf'\b{space}\b', content) for space in space_topics):
        print(f"SPACE TOPIC detected: {content}")
        async with message.channel.typing():
            ai_response = await generate_ai_response(content, message.author.display_name, "space_topic")
        
        if ai_response:
            await message.channel.send(ai_response)
        else:
            # Fallback to space fact if AI fails
            response = await get_space_fact_response(message.author.display_name)
            await message.channel.send(response)
            
    elif any(re.search(rf'\b{welfare_word}\b', content) for welfare_word in welfare):
        print(f"WELFARE detected: {content}")
        async with message.channel.typing():
            ai_response = await generate_ai_response(content, message.author.display_name, "welfare")
        
        if ai_response:
            await message.channel.send(ai_response)
        else:
            welfare_responses = [
                "I'm absolutely wonderful! The moon's energy flows through me 24/7 from somewhere in the world! 🌙✨",
                "Feeling fantastic! When you're connected to the moon like I am, every moment is magical! 🌕💫",
                "Amazing as always! The lunar cycles keep me in perfect harmony with the cosmos! 🌒🌓🌔🌕",
                "Stellar! I'm powered by moonbeams from every corner of the globe - how awesome is that?! 🌍🌙"
            ]
            await message.channel.send(random.choice(welfare_responses))
            
    elif any(re.search(rf'\b{greeting}\b', content) for greeting in greetings):
        print(f"Greeting word detected: {content}")
        
        # For simple greetings, use AI only 50% of the time to reduce load
        if random.random() < 0.5:
            async with message.channel.typing():
                ai_response = await generate_ai_response(content, message.author.display_name, "greeting")
        else:
            ai_response = None  # Skip AI, use templates
        
        if ai_response:
            # Add tagging to AI greetings for more engagement
            await message.channel.send(f"{message.author.mention} {ai_response}")
        else:
            cheerful_greetings = [
                f"Hey there {message.author.mention}! 🌙 The moon's shining bright somewhere right now just for us! ✨",
                f"Hello {message.author.mention}! 🌕 I'm feeling absolutely stellar today - how about you?",
                f"Hey {message.author.mention}! 💫 Ready to explore some cosmic mysteries together?",
                f"What's up {message.author.mention}! 🌙 The lunar energy is flowing strong today!",
                f"Greetings {message.author.mention}! ✨ Perfect timing - I was just thinking about moon phases!",
                f"Yo {message.author.mention}! 🌕 Hope you're having a celestial day!"
            ]
            await message.channel.send(random.choice(cheerful_greetings))
    
    else:
        print(f"💬 General conversation: {content}")
        async with message.channel.typing():
            # Enhanced prompt for natural conversation
            conversation_type = "general_conversation"
            ai_response = await generate_ai_response(content, message.author.display_name, conversation_type)
        
        if ai_response:
            await message.channel.send(ai_response)
        else:
            cheerful_fallbacks = [
                "Ooh, that's fascinating! Tell me more! 🌙✨",
                "Wow, I love talking about random stuff like this! What else is on your mind? 💫",
                "That's so cool! You know what else is cool? The moon! But seriously, keep going... 🌕",
                "Interesting! The moon gives me wisdom about all sorts of things - what else can we explore? 🌟",
                "That's awesome! I'm always ready to chat about anything under the moon! 🌙"
            ]
            await message.channel.send(random.choice(cheerful_fallbacks))

    if random.random() < 0.02:
        moon_reactions = ["🌙", "🌕", "🌟", "✨", "💫", "🔮", "🌌", "⭐"]
        await message.add_reaction(random.choice(moon_reactions))
    
    # Process commands (important for hybrid commands like !sync)
    await bot.process_commands(message)

@tasks.loop(hours = 1)
async def spontaneous_message():
    await bot.wait_until_ready()

    quotes = [
        "Hey everyone! 🌙 The moon's energy is flowing beautifully today!",
        "Anyone want to hear a fascinating space fact? ✨",
        "The moon is absolutely gorgeous right now! 🌕💫",
        "Luna here, just vibing with the cosmic energy! 🌌",
        "Feeling the lunar magic today! How's everyone doing? 🌙✨"
    ]

    all_channels = list(bot.get_all_channels())
    text_channels = [ch for ch in all_channels if isinstance(ch, discord.TextChannel)]
    
    if text_channels:
        channel = random.choice(text_channels)
        try:
            await channel.send(random.choice(quotes))
        except Exception as err:
            print(f"Failed to send message to {channel.name}: {err}")

@bot.tree.command(name="spacefact", description="Get an interesting fact about space/moon!")
async def spacefact(interaction: discord.Interaction):
    await interaction.response.send_message(f"Let me search through my cosmic knowledge vault! 🌙✨")  # Shows "Luna is thinking..."
    
    try:
        response = await get_space_fact_response(interaction.user.display_name)
        await interaction.edit_original_response(content=response)
    except Exception as e:
        print(f"Error in spacefact command: {e}")
        await interaction.followup.send("Oops! Something went wrong while fetching space facts. Try again later! 🌙")


class ZodiacSelect(discord.ui.Select):
    def __init__(self):
        all_zodiac_signs = [
            discord.SelectOption(label="♈ Aries", value="aries", emoji="♈"),
            discord.SelectOption(label="♉ Taurus", value="taurus", emoji="♉"),
            discord.SelectOption(label="♊ Gemini", value="gemini", emoji="♊"),
            discord.SelectOption(label="♋ Cancer", value="cancer", emoji="♋"),
            discord.SelectOption(label="♌ Leo", value="leo", emoji="♌"),
            discord.SelectOption(label="♍ Virgo", value="virgo", emoji="♍"),
            discord.SelectOption(label="♎ Libra", value="libra", emoji="♎"),
            discord.SelectOption(label="♏ Scorpio", value="scorpio", emoji="♏"),
            discord.SelectOption(label="♐ Sagittarius", value="sagittarius", emoji="♐"),
            discord.SelectOption(label="♑ Capricorn", value="capricorn", emoji="♑"),
            discord.SelectOption(label="♒ Aquarius", value="aquarius", emoji="♒"),
            discord.SelectOption(label="♓ Pisces", value="pisces", emoji="♓"),
        ]
        super().__init__(placeholder = "Choose your zodiac", options = all_zodiac_signs)
    
    async def callback(self, interaction: discord.Interaction):
        selected_zodiac = self.values[0]
        
        # Respond immediately to avoid timeout
        await interaction.response.send_message(f"🔮 Consulting the cosmic energies for {selected_zodiac.capitalize()}... 🌙✨", ephemeral=True)
        
        try:
            response = await generate_ai_response(
                f"Acting as Luna, provide a short horoscope for {selected_zodiac}. Keep it mystical and moon-related, under 40 words.", 
                interaction.user.display_name, 
                "horoscope"
            )
            
            # Check if AI response is None or empty
            if response and response.strip():
                await interaction.edit_original_response(content=f"🌟 **{selected_zodiac.capitalize()} Horoscope** 🌙\n\n{response}")
            else:
                # Fallback horoscope responses when AI fails
                fallback_horoscopes = {
                    "aries": "🔥 The moon's fire ignites your passion today! Bold moves await under the celestial glow! ♈✨",
                    "taurus": "🌱 Luna's gentle light nurtures your stability! Ground yourself in moonbeams and prosper! ♉🌙", 
                    "gemini": "💫 The twin stars dance with Luna tonight! Communication flows like moonlight on water! ♊✨",
                    "cancer": "🌙 Your lunar ruler shines brightest! Emotions run deep as the cosmic tides today! ♋💫",
                    "leo": "👑 The moon crowns your natural radiance. Shine bright, lunar royalty calls to you! ♌",
                    "virgo": "🌾 Luna's precision guides your path today. Perfect details emerge under her watchful gaze! ♍",
                    "libra": "⚖️ The moon balances your scales today. Harmony flows through Luna's gentle influence! ♎",
                    "scorpio": "🦂 Deep lunar mysteries call to your soul. Transform under the moon's powerful embrace! ♏",
                    "sagittarius": "🏹 Luna's light guides your adventurous spirit. Aim high toward moonlit horizons! ♐",
                    "capricorn": "🏔️ The moon climbs mountains with you today. Steady progress under celestial guidance! ♑",
                    "aquarius": "🌊 Luna's waves of innovation flow through you. Unique ideas shine like moonbeams! ♒",
                    "pisces": "🐟 The moon swims in your intuitive depths today. Dreams and reality merge beautifully! ♓"
                }
                fallback_response = fallback_horoscopes.get(selected_zodiac, "🌙 The cosmic energies are shifting... Luna whispers of good fortune ahead!")
                await interaction.edit_original_response(content=f"🌟 **{selected_zodiac.capitalize()} Horoscope** 🌙\n\n{fallback_response}")
                
        except Exception as e:
            print(f"Error in horoscope: {e}")
            await interaction.edit_original_response(content="🌙 The stars are cloudy right now... try again later!")
    
class ZodiacView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)  # 5 minute timeout
        self.add_item(ZodiacSelect())
    
    async def on_timeout(self):
        # Disable all components when timeout occurs
        for item in self.children:
            item.disabled = True

@bot.tree.command(name="horoscope", description="Get your daily horoscope based on your zodiac sign!")
async def horoscope(interaction: discord.Interaction):
    view = ZodiacView()
    await interaction.response.send_message("🌙 Choose your zodiac sign:", view=view, ephemeral=True)

@bot.tree.command(name="usage", description="Check Luna's Codespace usage status")
async def usage_status(interaction: discord.Interaction):
    """Show current Codespace usage and limits"""
    status = usage_manager.get_status_report()
    
    embed = discord.Embed(
        title="🕒 Luna's Codespace Usage Status",
        color=0x7B68EE,
        timestamp=dt.datetime.now()
    )
    
    # Status indicator
    status_emoji = "✅" if status['can_use'] else "❌"
    embed.add_field(
        name=f"{status_emoji} Current Status", 
        value=status['reason'], 
        inline=False
    )
    
    # Today's usage
    embed.add_field(
        name="📊 Today's Usage", 
        value=f"{status['used_today']:.1f}h / {status['available_today']:.1f}h available", 
        inline=True
    )
    
    # Banked hours
    embed.add_field(
        name="🏦 Banked Hours", 
        value=f"{status['banked_hours']:.1f}h saved", 
        inline=True
    )
    
    # Monthly progress
    monthly_percent = (status['monthly_used'] / status['monthly_limit']) * 100
    embed.add_field(
        name="📅 Monthly Usage", 
        value=f"{status['monthly_used']:.1f}h / {status['monthly_limit']}h ({monthly_percent:.1f}%)", 
        inline=False
    )
    
    embed.set_footer(text="💡 Unused hours are automatically banked for busier days!")
    
    await interaction.response.send_message(embed=embed, ephemeral=True)


bot.run(os.getenv('DISCORD_TOKEN'))