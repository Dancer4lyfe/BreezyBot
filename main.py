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
    "Hey how you doing! 👋",
    "Sup",
    "Hope you're day is going good!",
    "Hello 😄",
    "Nice to see you!",
    "Yo! What’s good? 😎",
]

# Quote responses
quotes = [
    " I don't care to make you believe I'm a great person, I'm just gonna be one. – Chris Brown",
    "They can write it, who gone sing it like me -Chris Brown",
    "Like ok don't slack up just because you can smile or look cool in front of the camera, Nah, go hard - Chris Brown",
    "Haters keep on hating, cause somebody's gotta do it. - Chris Brown",
    "I try to stay in my lane, get out the way, don't bother nobody, but I'm not gonna take no nonsense - Chris Brown"
]

# News responses
news_items = [
    "Hey I just dropped my latest video for Holy Blindfold, check it out 🎬 https://youtu.be/X4g30-XY9Ck?si=ykJnPvLyYsjmuOrb"
    "Chris Brown teased a new single dropping later this month!",
    "Breezy just performed at the BET Awards and killed it 🔥",
    "Chris posted behind-the-scenes clips from the 'Residuals' music video.",
    "New Breezy merch just dropped — check his official site!"
]

# Track current news index
news_index = 0

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if any(greet in message.content.lower() for greet in ["hello", "hi", "hey", "sup"]) and \
       any(name in message.content.lower() for name in ["chris", "breezy"]):
        response = random.choice(responses)
        user_mention = message.author.mention
        await message.channel.send(f"{response} {user_mention}")

    await bot.process_commands(message) # Required to allow commands

@bot.command()
async def sing(ctx, *, song_name: str):
    song_name = song_name.lower()

    if song_name == "holy blindfold":
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

    elif song_name == "residuals":
        chorus_lines = [
            "🎶 Did we build it up, build it up",
            "Just to let it wash away?",
            "Tell me, did I lace you up, lace you up",
            "Just to watch you run away?",
            "Please tell me whoooooooooo",
            "Who's gettin' all my love? (Love)",
            "Who's gettin' all my love?",
            "Tell me whoooooooooooooo",
            "Who’s gettin’ all my time?",
            "All of that used to be mine, ohhh",
            "Who did you teach what I taught ya? (Oh)",
            "Better not give him my nickname",
            "I don't like thinkin’ about it",
            "I swear that it's wearin' me down, noooooo",
            "But tell me whoooooooooo",
            "Who's gettin’ all of my?",
            "Who's gettin' all of my residuals?",
            "(Whooooooooo)",
            "Who's gettin' all of my?",
            "Who's gettin' all of my residuals?🎶",
        ]
    elif song_name == "it depends":
        chorus_lines = [
            "🎶 You bad as hell, I'll treat you well, I will",
            "It's good, I can tell, come give me hell, come here",
            "Your fairytale, under your spell, I am",
            "She get Chanel, oh well, it all depends (Oh yeah, baby)",
            "You scream and yell, can't call for help, I'm here (No)",
            "You leaving welts, I feel your nails, for real",
            "I eat you good, you sleepin' good, for real",
            "I freak you well, I freak you well, I will",
            "I'll freak you right I will",
            "I'll freak you right, I will",
            "I'll freak you like no one has ever, ever made you feel",
            "I'll freak you right, I will",
            "I'll freak you right, I will",
            "I'll freak you, freak you like no one has ever made you feel, yeah 🎶"
        ]
    else:
        await ctx.send("😅 I don't know that one yet.")
        return

    for line in chorus_lines:
        await ctx.send(line)
        await asyncio.sleep(3)  # Wait 3 seconds between lines

@bot.command()
async def quote(ctx):
    chosen_quote = random.choice(quotes)
    await ctx.send(f"💬 {chosen_quote}")

@bot.command()
async def news(ctx):
    global news_index
    user_mention = ctx.author.mention
    item = news_items[news_index]
    await ctx.send(f"📰 {user_mention} {item}")

    # Move to next index
    news_index = (news_index + 1) % len(news_items)

keep_alive()
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
