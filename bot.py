import sys
import traceback
import discord
import aiohttp

from discord.ext import commands
from utils import Context
import config


class Bot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        self.config = config
        super().__init__(command_prefix=self.config.prefix, description='Skyblock Simplified',
                         owner_ids=self.config.owner_ids, *args, **kwargs)
        self.session = aiohttp.ClientSession(loop=self.loop, timeout=aiohttp.ClientTimeout(total=3),
                                             raise_for_status=True)
        for extension in self.config.extensions:
            try:
                self.load_extension(extension)
            except Exception:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

    async def process_commands(self, message):
        if message.author.bot:
            return

        ctx = await self.get_context(message, cls=Context)
        await self.invoke(ctx)

    async def on_message(self, message):
        if message.author.bot or not self.is_ready():
            return
        await self.process_commands(message)

    async def on_error(self, event_method, *args, **kwargs):
        type_, value_, traceback_ = sys.exc_info()
        if isinstance(value_, discord.errors.Forbidden):
            # in case it raised from on_command_error
            return
        error = traceback.format_exc().replace('```', '"""')
        for id in self.config.dev_ids:
            await self.get_user(id).send(f'```{error[-1950:]}```')
        print(error)

    def add_cog(self, cog: commands.Cog):
        super().add_cog(cog)
        print(f"Cog loaded: {type(cog).__name__} ({cog.qualified_name}).")
