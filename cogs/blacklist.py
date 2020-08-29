import discord
from discord.ext import commands
import time
from copy import deepcopy

from lib import SessionTimeout
from utils import UserConverterSafe, checks
from constants.db_schema import GUILD_CONFIG, PLAYER_DATA


class Blacklist(commands.Cog, name='Staff'):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @checks.is_sbs_admin()
    async def blacklist(self, ctx):
        """
        Command for staff to blacklist.
        """
        await ctx.send_help(ctx.command)

    @blacklist.group(invoke_without_command=True)
    @checks.is_sbs_admin()
    async def guild(self, ctx):
        """
        Command for staff to blacklist a guild.
        """
        await ctx.send_help(ctx.command)

    @guild.command(name='add')
    @checks.is_sbs_admin()
    async def guild_add(self, ctx, guild_id):
        """
        Command to add a guild to global blacklist.
        """
        guilds_db = self.bot.db['guilds']
        if not guild_id.isdigit():
            return await ctx.send(f'{ctx.author.mention}\nEnter guild ID only.')

        if int(guild_id) == 652148034448261150:
            return await ctx.send('https://tenor.com/view/nick-young-what-huh-wait-what-wtf-gif-4793800')

        guild_config = await guilds_db.find_one({'_id': int(guild_id)})
        if guild_config is None:
            guild = self.bot.get_guild(int(guild_id))
            if guild is None:
                return await ctx.send(f'{ctx.author.mention}\nI can\'t find this guild.')

            guild_config = deepcopy(GUILD_CONFIG)

            guild_config['_id'] = int(guild_id)
            guild_config['name'] = guild.name if guild is not None else None
            guild_config['icon'] = str(guild.icon_url) if guild is not None else None
            guild_config['banner'] = str(guild.banner_url) if guild is not None else None
            guild_config['global_blacklisted'] = True
            guild_config['last_updated'] = int(time.time())

            confirm = await ctx.prompt(
                message=f'{ctx.author.mention}\nDo you want to blacklist guild: {guild_config["name"]} ({guild_id})?')
            if not confirm:
                raise SessionTimeout from None

            await guilds_db.insert_one(guild_config)
            self.bot.blacklisted_guild_ids.append(int(guild_id))

            return await ctx.send(f'{ctx.author.mention}\nYou blacklisted guild {guild_config["name"]} ({guild_id})')

        if guild_config['global_blacklisted']:
            return await ctx.send(f'{ctx.author.mention}\nThis guild is already blacklisted!')

        confirm = await ctx.prompt(
            message=f'{ctx.author.mention}\nDo you want to blacklist guild: {guild_config["name"]} ({guild_id})?')
        if not confirm:
            raise SessionTimeout from None

        await guilds_db.update_one({'_id': guild_config['_id']}, {'$set': {'global_blacklisted': True}})
        self.bot.blacklisted_guild_ids.append(guild_config['_id'])

        await ctx.send(f'{ctx.author.mention}\nYou blacklisted guild {guild_config["name"]} ({guild_id}).')

    @guild.command(name='remove')
    @checks.is_sbs_admin()
    async def guild_remove(self, ctx, guild_id):
        """
        Command to remove a guild from global blacklist.
        """
        guilds_db = self.bot.db['guilds']
        if not guild_id.isdigit():
            return await ctx.send(f'{ctx.author.mention}\nEnter guild ID only.')

        if int(guild_id) == 652148034448261150:
            return await ctx.send('https://tenor.com/view/nick-young-what-huh-wait-what-wtf-gif-4793800')

        guild_config = await guilds_db.find_one({'_id': int(guild_id)})
        if guild_config is None:
            return await ctx.send(f'{ctx.author.mention}\nI can\'t find this guild in database.\n'
                                  f'But by default guild not in database shouldn\'t be blacklisted.')

        if not guild_config['global_blacklisted']:
            return await ctx.send(f'{ctx.author.mention}\nThis guild is not blacklisted!')

        confirm = await ctx.prompt(
            message=f'{ctx.author.mention}\nDo you want to remove this guild: {guild_config["name"]} ({guild_id}) from blacklist?')
        if not confirm:
            raise SessionTimeout from None

        await guilds_db.update_one({'_id': guild_config['_id']}, {'$set': {'global_blacklisted': False}})
        self.bot.blacklisted_guild_ids.remove(guild_config['_id'])

        await ctx.send(f'{ctx.author.mention}\nYou removed guild {guild_config["name"]} ({guild_id}) from blacklist.')

    @blacklist.group(invoke_without_command=True)
    @checks.is_sbs_admin()
    async def user(self, ctx):
        """
        Command for staff to blacklist a user.
        """
        await ctx.send_help(ctx.command)

    @user.command(name='add')
    @checks.is_sbs_admin()
    async def user_add(self, ctx, discord_user: UserConverterSafe):
        """
        Command to add a user to global blacklist.
        """
        players_db = self.bot.db['players']

        if not isinstance(discord_user, discord.User):
            discord_user = await self.bot.fetch_user(discord_user)
            if discord_user is None:
                return await ctx.send(f'{ctx.author.mention}\nI can\'t find this user.')

        player_data = await players_db.find_one({'discord_ids': discord_user.id})
        if player_data is None:
            if await self.bot.is_owner(discord_user):
                return await ctx.send('https://tenor.com/view/nick-young-what-huh-wait-what-wtf-gif-4793800')

            player_data = deepcopy(PLAYER_DATA)

            player_data['discord_ids'].append(discord_user.id)
            player_data['global_blacklisted'] = False

            confirm = await ctx.prompt(
                message=f'{ctx.author.mention}\nDo you want to blacklist this user: {discord_user.name} ({discord_user.id})?')
            if not confirm:
                raise SessionTimeout from None

            await players_db.insert_one(player_data)
            self.bot.blacklisted_discord_ids.append(discord_user.id)

            return await ctx.send(
                f'{ctx.author.mention}\nYou blacklisted user {discord_user.name} ({discord_user.id}).')

        for discord_id in player_data['discord_ids']:
            discord_user = self.bot.get_user(discord_id)
            if discord_user is not None and await self.bot.is_owner(discord_user):
                return await ctx.send('https://tenor.com/view/nick-young-what-huh-wait-what-wtf-gif-4793800')

        if player_data['global_blacklisted']:
            return await ctx.send(f'{ctx.author.mention}\nThis user is already blacklisted.')

        confirm = await ctx.prompt(
            message=f'{ctx.author.mention}\nDo you want to blacklist this user: {discord_user.name} ({discord_user.id})?')
        if not confirm:
            raise SessionTimeout from None

        await players_db.update_one({'_id': player_data['_id']}, {'$set': {'global_blacklisted': True}})
        for discord_id in player_data['discord_ids']:
            self.bot.blacklisted_discord_ids.append(discord_id)

        await ctx.send(f'{ctx.author.mention}\nYou blacklisted user {discord_user.name} ({discord_user.id}).')

    @user.command(name='remove')
    @checks.is_sbs_admin()
    async def user_remove(self, ctx, discord_user: UserConverterSafe):
        """
        Command to add a user to global blacklist.
        """
        players_db = self.bot.db['players']
        if not isinstance(discord_user, discord.User):
            discord_user = await self.bot.fetch_user(discord_user)
            if discord_user is None:
                return await ctx.send(f'{ctx.author.mention}\nI can\'t find this user.')

        player_data = await players_db.find_one({'discord_ids': discord_user.id})
        if player_data is None:
            return await ctx.send(f'{ctx.author.mention}\nI can\'t find this user in database.\n'
                                  f'But by default user not in database shouldn\'t be blacklisted.')

        for discord_id in player_data['discord_ids']:
            discord_user = self.bot.get_user(discord_id)
            if discord_user is not None and await self.bot.is_owner(discord_user):
                return await ctx.send('https://tenor.com/view/nick-young-what-huh-wait-what-wtf-gif-4793800')

        if not player_data['global_blacklisted']:
            return await ctx.send(f'{ctx.author.mention}\nThis user is not blacklisted!')

        confirm = await ctx.prompt(
            message=f'{ctx.author.mention}\nDo you want to remove this user: {discord_user.name} ({discord_user.id}) from blacklist?')
        if not confirm:
            raise SessionTimeout from None

        await players_db.update_one({'_id': player_data['_id']}, {'$set': {'global_blacklisted': False}})
        for discord_id in player_data['discord_ids']:
            self.bot.blacklisted_discord_ids.remove(discord_id)

        await ctx.send(
            f'{ctx.author.mention}\nYou removed user {discord_user.name} ({discord_user.id}) from blacklist.')


def setup(bot):
    bot.add_cog(Blacklist(bot))
