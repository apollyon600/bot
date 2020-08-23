import itertools
from discord.ext import commands
from discord.ext.commands import CommandError, NoPrivateMessage

from . import Embed, HelpPages


class PaginatedHelpCommand(commands.HelpCommand):
    def __init__(self, *, dm_help=False):
        self.dm_help = dm_help
        super().__init__(command_attrs={
            'help': 'Shows help about the bot or a command/category.'
        })

    # noinspection PyShadowingNames
    async def send_bot_help(self, mapping):
        bot = self.context.bot
        entries = await self.get_all_commands()
        pages = []

        for cog, commands in itertools.groupby(entries, key=self.key):
            commands = sorted(commands, key=lambda c: c.name)
            if len(commands) == 0:
                continue

            actual_cog = bot.get_cog(cog)
            if not actual_cog or not hasattr(actual_cog, 'emoji'):
                continue
            description = actual_cog.description or '\u200b'
            cog_emoji = actual_cog.emoji
            pages.append((cog, description, cog_emoji, commands))

        help_pages = HelpPages(self.context, pages, dm_help=self.dm_help)
        await help_pages.paginate()

    async def send_cog_help(self, cog):
        all_commands = await self.get_all_commands()
        cog_commands = filter(lambda c: c.cog_name == cog.qualified_name, all_commands)
        cog_commands = sorted(cog_commands, key=lambda c: c.name)
        entries = [(cog.qualified_name, cog.description, cog.emoji, cog_commands)]
        help_pages = HelpPages(self.context, entries, dm_help=self.dm_help)

        await help_pages.paginate()

    def common_command_formatting(self, embed, command):
        embed.title = self.get_command_signature(command)
        if command.description:
            embed.description = f'{command.description}\n\n{command.help}'
        else:
            embed.description = command.help or 'No help found...'

    async def send_command_help(self, command):
        embed = Embed(ctx=self.context)
        self.common_command_formatting(embed, command)
        await embed.send()

    async def send_group_help(self, group):
        subcommands = group.commands
        if len(subcommands) == 0:
            return await self.send_command_help(group)

        entries = await self.filter_commands(subcommands, sort=True)
        entries = [(group.qualified_name, group.help, '', entries)]
        pages = HelpPages(self.context, entries, dm_help=self.dm_help)

        await pages.paginate()

    async def get_all_commands(self):
        bot = self.context.bot
        return await self.filter_commands(bot.commands, sort=True, key=self.key)

    def get_destination(self):
        ctx = self.context
        if self.dm_help is True:
            return ctx.author
        else:
            return ctx.channel

    async def send_error_message(self, error):
        destination = self.get_destination()
        ctx = self.context
        await destination.send(f'{ctx.author.mention}, {error}')

    @staticmethod
    def key(c):
        return c.cog_name or '\u200bNo Category'

    # noinspection PyShadowingNames
    async def filter_commands(self, commands, *, sort=False, key=None):
        """
        Modified filter_commands to bypass guild_only() and is_guild_owner() check.
        """

        if sort and key is None:
            key = lambda c: c.name

        iterator = commands if self.show_hidden else filter(lambda c: not c.hidden, commands)

        if not self.verify_checks:
            # if we do not need to verify the checks then we can just
            # run it straight through normally without using await.
            return sorted(iterator, key=key) if sort else list(iterator)

        # if we're here then we need to check every command if it can run
        # noinspection PyShadowingNames
        async def predicate(cmd):
            try:
                return await cmd.can_run(self.context)
            except NoPrivateMessage:
                return True
            except CommandError:
                return False

        ret = []
        for cmd in iterator:
            valid = await predicate(cmd)
            if valid:
                ret.append(cmd)

        if sort:
            ret.sort(key=key)
        return ret
