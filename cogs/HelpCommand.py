import discord
from discord.ext import commands
from discord.commands import slash_command, Option

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description=f'Liste alle Commands von Vulture auf')
    @commands.has_permissions(administrator=True)
    @discord.guild_only()
    async def help(self, ctx: discord.ApplicationContext):

        helpembed = discord.Embed(
            title=f"{self.bot.user.name} - Helpmenu",
            description=f"Hier siehst du alle Commands von {self.bot.user.mention}",
            color=discord.Color.embed_background()
        )
        helpembed.add_field(name="</clear:1258819288119119982>", value="Lösche eine Bestimmte anzahl an Chat-Nachrichten", inline=False)

        await ctx.respond(content=f"{ctx.author.mention}", embed=helpembed, ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))
