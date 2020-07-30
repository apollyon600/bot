from discord.ext import commands

from config import ADMIN_IDS


class CommandWithCooldown(commands.Command):
    async def prepare(self, ctx):
        try:
            return await super().prepare(ctx)
        except commands.CommandOnCooldown as e:
            if ctx.message.author.id in ADMIN_IDS:
                return
            else:
                raise e
