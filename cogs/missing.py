import os

from discord.ext import commands
from constants import general as constants
from lib import Player, Embed

if os.environ.get('API_KEY') is None:
    import dotenv

    dotenv.load_dotenv()

keys = os.getenv('API_KEY')


class Missing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def missing(self, ctx, player, profile):
        user = ctx.author
        channel = ctx.channel

        player = await Player(keys, uname=player)

        # try:
        await player.set_profile(player.profiles[profile.capitalize()])
        # except KeyError:
        #     await channel.send(f'{user.mention} invalid profile!')
        #     return None

        # player = await self.args_to_player(user, channel, *args)

        if not player:
            await channel.send('Invalid player\'s name, if you think it is corrected, DM the devs to report bugs')
            return

        # if player.enabled_api['inventory'] is False:
        #     await self.api_disabled(f'{player.uname}, your inventory API is disabled on {player.profile_name.title()}!',
        #                             channel, user)
        #     return

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

        inactive = [talisman for talisman in player.talismans if
                    talisman.active is False and talisman.internal_name != 'PERSONAL_COMPACTOR_6000']

        if inactive:
            embed.add_field(
                name=f'You also have {len(inactive)} unnecessary talismans',
                value='```' + '\n'.join(map(str,
                                            inactive)) + '``````An unnecessary talisman is any talisman is\nduplicated or part of a talisman family```'
            )

        await embed.send()


def setup(bot):
    bot.add_cog(Missing(bot))
