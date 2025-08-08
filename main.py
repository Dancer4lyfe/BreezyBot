import discord
from discord.ext import commands, tasks
import random
import os
import asyncio
import json
import feedparser   # <--- NEW
from keep_alive import keep_alive  # Your Flask keep-alive server

# Set up intents and bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# --- CONFIG ---
YOUTUBE_FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id=UCcYrdFJF7hmPXRNaWdrko4w"
NEWS_CHANNEL_ID = 1395983039288315965  #1208949333987168306  # Channel where updates will post
LAST_VIDEO_FILE = "last_video.txt"

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
    check_youtube.start()  # Start YouTube watcher loop

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if any(greet in message.content.lower() for greet in ["hello", "hi", "hey", "sup"]) and any(name in message.content.lower() for name in ["chris", "breezy"]):
        response = random.choice(responses)
        user_mention = message.author.mention
        await message.channel.send(f"{response} {user_mention}")

    await bot.process_commands(message)

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

    news_index = (news_index + 1) % len(news_items)
    with open(NEWS_INDEX_FILE, "w") as f:
        json.dump({"index": news_index}, f)


# --- NEW: YouTube Watcher ---
@tasks.loop(minutes=5)  # check every 5 minutes
async def check_youtube():
    feed = feedparser.parse(YOUTUBE_FEED_URL)
    if not feed.entries:
        return

    latest_video = feed.entries[0]
    video_id = latest_video.yt_videoid
    video_url = latest_video.link

    # Check last posted video
    last_video_id = None
    if os.path.exists(LAST_VIDEO_FILE):
        with open(LAST_VIDEO_FILE, "r") as f:
            last_video_id = f.read().strip()

    # Only post if it's a new video
    if video_id != last_video_id:
        channel = bot.get_channel(NEWS_CHANNEL_ID)
        if channel:
            await channel.send(
                f"@everyone Hey Team Breezy I just dropped a new video on YouTube. Go check it out!\n{video_url}"
            )

        # Save this video ID as the last posted
        with open(LAST_VIDEO_FILE, "w") as f:
            f.write(video_id)

# Immediate startup check
@check_youtube.before_loop
async def before_check_youtube():
    await bot.wait_until_ready()
    await check_youtube()
    print("✅ First YouTube check run — starting 5-minute loop.")

# --- NEW: Manual check command ---
@bot.command(name="checknow")
async def check_now(ctx):
    """Manually trigger a YouTube feed check."""
    await check_youtube()
    await ctx.send("✅ Manual feed check completed.")

# Start loop in on_ready or after all tasks are defined
# check_youtube.start()

keep_alive()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
