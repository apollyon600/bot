from discord.ext import commands

from lib import NotVerified


async def check_guild_permissions(ctx, perms, *, check=all):
    if ctx.guild is None:
        raise commands.NoPrivateMessage

    # Bot owner/dev bypass
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True

    resolved = ctx.author.guild_permissions
    if not check(getattr(resolved, name, None) == value for name, value in perms.items()):
        raise commands.MissingPermissions([perm for perm in perms.keys()])

    return True


async def check_sbs_permissions(ctx, perms, *, check=all):
    # Bot owner/dev bypass
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True

    sbs_guild = ctx.guild
    if sbs_guild is None or sbs_guild.id != 652148034448261150:
        sbs_guild = ctx.bot.get_guild(652148034448261150)

    member = sbs_guild.get_member(ctx.author.id)
    if member is None:
        raise commands.MissingPermissions([perm for perm in perms.keys()])

    resolved = member.guild_permissions
    if not check(getattr(resolved, name, None) == value for name, value in perms.items()):
        raise commands.MissingPermissions([perm for perm in perms.keys()])

    return True


def is_sbs_admin():
    async def pred(ctx):
        return await check_sbs_permissions(ctx, {'administrator': True})

    return commands.check(pred)


def is_sbs_mod():
    async def pred(ctx):
        return await check_sbs_permissions(ctx, {'manage_guild': True})

    return commands.check(pred)


def is_guild_owner():
    async def pred(ctx):
        if ctx.guild is None:
            raise commands.NoPrivateMessage

        # Bot owner/dev bypass
        is_owner = await ctx.bot.is_owner(ctx.author)
        if is_owner:
            return True

        if ctx.author.id != ctx.guild.owner_id:
            raise commands.NotOwner

        return True

    return commands.check(pred)


def is_guild_admin():
    async def pred(ctx):
        return await check_guild_permissions(ctx, {'administrator': True})

    return commands.check(pred)


def is_guild_mod():
    async def pred(ctx):
        return await check_guild_permissions(ctx, {'manage_guild': True})

    return commands.check(pred)


def is_player_verified():
    async def pred(ctx):
        user_data = await ctx.bot.db['players'].find_one({'discord_ids.discord_id': ctx.author.id})
        if user_data is None or not user_data['global_blacklisted'] or not user_data['discord_ids']:
            try:
                # Sbs Admin bypass
                await check_sbs_permissions(ctx, {'administrator': True})
            except commands.MissingPermissions:
                raise NotVerified

        return True

    return commands.check(pred)
