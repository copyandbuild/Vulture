import discord
from discord.ext import commands
from discord.commands import slash_command, Option

class Clear(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description='Lösche eine bestimmte Anzahl an Nachrichten.')
    @commands.has_permissions(manage_messages=True)
    @discord.guild_only()
    async def clear(self, ctx: discord.ApplicationContext, amount: Option(int, "Die Anzahl der Nachrichten, die du löschen möchtest [0 = Alle]")):
        try:
            if amount == 0:
                await ctx.respond(f"> **Alle** Nachrichten wurden erfolgreich aus dem Kanal gelöscht.", delete_after=3, ephemeral=True)
                await ctx.channel.purge()
                return

            if amount == 1:
                await ctx.respond(f"> Es wurde erfolgreich **{amount}** Nachricht gelöscht.", delete_after=3, ephemeral=True)
                await ctx.channel.purge(limit=1)
                return

            await ctx.respond(f"> Es wurden erfolgreich **{amount}** Nachrichten gelöscht.\nDiese Nachricht wird nach `3` Sekunden gel", delete_after=3, ephemeral=True)
            await ctx.channel.purge(limit=amount)
            return
        except Exception as e:
            await ctx.respond("## Das sollte eigentlich nicht passieren...\nFalls dies erneut auftritt, sagen sie bitte umgehend im Support bescheid!", delete_after=3, ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(Clear(bot))
