from discord.ext import commands
import discord

from utils import Embed, checks


class CheckUser(commands.Cog, name='Staff'):
    def __init__(self, bot):
        self.bot = bot
        self.players_db = bot.db['players']

    @commands.group(invoke_without_command=True)
    @checks.is_sbs_admin()
    async def check(self, ctx):
        """
        Command to check a user information.
        """
        await ctx.send_help(ctx.command)

    @check.command(name='discord')
    @checks.is_sbs_admin()
    async def discord_id(self, ctx, discord_user: discord.User = ''):
        """
        Command to check a player by discord id.
        """
        if not discord_user:
            discord_user = ctx.author

        player_data = await self.players_db.find_one({'discord_ids': discord_user.id})
        if player_data is None:
            return await ctx.send(f'{ctx.author.mention}\nThis user has never verified.')

        discord_usernames = ''
        for discord_id in player_data['discord_ids']:
            discord_usernames += f'{self.bot.get_user(discord_id)} ({discord_id})'

        mojang_usernames = ''
        for mojang_uuid in player_data['mojang_uuids']:
            mojang_usernames += f'({mojang_uuid})'

        await Embed(
            ctx=ctx,
            title=f'{discord_user.name} Information'
        ).add_field(
            name='Verified Discord Account',
            value=f'{discord_usernames if discord_usernames else None}'
        ).add_field(
            name='Verified Mojang Account',
            value=f'{mojang_usernames if mojang_usernames else None}'
        ).add_field().send()

    # @check.command(name='mojang')
    # @checks.is_sbs_admin()
    # async def mojang_name(self, ctx, mojang_name):
    #     """
    #     Command to check a player by mojang name.
    #     """
    #     player_data = await self.players_db.find_one({'mojang_uuids.mojang_usernames.mojang_username': mojang_name})
    #     if player_data is None:
    #         return await ctx.send(f'{ctx.author.mention}\nThis user has never verified.')
    #
    #     discord_usernames = ''
    #     for discord_id in player_data['discord_ids']:
    #         discord_usernames += f'{self.bot.get_user(discord_id)} ({discord_id})'
    #
    #     mojang_usernames = ''
    #     for mojang_uuid in player_data['mojang_uuids']:
    #         mojang_usernames += f'({mojang_uuid})'
    #
    #     await Embed(
    #         ctx=ctx,
    #         title=f'{mojang_name} Information'
    #     ).add_field(
    #         name='Verified Discord Account',
    #         value=f'{discord_usernames if discord_usernames else None}'
    #     ).add_field(
    #         name='Verified Mojang Account',
    #         value=f'{mojang_usernames if mojang_usernames else None}'
    #     ).add_field().send()


def setup(bot):
    bot.add_cog(CheckUser(bot))
