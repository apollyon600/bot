import copy
from discord.ext import commands

from lib import damage_optimizer
from lib import APIDisabledError, SessionTimeout, PlayerOnlineError, NoArmorError, NoWeaponError
from utils import CommandWithCooldown, Embed, colorize, format_pet, emod, damage, ask_for_skyblock_profiles
from constants.discord import OPTIMIZER_GOALS, RARITY_COLORS, PET_EMOJIS, DAMAGE_POTIONS, NUMBER_EMOJIS, SUPPORT_ITEMS
from constants import DAMAGE_REFORGES


class OptimizeGear(commands.Cog, name='Damage'):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command(cls=CommandWithCooldown, cooldown_after_parsing=True)
    @commands.cooldown(1, 10.0, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.channel, wait=False)
    async def optimizer(self, ctx, player: str = '', profile: str = ''):
        """
        Optimizes your equipments to their best reforges.
        """
        await ctx.send(f'{ctx.author.mention}, Welcome to the optimizer!\n'
                       f'Please enter `exit` at any given point in the optimizer to exit')

        player = await ask_for_skyblock_profiles(ctx, player, profile, session=self.bot.http_session,
                                                 hypixel_api_client=self.bot.hypixel_api_client)
        profile = player.profile

        if player.online:
            raise PlayerOnlineError

        if not profile.enabled_api['skills'] or not profile.enabled_api['inventory']:
            raise APIDisabledError(player.uname, profile.name)

        weapon = await self.prompt_for_weapon(ctx, profile)
        if not weapon:
            raise NoWeaponError

        armor = await self.prompt_for_armor(ctx, profile)
        if not armor:
            raise NoArmorError

        pet = await self.prompt_for_pet(ctx, profile)

        # Check if user selected dungeon items
        dungeon_item_used = False
        if weapon.dungeon:
            dungeon_item_used = True
        if not dungeon_item_used:
            for piece in armor.values():
                if piece is None:
                    continue
                if piece.dungeon:
                    dungeon_item_used = True
                    break

        include_dungeon = False
        if dungeon_item_used:
            include_dungeon = await ctx.prompt(
                embed=Embed(
                    ctx=ctx,
                    title="Do you want to use your items' dungeon stats? yes/no"
                )
            )

        profile.set_weapon(weapon)
        profile.set_armor(armor, dungeon=include_dungeon)
        profile.set_pet(pet, dungeon=include_dungeon)

        profile_confirm = await self.confirm_equipment(ctx, profile)
        if not profile_confirm:
            raise SessionTimeout

        perfect_crit_chance = await ctx.prompt(embed=Embed(
            ctx=ctx,
            title='What would you like to optimize for?'
        ).add_field(
            value='\n\n'.join(f'> {o["emoji"]}\n`{o["name"]}`' for o in OPTIMIZER_GOALS)
        ), emoji_list=[('💯', True), ('💥', False)])

        attack_speed_limit = await self.prompt_for_attack_speed(ctx)

        only_blacksmith, reforges_set, ignored_reforges = await self.prompt_for_reforges(ctx)

        selected_pots = await self.prompt_for_potions(ctx, profile)

        selected_buffs = await self.prompt_for_support_item(ctx, profile)

        option_confirm = await self.confirm_options(ctx, perfect_crit_chance, attack_speed_limit, only_blacksmith,
                                                    ignored_reforges, selected_pots, selected_buffs, dungeon_item_used,
                                                    include_dungeon)
        if not option_confirm:
            raise SessionTimeout

        best_route = damage_optimizer(
            profile,
            perfect_crit_chance=perfect_crit_chance,
            attack_speed_limit=attack_speed_limit,
            only_blacksmith_reforges=only_blacksmith,
            include_dungeon=include_dungeon,
            reforges_set=reforges_set
        )

        await self.send_optimizer_result(ctx, profile, best_route, include_dungeon)

    @staticmethod
    async def send_optimizer_result(ctx, profile, best_route, include_dungeon):
        weapon = profile.weapon
        best_stats = best_route[0] or {}
        best_equip = best_route[1] or {}
        is_optimized = best_route[0]['is optimized']

        if not best_equip:
            return await ctx.send(f'{ctx.author.mention}, Optimization is not possible with the options you chose!\n'
                                  f'Collect more talismans or raise your combat level before trying again.')

        embed = Embed(
            ctx=ctx,
            title='{s}'.format(s='Successful!' if is_optimized else 'Unsuccessful!')
        ).add_footer(
            text='Player\'s stats include pots.\n'
                 '{s}'.format(s='Armor/Weapon includes dungeon stats.\n' if include_dungeon else '') +
                 'Please make sure your "before" stats are correct before reforging.'
        )

        for equipment in best_equip:
            for rarity in best_equip[equipment]:
                text = colorize(' + '.join([f'{best_equip[equipment][rarity][reforge]} {reforge.title()}' for reforge in
                                            best_equip[equipment][rarity]]), RARITY_COLORS[rarity])
                embed.add_field(
                    name=f'**{rarity.title()} {equipment.title()}**',
                    value=text,
                    inline=False
                )

        base_mod = profile.stats.combat_bonus + (profile.stats.archery_bonus if weapon.type == 'bow' else 0)

        if include_dungeon:
            normal_mod = emod('base', weapon) + base_mod

            normal_damage_before = damage(profile.weapon.stats.get_stat('damage', dungeon=include_dungeon),
                                          profile.stats.get_stat('strength', dungeon=include_dungeon),
                                          profile.stats.get_stat('crit damage', dungeon=include_dungeon), normal_mod)

            normal_damage_after = damage(best_stats['damage'], best_stats['strength'],
                                         best_stats['crit damage'], normal_mod)

            before_damage = f'```Base > {normal_damage_before:,.0f}```'
            after_damage = f'```Base > {normal_damage_after:,.0f}```'
        else:
            zealot_mod = emod('zealots', weapon) + base_mod
            slayer_mod = emod('slayer bosses', weapon) + base_mod

            slayer_mult = 1
            if weapon.internal_name == 'REAPER_SWORD':
                slayer_mult = 3
            elif weapon.internal_name == 'SCORPION_FOIL':
                slayer_mult = 2.5

            zealot_damage_before = damage(profile.weapon.stats.get_stat('damage', dungeon=include_dungeon),
                                          profile.stats.get_stat('strength', dungeon=include_dungeon),
                                          profile.stats.get_stat('crit damage', dungeon=include_dungeon), zealot_mod)
            slayer_damage_before = damage(profile.weapon.stats.get_stat('damage', dungeon=include_dungeon),
                                          profile.stats.get_stat('strength', dungeon=include_dungeon),
                                          profile.stats.get_stat('crit damage', dungeon=include_dungeon), slayer_mod)
            slayer_damage_before *= slayer_mult

            zealot_damage_after = damage(best_stats['damage'], best_stats['strength'],
                                         best_stats['crit damage'], zealot_mod)
            slayer_damage_after = damage(best_stats['damage'], best_stats['strength'],
                                         best_stats['crit damage'], slayer_mod)
            slayer_damage_after *= slayer_mult

            before_damage = f'```Zealots > {zealot_damage_before:,.0f}\nSlayers > {slayer_damage_before:,.0f}```'
            after_damage = f'```Zealots > {zealot_damage_after:,.0f}\nSlayers > {slayer_damage_after:,.0f}```'

        weapon_damage_before = ''
        weapon_damage_after = ''
        if weapon.internal_name == 'MIDAS_SWORD':
            weapon_damage_before = f'Weapon damage > {profile.weapon.stats.get_stat("damage", dungeon=include_dungeon):.0f}'
            weapon_damage_after = f'Weapon damage > {best_stats["damage"]:.0f}'

        embed.add_field(
            name='**Before**',
            value=f'```Strength > {profile.stats.get_stat("strength", dungeon=include_dungeon):.0f}\n'
                  f'Crit damage > {profile.stats.get_stat("crit damage", dungeon=include_dungeon):.0f}%\n'
                  f'Crit chance > {profile.stats.get_stat("crit chance", dungeon=include_dungeon):.0f}%\n'
                  f'Attack speed > {profile.stats.get_stat("attack speed", dungeon=include_dungeon):.0f}%\n'
                  f'{weapon_damage_before}```{before_damage}'
        )
        embed.add_field(
            name='**After**',
            value=f'```Strength > {best_stats["strength"]:.0f}\nCrit damage > {best_stats["crit damage"]:.0f}%\n'
                  f'Crit chance > {best_stats["crit chance"]:.0f}%\nAttack speed > {best_stats["attack speed"]:.0f}%\n'
                  f'{weapon_damage_after}```{after_damage}'
        )

        if not is_optimized:
            embed.add_field(
                name='**Warning**',
                value='The bot took too long to optimize your gear so it gave up.\n'
                      'This result is the best it could do in the allotted time.',
                inline=False
            )

        await embed.send()

    @staticmethod
    async def prompt_for_attack_speed(ctx):
        await Embed(
            ctx=ctx,
            title='Do you want to include attack speed?',
            description='```0 > Don\'t include attack speed```\n'
                        '```100 > Maximum attack speed```'
        ).add_field(
            name='Option',
            value='If you want to choose a customized attack speed limit, enter a number between 0 and 100.'
        ).add_footer(
            text='The attack speed limit must be a whole number!'
        ).send()

        def check(m):
            if m.author.id == ctx.author.id and m.channel.id == ctx.channel.id:
                if m.clean_content.lower() == 'exit':
                    raise SessionTimeout
                if m.clean_content.isdigit():
                    return True
            return False

        while True:
            msg = await ctx.bot.wait_for('message', timeout=60.0, check=check)
            if int(msg.clean_content) in range(0, 101):
                return int(msg.clean_content)
            else:
                await ctx.send(f'{ctx.author.mention}, Invalid number! Did you make a typo?')

    @staticmethod
    async def prompt_for_weapon(ctx, profile):
        if len(profile.weapons) == 0:
            return None
        elif len(profile.weapons) == 1:
            return profile.weapons[0]
        else:
            weapon_index = await ctx.prompt_with_list(
                entries=[weapon for weapon in profile.weapons],
                title='Which weapon would you like to use?',
                footer='You may enter the corresponding weapon number.'
            )
            return profile.weapons[weapon_index - 1]

    @staticmethod
    async def prompt_for_armor(ctx, profile):
        if len(profile.wardrobe) > 1:
            entries = []
            for i, armor in enumerate(profile.wardrobe):
                entries.append(f'{armor["helmet"]}\n'
                               f'{"".ljust(len(str(i + 1)) + 3)}{armor["chestplate"]}\n'
                               f'{"".ljust(len(str(i + 1)) + 3)}{armor["leggings"]}\n'
                               f'{"".ljust(len(str(i + 1)) + 3)}{armor["boots"]}')
            armor_index = await ctx.prompt_with_list(
                entries=entries,
                title='Which armor set would you like to use?',
                footer='You may enter the corresponding armor set number.',
                per_page=3
            )
            return profile.wardrobe[armor_index - 1]
        else:
            if profile.current_armor:
                return profile.current_armor
            else:
                return None

    @staticmethod
    async def prompt_for_pet(ctx, profile):
        if len(profile.pets) == 0:
            return None
        elif len(profile.pets) == 1:
            return profile.pets[0]
        else:
            pet_index = await ctx.prompt_with_list(
                entries=[format_pet(pet) for pet in profile.pets],
                title='Which pet would you like to use?',
                footer='You may enter the corresponding pet number.'
            )
            return profile.pets[pet_index - 1]

    @staticmethod
    async def confirm_equipment(ctx, profile):
        weapon = profile.weapon
        pet = profile.pet
        return await ctx.prompt(embed=Embed(
            ctx=ctx,
            title='Is this the correct equipment?'
        ).add_field(
            name='⚔️\tWeapon',
            value=f'```{weapon}```',
            inline=False
        ).add_field(
            name=f'{PET_EMOJIS[pet.internal_name] if pet and pet.internal_name in PET_EMOJIS else "🐣"}\tPet',
            value=f'```{format_pet(pet) if pet else None}```',
            inline=False
        ).add_field(
            name='💎\tPet Item',
            value=f'```{pet.item_name if pet else None}```',
            inline=False
        ).add_field(
            name='⛑️\tHelmet',
            value=f'```{profile.armor["helmet"]}```',
            inline=False
        ).add_field(
            name='👚\tChestplate',
            value=f'```{profile.armor["chestplate"]}```',
            inline=False
        ).add_field(
            name='👖\tLeggings',
            value=f'```{profile.armor["leggings"]}```',
            inline=False
        ).add_field(
            name='👞\tBoots',
            value=f'```{profile.armor["boots"]}```',
            inline=False
        ).add_field(
            name='🏺\tTalismans',
            value=''.join(
                colorize(f'{amount} {name.capitalize()}', RARITY_COLORS[name])
                for name, amount in profile.talisman_counts.items()
            )
        ))

    @staticmethod
    async def confirm_options(ctx, perfect_crit_chance, attack_speed_limit, only_blacksmith, ignored_reforges,
                              selected_pots, selected_buffs, dungeon_item_used, include_dungeon):
        potions_list = [f'{name.capitalize()}: {level}' for name, level in selected_pots if level != 0]
        embed = Embed(
            ctx=ctx,
            title='Are these options correct?'
        ).add_field(
            name='Goal',
            value=f'```{"Perfect crit chance" if perfect_crit_chance else "Maximum damage"}```'
        ).add_field(
            name='Attack speed limit',
            value=f'```{attack_speed_limit}%```'
        ).add_field(
            name='Reforges',
            value=f'```{"Only blacksmith reforges" if only_blacksmith else "All reforges"}```' +
                  '{s}'.format(
                      s=f'\n```Ignored reforges: {", ".join(ignored_reforges)}```' if ignored_reforges else ""),
            inline=False
        ).add_field(
            name='Potions',
            value=f"```{', '.join(potions_list) if potions_list else 'None'}```"
        ).add_field(
            name='Support items',
            value=f"```{', '.join([f'{item.capitalize()}' for item in selected_buffs]) if selected_buffs else 'None'}```"
        )
        if dungeon_item_used:
            embed.add_field(
                name='Dungeon items',
                value=f'```{"Dungeon stats" if include_dungeon else "Regular stats"}```',
                inline=False
            )
        return await ctx.prompt(embed=embed)

    @staticmethod
    async def prompt_for_potions(ctx, profile):
        weapon = profile.weapon
        selected_pots = []
        for name, pot in DAMAGE_POTIONS.items():
            buff = pot['stats']
            levels = pot['levels']

            if weapon.type != 'bow' and name == 'archery':
                continue

            emoji_list = [(NUMBER_EMOJIS[level], level) for level in levels]

            selected_level = await ctx.prompt(
                message=f'{ctx.author.mention}, What level of `{name} potion` do you want to use?' +
                        '{s}'.format(
                            s='\nSelect 0 if you want to choose normal potions instead of a dungeon potion!' if name == 'dungeon' else ''),
                emoji_list=emoji_list)

            selected_pots.append((name, selected_level))

            for stat, amount in buff.items():
                if stat == 'archery bonus':
                    profile.stats.archery_bonus += amount[selected_level]
                else:
                    profile.stats.add_stat(stat, amount[selected_level])

            if name == 'dungeon' and selected_level > 0:
                break
        return selected_pots

    @staticmethod
    async def prompt_for_support_item(ctx, profile):
        selected_buffs = []
        for name, orb in SUPPORT_ITEMS.items():
            internal_name = orb['internal']
            buff = orb['stats']

            if internal_name in profile.inventory or internal_name in profile.echest:
                confirm = await ctx.prompt(message=f'{ctx.author.mention}, Will you be using your `{name}`?')
                if confirm:
                    selected_buffs.append(name)
                    for stat, amount in buff.items():
                        profile.stats.add_stat(stat, amount)
        return selected_buffs

    async def prompt_for_reforges(self, ctx):
        await Embed(
            ctx=ctx,
            title='What reforges do you want to use?',
            description='```blacksmith > Only the reforges from blacksmith```\n'
                        '```all > All the blacksmith reforges and reforge stones```'
        ).add_field(
            name='Option',
            value='If you want to ignore specific reforges that you don\'t like, enter using this format\n'
                  '`<blacksmith / all> ignore [ignored reforge followed by a space for multiple]`\n'
                  'Example: `all ignore renowned spiked`'
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
            msg_list = msg.clean_content.lower().split(' ')
            filtered_msg = self.check_reforge_message(msg_list)
            if filtered_msg:
                if isinstance(filtered_msg, list):
                    await ctx.send(
                        f'{ctx.author.mention}, These reforges `{", ".join(filtered_msg)}` aren\'t in the reforges list!\n'
                        f'Please double check their name or they are already not in the list.')
                    continue
                else:
                    return filtered_msg
            await ctx.send(f'{ctx.author.mention}, Invalid options! Did you make a typo?\n'
                           f'Please check the usage and example!')

    @staticmethod
    def check_reforge_message(m):
        reforge_options = {'blacksmith': True, 'all': False}
        reforges = copy.deepcopy(DAMAGE_REFORGES)
        ignored = []
        if m[0] in reforge_options.keys():
            only_blacksmith = reforge_options[m[0]]
        else:
            return None
        if len(m) > 1:
            if m[1] == 'ignore' and len(m[2:]) > 0:
                ignore = m[2:]
                for equip in reforges:
                    for reforge in list(reforges[equip]):
                        if reforge in ignore:
                            ignored.append(reforge)
                            reforges[equip].pop(reforge)
                            ignore.remove(reforge)
                if len(ignore) > 0:
                    return ignore
            else:
                return None
        return only_blacksmith, reforges, ignored


def setup(bot):
    bot.add_cog(OptimizeGear(bot))
