import discord
from discord.ext import commands
import random
import os
import asyncio
import json
from keep_alive import keep_alive  # Your Flask keep-alive server

# Set up intents and bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Load greeting responses
responses = [
    "Hey there! 👋",
    "What’s up?",
    "Hope you're doing awesome!",
    "Hello, legend 😄",
    "Nice to see you!",
    "Yo! What’s good? 😎",
]

# Load quotes from JSON
with open("quotes.json", "r") as f:
    quotes = json.load(f)["quotes"]

# Load songs from JSON
with open("songs.json", "r") as f:
    songs = json.load(f)

# Load news from JSON
with open("news.json", "r") as f:
    news_items = json.load(f)["news"]

# Load or initialize news index
NEWS_INDEX_FILE = "news_index.json"
if os.path.exists(NEWS_INDEX_FILE):
    with open(NEWS_INDEX_FILE, "r") as f:
        news_index = json.load(f).get("index", 0)
else:
    news_index = 0

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if any(greet in message.content.lower() for greet in ["hello", "hi", "hey", "sup"]) and any(name in message.content.lower() for name in ["chris", "breezy"]):
        response = random.choice(responses)
        user_mention = message.author.mention
        await message.channel.send(f"{response} {user_mention}")

    await bot.process_commands(message)  # Required to allow commands

@bot.command()
async def sing(ctx, *, song_name: str):
    song_name = song_name.lower()

    if song_name in songs:
        chorus_lines = songs[song_name]
        for line in chorus_lines:
            await ctx.send(line)
            await asyncio.sleep(3)
    else:
        await ctx.send("😅 I don't know that one yet.")

@bot.command()
async def quote(ctx):
    chosen_quote = random.choice(quotes)
    await ctx.send(f"💬 {chosen_quote}")

@bot.command()
async def news(ctx):
    global news_index
    item = news_items[news_index]
    await ctx.send(f"📰 {item}")

    # Move to next index
    news_index = (news_index + 1) % len(news_items)

    # Save updated index to file
    with open(NEWS_INDEX_FILE, "w") as f:
        json.dump({"index": news_index}, f)

keep_alive()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
