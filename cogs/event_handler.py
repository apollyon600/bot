import discord
from discord.ext import commands


class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged on as {self.bot.user}! (ID: {self.bot.user.id})')

    @commands.Cog.listener()
    async def on_command(self, ctx):
        filtered_args = ctx.message.clean_content.split()[2:] or []
        print(f'{ctx.author} used {ctx.command} {filtered_args} in '
              f'{"a DM" if isinstance(ctx.channel, discord.DMChannel) else ctx.channel.guild.name} '
              f'at {ctx.message.created_at}.')


def setup(bot):
    bot.add_cog(EventHandler(bot))
