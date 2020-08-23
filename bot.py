import sys
import traceback
import discord
import aiohttp
import socket
import motor.motor_asyncio
from typing import Optional
from discord.ext import commands

from lib import HypixelAPIClient
from utils import Context
import config


class Bot(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        if "connector" in kwargs:
            print(
                "If login() is called (or the bot is started), the connector will be overwritten with an internal one")

        super().__init__(*args, **kwargs)

        self.config = config
        self.http_session: Optional[aiohttp.ClientSession] = None
        self.hypixel_api_client = HypixelAPIClient(config.API_KEY, self.loop, timeout=aiohttp.ClientTimeout(total=30))
        self.mongo_client = motor.motor_asyncio.AsyncIOMotorClient(config.DATABASE_URI)
        self.db = self.mongo_client.sbs

        self.verified_discord_ids = []
        self.blacklisted_discord_ids = []
        self.blacklisted_guild_ids = []

        self._connector = None
        self._resolver = None

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)
        if ctx.message.content == (f'<@!{self.user.id}>', self.user.mention) and len(ctx.message.content.split()) == 1:
            await ctx.send_help()  # Send help if bot get ping
        else:
            await self.invoke(ctx)

    async def on_message(self, message):
        # ignore bots or if bot isnt ready
        if message.author.bot or not self.is_ready():
            return

        # ignore blacklisted discord id
        if message.author.id in self.blacklisted_discord_ids:
            return

        # ignore blacklisted guild
        if message.guild is not None and message.guild.id in self.blacklisted_guild_ids:
            return

        await self.process_commands(message)

    async def on_error(self, event_method, *args, **kwargs):
        type_, value_, traceback_ = sys.exc_info()
        if isinstance(value_, discord.errors.Forbidden):
            # in case it raised from on_command_error
            return
        error = traceback.format_exc().replace('```', '"""')
        for maintainer_id in config.MAINTAINER_IDS.split(','):
            await self.get_user(maintainer_id).send(f'```{error[-1950:]}```')
        print(error)

    def add_cog(self, cog: commands.Cog):
        super().add_cog(cog)
        print(f"Cog loaded: {type(cog).__name__} ({cog.qualified_name}).")

    def clear(self):
        """
        Clears the internal state of the bot and recreates the connector and sessions.
        Will cause a DeprecationWarning if called outside a coroutine.
        """
        self._recreate()
        super().clear()

    async def close(self):
        """
        Close the Discord connection, the http session, connector, resolver and hypixel api client.
        """
        await super().close()

        await self.hypixel_api_client.close()

        if self._connector:
            await self._connector.close()

        if self._resolver:
            await self._resolver.close()

        if self.http_session:
            await self.http_session.close()

    async def login(self, *args, **kwargs):
        """
        Re-create the connector and set up sessions before logging into Discord.
        """
        self._recreate()
        await self._cache()
        await super().login(*args, **kwargs)

    # noinspection PyProtectedMember
    def _recreate(self):
        """
        Re-create the connector, aiohttp session and the APIClient.
        """
        # Use asyncio for DNS resolution instead of threads so threads aren't spammed.
        self._resolver = aiohttp.AsyncResolver()

        if self._connector and not self._connector._closed:
            print("The previous connector was not closed; it will remain open and be overwritten")
        if self.http_session and not self.http_session.closed:
            print('The previous http session was not closed, it will remain open and be overwritten')

        self._connector = aiohttp.TCPConnector(
            resolver=self._resolver,
            family=socket.AF_INET,
        )
        self.http.connector = self._connector

        self.http_session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30), connector=self._connector,
                                                  raise_for_status=True)
        self.hypixel_api_client.recreate(force=True, connector=self._connector)

    async def _cache(self):
        """
        Cache stuff from db
        """
        async for player in self.db['players'].find():
            for discord_id in player['discord_ids']:
                if player['global_blacklisted']:
                    # Cache blacklisted discord ids
                    self.blacklisted_discord_ids.append(discord_id['discord_id'])
                else:
                    # Cache verified discord ids
                    self.verified_discord_ids.append(discord_id['discord_id'])

        # Cache blacklisted guild ids
        async for guild in self.db['guilds'].find({'global_blacklisted': True}):
            self.blacklisted_guild_ids.append(guild['_id'])
