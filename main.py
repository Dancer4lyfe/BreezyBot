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

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if any(word in message.content.lower() for word in ["hello", "hi", "hey"]):
        await message.channel.send(random.choice(responses))

    await bot.process_commands(message)  # Required to allow commands

keep_alive()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
