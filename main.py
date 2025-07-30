import discord
from discord.ext import commands
import random
import os
import openai
from keep_alive import keep_alive  # Your Flask keep-alive server

# Load API key
openai.api_key = os.getenv("OPENAI_API_KEY")

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

    await bot.process_commands(message)  # Required to allow commands like !chat

@bot.command()
async def chat(ctx, *, message):
    try:
        async with ctx.channel.typing():  # ✅ This line needs a block under it
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful, witty Discord bot named BreezyBot."},
                    {"role": "user", "content": message}
                ],
                max_tokens=100,
                temperature=0.8,
            )

            reply = response.choices[0].message["content"]
            await ctx.send(reply)

    except Exception as e:
        await ctx.send("😅 Something went wrong.")
        print(e)

keep_alive()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))

