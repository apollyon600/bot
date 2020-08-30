from discord.ext import commands

from lib import SessionTimeout
from utils import Embed, checks


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
        enabled_commands = []
        for command in self.bot.walk_commands():
            if command.enabled and command.qualified_name not in ['disable', 'enable']:
                enabled_commands.append(command)

        if not enabled_commands:
            return await ctx.send(f'{ctx.author.mention}\nThere is no enabled commands to disable!')

        embed = Embed(
            ctx=ctx,
            title='Enter a command from the list below to disable!'
        )
        _num = (len(enabled_commands) // 3)
        _left_over = len(enabled_commands) % 3
        _field1 = '\n'.join([command.qualified_name for command in enabled_commands[:_num + _left_over]]) + '\u200b'
        embed.add_field(
            value=f'{_field1}'
        )
        _field2 = '\n'.join([command.qualified_name for command in
                             enabled_commands[_num + _left_over:(_num * 2) + _left_over]]) + '\u200b'
        embed.add_field(
            value=f'{_field2}'
        )
        _field3 = '\n'.join(
            [command.qualified_name for command in enabled_commands[(_num * 2) + _left_over:]]) + '\u200b'
        embed.add_field(
            value=f'{_field3}'
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
                if msg.clean_content.lower() == command.qualified_name:
                    command.enabled = False
                    await ctx.send(f'{ctx.author.mention}\nSuccessfully disable command `{command.qualified_name}`!')
                    _run = False
                    break
            if _run:
                await ctx.send(f'{ctx.author.mention}\nDid you make a typo? Choose a command from the list.')

    @commands.command()
    @checks.is_sbs_admin()
    async def enable(self, ctx):
        """
        Use this to enable a command!
        """
        disabled_commands = []
        for command in self.bot.walk_commands():
            if not command.enabled and command.qualified_name not in ['disable', 'enable']:
                disabled_commands.append(command)

        if not disabled_commands:
            return await ctx.send(f'{ctx.author.mention}\nThere is no disabled commands to enable!')

        embed = Embed(
            ctx=ctx,
            title='Enter a command from the list below to enable!'
        )
        _num = (len(disabled_commands) // 3)
        _left_over = len(disabled_commands) % 3
        _field1 = '\n'.join([command.qualified_name for command in disabled_commands[:_num + _left_over]]) + '\u200b'
        if _field1:
            embed.add_field(
                value=f'{_field1}'
            )
        else:
            embed.add_field()
        _field2 = '\n'.join([command.qualified_name for command in
                             disabled_commands[_num + _left_over:(_num * 2) + _left_over]]) + '\u200b'
        embed.add_field(
            value=f'{_field2}'
        )
        _field3 = '\n'.join(
            [command.qualified_name for command in disabled_commands[(_num * 2) + _left_over:]]) + '\u200b'
        embed.add_field(
            value=f'{_field3}'
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
                if msg.clean_content.lower() == command.qualified_name:
                    command.enabled = True
                    await ctx.send(f'{ctx.author.mention}\nSuccessfully enable command `{command.qualified_name}`!')
                    _run = False
                    break
            if _run:
                await ctx.send(f'{ctx.author.mention}\nDid you make a typo? Choose a command from the list.')

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
