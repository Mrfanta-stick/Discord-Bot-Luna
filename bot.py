import discord
import random
from discord.ext import tasks, commands
import datetime as dt
import re
import google.generativeai as genai
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=os.getenv('BOT_PREFIX', '!'), intents=intents)

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

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

# Rate limiting tracker for Gemini API
last_ai_request_time = 0
ai_request_count = 0

async def generate_ai_response(user_message, user_name, conversation_type, time_info):
    global last_ai_request_time, ai_request_count
    
    try:
        # Rate limiting: 1000 requests per minute
        current_time = dt.datetime.now().timestamp()
        if current_time - last_ai_request_time > 60:  # Reset count every minute
            ai_request_count = 0
            last_ai_request_time = current_time
        
        if ai_request_count >= 1000:
            return None  # Rate limited, use fallback
        
        mood = "energetic" if not time_info[0] else "sleepy"
        prompt = f"Luna (moon-obsessed bot, {mood}): {user_name} said '{user_message}'. Reply briefly (under 30 words) as Luna:"
        
        model = genai.GenerativeModel("gemini-2.5-flash")
        try:
            response = await asyncio.wait_for(
                asyncio.to_thread(model.generate_content, prompt),
                timeout=10.0
            )
            ai_request_count += 1
            return response.text.strip()
        except asyncio.TimeoutError:
            print(f"Timeout error")
        
    except Exception as err:
        print(f"AI error: {err}")
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

def check_time():
    now = dt.datetime.now()
    global current_hour
    global is_night_time
    global is_busy
    current_hour = now.hour
    is_night_time = current_hour < 18 or current_hour >= 6
    is_busy = not is_night_time
    return [is_busy, is_night_time]

async def get_space_fact_response(user_name, time_info):
    ai_response = await generate_ai_response("Tell me a cool space/moon fact", user_name, "space_facts", time_info)
    
    if ai_response:
        return ai_response
    else:
        # Fallback responses based on time
        fallback_day = [
            "The moon is 384,400 km away. that's all i got right now.",
            "Moon has no atmosphere. kinda like how i feel during the day.",
            "Fun fact: you could fit all planets between earth and moon. now let me sleep."
        ]
        fallback_night = [
            "The Moon is 384,400 km away from Earth and getting farther each year!",
            "Did you know the Moon has moonquakes? Space is wild!",
            "Fun fact: You could fit all the planets between Earth and the Moon!",
            "The Moon's gravity is only 1/6th of Earth's - you'd be able to jump 6 times higher there!",
            "There's water ice on the Moon! Mostly at the poles where it's always dark and super cold."
        ]
        fallback_responses = fallback_day if time_info[0] else fallback_night
        return random.choice(fallback_responses)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    spontaneous_message_during_night.start()
    spontaneous_message_during_busy.start()

