import discord
from discord.ext import commands
from discord.commands import Option, SlashCommandGroup
from datetime import timedelta
import re

banreasons = ["Nutzer unter 13 Jahren", "Ban Umgehung", "Drohungen", "Terrorismus", "Nationalismus"]

def reasons(ctx: discord.AutocompleteContext):
    return banreasons

def parse_duration(duration: str) -> timedelta:
    regex = r"(\d+)([smhd])"
    matches = re.findall(regex, duration)
    total_seconds = 0
    for value, unit in matches:
        value = int(value)
        if unit == "s":
            total_seconds += value
        elif unit == "m":
            total_seconds += value * 60
        elif unit == "h":
            total_seconds += value * 3600
        elif unit == "d":
            total_seconds += value * 86400
    return timedelta(seconds=total_seconds)

class Moderation(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    mod = SlashCommandGroup("mod")

    @mod.command(description="› Banne einen Nutzer")
    async def ban(self, ctx, user: Option(discord.Member, description="› Der Nutzer, den du Bannen möchtest"),
                  grund: str = Option(autocomplete=reasons,
                                      description="Grund für den Ban",
                                      default="Kein Grund angegeben")):
        try:
            if ctx.author.guild_permissions.ban_members:
                await user.send(f"> Du wurdest von `{ctx.guild.name}` gebannt! Grund: {grund}")
                await user.ban(reason=grund)
                embed = discord.Embed(
                    title=f"{self.bot.user.name} - {ctx.command.mention}",
                    description=f"{user.display_name}",
                    color=discord.Color.dark_red()
                )
                embed.add_field(name="Ban Grund", value=f"```yml\n{grund}\n```", inline=True)
                embed.add_field(name="Verantwortlicher Moderator", value=f"```yml\n{ctx.author.name}\n```", inline=True)
                await ctx.respond(embed=embed)
            else:
                raise discord.Forbidden("Du hast nicht die Berechtigung, Mitglieder zu bannen.")
        except discord.Forbidden as e:
            embed = discord.Embed(
                title=":warning: NUTZER ZU HOCH oder GLEICHE ROLLE :warning:",
                description="**Info for Devs:\n*" + str(e) + "*",
                color=discord.Color.dark_blue()
            )
            await ctx.respond(embed=embed)

    @mod.command(description="› Entbanne einen Nutzer")
    async def unban(self, ctx,
                    user_id: Option(int, "› Die ID von dem Nutzer den du Entbannen möchtest", required=True),
                    reason: str = "Kein Grund angegeben"):
        try:
            if ctx.author.guild_permissions.ban_members:
                banned_users = await ctx.guild.bans()
                for ban_entry in banned_users:
                    user = ban_entry.user
                    if user.id == user_id:
                        await ctx.guild.unban(user, reason=reason)
                        embed = discord.Embed(
                            title="Larrox - Moderation",
                            description=f"{user.name} wurde entbannt.",
                            color=discord.Color.dark_red()
                        )
                        embed.add_field(name="Verantwortlicher Moderator", value=ctx.author.name, inline=False)
                        await ctx.respond(embed=embed)
                        return
                embed = discord.Embed(
                    title=":x: Fehler beim Entbannen",
                    description="Der angegebene Nutzer ist nicht auf der Bannliste.",
                    color=discord.Color.dark_red()
                )
                await ctx.respond(embed=embed, ephemeral=True, delete_after=3)
        except discord.Forbidden as e:
            embed = discord.Embed(
                title=":warning: FEHLER",
                description="Du hast nicht die Berechtigung, diesen Befehl auszuführen.",
                color=discord.Color.dark_blue()
            )
            await ctx.respond(embed=embed, ephemeral=True, delete_after=3)

    @mod.command(description="› Setze einen Nutzer in den Timeout")
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, user: discord.Member, duration: str, reason: str = None):
        if user is None:
            return await ctx.respond("Bitte gib einen Nutzer an.", ephemeral=True)

        try:
            timeout_duration = parse_duration(duration)
            if timeout_duration.total_seconds() <= 0:
                return await ctx.respond("Die Dauer muss größer als 0 sein.", ephemeral=True)

            await user.timeout_for(duration=timeout_duration, reason=reason)
            if reason != None:
                await user.send(f"Du wurdest für `{duration}` mit dem Grund `{reason}` getimeouted.")
            else:
                await user.send(f"Du wurdest für `{duration}` getimeouted.")

            await ctx.respond(f"{user.mention} wurde für `{duration}` getimeouted. Grund: `{reason}`", ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title="⛔ × Ein fehler ist aufgetreten",
                description=f"```{e}```",
                color=discord.Color.red()
            )
            embed.set_footer(text="Ich habe meinen Entwickler informiert")

            await ctx.respond(embed=embed, ephemeral=True)

    @mod.command(description="› Entferne den Timeout eines Nutzers der im Timeout ist")
    @commands.has_permissions(moderate_members=True)
    async def untimeout(self, ctx, user: discord.Member):
        if user is None:
            return await ctx.respond("Bitte gib einen Nutzer an.", ephemeral=True)
        try:
            await user.remove_timeout()
            await user.send(f"Dein Timeout wurde von `{ctx.author.global_name}` aufgehoben.")
            await ctx.respond(f"Der Timeout von {user.mention} wurde erfolgreich aufgehoben.", ephemeral=True)

        except discord.Forbidden as e:
            await  ctx.respond(f"**Du hast keine Berechtigung {ctx.command.mention} zu nutzen")

        except Exception as e:
            embed = discord.Embed(
                title="⛔ × Ein fehler ist aufgetreten",
                description=f"```{e}```",
                color=discord.Color.red()
            )
            embed.set_footer(text="Ich habe meinen Entwickler informiert")

            await ctx.respond(embed=embed, ephemeral=True)

def setup(bot: discord.Bot):
    bot.add_cog(Moderation(bot))
