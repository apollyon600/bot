import copy
from discord.ext import commands

import constants
from utils import Embed, CommandWithCooldown
from lib import APIDisabledError, Player


class ViewMissing(commands.Cog, name='Damage'):
    """
    A collection of tools designed for hypixel skyblock.
    """

    emoji = '💪'

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    # noinspection PyUnresolvedReferences
    @commands.command(cls=CommandWithCooldown, cooldown_after_parsing=True)
    @commands.cooldown(1, 10.0, commands.BucketType.user)
    # @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    @commands.max_concurrency(100, per=commands.BucketType.default, wait=False)
    async def missing(self, ctx, player: str, profile: str = ''):
        """
        Displays a list of player's missing talismans.
        Also displays inactive/unnecessary talismans if player have them.
        """
        player = await Player(self.config.API_KEY, uname=player, session=ctx.bot.session)

        if not profile:
            await player.set_profile_automatically()
        else:
            await player.set_profile(profile)

        if not player.enabled_api['skills'] or not player.enabled_api['inventory']:
            raise APIDisabledError(player.uname, player.profile_name)

        talismans = copy.deepcopy(constants.TALISMANS)
        for talisman in player.talismans:
            if talisman.active:
                for regex in constants.TALISMANS.keys():
                    if regex.match(talisman.internal_name):
                        talismans.pop(regex)

        embed = Embed(
            ctx=ctx,
            title=f'Player {player.uname} on profile {player.profile_name} is missing {len(talismans)}/{len(constants.TALISMANS)} talisman{"" if len(talismans) == 1 else "s"}!',
        )

        if talismans:
            embed.add_field(
                name='[Roughly sorted by price]',
                value='```' + '\n'.join(talismans.values()) + '```',
                inline=False
            )

        inactive = [talisman for talisman in player.talismans if not talisman.active]

        if inactive:
            embed.add_field(
                name=f'Player also has {len(inactive)} unnecessary talisman{"" if len(inactive) == 1 else "s"}!',
                value='```' + '\n'.join(map(str, inactive)) + '``````An unnecessary talisman is any talisman that is'
                                                              '\nduplicated or part of a talisman family.```'
            )

        embed.set_footer(text='Only counting talismans in your talisman bag or inventory.')

        await embed.send()


def setup(bot):
    bot.add_cog(ViewMissing(bot))
