import discord
from discord.ext import commands
from discord.commands import slash_command, Option

class Credit(commands.Cog):
    def __int__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description=f'Zeige die Credits')
    async def author(self, ctx: discord.ApplicationContext):
        await ctx.respond("> Der Author vom bot ist [**Larrox**](<https://discord.com/users/1143510845368832111/>).", ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(Credit(bot))
