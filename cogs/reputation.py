import discord
from discord.ext import commands


class Reputation(commands.Cog, name='Skyblock'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def rep(self, ctx, player: discord.Member, reason):
        pass


def setup(bot):
    bot.add_cog(Reputation(bot))
