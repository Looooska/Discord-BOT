from discord.ext import commands
import discord
import random
import requests 
from bs4 import BeautifulSoup

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = 294853993556082688  # Change to your discord id

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

@bot.command()
async def name(ctx):
    await ctx.send(f"Ton prénom moche est : {ctx.author.name}")

@bot.command()
async def d6(ctx):
    resultat = random.randint(1, 6)
    await ctx.send(f"Ton numéro gagnant est : {resultat}")

@bot.event
async def on_message(message):
    if message.content.lower() == "salut tout le monde" and message.author != bot.user:
        await message.channel.send(f"Salut tout seul, {message.author.mention}!")
    await bot.process_commands(message)

@bot.command()
async def ban(ctx, membre: discord.Member, raison):
    phrases_ban = ["être un boloss, être guez, être de droite"]
    await membre.ban(reason=raison)
    await ctx.send(f"{membre.name} a été banni pour {raison if raison else random.choice(phrases_ban)}")

@bot.command()
async def admin(ctx, membre: discord.Member):
    grade = discord.utils.get(ctx.guild.roles, name="Administrateur")
    if grade is None:
        grade = await ctx.guild.create_role(name="Administrateur", permissions=discord.Permissions.all())
    await membre.add_roles(grade)

@bot.command()
async def poll(ctx, question):
    message_sondage = await ctx.send(f"@here {question}")
    await message_sondage.add_reaction("👍")
    await message_sondage.add_reaction("👎")

@bot.command()
async def xkcd(ctx):
    url = "https://c.xkcd.com/random/comic/"
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")
    url_image_bande_dessinee = soup.find("img", {"title": True})["src"]
    await ctx.send(url_image_bande_dessinee)

token = ""
bot.run(token)  # Starts the bot
