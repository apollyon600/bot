from discord.ext import commands

from lib import APIDisabledError
from utils import Embed, CommandWithCooldown, ask_for_skyblock_profiles
from constants import TALISMANS


class ViewMissing(commands.Cog, name='Damage'):
    """
    A collection of tools designed to optimize your damage and talismans.
    """

    emoji = '💪'

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command(cls=CommandWithCooldown, cooldown_after_parsing=True)
    @commands.cooldown(1, 10.0, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    async def missing(self, ctx, player: str = '', profile: str = ''):
        """
        Displays a list of player's missing talismans.
        Also displays inactive/unnecessary talismans if player have them.
        """
        player = await ask_for_skyblock_profiles(ctx, player, profile, session=self.bot.http_session,
                                                 hypixel_api_client=self.bot.hypixel_api_client)
        profile = player.profile

        if not profile.enabled_api['inventory']:
            raise APIDisabledError(player.uname, profile.name)

        talismans = TALISMANS.copy()
        for talisman in profile.talismans:
            if talisman.active:
                for regex in TALISMANS.keys():
                    if regex.match(talisman.internal_name):
                        talismans.pop(regex)

        embed = Embed(
            ctx=ctx,
            title=f'{player.uname} | {profile.name.capitalize()}',
            description=f'```This porfile is currently missing '
                        f'{len(talismans)}/{len(TALISMANS)} talisman{"" if len(talismans) == 1 else "s"}!```'
        ).set_thumbnail(
            url=player.get_avatar_url()
        )

        if talismans:
            embed.add_field(
                name='[Roughly sorted by price]',
                value='```' + '\n'.join(talismans.values()) + '```',
                inline=False
            )

        inactive = [talisman for talisman in profile.talismans if not talisman.active]

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
