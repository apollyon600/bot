import discord


async def record_usage(ctx):
    filtered_args = list(filter(lambda a: isinstance(str(a), str), ctx.args[2:]))
    print(f'{ctx.author} used {ctx.command} {filtered_args} in '
          f'{"a DM" if isinstance(ctx.channel, discord.DMChannel) else ctx.channel.guild.name} '
          f'at {ctx.message.created_at}')
