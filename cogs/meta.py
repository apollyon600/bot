from discord.ext import commands

from utils import Embed, PaginatedHelpCommand


class Meta(commands.Cog, name='Bot'):
    """
    Commands for utilities related to the Bot itself.
    """

    emoji = '🤖'

    def __init__(self, bot):
        self.bot = bot
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
        server_rankings = sorted(self.bot.guilds, key=lambda guild: len(guild.members), reverse=True)[:10]
        server_rankings = f'{"Top Servers".ljust(28)} | Users\n' + '\n'.join(
            [f'{guild.name[:28].ljust(28)} | {len(guild.members)}' for guild in server_rankings])

        embed = Embed(
            ctx=ctx,
            title='Discord Stats',
            description=f'This Command was run on shard {(ctx.guild.shard_id if ctx.guild else 0) + 1} / {self.bot.shard_count}\n```{server_rankings}```'
        ).add_field(
            name='Servers',
            value=f'{self.bot.user.name} is running in {len(self.bot.guilds)} servers with {sum(len(guild.text_channels) for guild in self.bot.guilds)} channels',
            inline=False
        ).add_field(
            name='Users',
            value=f'There are currently {sum(len(guild.members) for guild in self.bot.guilds)} users with access to the bot',
            inline=False
        )

        shards = [[0, 0, 0]] * self.bot.shard_count
        for x in self.bot.guilds:
            shards[x.shard_id][0] += 1
            shards[x.shard_id][1] += len(x.text_channels)
            shards[x.shard_id][2] += len(x.members)

        for x in range(self.bot.shard_count):
            embed.add_field(
                name=f'Shard {x + 1}',
                value=f'{shards[x][0]} servers\n{shards[x][1]} channels\n{shards[x][2]} members',
                inline=True
            )
        embed.add_field(
            name='Latency',
            value=f'This message was delivered in {self.bot.latency * 1000:.0f} milliseconds',
            inline=False
        )
        await embed.send()


def setup(bot):
    bot.add_cog(Meta(bot))
