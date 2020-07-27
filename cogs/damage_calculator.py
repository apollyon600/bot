from discord.ext import commands

from utils import Embed
from constants import relavant_enchants, enchantment_effects, cheap_max_book_levels, max_book_levels
from lib import SessionTimeout, damage


class DamageCalculator(commands.Cog, name='Damage'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    async def damage(self, ctx):
        """
        Calculates damage based on hypothetical stat values.
        """
        stats = {'strength': 0, 'crit damage': 0, 'weapon damage': 0, 'combat level': 0}
        questions = {
            'strength': f'{ctx.author.mention}, How much **strength** do you want to have?',
            'crit damage': f'{ctx.author.mention}, How much **crit damage** do you want to have?',
            'weapon damage': f'{ctx.author.mention},, How much **damage** does your weapon have on the tooltip?',
            'combat level': f'{ctx.author.mention}, What is your **combat level**?'
        }

        for stat in stats.keys():
            ans = await self.prompt_for_stat(ctx, questions[stat])
            stats[stat] = ans

        mob = await self.prompt_for_mobs(ctx)

        enchant_levels = await ctx.prompt(
            message=f'{ctx.author.mention}, Do you want to use **level 5** or **level 6** enchantments?',
            emoji_list=[('5️⃣', cheap_max_book_levels), ('6️⃣', max_book_levels)]
        )

        modifier = stats['combat level'] * 4
        for enchantment in relavant_enchants[mob]:
            perk = enchantment_effects[enchantment]
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
            title=f'You should be doing {calculated_dmg} damage with those stats.'
        ).add_field(
            value=f'or **{no_crit_dmg}** without a crit.',
            inline=False
        ).add_field(
            name='Damage formula',
            value='```lua\n(5 + damage + floor(str ÷ 5)) ⋅\n(1 + str ÷ 100) ⋅\n(1 + cd ÷ 100) ⋅\n(1 + enchants bonus ÷ combat bonus)```'
        ).send()

    @staticmethod
    async def prompt_for_mobs(ctx):
        mobs = '\n'.join([k.capitalize() for k in relavant_enchants.keys()])
        await Embed(
            ctx=ctx,
            title='Which mob will you be targeting with this setup?'
        ).add_field(
            value=f'```{mobs}```'
        ).send()

        def check(m):
            if m.clean_content == 'exit':
                raise SessionTimeout
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and not m.clean_content.isdigit()

        while True:
            msg = await ctx.bot.wait_for('message', timeout=60.0, check=check)
            if msg.clean_content in relavant_enchants:
                return msg.clean_content
            else:
                await ctx.send(f'{ctx.author.mention}, Invalid mob! Please choose one of the listed mobs.')

    @staticmethod
    async def prompt_for_stat(ctx, message):
        await ctx.send(f'{message}')

        def check(m):
            if m.clean_content == 'exit':
                raise SessionTimeout
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and m.clean_content.isdigit()

        while True:
            msg = await ctx.bot.wait_for('message', timeout=60.0, check=check)
            if int(msg.clean_content) in range(0, 10000):
                return int(msg.clean_content)
            else:
                await ctx.send(f'{ctx.author.mention}, Invalid number! Please choose a number between 0 and 10000')


def setup(bot):
    bot.add_cog(DamageCalculator(bot))
