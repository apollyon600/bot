import discord
from discord.ext import commands

from constants import skyblock as constants
from utils import PlayerConverter, Embed, CommandWithCooldown


class Missing(commands.Cog, name='Combat'):
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
    @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    async def missing(self, ctx, player: PlayerConverter, profile: str = ''):
        """
        Displays a list of player's missing talismans.
        Also displays inactive/unnecessary talismans if player have them.
        """

        user = ctx.author

        if not profile:
            await player.set_profile_automatically()
        else:
            await player.set_profile(player.profiles[profile.capitalize()])

        talismans = constants.talismans.copy()
        for talisman in player.talismans:
            if talisman.active:
                for regex in constants.talismans.keys():
                    if regex.match(talisman.internal_name):
                        talismans.pop(regex)

        embed = Embed(
            ctx=ctx,
            title=f'{user.name}, you are missing {len(talismans)}/{len(constants.talismans)} talisman{"" if len(talismans) == 1 else "s"}!',
            description='Only counting talismans in your bag or inventory'
        )

        if talismans:
            embed.add_field(
                name='[Roughly sorted by price]',
                value='```' + '\n'.join(talismans.values()) + '```',
                inline=False
            )

        inactive = [talisman for talisman in player.talismans if talisman.active is False]

        if inactive:
            embed.add_field(
                name=f'You also have {len(inactive)} unnecessary talismans',
                value='```' + '\n'.join(map(str, inactive)) + '``````An unnecessary talisman is any talismans is'
                                                              '\nduplicated or part of a talisman family```'
            )

        await embed.send()


def setup(bot):
    bot.add_cog(Missing(bot))
