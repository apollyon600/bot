import copy
from discord.ext import commands

from lib import damage_optimizer
from lib import APIDisabledError, SessionTimeout, PlayerOnlineError, NoArmorError, NoWeaponError
from utils import CommandWithCooldown, Embed, colorize, format_pet, emod, damage, get_uuid_from_name
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

        if not player:
            player = await ctx.ask(message=f'{ctx.author.mention}, What is your minecraft username?')

        player_name, player_uuid = await get_uuid_from_name(player, session=self.bot.http_session)
        player = await self.bot.hypixel_api_client.get_player(player_name, player_uuid)

        if profile:
            await player.get_set_skyblock_profiles(selected_profile=profile)
        else:
            await player.get_set_skyblock_profiles()

        if player.online:
            raise PlayerOnlineError

        if not player.profile.enabled_api['skills'] or not player.profile.enabled_api['inventory']:
            raise APIDisabledError(player.uname, player.profile.profile_name)

        weapon = await self.prompt_for_weapon(ctx, player.profile)
        if not weapon:
            raise NoWeaponError
        player.profile.set_weapon(weapon)

        armor = await self.prompt_for_armor(ctx, player.profile)
        if not armor:
            raise NoArmorError
        player.profile.set_armor(armor)

        pet = await self.prompt_for_pet(ctx, player.profile)
        player.profile.set_pet(pet)

        profile_confirm = await self.confirm_equipment(ctx, player.profile)
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

        selected_pots = await self.prompt_for_potions(ctx, player.profile)

        selected_buffs = await self.prompt_for_support_item(ctx, player.profile)

        option_confirm = await self.confirm_options(ctx, perfect_crit_chance, attack_speed_limit, only_blacksmith,
                                                    ignored_reforges, selected_pots, selected_buffs)
        if not option_confirm:
            raise SessionTimeout

        best_route = damage_optimizer(
            player.profile,
            perfect_crit_chance=perfect_crit_chance,
            attack_speed_limit=attack_speed_limit,
            only_blacksmith_reforges=only_blacksmith,
            reforges_set=reforges_set
        )

        await self.send_optimizer_result(ctx, player.profile, best_route)

    @staticmethod
    async def send_optimizer_result(ctx, profile, best_route):
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
        ).set_footer(
            text='Player\'s stats include pots.\nPlease double check result stats and in game before reforge.\n'
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

        base_mod = profile.stats['enchantment modifier']
        zealot_mod = emod('zealots', weapon) + base_mod
        slayer_mod = emod('slayer bosses', weapon) + base_mod

        slayer_mult = 1
        if weapon.internal_name == 'REAPER_SWORD':
            slayer_mult = 3
        elif weapon.internal_name == 'SCORPION_FOIL':
            slayer_mult = 2.5

        zealot_damage = damage(profile.weapon.stats['damage'], profile.stats['strength'],
                               profile.stats['crit damage'], zealot_mod)
        slayer_damage = damage(profile.weapon.stats['damage'], profile.stats['strength'],
                               profile.stats['crit damage'], slayer_mod)
        slayer_damage *= slayer_mult

        zealot_damage_after = damage(best_stats['damage'], best_stats['strength'],
                                     best_stats['crit damage'], zealot_mod)
        slayer_damage_after = damage(best_stats['damage'], best_stats['strength'],
                                     best_stats['crit damage'], slayer_mod)
        slayer_damage_after *= slayer_mult

        embed.add_field(
            name='**Before**',
            value=f'```{profile.stats["strength"]:.0f} strength\n{profile.stats["crit damage"]:.0f} crit damage\n'
                  f'{profile.stats["crit chance"]:.0f} crit chance\n{profile.stats["attack speed"]:.0f} attack speed\n'
                  f'{profile.weapon.stats["damage"]:.0f} weapon damage```'
                  f'```{zealot_damage:,.0f} to zealots\n{slayer_damage:,.0f} to slayers```'
        )
        embed.add_field(
            name='**After**',
            value=f'```{best_stats["strength"]:.0f} strength\n{best_stats["crit damage"]:.0f} crit damage\n'
                  f'{best_stats["crit chance"]:.0f} crit chance\n{best_stats["attack speed"]:.0f} attack speed\n'
                  f'{best_stats["damage"]:.0f} weapon damage```'
                  f'```{zealot_damage_after:,.0f} to zealots\n{slayer_damage_after:,.0f} to slayers```'
        )

        if not is_optimized:
            embed.add_field(
                name='**Warning**',
                value='The bot took too long to optimize your gear so it gave up.'
                      '\nThe result is the best it could do for this short amount of time.',
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
        ).set_footer(
            text='The attack speed limit must be a whole number!'
        ).send()

        def check(m):
            if m.author.id != ctx.author.id or m.channel.id != ctx.channel.id:
                return False
            if m.clean_content.lower() == 'exit':
                raise SessionTimeout
            elif m.clean_content.isdigit():
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
                              selected_pots, selected_buffs):
        potions_list = [f'{name.capitalize()}: {level}' for name, level in selected_pots if level != 0]
        return await ctx.prompt(embed=Embed(
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
        ))

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
                profile.stats.__iadd__(stat, amount[selected_level])

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
                        profile.stats.__iadd__(stat, amount)
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
            if m.clean_content.lower() == 'exit':
                raise SessionTimeout
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and not m.clean_content.isdigit()

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
