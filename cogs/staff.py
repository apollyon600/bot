from discord.ext import commands

from lib import SessionTimeout
from utils import checks, Embed


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


def setup(bot):
    bot.add_cog(Staff(bot))
