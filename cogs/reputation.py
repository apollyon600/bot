import discord
from discord.ext import commands
import time

from utils import CommandWithCooldown
from constants.db_schema import REPUTATION


class Reputation(commands.Cog, name='Skyblock'):
    def __init__(self, bot):
        self.bot = bot
        self.reps_db = bot.db['reputations']

    @commands.command(name='+rep', cls=CommandWithCooldown, cooldown_after_parsing=True)
    @commands.cooldown(1, 60.0, commands.BucketType.member)
    @commands.guild_only()
    async def positive_rep(self, ctx, player: discord.Member, *, reason: str):
        """
        Give a player a postive reputation.
        """
        rep = REPUTATION.copy()
        rep['guild_id'] = ctx.guild.id
        rep['reported_discord_id'] = player.id
        rep['submitter_discord_id'] = ctx.author.id
        rep['reason'] = reason
        rep['submitted_timestamp'] = int(time.time())

        await self.reps_db.insert_one(rep)

        await ctx.send(f'{ctx.author.mention}\nYou gave {player.name} a positive rep!')

    @commands.command(name='-rep', cls=CommandWithCooldown, cooldown_after_parsing=True)
    @commands.cooldown(1, 60.0, commands.BucketType.member)
    @commands.guild_only()
    async def negative_rep(self, ctx, player: discord.Member, *, reason: str):
        """
        Give a player a negative reputation.
        """
        rep = REPUTATION.copy()
        rep['guild_id'] = ctx.guild.id
        rep['reported_discord_id'] = player.id
        rep['submitter_discord_id'] = ctx.author.id
        rep['reason'] = reason
        rep['positive'] = False
        rep['submitted_timestamp'] = int(time.time())

        await self.reps_db.insert_one(rep)

        await ctx.send(f'{ctx.author.mention}\nYou gave {player.name} a negative rep!')


def setup(bot):
    bot.add_cog(Reputation(bot))
