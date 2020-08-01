from discord.ext import commands

from lib import NotStaff
from config import DEV_IDS, ADMIN_IDS


def is_admin():
    async def pred(ctx):
        if ctx.author.id not in ADMIN_IDS:
            raise NotStaff from None
        return True

    return commands.check(pred)


def is_dev():
    async def pred(ctx):
        if ctx.author.id not in DEV_IDS:
            raise NotStaff from None
        return True

    return commands.check(pred)