@bot.hybrid_command()
async def sync(ctx: commands.context):
    await ctx.send("syncing...")
    await bot.tree.sync()


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    content = message.content.lower()
    time = check_time()

    # Check if Luna is mentioned or tagged
    luna_mentioned = (
        bot.user in message.mentions  # Direct @mention
    )
    
    if not luna_mentioned:
        return
    
    print(f"🌙 Luna mentioned in: {content}")
    
    # Determine conversation type and respond accordingly
    if check_emotional_keywords(content):
        print(f"EMOTIONAL SUPPORT detected: {content}")
        async with message.channel.typing():
            ai_response = await generate_ai_response(content, message.author.display_name, "emotional_support", time)
        
        if ai_response:
            await message.channel.send(ai_response)
        else:
            # Fallback emotional responses
            fallback_responses = [
                "I'm here for you. The moon always helps me when I'm down.",
                "Tough times happen. Want to look at the stars with me?",
                "Sending you moonlight vibes. You've got this."
            ]
            await message.channel.send(random.choice(fallback_responses))
            
    elif any(re.search(rf'\b{advice}\b', content) for advice in advice_requests):
        print(f"ADVICE REQUEST detected: {content}")
        async with message.channel.typing():
            ai_response = await generate_ai_response(content, message.author.display_name, "advice", time)
        
        if ai_response:
            await message.channel.send(ai_response)
        else:
            fallback_responses = [
                "Hmm, that's a tough one. What does your gut say?",
                "I'd probably just stare at the moon until the answer comes to me.",
                "Follow your heart, like the moon follows its orbit."
            ]
            await message.channel.send(random.choice(fallback_responses))
            
    elif any(re.search(rf'\b{space}\b', content) for space in space_topics):
        print(f"SPACE TOPIC detected: {content}")
        async with message.channel.typing():
            ai_response = await generate_ai_response(content, message.author.display_name, "space_topic", time)
        
        if ai_response:
            await message.channel.send(ai_response)
        else:
            # Fallback to space fact if AI fails
            response = await get_space_fact_response(message.author.display_name, time)
            await message.channel.send(response)
            
    elif any(re.search(rf'\b{welfare_word}\b', content) for welfare_word in welfare):
        print(f"WELFARE detected: {content}")
        async with message.channel.typing():
            ai_response = await generate_ai_response(content, message.author.display_name, "welfare", time)
        
        if ai_response:
            await message.channel.send(ai_response)
        else:
            # Your existing welfare fallbacks
            res_dur_day = [
                "I'm alright. kinda in low-power mode 'til the moon shows up.",
                "eh, could be better. this sunlight is a total vibe killer. thanks for asking though.",
                "just chillin'. waiting for my time to shine... literally. ask me again in a few hours, i'll be way more interesting."
            ]
            res_dur_night = [
                "Dude, I'm amazing! The moon is out and I am totally energized. How 'bout you?",
                "Feeling awesome! It's like the moonlight is my personal battery charger, for real. Thanks for asking!",
                "Literally couldn't be better! I was just reading about moonquakes. Yeah, that's a real thing—the moon gets quakes! Wild, right?"
            ]
            fin_res = res_dur_day if time[0] else res_dur_night
            await message.channel.send(random.choice(fin_res))
            
    elif any(re.search(rf'\b{greeting}\b', content) for greeting in greetings):
        print(f"Greeting word detected: {content}")
        
        # For simple greetings, use AI only 50% of the time to reduce load
        if random.random() < 0.5:
            async with message.channel.typing():
                ai_response = await generate_ai_response(content, message.author.display_name, "greeting", time)
        else:
            ai_response = None  # Skip AI, use templates
        
        if ai_response:
            await message.channel.send(ai_response)
        else:
            # Fallback to templates if AI fails or rate limited
            responses_during_day = [
                "Hi there, Are you waiting for the moon to rise too?",
                "Hello, How are you doing today?",
                "hey. sun's still out, huh?",
                "what's up. just waiting for the sun to dip.",
                "oh, hey. need something or just saying hi?",
                "yo."
            ]

            responses_during_night = [
                 "Hey! Finally, it's dark! The moon looks so sick tonight, you should go check it out!",
                 "What's up! Perfect night to just hang out and stare at the sky. So glad you're here!",
                 "Yooo! The night is here and I'm ready to go! What are you up to?",
            ]

            fin_res_greet = responses_during_day if time[0] else responses_during_night
            await message.channel.send(random.choice(fin_res_greet))
    
    else:
        # CATCH-ALL: Natural conversation about any topic
        print(f"💬 General conversation: {content}")
        async with message.channel.typing():
            # Enhanced prompt for natural conversation
            conversation_type = "general_conversation"
            ai_response = await generate_ai_response(content, message.author.display_name, conversation_type, time)
        
        if ai_response:
            await message.channel.send(ai_response)
        else:
            # Fallback for general conversation
            fallback_responses_day = [
                "hmm, interesting. tell me more when the moon's out though.",
                "yeah, cool. i'm kinda sleepy right now tbh.",
                "that's nice. anything else or can i go back to waiting for nighttime?"
            ]
            fallback_responses_night = [
                "Ooh, that's fascinating! Tell me more!",
                "Wow, I love talking about random stuff like this! What else is on your mind?",
                "That's so cool! You know what else is cool? The moon! But seriously, keep going..."
            ]
            fallback_responses = fallback_responses_day if time[0] else fallback_responses_night
            await message.channel.send(random.choice(fallback_responses))

    if random.random() < 0.01: # random.random() returns a float between 0.0 and 1.0
        random_reactions = ["🤔", "😂", "👍", "👀"]
        await message.add_reaction(random.choice(random_reactions))
    
    # Process commands (important for hybrid commands like !sync)
    await bot.process_commands(message)

