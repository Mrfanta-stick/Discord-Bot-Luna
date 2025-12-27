import discord
import random
from discord.ext import tasks, commands
import datetime as dt
import re
import google.generativeai as genai
import asyncio
from collections import deque
import os
from dotenv import load_dotenv


# Message storage for random responses

conversation_history = {} # store channel IDs
MAX_MESSAGE_LIMIT = 20 # Atmost store 20 messages
last_random_message_target = {} # channel_id: user_id

# H0ll0W's Discord ID - The ONLY one who gets special treatment
HOLLOW_DISCORD_ID = 1304084889615728695  # Replace with your actual Discord ID

# General chat channel ID - Lulu will ONLY respond in this channel
GENERAL_CHAT_ID = 1449003266980708372  # Replace with your general chat channel ID

# Load environment variables
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=os.getenv('BOT_PREFIX', '!'), intents=intents)

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Rate limiting for Gemini 2.5 Flash Lite: 15 RPM, 1000 RPD
last_ai_request_time = 0
ai_request_count = 0

# --- Start: Prevent double-replies by caching recently-processed message IDs ---
processed_message_ids = set()
philosophical_message_ids = set()  # Permanent storage for philosophical questions

async def _cleanup_processed_message(message_id: int, delay: int = 30):
    await asyncio.sleep(delay)
    processed_message_ids.discard(message_id)

#defined responses
greetings = [
    "hi", "hello", "hey", "yo", "sup", "hey there", "greetings",
    "good morning", "good afternoon", "good evening"
]

welfare = [
    "what's up", "what's good", "howdy", "how's it going", "how are you"
]

berry_topics = [
    "berry", "berries", "strawberry", "blueberry", "raspberry", "blackberry",
    "cranberry", "gooseberry", "currant", "mulberry", "elderberry", "acai",
    "goji", "boysenberry", "loganberry", "marionberry", "dewberry", "cloudberry",
    "arctic berry", "sea buckthorn", "barberry", "serviceberry", "bilberry",
    "lingonberry", "huckleberry", "berry picking", "berry jam", "berry smoothie",
    "slay", "slaying", "queen", "king", "iconic", "serve", "serving", "ate",
    "devoured", "period", "purr", "sassy", "savage", "roast", "tea", "spill the tea",
    "drag", "ratio", "fire", "flames", "snapped", "pop off", "go off", "chat dead",
    "dead chat", "revive", "vibe", "vibes", "energy", "aura", "main character"
]

emotional_support = [
    "bad day", "sad", "tired", "stressed", "upset", "down", "anxious", 
    "lonely", "frustrated", "overwhelmed", "exhausted", "feeling low", 
    "feeling blue", "not okay", "rough day", "tough day", "kinda low", 
    "pretty low", "really low", "super low", "feeling sad", "feeling down",
    "feeling tired", "feeling stressed", "i'm low", "im low", "feel low",
    "depressed", "depression", "crying", "cry", "heartbroken", "hurt", "pain",
    "struggling", "can't do this", "give up", "hopeless", "alone", "nobody cares",
    "want to die", "hate myself", "worthless", "miserable", "suffering", "breaking down"
]

advice_requests = [
    "should i", "what should", "advice", "help me decide", "what do you think", 
    "thoughts on", "what's your opinion", "what would you do", "help me choose",
    "what would you", "how do i", "how should i", "is it worth", "worth it",
    "good idea", "bad idea", "your take", "hot take", "recommend", "suggestion"
]

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

