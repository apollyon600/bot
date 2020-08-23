from discord.ext import commands
from copy import deepcopy
import time

from lib import SessionTimeout
from utils import Embed, checks
from constants.db_schema import GUILD_CONFIG


class Staff(commands.Cog):
    """
    A collection of tools for the sbs staff to manage the bot.
    """

    emoji = '⚠️'

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.hypixel_api_client = bot.hypixel_api_client

    # TODO: adding logs and reason for enable/disable command
    @commands.command()
    @checks.is_sbs_admin()
    async def disable(self, ctx):
        """
        Use this to disable a command!
        """
        all_commands = self.bot.commands
        enabled_commands = [command for command in all_commands if
                            command.enabled and command.name not in ['disable', 'enable']]
        if not enabled_commands:
            return await ctx.send(f'{ctx.author.mention}, There is no enabled commands to disable!')

        embed = Embed(
            ctx=ctx,
            title='Enter a command from the list below to disable!'
        )
        for command in enabled_commands:
            embed.add_field(
                value=f'```> {command.name}```'
            )
        await embed.send()

        def check(m):
            if m.author.id == ctx.author.id and m.channel.id == ctx.channel.id:
                if m.clean_content.lower() == 'exit':
                    raise SessionTimeout
                if not m.clean_content.isdigit():
                    return True
            return False

        _run = True
        while _run:
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            for command in enabled_commands:
                if msg.clean_content.lower() == command.name:
                    command.enabled = False
                    await ctx.send(f'{ctx.author.mention}, Successfully disable command `{command.name}`!')
                    _run = False
                    break
            if _run:
                await ctx.send(f'{ctx.author.mention}, Did you make a typo? Choose a command from the list.')

    @commands.command()
    @checks.is_sbs_admin()
    async def enable(self, ctx):
        """
        Use this to enable a command!
        """
        all_commands = self.bot.commands
        disabled_commands = [command for command in all_commands if
                             not command.enabled and command.name not in ['disable', 'enable']]
        if not disabled_commands:
            return await ctx.send(f'{ctx.author.mention}, There is no disabled commands to enable!')

        embed = Embed(
            ctx=ctx,
            title='Enter a command from the list below to enable!'
        )
        for command in disabled_commands:
            embed.add_field(
                value=f'```> {command.name}```'
            )
        await embed.send()

        def check(m):
            if m.author.id == ctx.author.id and m.channel.id == ctx.channel.id:
                if m.clean_content.lower() == 'exit':
                    raise SessionTimeout
                if not m.clean_content.isdigit():
                    return True
            return False

        _run = True
        while _run:
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)
            for command in disabled_commands:
                if msg.clean_content.lower() == command.name:
                    command.enabled = True
                    await ctx.send(f'{ctx.author.mention}, Successfully enable command `{command.name}`!')
                    _run = False
                    break
            if _run:
                await ctx.send(f'{ctx.author.mention}, Did you make a typo? Choose a command from the list.')

    @commands.command()
    @checks.is_sbs_admin()
    async def apikey(self, ctx):
        """
        Use this command to check the current api key status.
        """
        data = await self.hypixel_api_client.get_key_status()
        if not data:
            ctx.send(f'{ctx.author.mention}, Something is wrong!')
        censored_key = '\*' * (len(data['key']) - 3)
        censored_key += data['key'][len(data['key']) - 3:]
        censored_owner = '\*' * (len(data['owner']) - 3)
        censored_owner += data['owner'][len(data['owner']) - 3:]
        await Embed(
            ctx=ctx,
            title='API Key status'
        ).add_field(
            name='Key',
            value=f'{censored_key}',
            inline=False
        ).add_field(
            name='Owner',
            value=f'{censored_owner}',
            inline=False
        ).add_field(
            name='Limit',
            value=f'{data["limit"]}',
            inline=False
        ).add_field(
            name='Queries in past minute',
            value=f'{data["queriesInPastMin"]}',
            inline=False
        ).add_field(
            name='Total queries',
            value=f'{data["totalQueries"]}',
            inline=False
        ).send()

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

    @guild.command()
    @checks.is_sbs_admin()
    async def add(self, ctx, guild_id):
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

            # If bot not in the guild
            if guild is None:
                confirm = await ctx.prompt(
                    message=f'{ctx.author.mention}\nI am not in this guild, do you want to blacklist anyways?')
                if not confirm:
                    raise SessionTimeout from None

            guild_config = deepcopy(GUILD_CONFIG)

            guild_config['_id'] = int(guild_id)
            guild_config['name'] = guild.name if guild is not None else None
            guild_config['icon'] = str(guild.icon_url) if guild is not None else None
            guild_config['banner'] = str(guild.banner_url) if guild is not None else None
            guild_config['global_blacklisted'] = True
            guild_config['last_updated'] = int(time.time())

            confirm = await ctx.prompt(
                message=f'{ctx.author.mention}\nDo you want to blacklist guild: {guild_id}?')
            if not confirm:
                raise SessionTimeout from None

            await guilds_db.insert_one(guild_config)
            self.bot.blacklisted_guild_ids.append(int(guild_id))

            return await ctx.send(f'{ctx.author.mention}\nYou blacklisted guild {guild_id}')

        if guild_config['global_blacklisted']:
            return await ctx.send(f'{ctx.author.mention}\nThis guild is already blacklisted!')

        confirm = await ctx.prompt(
            message=f'{ctx.author.mention}\nDo you want to blacklist guild: {guild_id}?')
        if not confirm:
            raise SessionTimeout from None

        await guilds_db.update_one({'_id': guild_config['_id']}, {'$set': {'global_blacklisted': True}})
        self.bot.blacklisted_guild_ids.append(guild_config['_id'])

        await ctx.send(f'{ctx.author.mention}\nYou blacklisted guild {guild_id}')

    @guild.command()
    @checks.is_sbs_admin()
    async def remove(self, ctx, guild_id):
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
            message=f'{ctx.author.mention}\nDo you want to remove this guild: {guild_id} from blacklist?')
        if not confirm:
            raise SessionTimeout from None

        await guilds_db.update_one({'_id': guild_config['_id']}, {'$set': {'global_blacklisted': False}})
        self.bot.blacklisted_guild_ids.remove(guild_config['_id'])

        await ctx.send(f'{ctx.author.mention}\nYou removed guild {guild_id} from blacklist')


def setup(bot):
    bot.add_cog(Staff(bot))
