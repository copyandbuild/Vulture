import discord
from discord.ext import commands
from discord.commands import slash_command, Option

class ServerInfo(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @slash_command(description=f'Zeige wie viele Member dein Discord Server hat')
    async def serverinfo(self, ctx: discord.ApplicationContext):
        guild = ctx.guild
        embed = discord.Embed(

            title=f"{self.bot.user.name} - Serverinformationen",
            description=f"Hier sind alle Informationen für den **{guild.name}** Server",
            color=discord.Color.embed_background()
        )
        embed.add_field(name=f"Members", value=f"```yml\n{guild.member_count}\n```", inline=True)

        if guild.premium_subscription_count != 0:
            embed.add_field(name=f"Premium Members", value=f"````yml\n{guild.premium_subscription_count}```\n", inline=True)
            return

        if guild.premium_tier != 0:
            embed.add_field(name=f"Premium tier", value=f"```yml{guild.premium_tier}\n```", inline=True)
            return

        embed.add_field(name="Kanäle", value=f"```yml\n{len(guild.channels)}\n```", inline=True)
        embed.add_field(name="Voice-Kanäle", value=f"```yml\n{len(guild.voice_channels)}\n```", inline=True)
        embed.add_field(name="Rollen", value=f"```yml\n{len(guild.roles)}\n```", inline=True)
        embed.add_field(name="Server-Inhaber", value=f"```yml\n{guild.owner}\n``` ", inline=True)

        embed.set_author(name=ctx.author.global_name, icon_url=ctx.author.avatar.url)

        await ctx.respond(content=f"{ctx.author.mention}", embed=embed, ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(ServerInfo(bot))
