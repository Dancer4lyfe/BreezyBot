import discord
from discord.ext import commands
import random
import os
from keep_alive import keep_alive  # Your Flask keep-alive server

# Set up intents and bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Greeting responses
responses = [
    "Hey there! 👋",
    "What’s up?",
    "Hope you're doing awesome!",
    "Hello, legend 😄",
    "Nice to see you!",
    "Yo! What’s good? 😎",
]

# Holy Blindfold chorus lyrics
holy_blindfold_chorus = (
    "🎶\n"
    "Let the sky fall\n"
    "If I'm lookin' at you, then my lens is a rose\n"
    "(Lookin' at you, lookin' at you)\n"
    "(If I'm lookin' at you, then my lens is a rose)\n"
    "Holy blindfold (Ooh)\n"
    "When I'm lookin' at you, God rest my soul\n"
    "Feel like I saw the light\n"
    "It feel like\n"
    "🎶"
)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    msg_lower = message.content.lower()

    # Respond to greetings
    if any(word in msg_lower for word in ["hello", "hi", "hey"]):
        await message.channel.send(random.choice(responses))

    # Respond to "sing Holy Blindfold"
    if "sing holy blindfold" in msg_lower:
        await message.channel.send(holy_blindfold_chorus)

    await bot.process_commands(message)  # Required to allow commands

keep_alive()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
