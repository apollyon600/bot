from discord.ext import commands

from utils import Embed, ask_for_guild, CommandWithCooldown
from constants.discord import SKILL_EMOJIS


class ViewGuild(commands.Cog, name='Spy'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(cls=CommandWithCooldown, cooldown_after_parsing=True)
    @commands.cooldown(1, 60.0, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    async def guild(self, ctx, *, guild=''):
        """
        Displays information of a guild.
        """
        guild = await ask_for_guild(ctx, guild, hypixel_api_client=self.bot.hypixel_api_client, load_members=True)

        description = f'```{guild.description}```' if guild.description else ''
        embed = Embed(
            ctx=ctx,
            title=f'{guild.name} | {guild.tag}' if guild.tag else guild.name,
            description=f'{description}```'
                        f'Level > {guild.level}\n'
                        f'Members > {guild.member_amount}\n'
                        f'Online members > {guild.current_online}\n'
                        f'Owner > {guild.owner.player.uname if guild.owner.player else None}\n'
                        f'Created at > {guild.created_at.replace(microsecond=0)}``````'
                        f'Average deaths > {guild.average_deaths:,}\n'
                        f'Average money > {guild.average_money:,.2f}\n'
                        f'Average skills > {guild.average_skills:.2f}\n'
                        f'Average minion slots > {guild.minion_slot} ({guild.unique_minions} average crafted)```'
        )

        for skill, level in guild.skills.items():
            embed.add_field(
                name=f'{SKILL_EMOJIS[skill]}\t{skill.capitalize()}',
                value=f'```diff\n'
                      f'Level > {level}\n'
                      f'XP > {guild.skills_xp.get(skill, 0):,.0f}```'
            )
        # So every skill embed field is same size
        left_over_field = 3 - (len(guild.skills) % 3)
        if left_over_field < 3:
            for i in range(0, left_over_field):
                embed.add_field()

        for slayer, level in guild.slayers.items():
            embed.add_field(
                name=f'{SKILL_EMOJIS[slayer]}\t{slayer.capitalize()}',
                value=f'```diff\n'
                      f'Level > {level}\n'
                      f'XP > {guild.slayers_xp.get(slayer, 0):,.0f}```'
            )

        # embed.set_footer(
        #     text='React to corresponding skill/slayer icon to check the guild leaderboard for that category'
        # )
        await embed.send()


def setup(bot):
    bot.add_cog(ViewGuild(bot))
