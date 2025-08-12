import discord
from discord.ext import commands, tasks
import random
import os
import asyncio
import json
from datetime import datetime
from keep_alive import keep_alive  # Your Flask keep-alive server
import feedparser

# Set up intents and bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# ----------- Load Data Files -----------
with open("quotes.json", "r") as f:
    quotes = json.load(f)["quotes"]

with open("songs.json", "r") as f:
    songs = json.load(f)

with open("news.json", "r") as f:
    news_items = json.load(f)["news"]

with open("tour.json", "r") as f:
    tour_dates = json.load(f)["tour_dates"]

# Load or initialize news index
NEWS_INDEX_FILE = "news_index.json"
if os.path.exists(NEWS_INDEX_FILE):
    with open(NEWS_INDEX_FILE, "r") as f:
        news_index = json.load(f).get("index", 0)
else:
    news_index = 0

# Greeting responses
greeting_responses = [
    "Hey there! 👋",
    "What’s up?",
    "Hope you're doing awesome!",
    "Hello, legend 😄",
    "Nice to see you!",
    "Yo! What’s good? 😎",
]

# ----------- Greeting Logic -----------
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Improved greeting detection
    greetings = ["hello", "hi", "hey", "sup"]
    trigger_names = ["chris", "breezy"]

    if any(word in message.content.lower().split() for word in greetings) and any(name in message.content.lower() for name in trigger_names):
        response = random.choice(greeting_responses)
        await message.channel.send(f"{response} {message.author.mention}")

    await bot.process_commands(message)  # Allow commands to still run

# ----------- Commands -----------

@bot.command()
async def sing(ctx, *, song_name: str):
    song_name = song_name.lower()
    if song_name in songs:
        for line in songs[song_name]:
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

    news_index = (news_index + 1) % len(news_items)
    with open(NEWS_INDEX_FILE, "w") as f:
        json.dump({"index": news_index}, f)

@bot.command()
async def tour(ctx):
    today = datetime.now().date()
    upcoming = [t for t in tour_dates if datetime.strptime(t["date"], "%Y-%m-%d").date() >= today]

    if not upcoming:
        await ctx.send(f"Sorry {ctx.author.mention}, there are no upcoming shows right now.")
        return

    # Find the closest date
    next_date = datetime.strptime(upcoming[0]["date"], "%Y-%m-%d").date()
    same_day_events = [t for t in upcoming if datetime.strptime(t["date"], "%Y-%m-%d").date() == next_date]

    # Build response
    response = f"🎤 {ctx.author.mention} here's my next show info:\n"
    for event in same_day_events:
        response += f"📅 {event['date']} {event['time']} - {event['city']} @ {event['venue']} | [More Info]({event['info_url']})\n"

    await ctx.send(response)

# ----------- YouTube Check Task -----------
YOUTUBE_RSS_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCcYrdFJF7i8aPj91Q5Z_7Bw"
last_video_id = None

@tasks.loop(minutes=10)
async def check_youtube():
    global last_video_id
    feed = feedparser.parse(YOUTUBE_RSS_URL)
    if feed.entries:
        latest = feed.entries[0]
        video_id = latest.id
        if video_id != last_video_id:
            last_video_id = video_id
            channel = bot.get_channel(1208949333987168306)
            if channel:
                await channel.send(
                    f"Hey Team Breezy I just dropped a new video on Youtube. Go Check it out!\n{latest.link}"
                )

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    check_youtube.start()

# ----------- Start Bot -----------
keep_alive()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
