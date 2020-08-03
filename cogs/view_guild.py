from discord.ext import commands

from utils import CommandWithCooldown, GuildPages, ask_for_guild, get_guild_leaderboard


class ViewGuild(commands.Cog, name='Spy'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(cls=CommandWithCooldown, cooldown_after_parsing=True)
    @commands.cooldown(1, 60.0, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    async def guild(self, ctx, *, guild=''):
        """
        Displays information of a guild aswell as leaderboards for all the guild members.
        """
        guild = await ask_for_guild(ctx, guild, hypixel_api_client=self.bot.hypixel_api_client, load_members=True)

        all_leaderboard = get_guild_leaderboard(guild)

        entries = ['first page'] + [leaderboard for leaderboard in all_leaderboard.values()]
        header_entries = ['General guild information'] + \
                         [f'{name.capitalize()} Leaderboard' for name in all_leaderboard.keys()]

        leaderboard_pages = GuildPages(ctx, guild, entries, header_entries)
        await leaderboard_pages.paginate()


def setup(bot):
    bot.add_cog(ViewGuild(bot))
