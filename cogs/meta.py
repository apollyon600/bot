import psutil
from discord.ext import commands

from utils import Embed, PaginatedHelpCommand


class Meta(commands.Cog, name='Bot'):
    """
    Commands for utilities related to the Bot itself.
    """

    emoji = '🤖'

    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()
        self._original_help_command = bot.help_command
        bot.help_command = PaginatedHelpCommand(dm_help=True)
        bot.help_command.cog = self

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

    async def bot_check(self, ctx):
        perms = {
            'embed_links': True,
            'send_messages': True,
            'read_messages': True,
            'add_reactions': True,
            'read_message_history': True
        }
        guild = ctx.guild
        me = guild.me if guild is not None else ctx.bot.user
        permissions = ctx.channel.permissions_for(me)

        missing = [perm for perm, value in perms.items() if getattr(permissions, perm) != value]

        if not missing:
            return True

        raise commands.BotMissingPermissions(missing)

    @commands.command()
    async def stats(self, ctx):
        """
        Displays stats about the bot including number of servers and users.
        """
        server_rankings = sorted(ctx.bot.guilds, key=lambda guild: len(guild.members), reverse=True)[:10]
        server_rankings = f'{"Top Servers".ljust(28)} | Users\n' + '\n'.join(
            [f'{guild.name[:28].ljust(28)} | {len(guild.members)}' for guild in server_rankings])

        embed = Embed(
            ctx=ctx,
            title='Discord Stats',
            description=f'This command was run on shard {(ctx.guild.shard_id if ctx.guild else 0) + 1} / {ctx.bot.shard_count}.\n```{server_rankings}```'
        ).add_field(
            name='Servers',
            value=f'{ctx.bot.user.name} is running in {len(ctx.bot.guilds)} servers with {sum(len(guild.text_channels) for guild in ctx.bot.guilds)} channels.',
            inline=False
        ).add_field(
            name='Users',
            value=f'There are currently {sum(len(guild.members) for guild in ctx.bot.guilds)} users with access to the bot.',
            inline=False
        )

        shards = [[0, 0, 0]] * ctx.bot.shard_count
        for guild in ctx.bot.guilds:
            shards[guild.shard_id][0] += 1
            shards[guild.shard_id][1] += len(guild.text_channels)
            shards[guild.shard_id][2] += len(guild.members)

        for x in range(ctx.bot.shard_count):
            embed.add_field(
                name=f'Shard {x + 1}',
                value=f'{shards[x][0]} servers\n{shards[x][1]} channels\n{shards[x][2]} members',
                inline=True
            )

        memory_usage = self.process.memory_full_info().uss / 1024 ** 2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()
        embed.add_field(
            name='Process',
            value=f'{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU',
            inline=False
        )

        embed.set_footer(text=f'This message was delivered in {ctx.bot.latency * 1000:.0f} milliseconds.')

        await embed.send()

    @commands.command()
    async def invite(self, ctx):
        """
        Want to invite the bot to your server? Use this command to generate an invite link.
        """
        await Embed(
            ctx=ctx,
            title='Here\'s an invite link',
            description='[Click me to invite the bot](https://tinyurl.com/add-sbs)'
        ).send()

    @commands.command()
    async def support(self, ctx):
        """
        Have a question about the bot? Use this command to join the official server to ask.
        """
        await Embed(
            ctx=ctx,
            title='Here\'s a link to my support server',
            description='[https://discord.gg/sbs]'
        ).set_footer(
            text='(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧'
        ).send()


def setup(bot):
    bot.add_cog(Meta(bot))