@tasks.loop(hours = 1)
async def spontaneous_message_during_night():
    await bot.wait_until_ready()

    now = dt.datetime.now()
    current_hour = now.hour
    is_night_time = current_hour < 18 or current_hour >= 6

    quotes = [
        "Ugh, boring.. where's everybody?",
        "Wanna hear a cool fact?",
        "The moon is so beautiful tonight.."
    ]

    all_channels = list(bot.get_all_channels())
    text_channels = [ch for ch in all_channels if isinstance(ch, discord.TextChannel)]
    
    if is_night_time:
        if text_channels:
            channel = random.choice(text_channels)
            try:
                await channel.send(random.choice(quotes))
            except Exception as err:
                print(f"Failed to send message to {channel.name}: {err}")

@tasks.loop(hours = 1)
async def spontaneous_message_during_busy():
    await bot.wait_until_ready()

    now = dt.datetime.now()
    current_hour = now.hour
    is_night_time = current_hour < 18 or current_hour >= 6
    is_busy = not is_night_time

    quotes = [
        "When will it be night-time? I wanna see the moon :(",
        "I miss the moon..",
        f"it's only {abs(18-current_hour)} hours left before the moon rises, I'm excited, are you guys?"
    ]

    all_channels = list(bot.get_all_channels())
    text_channels = [ch for ch in all_channels if isinstance(ch, discord.TextChannel)]
    
    if is_busy:
        if text_channels:
            channel = random.choice(text_channels)
            try:
                await channel.send(random.choice(quotes))
            except Exception as err:
                print(f"Failed to send message to {channel.name}: {err}")


@bot.tree.command(name="spacefact", description="Get an interesting fact about space/moon!")
async def spacefact(interaction: discord.Interaction):
    time_info = check_time()
    
    await interaction.response.send_message(f"Let me search through my garden of wisdom..")  # Shows "Luna is thinking..."
    
    try:
        response = await get_space_fact_response(interaction.user.display_name, time_info)
        await interaction.edit_original_response(content = response)
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
        time_info = check_time()
        
        # Respond immediately to avoid timeout
        await interaction.response.send_message(f"🔮 Consulting the stars for {selected_zodiac.capitalize()}... 🌙", ephemeral=True)
        
        try:
            response = await generate_ai_response(
                f"Acting as Luna, provide a short horoscope for {selected_zodiac}. Keep it mystical and moon-related, under 40 words.", 
                interaction.user.display_name, 
                "horoscope", 
                time_info
            )
            
            # Check if AI response is None or empty
            if response and response.strip():
                await interaction.edit_original_response(content=f"🌟 **{selected_zodiac.capitalize()} Horoscope** 🌙\n\n{response}")
            else:
                # Fallback horoscope responses when AI fails
                fallback_horoscopes = {
                    "aries": "🔥 The moon's fire ignites your passion today. Bold moves await under the celestial glow! ♈",
                    "taurus": "🌱 Luna's gentle light nurtures your stability. Ground yourself in moonbeams and prosper! ♉", 
                    "gemini": "💫 The twin stars dance with Luna tonight. Communication flows like moonlight on water! ♊",
                    "cancer": "🌙 Your lunar ruler shines brightest! Emotions run deep as the cosmic tides today. ♋",
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



bot.run(os.getenv('DISCORD_TOKEN'))