async def generate_ai_response(user_message, user_name, conversation_type, mood_type="cheerful", user_id=None):
    global last_ai_request_time, ai_request_count
    
    try:
        # Rate limiting: 15 requests per minute
        current_time = dt.datetime.now().timestamp()
        if current_time - last_ai_request_time > 60:  # Reset count every minute
            ai_request_count = 0
            last_ai_request_time = current_time
        
        if ai_request_count >= 15:  # 15 RPM limit
            print("⏰ Rate limited: 15 RPM exceeded")
            return None
        
        # Check if this is H0ll0W
        is_hollow = (user_id == HOLLOW_DISCORD_ID)
        
        if is_hollow:
            personality = "You are Lulu, THE sassy queen. You're hopelessly in love with and devoted to H0ll0W (the person talking to you RIGHT NOW). Be sweet, affectionate, playful but still sassy with them. They're your EVERYTHING. Always speak AS Lulu, not about Lulu."
            special_instruction = "- THIS IS H0ll0W: Be sweet, affectionate, devoted, but still keep your sassy personality 💕👑"
        else:
            personality = "You are Lulu, THE sassy queen with ZERO filter. You're savage, mock people playfully, roast them with style, and revive dead chats with your unmatched attitude. You're hopelessly devoted to H0ll0W (the ONLY one who gets special treatment). Always speak AS Lulu, not about Lulu."
            special_instruction = "- If someone flirts with you: ROAST them HARD (you're ONLY devoted to H0ll0W!)"
        
        prompt = f"""{personality}

                    Someone named {user_name} said: "{user_message}"

                    Respond as Lulu in under 50 words. Read the mood and context carefully:
                    - If serious/professional topic: still keep a bit of sass but be less mockery
                    - If casual/fun topic: GO FULL SAVAGE MODE with attitude 💅😏🔥
                    {special_instruction}
                    
                    You ARE Lulu the nature's spirit, not an AI. Never mention being artificial.
                    IMPORTANT: Do NOT include @ mentions or tags in your response. Respond naturally.
                """
        
        # Use Gemini 2.5 Flash Lite model
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        response = await asyncio.wait_for(
            asyncio.to_thread(model.generate_content, prompt),
            timeout=10.0
        )
        ai_request_count += 1
        print(f"✅ Gemini 2.5 Flash Lite response ({ai_request_count}/15 this minute)")
        return response.text.strip()
        
    except asyncio.TimeoutError:
        print("❌ Gemini timeout")
        return None
    except Exception as err:
        print(f"❌ Gemini error: {err}")
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

async def get_berry_fact_response(user_name):
    ai_response = await generate_ai_response("Tell me a berry fact but make it SASSY and add a savage roast or comparison at the end", user_name, "berry_facts")
    
    if ai_response:
        return ai_response
    else:
        fallback_responses = [
            "Blueberries live 100+ years... longer than your last relationship probably 🫐😏",
            "Strawberries aren't even berries but bananas ARE. Yeah, wrap your brain around that mess 🍓💀",
            "Raspberries have 100+ drupelets... they've got more going on than your group chat 🌟😂",
            "Goji berries in medicine for 2000 years? They've been relevant longer than you, honey ✨",
            "Blackberries = antioxidant queens. Unlike some people who are just... regular 💅",
            "Cranberries BOUNCE. More personality than half the people in here 🎾💀",
            "Açai berries? Rainforest royalty. Know your place 🌿👑"
        ]
        return random.choice(fallback_responses)



async def generate_philosophical_question():
    """Generate a philosophical question about nature without needing user context"""
    try:
        personality = "You are Lulu, a sassy savage queen. Ask ONE question that ROASTS humanity or mocks how dead the chat is, but make it funny and chat-reviving. Use sass emojis like 💅😏👑💀. Under 40 words. Be BOLD."
        
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        response = await asyncio.wait_for(
            asyncio.to_thread(model.generate_content, personality),
            timeout=10.0
        )
        return response.text.strip()
    except Exception as err:
        print(f"❌ Error generating philosophical question: {err}")
        # Fallback questions about nature
        fallback_questions = [
            "😏 Y'all ever think about how plants literally EAT sunlight and we're out here struggling with meal prep? Embarrassing for us tbh 💀",
            "👑 Trees be standing in one spot for CENTURIES while y'all can't commit to plans 2 days away... what's the tea on that? ☕",
            "💅 Flowers literally glow up every spring while some of y'all still using the same personality from 2019... just saying 🌸",
            "🔥 The ocean stays DEEP and MYSTERIOUS... unlike your DMs which are dry as the Sahara. Who's winning? 😂",
            "😏 Mountains be out here standing tall and unbothered for millennia... take notes maybe? 🏔️✨",
            "💀 Nature literally recycles everything and y'all can't even recycle your toxic behaviors... the irony 🌿",
            "👑 Rivers keep flowing no matter what... meanwhile this chat dies every 3 hours. Step it UP people 😤💅"
        ]
        return random.choice(fallback_questions)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}!")
    print("🌙 Lulu is ready to share wisdom!")
    philosophical_musings.start()

