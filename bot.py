import discord
import sys
import traceback

from discord.ext import commands
from config import *


class Bot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        self.ready = False
        super().__init__(command_prefix=prefix, description='Test Bot', *args, **kwargs)

        for extension in extensions:
            try:
                self.load_extension(extension)
            except Exception:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

    async def on_error(self, event_method, *args, **kwargs):
        error = traceback.format_exc().replace('```', '"""')
        await self.get_user(148460858438057985).send(f'```{error[-1950:]}```')  # yuerino
        print(error)

    async def on_ready(self):
        print(f'Logged on as {self.user}! (ID: {self.user.id})')
        await self.change_presence(activity=discord.Game(f'| 🍤 {prefix} help'))
        self.ready = True

    async def on_message(self, message):
        if message.author.bot:
            return
        await self.process_commands(message)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'This command requires arguments!: {error.param.name}')
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown for you! Please try again after {error.retry_after:.0f}s')
        else:
            print(error)
