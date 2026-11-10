import os
import random
import asyncio
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")  # set this in Railway's variables, never hardcode it

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

MAX_SPAM = 20  # hard cap so one command can't be used to actually flood/DOS a channel

# ---------- lifecycle ----------

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()  # global sync = works in every server, no per-server setup
        print(f"Logged in as {bot.user}. Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Sync failed: {e}")


# ---------- basic commands ----------

@bot.tree.command(name="say", description="Make the bot say something")
@app_commands.describe(message="What should the bot say?")
async def say(interaction: discord.Interaction, message: str):
    await interaction.response.send_message("Sent.", ephemeral=True)
    await interaction.channel.send(message)


@bot.tree.command(name="troll", description="Spam a custom message a number of times")
@app_commands.describe(message="The message to repeat", times=f"How many times (max {MAX_SPAM})")
async def troll(interaction: discord.Interaction, message: str, times: app_commands.Range[int, 1, MAX_SPAM]):
    await interaction.response.send_message(f"Trolling with: {message} x{times}", ephemeral=True)
    for _ in range(times):
        await interaction.channel.send(message)
        await asyncio.sleep(0.5)  # small delay so it doesn't trip Discord's rate limit


@bot.tree.command(name="spamemoji", description="Spam an emoji a number of times")
@app_commands.describe(emoji="Emoji to spam", times=f"How many times (max {MAX_SPAM})")
async def spamemoji(interaction: discord.Interaction, emoji: str, times: app_commands.Range[int, 1, MAX_SPAM]):
    await interaction.response.send_message(f"Spamming {emoji} x{times}", ephemeral=True)
    for _ in range(times):
        await interaction.channel.send(emoji)
        await asyncio.sleep(0.5)


@bot.tree.command(name="roastuser", description="Roast a user (all in good fun)")
@app_commands.describe(user="Who to roast")
async def roastuser(interaction: discord.Interaction, user: discord.Member):
    roasts = [
        f"{user.mention} has the rizz of a dial-up modem.",
        f"{user.mention} is proof that evolution can go in reverse.",
        f"{user.mention} types with more confidence than skill.",
        f"{user.mention} got ratio'd by a bot and didn't even notice.",
        f"{user.mention}'s W/L ratio is mostly L.",
    ]
    await interaction.response.send_message(random.choice(roasts))


@bot.tree.command(name="8ball", description="Ask the magic 8-ball a question")
@app_commands.describe(question="Your question")
async def eight_ball(interaction: discord.Interaction, question: str):
    answers = [
        "Yes.", "No.", "Definitely.", "Ask again later.",
        "Doubtful.", "Absolutely not.", "100%.", "Not a chance.",
    ]
    await interaction.response.send_message(f"🎱 {random.choice(answers)}")


@bot.tree.command(name="coinflip", description="Flip a coin")
async def coinflip(interaction: discord.Interaction):
    await interaction.response.send_message(random.choice(["Heads", "Tails"]))


@bot.tree.command(name="rate", description="Rate something out of 10")
@app_commands.describe(thing="The thing to rate")
async def rate(interaction: discord.Interaction, thing: str):
    await interaction.response.send_message(f"I'd rate {thing} a {random.randint(1,10)}/10.")


