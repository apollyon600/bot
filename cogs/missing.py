from discord.ext import commands
from constants import general as constants
from utils import args_to_player, Embed, CommandWithCooldown


class Missing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(cls=CommandWithCooldown, cooldown_after_parsing=True)
    @commands.cooldown(1, 10.0, commands.BucketType.user)
    # @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    async def missing(self, ctx, player: str, profile: str = ''):
        user = ctx.author
        channel = ctx.channel

        player = await args_to_player(player, profile)

        talismans = constants.talismans.copy()
        for talisman in player.talismans:
            if talisman.active:
                for regex in constants.talismans.keys():
                    if regex.match(talisman.internal_name):
                        talismans.pop(regex)

        embed = Embed(
            channel,
            user=user,
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
                value='```' + '\n'.join(map(str,
                                            inactive)) + '``````An unnecessary talisman is any talisman is\nduplicated or part of a talisman family```'
            )

        await embed.send()


def setup(bot):
    bot.add_cog(Missing(bot))
