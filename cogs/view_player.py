from discord.ext import commands

from utils import Embed, ask_for_skyblock_profiles, CommandWithCooldown, format_pet
from constants import SKILL_NAMES, COSMETIC_SKILL_NAMES, SKILL_LEVEL_REQUIREMENT, RUNECRAFTING_LEVEL_REQUIREMENT, \
    SLAYER_LEVEL_REQUIREMENT
from constants.discord import SKILL_EMOJIS


class ViewPlayer(commands.Cog, name='Spy'):
    """
    View stats and leaderboards for both guilds and players.
    """

    emoji = '🕵️‍♂️'

    def __init__(self, bot):
        self.bot = bot

    @commands.command(cls=CommandWithCooldown, cooldown_after_parsing=True)
    @commands.cooldown(1, 10.0, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    async def player(self, ctx, player: str = '', profile: str = ''):
        """
        Displays a player\'s guild, skills, and slayer levels.
        """
        player = await ask_for_skyblock_profiles(ctx, player, profile, session=self.bot.http_session,
                                                 hypixel_api_client=self.bot.hypixel_api_client, auto_set=True,
                                                 get_guild=True)
        profile = player.profile
        guild = player.guild

        api_header = ' '.join(
            f'{key.capitalize()} {"✅" if value else "❌"}' for key, value in profile.enabled_api.items())

        total_xp = 0
        for skill in SKILL_NAMES:
            if skill in COSMETIC_SKILL_NAMES:
                continue
            total_xp += profile.skills_xp.get(skill, 0)

        embed = Embed(
            ctx=ctx,
            title=f'{player.uname} | {profile.name}',
            description=f'```{api_header}```\n'
                        f'```Deaths > {profile.deaths:,}\n'
                        f'Guild > {guild.name if guild else None}\n'
                        f'Money > {profile.bank_balance + profile.purse:,.2f}\n'
                        f'Pet > {format_pet(profile.pet)}```'
        ).add_field(
            name=f'🔰 \tSkills',
            value=f'```diff\n'
                  f'Average > {profile.skill_average:.2f}\n'
                  f'Total XP > {total_xp:,.0f}\n'
                  f'{(profile.skill_average / 50 * 100):.2f}% Maxed```',
            inline=False
        ).add_field(
            name=f'🛠️ \tMinions',
            value=f'```diff\n'
                  f'Slots > {profile.minion_slots}\n'
                  f'Uniques > {profile.unique_minions}```',
            inline=False
        ).set_thumbnail(
            url=player.get_avatar_url()
        )

        for skill, level in profile.skills.items():
            percent_to_max = 100 * min(1, profile.skills_xp.get(skill, 0) / (
                RUNECRAFTING_LEVEL_REQUIREMENT[-1] if skill == 'runecrafting' else SKILL_LEVEL_REQUIREMENT[-1]))
            embed.add_field(
                name=f'{SKILL_EMOJIS[skill]}\t{skill.capitalize()}',
                value=f'```diff\n'
                      f'Level > {level}\n'
                      f'XP > {profile.skills_xp.get(skill, 0):,.0f}\n'
                      f'{percent_to_max:.2f}% Maxed```'
            )
        # So every skill embed field is same size
        left_over_field = 3 - (len(profile.skills) % 3)
        if left_over_field < 3:
            for i in range(0, left_over_field):
                embed.add_field()

        for slayer, level in profile.slayers.items():
            percent_to_max = 100 * min(1, profile.slayers_xp.get(slayer, 0) / SLAYER_LEVEL_REQUIREMENT[slayer][-1])
            embed.add_field(
                name=f'{SKILL_EMOJIS[slayer]}\t{slayer.capitalize()}',
                value=f'```diff\n'
                      f'Level > {level}\n'
                      f'XP > {profile.slayers_xp.get(slayer, 0):,.0f}\n'
                      f'{percent_to_max:.2f}% Maxed```'
            )

        embed.add_field(
            name=f'{SKILL_EMOJIS["dungeons"]}\tDungeon Catacombs',
            value=f'```diff\n'
                  f'Level > {profile.dungeon_skill}```',
            inline=False
        ).set_footer(
            text=f'Player is current {"online" if player.online else "offline"} in game.'
        )

        await embed.send()


def setup(bot):
    bot.add_cog(ViewPlayer(bot))