@bot.tree.command(name="reverse", description="Reverse a message")
@app_commands.describe(message="Text to reverse")
async def reverse(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(message[::-1])


@bot.tree.command(name="mock", description="MoCk TeXt lIkE tHiS")
@app_commands.describe(message="Text to mock")
async def mock(interaction: discord.Interaction, message: str):
    mocked = "".join(c.upper() if i % 2 else c.lower() for i, c in enumerate(message))
    await interaction.response.send_message(mocked)


@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")


# ---------- more spam commands ----------

@bot.tree.command(name="spamword", description="Spam a word/phrase, each on its own line")
@app_commands.describe(word="Word or phrase to spam", times=f"How many times (max {MAX_SPAM})")
async def spamword(interaction: discord.Interaction, word: str, times: app_commands.Range[int, 1, MAX_SPAM]):
    await interaction.response.send_message(f"Spamming '{word}' x{times}", ephemeral=True)
    for _ in range(times):
        await interaction.channel.send(word)
        await asyncio.sleep(0.5)


@bot.tree.command(name="spamping", description="Ping a user repeatedly with a message")
@app_commands.describe(user="Who to ping", message="Message to send each time", times=f"How many times (max {MAX_SPAM})")
async def spamping(interaction: discord.Interaction, user: discord.Member, message: str, times: app_commands.Range[int, 1, MAX_SPAM]):
    await interaction.response.send_message(f"Pinging {user.mention} x{times}", ephemeral=True)
    for _ in range(times):
        await interaction.channel.send(f"{user.mention} {message}")
        await asyncio.sleep(0.5)


@bot.tree.command(name="spamcaps", description="Spam a message IN ALL CAPS")
@app_commands.describe(message="Message to caps-spam", times=f"How many times (max {MAX_SPAM})")
async def spamcaps(interaction: discord.Interaction, message: str, times: app_commands.Range[int, 1, MAX_SPAM]):
    await interaction.response.send_message("Spamming caps...", ephemeral=True)
    for _ in range(times):
        await interaction.channel.send(message.upper() + "!!!")
        await asyncio.sleep(0.5)


@bot.tree.command(name="spamrandom", description="Spam random troll one-liners")
@app_commands.describe(times=f"How many times (max {MAX_SPAM})")
async def spamrandom(interaction: discord.Interaction, times: app_commands.Range[int, 1, MAX_SPAM]):
    lines = [
        "L + ratio", "skill issue", "cope harder", "bro woke up and chose chaos",
        "this you?", "nobody asked", "imagine", "down bad", "ratio'd",
        "mid take ngl", "certified clown moment", "ok and?", "who asked",
        "big L energy", "yikes",
    ]
    await interaction.response.send_message("Unleashing chaos...", ephemeral=True)
    for _ in range(times):
        await interaction.channel.send(random.choice(lines))
        await asyncio.sleep(0.5)


@bot.tree.command(name="spamembed", description="Spam a fake 'announcement' embed")
@app_commands.describe(title="Embed title", message="Embed message", times=f"How many times (max {MAX_SPAM})")
async def spamembed(interaction: discord.Interaction, title: str, message: str, times: app_commands.Range[int, 1, MAX_SPAM]):
    await interaction.response.send_message("Spamming embeds...", ephemeral=True)
    for _ in range(times):
        embed = discord.Embed(title=title, description=message, color=discord.Color.random())
        await interaction.channel.send(embed=embed)
        await asyncio.sleep(0.5)


@bot.tree.command(name="spamreact", description="React to the last message repeatedly with an emoji")
@app_commands.describe(emoji="Emoji to react with", times=f"How many times (max {MAX_SPAM})")
async def spamreact(interaction: discord.Interaction, emoji: str, times: app_commands.Range[int, 1, MAX_SPAM]):
    await interaction.response.send_message("Reacting...", ephemeral=True)
    history = [m async for m in interaction.channel.history(limit=1)]
    if not history:
        await interaction.followup.send("No message found to react to.", ephemeral=True)
        return
    target = history[0]
    for _ in range(times):
        try:
            await target.add_reaction(emoji)
        except discord.HTTPException:
            break
        await asyncio.sleep(0.5)


# ---------- more troll / fun commands ----------

@bot.tree.command(name="fakeban", description="Fake-ban someone for laughs (does nothing real)")
@app_commands.describe(user="Who to 'ban'")
async def fakeban(interaction: discord.Interaction, user: discord.Member):
    embed = discord.Embed(
        title="Member Banned",
        description=f"{user.mention} has been banned. (jk, this is fake)",
        color=discord.Color.red(),
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="fakekick", description="Fake-kick someone for laughs (does nothing real)")
@app_commands.describe(user="Who to 'kick'")
async def fakekick(interaction: discord.Interaction, user: discord.Member):
    embed = discord.Embed(
        title="Member Kicked",
        description=f"{user.mention} has been kicked. (jk, this is fake)",
        color=discord.Color.orange(),
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="jumpscare", description="Send a jumpscare-style message")
@app_commands.describe(user="Who to jumpscare")
async def jumpscare(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(f"👻 BOO {user.mention}! 👻")


@bot.tree.command(name="copypasta", description="Drop a classic copypasta-style troll message")
async def copypasta(interaction: discord.Interaction):
    text = (
        "Attention, this channel has been visited by the chaos bot. "
        "Nothing bad will happen, but you should probably send a funny gif "
        "just to be safe. This message is 100% a joke."
    )
    await interaction.response.send_message(text)


@bot.tree.command(name="zalgo", description="Turn text into creepy zalgo text")
@app_commands.describe(message="Text to zalgo-fy")
async def zalgo(interaction: discord.Interaction, message: str):
    marks = [chr(c) for c in range(0x300, 0x36F)]
    zalgofied = "".join(c + "".join(random.choice(marks) for _ in range(random.randint(1, 4))) for c in message)
    await interaction.response.send_message(zalgofied)


@bot.tree.command(name="clap", description="Add 👏 claps 👏 between 👏 every 👏 word")
@app_commands.describe(message="Text to clap-ify")
async def clap(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(" 👏 ".join(message.split()))


@bot.tree.command(name="vaporwave", description="Ｃｏｎｖｅｒｔ text to full-width vaporwave text")
@app_commands.describe(message="Text to convert")
async def vaporwave(interaction: discord.Interaction, message: str):
    result = "".join(chr(ord(c) + 0xFEE0) if 0x21 <= ord(c) <= 0x7E else c for c in message)
    await interaction.response.send_message(result)


bot.run(TOKEN)
