import sys
import discord
import traceback

from discord.ext import commands
from utils import record_usage
import config


class Bot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        self.config = config

        super().__init__(command_prefix=self.config.prefix, description='Test Bot', *args, **kwargs)

        for extension in self.config.extensions:
            try:
                self.load_extension(extension)
            except Exception:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

    def add_cog(self, cog: commands.Cog):
        super().add_cog(cog)
        print(f"Cog loaded: {type(cog).__name__} ({cog.qualified_name})")

    # noinspection PyShadowingBuiltins
    async def on_error(self, event_method, *args, **kwargs):
        error = traceback.format_exc().replace('```', '"""')
        for id in self.config.dev_ids:
            await self.get_user(id).send(f'```{error[-1950:]}```')
        print(error)

    async def on_ready(self):
        print(f'Logged on as {self.user}! (ID: {self.user.id})')
        self.before_invoke(record_usage)
        await self.change_presence(activity=discord.Game(f'| 🍤 {self.config.prefix} help'))

    async def on_message(self, message):
        if message.author.bot or not self.is_ready():
            return
        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'This command requires arguments: {error.param.name}')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown for you! Please try again after {error.retry_after:.2f}s')
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send(
                f'{ctx.author.mention}, someone is already using this command in this channel, please try again later or DM me directly!')
        elif isinstance(error, commands.CommandNotFound):
            pass
        else:
            await ctx.send(error)
            print(error)
            ctx.command.reset_cooldown(ctx)
