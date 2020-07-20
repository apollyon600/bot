from discord.ext import commands

from utils import CommandWithCooldown, PlayerConverter, Embed, colorize, format_pet
from constants.bot import optimizers, rarity_colors, pet_emojis, damage_potions, number_emojis, support_items
from constants import relavant_enchants, enchantment_effects
from lib import APIDisabledError, SessionTimeout, damage
from optimizer import damage_optimizer


class Optimizer(commands.Cog, name='Combat'):
    def __init__(self, bot):
        self.bot = bot

    # noinspection PyUnresolvedReferences,PyTypeChecker
    @commands.command(cls=CommandWithCooldown, cooldown_after_parsing=True)
    @commands.cooldown(1, 10.0, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    async def optimizer(self, ctx, player: PlayerConverter, profile: str = ''):
        """
        Optimizes your talismans to their best reforges.
        """
        if not profile:
            await player.set_profile_automatically()
        else:
            await player.set_profile(profile)

        if not player.enabled_api['skills'] or not player.enabled_api['inventory']:
            raise APIDisabledError(player.uname, player.profile_name)

        talisman_counts = {'common': 0, 'uncommon': 0, 'rare': 0, 'epic': 0, 'legendary': 0, 'mythic': 0}
        for tali in player.talismans:
            if tali.active:
                talisman_counts[tali.rarity] += 1

        perfect_crit_chance = await ctx.prompt(embed=Embed(
            ctx=ctx,
            title='What would you like to optimize for?'
        ).add_field(
            value='\n\n'.join(f'> {o["emoji"]}\n`{o["name"]}`' for o in optimizers)
        ), emoji_list=[('💯', True), ('💥', False)])

        include_attack_speed = await ctx.prompt(embed=Embed(
            ctx=ctx,
            title='Do you want to include attack speed?'
        ))

        only_blacksmith = await ctx.prompt(embed=Embed(
            ctx=ctx,
            title='Select Reforge Prices'
        ).add_field(
            value='> 🔨\n`only optimize with reforges`\n`from the blacksmith`\n\n> 🌈\n`include all reforges`'
        ), emoji_list=[('🔨', True), ('🌈', False)])

        if len(player.weapons) == 0:
            return await channel.send(f'{ctx.author.mention}, you have `no weapons` in your inventory')
        elif len(player.weapons) == 1:
            weapon = player.weapons[0]
        else:
            weapon_index = await ctx.prompt_with_list(
                prompt_list=[weapon.name for weapon in player.weapons if weapon.type != 'fishing rod'],
                embed=Embed(
                    ctx=ctx,
                    title='Which weapon would you like to use?'
                ).set_footer(
                    text='You may enter the corresponding weapon number'
                ))
            weapon = player.weapons[int(weapon_index) - 1]
        player.set_weapon(weapon)

        pet = player.pet
        profile_confirm = await ctx.prompt(embed=Embed(
            ctx=ctx,
            title='Is this the correct equipment?'
        ).add_field(
            name='⚔️\tWeapon',
            value=f'```{weapon.name}```',
            inline=False
        ).add_field(
            name=f'{pet_emojis[pet.internal_name] if pet and pet.internal_name in pet_emojis else "🐣"}\tPet',
            value=f'```{format_pet(pet) if pet else None}```',
            inline=False
        ).add_field(
            name='💎\tPet Item',
            value=f'```{pet.item_name if pet else None}```',
            inline=False
        ).add_field(
            name='⛑️\tHelmet',
            value=f'```{player.armor["helmet"]}```',
            inline=False
        ).add_field(
            name='👚\tChestplate',
            value=f'```{player.armor["chestplate"]}```',
            inline=False
        ).add_field(
            name='👖\tLeggings',
            value=f'```{player.armor["leggings"]}```',
            inline=False
        ).add_field(
            name='👞\tBoots',
            value=f'```{player.armor["boots"]}```',
            inline=False
        ).add_field(
            name='🏺\tTalismans',
            value=''.join(
                colorize(f'{amount} {name.capitalize()}', rarity_colors[name])
                for name, amount in talisman_counts.items()
            )
        ))
        if not profile_confirm:
            raise SessionTimeout

        for name, pot in damage_potions.items():
            buff = pot['stats']
            levels = pot['levels']

            if weapon.type != 'bow' and name == 'archery':
                continue

            emoji_list = [(number_emojis[level], level) for level in levels]

            selected_level = await ctx.prompt(
                f'{ctx.author.mention}, What level of `{name} potion` do you want to use?' +
                '{s}'.format(
                    s='\nSelect 0 if you want to choose normal potion instead of dungeon potion' if name == 'dungeon' else ''),
                emoji_list=emoji_list)

            for stat, amount in buff.items():
                player.stats.__iadd__(stat, amount[selected_level])

            if name == 'dungeon' and selected_level > 0:
                break

        for name, orb in support_items.items():
            internal_name = orb['internal']
            buff = orb['stats']

            if internal_name in player.inventory or internal_name in player.echest:
                confirm = await ctx.prompt(f'{ctx.author.mention}, Will you be using your `{name}`?')
                if confirm:
                    for stat, amount in buff.items():
                        player.stats.__iadd__(stat, amount)

        best_route = damage_optimizer(
            player,
            perfect_crit_chance=perfect_crit_chance,
            include_attack_speed=include_attack_speed,
            only_blacksmith_reforges=only_blacksmith
        )

        await self.send_optimizer_result(ctx, player, weapon, best_route)

    @staticmethod
    async def send_optimizer_result(ctx, player, weapon, best_route):
        best_stats = best_route[0] or {}
        best_equip = best_route[1] or {}
        optimized = best_route[0]['is optimized']

        if not best_equip:
            return await ctx.send(f'{ctx.author.mention}, Optimization is not possible!\n'
                                  f'Collect more talismans or raise your combat level before trying again.')

        embed = Embed(
            ctx=ctx,
            title='{s}'.format(s='Successful!' if optimized else 'Unsuccessful!')
        ).set_footer(
            text='Player\'s stats include pots\nPlease double check your stats before and in game before reforge\n'
                 'If it is wrong by a lot please post the result in bugs channel'
        )

        for equipment in best_equip:
            for rarity in best_equip[equipment]:
                text = f''
                for reforge in best_equip[equipment][rarity]:
                    text += f'\n{best_equip[equipment][rarity][reforge]} {reforge.title()}'
                embed.add_field(
                    name=f'**{rarity.title()} {equipment.title()}**',
                    value=text,
                    inline=False
                )

        def emod(activity):
            result = 0
            for enchantment in relavant_enchants[activity]:
                if enchantment in weapon.enchantments:
                    value = enchantment_effects[enchantment]
                    if callable(value):
                        result += value(weapon.enchantments[enchantment])
                    else:
                        result += value * weapon.enchantments[enchantment]
            return result

        base_mod = player.stats['enchantment modifier']
        zealot_mod = emod('zealots') + base_mod
        slayer_mod = emod('slayer bosses') + base_mod

        if weapon.internal_name == 'REAPER_SWORD':
            slayer_mult = 3
        elif weapon.internal_name == 'SCORPION_FOIL':
            slayer_mult = 2.5
        else:
            slayer_mult = 1

        zealot_damage = damage(player.weapon.stats['damage'], player.stats['strength'],
                               player.stats['crit damage'], zealot_mod)
        slayer_damage = damage(player.weapon.stats['damage'], player.stats['strength'],
                               player.stats['crit damage'], slayer_mod)
        slayer_damage *= slayer_mult

        zealot_damage_after = damage(player.weapon.stats['damage'], best_stats['strength'],
                                     best_stats['crit damage'], zealot_mod)
        slayer_damage_after = damage(player.weapon.stats['damage'], best_stats['strength'],
                                     best_stats['crit damage'], slayer_mod)
        slayer_damage_after *= slayer_mult

        embed.add_field(
            name='**Before**',
            value=f'```{player.stats["strength"]:.0f} strength\n{player.stats["crit damage"]:.0f} crit damage\n{player.stats["crit chance"]:.0f} crit chance\n{player.stats["attack speed"]:.0f} attack speed```'
                  f'```{zealot_damage:,.0f} to zealots\n{slayer_damage:,.0f} to slayers```'
        )
        embed.add_field(
            name='**After**',
            value=f'```{best_stats["strength"]:.0f} strength\n{best_stats["crit damage"]:.0f} crit damage\n{best_stats["crit chance"]:.0f} crit chance\n{best_stats["attack speed"]:.0f} attack speed```'
                  f'```{zealot_damage_after:,.0f} to zealots\n{slayer_damage_after:,.0f} to slayers```'
        )

        if not optimized:
            embed.add_field(
                name='**Warning**',
                value='The bot took too long to optimize your gear so it gave up'
                      '\nThe result is the best it could do for this short amount of time',
                inline=False
            )
        await embed.send()


def setup(bot):
    bot.add_cog(Optimizer(bot))
