from discord.ext import commands

from lib import SessionTimeout
from utils import Embed, CommandWithCooldown, damage
from constants import MOBS_RELEVANT_ENCHANTS, ENCHANTMENT_BONUS, ENCHANTED_BOOK_5, ENCHANTED_BOOK_6


class DamageCalculator(commands.Cog, name='Damage'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(cls=CommandWithCooldown, cooldown_after_parsing=True)
    @commands.cooldown(1, 10.0, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    async def damage(self, ctx):
        """
        Calculates damage based on hypothetical stat values.
        """
        stats = {'strength': 0, 'crit damage': 0, 'weapon damage': 0, 'combat level': 0}
        questions = {
            'strength': f'{ctx.author.mention}\nHow much **strength** do you want to have?',
            'crit damage': f'{ctx.author.mention}\nHow much **crit damage** do you want to have?',
            'weapon damage': f'{ctx.author.mention}\nHow much **damage** does your weapon have on the tooltip?',
            'combat level': f'{ctx.author.mention}\nWhat is your **combat level**?'
        }

        for stat in stats.keys():
            ans = await self.prompt_for_stat(ctx, questions[stat])
            stats[stat] = ans

        mob = await self.prompt_for_mobs(ctx)

        enchant_levels = await ctx.prompt(
            message=f'{ctx.author.mention}\nDo you want to use **level 5** or **level 6** enchantments?',
            emoji_list=[('5️⃣', ENCHANTED_BOOK_5), ('6️⃣', ENCHANTED_BOOK_6)]
        )

        modifier = stats['combat level'] * 4
        for enchantment in MOBS_RELEVANT_ENCHANTS[mob]:
            perk = ENCHANTMENT_BONUS[enchantment]
            if callable(perk):
                modifier += perk(enchant_levels[enchantment])
            else:
                modifier += perk * enchant_levels[enchantment]

        calculated_dmg = round(damage(
            stats['weapon damage'],
            stats['strength'],
            stats['crit damage'],
            modifier
        ))

        no_crit_dmg = round(damage(
            stats['weapon damage'],
            stats['strength'],
            0,
            modifier
        ))

        await Embed(
            ctx=ctx,
            title=f'Calculated damage'
        ).add_field(
            name='Damage with crit',
            value=f'{calculated_dmg}'
        ).add_field(
            name='Damage without crit',
            value=f'{no_crit_dmg}'
        ).add_field().add_field(
            name='Strength',
            value=f'{stats["strength"]}'
        ).add_field(
            name='Crit damage',
            value=f'{stats["crit damage"]}%'
        ).add_field().add_field(
            name='Weapon damage',
            value=f'{stats["weapon damage"]}'
        ).add_field(
            name='Combat level',
            value=f'{stats["combat level"]}'
        ).add_field().send()

    @staticmethod
    async def prompt_for_mobs(ctx):
        mobs = '\n'.join([mob.capitalize() for mob in MOBS_RELEVANT_ENCHANTS.keys()])
        await Embed(
            ctx=ctx,
            title='Which mob will you be targeting with this setup?'
        ).add_field(
            value=f'{mobs}'
        ).send()

        def check(m):
            if m.author.id == ctx.author.id and m.channel.id == ctx.channel.id:
                if m.clean_content.lower() == 'exit':
                    raise SessionTimeout
                if not m.clean_content.isdigit():
                    return True
            return False

        while True:
            msg = await ctx.bot.wait_for('message', timeout=60.0, check=check)
            if msg.clean_content.lower() in MOBS_RELEVANT_ENCHANTS:
                return msg.clean_content.lower()
            else:
                await ctx.send(f'{ctx.author.mention}\nInvalid mob! Please choose one of the listed mobs.')

    @staticmethod
    async def prompt_for_stat(ctx, message):
        await ctx.send(f'{message}')

        def check(m):
            if m.author.id == ctx.author.id and m.channel.id == ctx.channel.id:
                if m.clean_content.lower() == 'exit':
                    raise SessionTimeout
                if m.clean_content.isdigit():
                    return True
            return False

        while True:
            msg = await ctx.bot.wait_for('message', timeout=60.0, check=check)
            if int(msg.clean_content) in range(0, 10000):
                return int(msg.clean_content)
            else:
                await ctx.send(f'{ctx.author.mention}\nInvalid number! Please choose a number between 0 and 10000')


def setup(bot):
    bot.add_cog(DamageCalculator(bot))
