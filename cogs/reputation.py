import discord
from discord.ext import commands


class Reputation(commands.Cog, name='Skyblock'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='+rep')
    @commands.guild_only()
    async def positive_rep(self, ctx, player: discord.Member, reason):
        """
        Give a player a postive reputation.
        """
        pass

    @commands.command(name='-rep')
    @commands.guild_only()
    async def negative_rep(self, ctx, player: discord.Member, reason):
        """
        Give a player a negative reputation.
        """
        pass


def setup(bot):
    bot.add_cog(Reputation(bot))
