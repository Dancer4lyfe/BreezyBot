import discord
from discord.ext import commands
import random
import os
import asyncio
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

@bot.command()
async def sing(ctx, *, song_name: str):
    if song_name.lower() == "holy blindfold":
        chorus_lines = [
            "🎶 Let the sky fall",
            "If I'm lookin' at you, then my lens is a rose",
            "(Lookin' at you, lookin' at you)",
            "(If I'm lookin' at you, then my lens is a rose)",
            "Holy blindfold (Ooh)",
            "When I'm lookin' at you, God rest my soul",
            "Feel like I saw the light",
            "It feel like 🎶"
        ]
        for line in chorus_lines:
            await ctx.send(line)
            await asyncio.sleep(30)  # Wait 30 seconds between lines
    else:
        await ctx.send("😅 I don't know that one yet.")

keep_alive()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))

