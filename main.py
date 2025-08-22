import discord
from discord.ext import commands, tasks
from discord import Embed
import random
import os
import asyncio
import json
from datetime import datetime, timedelta
from keep_alive import keep_alive  # Your Flask keep-alive server

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

with open("on_this_day.json", "r") as f:
    on_this_day_events = json.load(f)

# Load or initialize news index
NEWS_INDEX_FILE = "news_index.json"
if os.path.exists(NEWS_INDEX_FILE):
    with open(NEWS_INDEX_FILE, "r") as f:
        news_index = json.load(f).get("index", 0)
else:
    news_index = 0

# Greeting responses
greeting_responses = [
    "Hey how you doing! 👋",
    "Sup",
    "Hope you're day is going good!",
    "Hello 😄",
    "Nice to see you!",
    "Yo! What’s good? 😎",
]
# ----------- Greeting & Love Logic -----------
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    greetings = ["hello", "hi", "hey", "sup"]
    trigger_names = ["chris", "breezy"]

    # Greeting check
    if any(word in message.content.lower().split() for word in greetings) and any(name in message.content.lower() for name in trigger_names):
        response = random.choice(greeting_responses)
        await message.channel.send(f"{response} {message.author.mention}")
        return  # prevent double response

    # Love check
    love_phrases = ["i love you", "love you", "luv u"]
    love_responses = [
        "❤️ I love you too {user}!",
        "💙 Thanks {user}, I love you too!",
        "🙌 Nothing but love for you {user}!",
        "🔥 Always got love for you {user}!",
        "🎶 Much love, {user}!"
    ]

    if any(phrase in message.content.lower() for phrase in love_phrases) and any(name in message.content.lower() for name in trigger_names):
        response = random.choice(love_responses).format(user=message.author.mention)
        await message.channel.send(response)
        return

    await bot.process_commands(message)


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

    next_date = datetime.strptime(upcoming[0]["date"], "%Y-%m-%d").date()
    same_day_events = [t for t in upcoming if datetime.strptime(t["date"], "%Y-%m-%d").date() == next_date]

    response = f"🎤 {ctx.author.mention} What's up, here's my next show can't wait to see you! info:\n"
    for event in same_day_events:
        response += f"📅 {event['date']} {event['time']} - {event['city']} @ {event['venue']} | [More Info]({event['info_url']})\n"

    await ctx.send(response)

# ----------- On This Day Feature -----------

@bot.command()
async def today(ctx):
    """Manually check today's On This Day events."""
    today_key = datetime.utcnow().strftime("%m-%d")  # use UTC consistently
    if today_key in on_this_day_events:
        for event in on_this_day_events[today_key]:
            if isinstance(event, dict):
                embed = Embed(description=f"📅 {event['text']}", color=0x1DA1F2)
                if "image" in event:
                    embed.set_image(url=event["image"])
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"📅 {event}")
    else:
        await ctx.send(f"🙁 {ctx.author.mention} — Nothing special found for today.")


@tasks.loop(hours=24)
async def daily_on_this_day():
    """Automatically post today's events once a day at 1 PM UTC."""
    channel_id = 1208949333987168306  # your channel ID
    channel = bot.get_channel(channel_id)
    if channel:
        today_key = datetime.utcnow().strftime("%m-%d")
        if today_key in on_this_day_events:
            for event in on_this_day_events[today_key]:
                if isinstance(event, dict):
                    embed = Embed(description=f"📅 {event['text']}", color=0x1DA1F2)
                    if "image" in event:
                        embed.set_image(url=event["image"])
                    await channel.send(embed=embed)
                else:
                    await channel.send(f"📅 {event}")


@daily_on_this_day.before_loop
async def before_daily_on_this_day():
    """Align task to start at exactly 1 PM UTC daily."""
    await bot.wait_until_ready()
    now = datetime.utcnow()
    target = now.replace(hour=13, minute=0, second=0, microsecond=0)  # 13:00 UTC
    if now > target:
        target += timedelta(days=1)
    await asyncio.sleep((target - now).total_seconds())

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    daily_on_this_day.start()

# ----------- Start Bot -----------
keep_alive()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
