from discord.ext import commands


class CommandWithCooldown(commands.Command):
    """
    Modified for owners to bypass cooldown.
    """

    async def prepare(self, ctx):
        try:
            return await super().prepare(ctx)
        except commands.CommandOnCooldown as e:
            if await ctx.bot.is_owner(ctx.author):
                return
            else:
                raise e


class GroupWithCooldown(commands.Group):
    """
    Modified for owners to bypass cooldown.
    """

    async def prepare(self, ctx):
        try:
            return await super().prepare(ctx)
        except commands.CommandOnCooldown as e:
            if await ctx.bot.is_owner(ctx.author):
                return
            else:
                raise e
