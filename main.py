import urbandictionary as ud
import discord
from discord.ext import commands
from discord import app_commands
import pickle

bot_prefix = "."
intents = discord.Intents.all()
intents.reactions = True

bot = commands.Bot(
    command_prefix=bot_prefix, application_id=1165085737541193809, intents=intents
)
tree = bot.tree


@bot.event
async def on_ready():
    await tree.sync()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you"))
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("------")


############################# PING #############################


@bot.command(aliases=["p"])
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! Latency: {latency}ms")


@tree.command(name="ping", description="Ping command to check bot's latency.")
async def slash_ping(inter):
    latency = round(bot.latency * 1000)
    await inter.response.send_message(f"Pong! Latency: {latency}ms")


########################## URBAN DICT ##########################


def kb(item: str) -> str:
    """kills the stupid urbandict brackets"""
    return item.replace("[", "").replace("]", "")


def find_best(defs, best: bool = True):
    max = (0, None)

    if best:
        for item in defs:
            if item.upvotes > max[0]:
                max = (item.upvotes, item)
    else:
        for item in defs:
            if item.downvotes > max[0]:
                max = (item.upvotes, item)

    return max[1]


# --------------------DEFINE--------------------


@bot.command(aliases=["d", "d1", "db", "def"])
async def define(ctx, args):
    """Basic defition command"""
    defs = ud.define(args)

    word = find_best(defs)

    if word == None:
        embedVar = discord.Embed(
            title=f"No definition found",
            description=f"Here's a random one instead",
            color=0xFF0000,
        )
        await ctx.send(embed=embedVar)
        word = find_best(ud.random())

    embedVar = discord.Embed(
        title=f"**{kb(word.word)}**",
        description=f"{kb(word.definition)}",
        color=0x00FF00,
    )
    embedVar.add_field(name=" ", value=f"```{kb(word.example)}```", inline=False)
    embedVar.set_footer(text=f"{word.upvotes} 👍  |  {word.downvotes} 👎")

    await ctx.send(embed=embedVar)


# ~~~~~~~~~~~~SLASH~~~~~~~~~~~~


@tree.command(
    name="define",
    description="Define a word using the most liked definition in Urban Dictionary",
)
async def define_slash(inter: discord.Interaction, word: str):
    """Basic defition command"""
    defs = ud.define(word)

    word = find_best(defs)

    if word == None:
        embedVar = discord.Embed(
            title=f"No definition found",
            description=f"Here's a random one instead",
            color=0xFF0000,
        )
        await inter.response.send_message(embed=embedVar)
        word = find_best(ud.random())

    embedVar = discord.Embed(
        title=f"**{kb(word.word)}**",
        description=f"{kb(word.definition)}",
        color=0x00FF00,
    )
    embedVar.add_field(name=" ", value=f"```{kb(word.example)}```", inline=False)
    embedVar.set_footer(text=f"{word.upvotes} 👍  |  {word.downvotes} 👎")

    await inter.response.send_message(embed=embedVar)


# --------------------DEFINE WORST--------------------


@bot.command(aliases=["d2", "dw"])
async def define_worst(ctx, args):
    """Basic defition command"""
    defs = ud.define(args)

    word = find_best(defs, False)

    if word == None:
        embedVar = discord.Embed(
            title=f"No definition found",
            description=f"Here's a random one instead",
            color=0xFF0000,
        )
        await ctx.send(embed=embedVar)
        word = find_best(ud.random(), False)

    embedVar = discord.Embed(
        title=f"**{kb(word.word)}**",
        description=f"{kb(word.definition)}",
        color=0x00FF00,
    )
    embedVar.add_field(name=" ", value=f"```{kb(word.example)}```", inline=False)
    embedVar.set_footer(text=f"{word.upvotes} 👍  |  {word.downvotes} 👎")

    await ctx.send(embed=embedVar)


# ~~~~~~~~~~~~SLASH~~~~~~~~~~~~


@tree.command(
    name="define_worst",
    description="Define a word using the most disliked definition in Urban Dictionary",
)
async def define_worst_slash(inter: discord.Interaction, word: str):
    """Basic defition command"""
    defs = ud.define(word)

    word = find_best(defs, False)

    if word == None:
        embedVar = discord.Embed(
            title=f"No definition found",
            description=f"Here's a random one instead",
            color=0xFF0000,
        )
        await inter.response.send_message(embed=embedVar)
        word = find_best(ud.random(), False)

    embedVar = discord.Embed(
        title=f"**{kb(word.word)}**",
        description=f"{kb(word.definition)}",
        color=0x00FF00,
    )
    embedVar.add_field(name=" ", value=f"```{kb(word.example)}```", inline=False)
    embedVar.set_footer(text=f"{word.upvotes} 👍  |  {word.downvotes} 👎")

    await inter.response.send_message(embed=embedVar)

# tokenn = "no"
# with open('token.p', 'wb') as f:
#     pickle.dump(tokenn, f)

with open("token.p", "rb") as tk:
    token = pickle.load(tk)

# Run the bot with your token
bot.run(token)
