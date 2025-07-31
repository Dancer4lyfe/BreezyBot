import discord
from discord.ext import commands
import random
import os
import time
from keep_alive import keep_alive
import google.generativeai as genai
from collections import defaultdict

# ========== 🔐 API Key Setup ==========
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ========== 💬 Gemini Model ==========
model = genai.GenerativeModel("gemini-pro")

# ========== 📡 Discord Bot Setup ==========
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ========== 🎯 Greeting Responses ==========
responses = [
    "Hey there! 👋",
    "What’s up?",
    "Hope you're doing awesome!",
    "Hello, legend 😄",
    "Nice to see you!",
    "Yo! What’s good? 😎",
]

# ========== 🚫 Rate Limiting Setup ==========
last_greet_time = defaultdict(float)
greet_cooldown = 10  # seconds

# ========== ✅ Bot Online ==========
@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

# ========== 💬 On Message Event ==========
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Greet only if not rate-limited
    now = time.time()
    user_id = message.author.id
    if any(word in message.content.lower() for word in ["hello", "hi", "hey"]):
        if now - last_greet_time[user_id] > greet_cooldown:
            last_greet_time[user_id] = now
            await message.channel.send(random.choice(responses))

    await bot.process_commands(message)

# ========== 💡 Chat Command with Gemini ==========
@bot.command()
async def chat(ctx, *, message):
    # Only respond if bot is mentioned
    if bot.user.mentioned_in(ctx.message):
        try:
            response = model.generate_content(message)
            await ctx.send(response.text)

        except Exception as e:
            if "429" in str(e):
                await ctx.send("⚠️ Whoa! BreezyBot is being rate limited. Try again soon.")
            else:
                await ctx.send("😅 Something went wrong.")
            print(f"❌ Error in chat command: {e}")
    else:
        await ctx.send("👋 Mention me if you want to chat! (e.g. `@BreezyBot !chat Tell me a joke`)")

# ========== 🌐 Keep-alive and Run Bot ==========
keep_alive()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
