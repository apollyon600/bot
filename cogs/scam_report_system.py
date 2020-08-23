import discord
from discord.ext import commands
import time
import re

from utils import CommandWithCooldown, Embed, checks
from constants.db_schema import REPORT


# TODO: add report management command
class ScamReport(commands.Cog, name='Skyblock'):
    def __init__(self, bot):
        self.bot = bot
        self.reports_db = bot.db['scam_reports']

    # TODO: command not done current disabled
    @commands.command(cls=CommandWithCooldown, cooldown_after_parsing=True, enabled=False)
    @commands.cooldown(1, 60.0, commands.BucketType.member)
    @commands.guild_only()
    @checks.is_player_verified()
    async def report(self, ctx, player: discord.Member, proof: str, *, reason: str):
        """
        Report a player.
        """
        imgur_regex = re.compile('https?://imgur.com/(a/)?(\S*)')
        proof_match = imgur_regex.match(proof)
        if proof_match is None:
            return await ctx.send(f'{ctx.author.mention}\nPlease post imgur link or imgur gallery/album link only\n'
                                  f'Example: one image: `sbs report (someone) https://imgur.com/Wb1z8y7 (reason)`\n'
                                  f'Or gallery/album link: `sbs report (someone) https://imgur.com/a/H1AKoI8 (reason)`.')

        report = REPORT.copy()
        report['guild_id'] = ctx.guild.id
        report['reported_discord_id'] = player.id
        report['reported_mojang_uuid'] = None
        report['submitter_discord_id'] = ctx.author.id
        report['submitter_mojang_uuid'] = None
        report['reason'] = reason
        report['proof'] = proof
        report['submitted_timestamp'] = int(time.time())

        confirm_embed = Embed(
            ctx=ctx,
            title='Do you want to report this player?'
        ).add_field(
            name='Reported Discord ID',
            value=f'{report["reported_discord_id"]}'
        ).add_field(
            name='Reported Mojang UUID',
            value=f'{report["reported_mojang_uuid"]}'
        ).add_field().add_field(
            name='Submitter Discord ID',
            value=f'{report["submitter_discord_id"]}'
        ).add_field(
            name='Submitter Mojang UUID',
            value=f'{report["submitter_mojang_uuid"]}'
        ).add_field().add_field(
            name='Reason',
            value=f'{report["reason"]}',
            inline=False
        ).add_field(
            name='Proof',
            value=f'{report["proof"]}',
            inline=False
        )
        confirmed = await ctx.prompt(embed=confirm_embed)
        if not confirmed:
            return await ctx.send(f'{ctx.author.mention}\nReport again if you make a typo!')

        await self.reports_db.insert_one(report)

        await ctx.send(f'{ctx.author.mention}\nYou reported {player.name}!')


def setup(bot):
    bot.add_cog(ScamReport(bot))
