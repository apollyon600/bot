from discord.ext import commands
from config import admin_ids


class CommandWithCooldown(commands.Command):
    async def prepare(self, ctx):
        try:
            return await super().prepare(ctx)
        except commands.CommandOnCooldown as e:
            if ctx.message.author.id in admin_ids:
                return
            else:
                raise e
