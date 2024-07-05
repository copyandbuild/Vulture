import discord
import json
import ezcord

bot = ezcord.Bot(intents=discord.Intents.all(),
                 activity=discord.CustomActivity(
                     name="Vulture | NextGen Discord System", emoji="🚀",

                 ),
                 debug_guilds=[
                     "1258813869091197141"
                 ])

with open('token.json', 'r') as f:
    data = json.load(f)
    TOKEN = data['TOKEN']

bot.load_cogs()
bot.run(TOKEN)