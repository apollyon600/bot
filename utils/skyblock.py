from discord.ext import commands

from lib import Player


class PlayerConverter(commands.Converter):
    async def convert(self, ctx, arg):
        api_keys = ctx.bot.config.keys
        return await Player(api_keys, uname=arg)
