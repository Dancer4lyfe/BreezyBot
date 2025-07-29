import discord
import random
import os
from keep_alive import keep_alive  # Make sure keep_alive.py exists

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

responses = [
    "Hey there! 👋",
    "What’s up?",
    "Hope you're doing awesome!",
    "Hello, legend 😄",
    "Nice to see you!",
    "Yo! What’s good? 😎",
]

@client.event
async def on_ready():
    print(f"✅ Bot is online as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if any(word in message.content.lower() for word in ["hello", "hi", "hey"]):
        await message.channel.send(random.choice(responses))

keep_alive()  # Keeps the server alive (for uptime pings)
client.run(os.environ["DISCORD_BOT_TOKEN"])