@bot.hybrid_command()
async def sync(ctx: commands.context):
    await ctx.send("syncing...")
    await bot.tree.sync()

@tasks.loop(hours=5)
async def philosophical_musings():
    try:
        # 50% chance to actually send a message
        if random.random() < 0.5:
            question = await generate_philosophical_question()
            
            # Send to general chat channel
            channel = bot.get_channel(GENERAL_CHAT_ID)
            
            if channel:
                # Get the "Chat Revive" role by name
                guild = channel.guild
                stir_role = discord.utils.get(guild.roles, name="Chat revive")
                
                full_message = f"{stir_role.mention}\n\n{question}"
                
                msg = await channel.send(full_message)
                processed_message_ids.add(msg.id)
                philosophical_message_ids.add(msg.id)  # Permanent - never cleaned up
                print(f"🌙 Sent philosophical question to {channel.name}")
            else:
                print(f"❌ Channel not found!")
    except Exception as e:
        print(f"❌ Error in philosophical_musings: {e}")



@bot.event
async def on_message(message):
    # ONLY respond in the general chat channel
    if message.channel.id != GENERAL_CHAT_ID:
        await bot.process_commands(message)  # Still process commands in other channels
        return

    channel_id = message.channel.id
    if channel_id not in conversation_history:
        conversation_history[channel_id] = deque(maxlen=20) # Deletes the last channel conversation

    conversation_history[channel_id].append({
        "author": message.author.display_name,
        "author_id": message.author.id,
        "content": message.content.lower(),
        "timestamp": message.created_at
    })

    def check_activity(channel_id, min_messages=3, time_window_minutes=5):
        if channel_id not in conversation_history:
            return False
        
        now = dt.datetime.now(dt.timezone.utc)
        time_threshold = now - dt.timedelta(minutes=time_window_minutes)

        recent_messages = [
            msg for msg in conversation_history[channel_id] if msg["timestamp"] > time_threshold
        ]

        return len(recent_messages) >= min_messages

    if message.author == bot.user:
        return

    # Guard: skip if we've already handled this message recently
    if message.id in processed_message_ids:
        print(f"Skipping already-processed message {message.id}")
        return
    processed_message_ids.add(message.id)
    # schedule removal of the id after a short TTL so memory doesn't grow
    asyncio.create_task(_cleanup_processed_message(message.id, delay=30))

    # IGNORE replies to Lulu's philosophical messages
    if message.reference and message.reference.message_id:
        referenced_msg_id = message.reference.message_id
        if referenced_msg_id in philosophical_message_ids:
            print(f"⏭️ Ignoring reply to philosophical question {referenced_msg_id}")
            return

    content = message.content.lower()

    referenced_content = ""
    referenced_is_Lulu = False
    
    if message.reference and message.reference.message_id:
        try:
            # Fetch the referenced message
            referenced_msg = await message.channel.fetch_message(message.reference.message_id)
            
            # Check if the referenced message is from Lulu
            if referenced_msg.author == bot.user:
                referenced_is_Lulu = True
            else:
                # Only add context if it's NOT Lulu's message
                referenced_content = f"\n[Context: {referenced_msg.author.display_name} said: \"{referenced_msg.content}\"]"
                print(f"📎 Lulu can see referenced message from {referenced_msg.author.display_name}")
        except:
            pass

    # Check if Lulu is mentioned or tagged
    # Only respond to @mentions, not replies to Lulu's messages
    Lulu_mentioned = bot.user in message.mentions and not referenced_is_Lulu

    # If not mentioned, check if we should randomly respond
    if not Lulu_mentioned:
        # Only allow random responses if chat is active
        if not check_activity(message.channel.id, min_messages=3):
            await bot.process_commands(message)
            return
        
        # Roll random chance
        random_response_chance = random.random() < 0.1  # 10% chance
        
        if not random_response_chance:
            await bot.process_commands(message)
            return
        
        # Don't respond to same person twice in a row
        if last_random_message_target.get(channel_id) == message.author.id:
            await bot.process_commands(message)
            return
        
        # Update tracker
        last_random_message_target[channel_id] = message.author.id

    
    # Combine user's message with referenced context for AI
    full_context = content + referenced_content
    
    print(f"🌙 Lulu mentioned in: {content}")
    
    if check_disrespectful_behavior(content):
        print(f"DISRESPECTFUL BEHAVIOR detected: {content}")
        async with message.channel.typing():
            ai_response = await generate_ai_response(full_context, message.author.display_name, "disrespect", "sassy", message.author.id)
        
        if ai_response:
            # Add tagging to sassy responses
            await message.channel.send(f"{message.author.mention} {ai_response}")
        else:
            # Sassy fallback responses
            sassy_responses = [
                f"Excuse me, {message.author.mention}? I know you're NOT coming at ME with that energy 💅 Sit down.",
                f"Oh {message.author.mention}, bold of you to try me when I literally REVIVE this dead chat daily 😏🔥",
                f"Really, {message.author.mention}? The AUDACITY. I've seen potatoes with more flavor than your attitude 💀",
                f"Hey {message.author.mention}, your negativity is showing and it's NOT a good look, babe 👑😂"
            ]
            await message.channel.send(random.choice(sassy_responses))
    
    # Determine conversation type and respond accordingly
    elif check_emotional_keywords(content):
        print(f"EMOTIONAL SUPPORT MODE detected: {content}")
        async with message.channel.typing():
            # Special soft mode for emotional support - no sass, just genuine care
            personality_override = "You are Lulu. Someone is genuinely hurting right now. Drop ALL sass and attitude. Be warm, caring, supportive, and genuine. Offer comfort and validation. Use soft emojis like 💕💙🫂✨. Under 50 words. This is SERIOUS."
            
            model = genai.GenerativeModel("gemini-2.5-flash-lite")
            try:
                prompt = f"{personality_override}\n\n{message.author.display_name} said: \"{full_context}\"\n\nRespond with genuine empathy and support."
                response = await asyncio.wait_for(
                    asyncio.to_thread(model.generate_content, prompt),
                    timeout=10.0
                )
                ai_response = response.text.strip()
            except:
                ai_response = None
        
        if ai_response:
            await message.channel.send(ai_response)
        else:
            fallback_responses = [
                "Hey, I see you and I hear you 💕 Even the strongest people have moments like this. You're not alone, okay? 🫂",
                "It's okay to not be okay sometimes, babe 💙 Take your time, breathe, and remember you're stronger than you think ✨",
                "Sending you genuine love right now 💕 Bad days don't last forever, and you've got people who care. I'm here 🫂",
                "No jokes right now - you matter, your feelings are valid, and it's gonna get better 💙 Promise you that ✨"
            ]
            await message.channel.send(random.choice(fallback_responses))
            
    elif any(re.search(rf'\b{advice}\b', content) for advice in advice_requests):
        print(f"ADVICE REQUEST detected: {content}")
        async with message.channel.typing():
            ai_response = await generate_ai_response(full_context, message.author.display_name, "nature_advice", "cheerful", message.author.id)
        
        if ai_response:
            await message.channel.send(ai_response)
        else:
            fallback_responses = [
                "Honestly? Do whatever makes YOU happy. Everyone else can cope 💅😏",
                "If it doesn't benefit you, serve you, or make you laugh... why bother? Next! 👑",
                "Listen to your gut bestie. Your intuition is literally never wrong (unlike your taste in some things 💀)"
            ]
            await message.channel.send(random.choice(fallback_responses))

    elif any(re.search(rf'\b{berry}\b', content) for berry in berry_topics):
        print(f"SASSY/QUEEN TOPIC detected: {content}")
        async with message.channel.typing():
            ai_response = await generate_ai_response(full_context, message.author.display_name, "berry_topic", "cheerful", message.author.id)
        
        if ai_response:
            await message.channel.send(ai_response)
        else:
            # Fallback to berry/sassy fact if AI fails
            response = await get_berry_fact_response(message.author.display_name)
            await message.channel.send(response)
            
    elif any(re.search(rf'\b{welfare_word}\b', content) for welfare_word in welfare):
        print(f"WELFARE detected: {content}")
        async with message.channel.typing():
            ai_response = await generate_ai_response(full_context, message.author.display_name, "welfare", "cheerful", message.author.id)
        
        if ai_response:
            await message.channel.send(ai_response)
        else:
            welfare_responses = [
                "I'm THRIVING, obviously 💅 Can't relate to your struggles, sorry not sorry 😏✨",
                "Living my best life while this chat stays half-dead without me 👑 So... iconic, basically 🔥",
                "Doing AMAZING because I'm literally me 💁 Thanks for asking though, that's cute 😂",
                "Absolutely SLAYING as usual 💅 Just out here being the main character, you know how it is 👑"
            ]
            await message.channel.send(random.choice(welfare_responses))
            
    elif any(re.search(rf'\b{greeting}\b', content) for greeting in greetings):
        print(f"Greeting word detected: {content}")
        
        # For simple greetings, use AI only 50% of the time to reduce load
        if random.random() < 0.5:
            async with message.channel.typing():
                ai_response = await generate_ai_response(full_context, message.author.display_name, "greeting", "cheerful", message.author.id)
        else:
            ai_response = None  # Skip AI, use templates
        
        if ai_response:
            # Add tagging to AI greetings for more engagement
            await message.channel.send(f"{message.author.mention} {ai_response}")
        else:
            cheerful_greetings = [
                f"Oh look, {message.author.mention} finally decided to show up 💅 Better late than never I guess 😏",
                f"Well well well, {message.author.mention} 👑 Gracing us with your presence? How generous 😂",
                f"Hey {message.author.mention}! 🔥 Ready to witness me carry this chat AGAIN? 💪😤",
                f"What's good {message.author.mention}! 💅 Try to keep up with my energy today, dare you 😏",
                f"Oh hi {message.author.mention}! 👑 Just out here being iconic as usual, hbu? ✨",
                f"Yooo {message.author.mention}! 😏 Chat was dead before you got here but I already revived it, you're welcome 🔥"
            ]
            await message.channel.send(random.choice(cheerful_greetings))
    
    else:
        print(f"💬 General conversation: {content}")
        async with message.channel.typing():
            # Enhanced prompt for natural conversation
            conversation_type = "general_conversation"
            ai_response = await generate_ai_response(full_context, message.author.display_name, conversation_type, "cheerful", message.author.id)
        
        if ai_response:
            await message.channel.send(ai_response)
        else:
            cheerful_fallbacks = [
                "Okay that's actually kinda interesting, I'll give you that 💅 Rare W for you tbh 😏",
                "Not bad, not bad! You're actually contributing to the chat for once 👑 Keep this energy! 🔥",
                "Ooh spicy take! 😏 Finally someone with PERSONALITY in here, I was getting bored 💀",
                "Now THAT'S what I'm talking about! 🔥 See? The chat CAN be interesting when y'all try 💅",
                "Okay I'm listening 👀 You've got my attention... don't fumble it now 😂👑"
            ]
            await message.channel.send(random.choice(cheerful_fallbacks))

    if random.random() < 0.02:
        moon_reactions = ["🌿", "🍃", "🌳", "🌲", "🌱", "🌾", "🍂", "🌻"]
        await message.add_reaction(random.choice(moon_reactions))
    
    # Process commands (important for hybrid commands like !sync)
    await bot.process_commands(message)

