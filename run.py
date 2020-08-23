import traceback
import sys
import discord
import os
import asyncio

from bot import Bot
import config

# On Windows, the selector event loop is required for aiodns.
if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

client = Bot(
    command_prefix=config.BOT_PREFIXES,
    description='Skyblock Simplified',
    case_insensitive=True,
    max_messages=None,
    fetch_offline_members=False,
    activity=discord.Game(f'| 🍤 {config.BOT_PREFIXES[-1]} help')
)

for extension in config.COG_EXTENSIONS:
    try:
        client.load_extension(extension)
    except Exception:
        print(f'Failed to load extension {extension}.', file=sys.stderr)
        traceback.print_exc()

client.run(config.DISCORD_TOKEN)