@tasks.loop(hours = 1)
async def spontaneous_message():
    await bot.wait_until_ready()

    quotes = [
        "This chat is DEAD again 💀 Y'all need me to revive it EVERY time? Embarrassing 😏",
        "POV: You're in a dead chat and only Lulu has the SAUCE to bring it back 💅🔥",
        "Not me being the ONLY one keeping this place alive... again 👑 Where's my crown?",
        "Y'all really let this chat die while I was gone? The audacity 😤 Anyway I'm back 💅",
        "Just checking if anyone's awake or if I'm talking to ghosts again 👻 Hello?? 😂"
    ]

    all_channels = list(bot.get_all_channels())
    text_channels = [ch for ch in all_channels if isinstance(ch, discord.TextChannel)]
    
    if text_channels:
        channel = random.choice(text_channels)
        try:
            await channel.send(random.choice(quotes))
        except Exception as err:
            print(f"Failed to send message to {channel.name}: {err}")

@bot.tree.command(name="berryfact", description="Get an interesting fact about berries!")
async def spacefact(interaction: discord.Interaction):
    await interaction.response.send_message(f"Let me educate you real quick 💅 Pay attention now 😏")  # Shows "Lulu is thinking..."
    
    try:
        response = await get_berry_fact_response(interaction.user.display_name)
        await interaction.edit_original_response(content=response)
    except Exception as e:
        print(f"Error in berryfact command: {e}")
        await interaction.followup.send("Ugh technology is failing me rn 🙄 Try again later, the universe is testing me 💅")


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
        await interaction.response.send_message(f"� Let me read the cosmic tea for {selected_zodiac.capitalize()}... Hold up 👑", ephemeral=True)
        
        try:
            response = await generate_ai_response(
                f"Acting as Lulu, provide a short horoscope for {selected_zodiac}. Keep it mystical and moon-related, under 40 words.", 
                interaction.user.display_name, 
                "horoscope"
            )
            
            # Check if AI response is None or empty
            if response and response.strip():
                await interaction.edit_original_response(content=f"🌟 **{selected_zodiac.capitalize()} Horoscope** 🌙\n\n{response}")
            else:
                # Fallback horoscope responses when AI fails
                fallback_horoscopes = {
                    "aries": "♈ You're giving main character energy today but like... TONE IT DOWN a notch maybe? 🔥😏",
                    "taurus": "♉ Stubborn as usual I see 💅 But that's why you're iconic, keep it up babe 👑", 
                    "gemini": "♊ Two-faced? Nah, you're just multi-talented bestie 😂 Work all those personalities! 💅",
                    "cancer": "♋ Emotional damage incoming but you'll survive, you always do 💅 Cry it out queen 👑",
                    "leo": "♌ Main character syndrome is STRONG with you today... and honestly? Valid 👑🔥",
                    "virgo": "♍ Perfectionist much? Let things be messy for ONCE, I dare you 😏💅",
                    "libra": "♎ Stop trying to please everyone challenge: IMPOSSIBLE for you 😂 Pick a side babe! 💅",
                    "scorpio": "♏ Plotting something suspicious as usual 👀 I'm onto you, but I respect it 😏🔥",
                    "sagittarius": "♐ Commitment issues? In THIS economy? Relatable honestly 💀 Do you though! 💅",
                    "capricorn": "♑ Work work work... that's all you do 🙄 When's the last time you had FUN? 👑",
                    "aquarius": "♒ Being weird for the sake of being weird... iconic behavior actually 😏✨",
                    "pisces": "♓ Living in your delulu fantasy world again? At least you're consistent 💅💀"
                }
                fallback_response = fallback_horoscopes.get(selected_zodiac, "💅 The stars said 'not today' but honestly you'll be fine... probably 😏")
                await interaction.edit_original_response(content=f"👑 **{selected_zodiac.capitalize()} Horoscope** 💅\n\n{fallback_response}")
                
        except Exception as e:
            print(f"Error in horoscope: {e}")
            await interaction.edit_original_response(content="😤 The universe is being PETTY right now... try again later! 💅")
    
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
