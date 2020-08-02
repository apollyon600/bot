import aiohttp
import asyncio
import re
from urllib.parse import quote

from lib import ExternalAPIError, BadNameError, BadGuildError, Guild
from constants import MOBS_RELEVANT_ENCHANTS, ENCHANTMENT_BONUS, STAT_NAMES
from constants.discord import TIMEOUT_EMOJIS


async def get_uuid_from_name(name, *, session):
    try:
        async with session.get(f'https://api.mojang.com/users/profiles/minecraft/{name}') as resp:
            if resp.status == 204:
                raise BadNameError(name) from None

            json = await resp.json(content_type=None)

            if json is None or 'name' not in json or 'id' not in json:
                raise BadNameError(name) from None

            return json['name'], json['id']
    except (asyncio.TimeoutError, aiohttp.ClientConnectorError):
        raise ExternalAPIError('Could not connect to https://api.mojang.com.') from None
    except aiohttp.ClientResponseError:
        raise BadNameError(name) from None


def level_from_xp_table(xp, table):
    """
    Takes a xp value and a list of level requirements.
    Returns whatever level the thing should be at.
    """
    level = 0
    for i, requirement in enumerate(table):
        if xp >= requirement:
            level = i + 1
        else:
            break
    return level


def safe_list_get(lst, i):
    try:
        return lst[i]
    except IndexError:
        return None


def damage(weapon_dmg, strength, crit_dmg, ench_modifier):
    return (5 + weapon_dmg + strength // 5) * (1 + strength / 100) * (1 + crit_dmg / 100) * (1 + ench_modifier / 100)


async def get_item_price_stats(item_id, *, session):
    """
    Get item's price stats with item id.
    """
    try:
        async with session.get(f'https://auctions.craftlink.xyz/api/items/{item_id}/quickStats') as response:
            json = await response.json(content_type=None)
            if json is None or 'success' not in json:
                return None
            if not json['success']:
                return None
            return json['data']
    except asyncio.TimeoutError:
        raise ExternalAPIError('Could not connect to https://auctions.craftlink.xyz.') from None


async def get_item_id(item_name, *, session):
    """
    Search with item name and return the first result's item id.
    """
    item_name = quote(item_name)
    try:
        async with session.get(f'https://auctions.craftlink.xyz/api/items/search?name={item_name}') as response:
            json = await response.json(content_type=None)
            if json is None or 'success' not in json:
                return None
            if not json['success']:
                return None
            return json['data']
    except asyncio.TimeoutError:
        raise ExternalAPIError('Could not connect to https://auctions.craftlink.xyz.') from None


def colorize(s, color):
    language, point = color
    s = str(s)
    if not s:
        return ''
    return f'```{language}\n{point}' + s.replace('\n', f'\n{point}') + '\n```'


def format_pet(pet):
    return f'{pet.title} |{pet.rarity.upper()}|' if pet else ''


async def embed_timeout_handler(ctx, emoji_list, message=None):
    message = message or ctx.message
    try:
        for (emoji, _) in emoji_list:
            await message.remove_reaction(emoji, ctx.bot.user)
        for emoji in TIMEOUT_EMOJIS:
            await message.add_reaction(emoji)
    except:
        pass


def emod(activity, weapon):
    result = 0
    for enchantment in MOBS_RELEVANT_ENCHANTS[activity]:
        if enchantment in weapon.enchantments:
            value = ENCHANTMENT_BONUS[enchantment]
            if callable(value):
                result += value(weapon.enchantments[enchantment])
            else:
                result += value * weapon.enchantments[enchantment]
    return result


def get_stats_from_description(desc, *, dungeon=False):
    """
    Get item stats from clean description and estimated total dungeon bonus.
    Return item stats dict, item reforge stats dict, estimated total dungeon bonus value.
    """
    stat_regex = re.compile('([\w ]*): \D?(\d*\.?\d*)(.*)')
    reforge_regex = re.compile('.*\(([\w ]*) \+(\d*)')
    dungeon_regex = re.compile('.*\(\D?(\d*\.\d*).*\)')
    stats = {}
    reforge_stats = {}
    dungeon_bonus = 1.00
    for line in desc:
        stat_match = stat_regex.match(line)
        if stat_match is None:
            continue  # if doesn't match

        stat_type = stat_match.group(1).lower()
        stat_value = stat_match.group(2)
        if not stat_value or not stat_type:
            continue
        stat_value = float(stat_value)

        if stat_type in STAT_NAMES:
            if stat_type == 'bonus attack speed':
                stat_type = 'attack speed'  # remove bonus
            stats[stat_type] = stat_value

        # check for reforge stat
        if stat_match.group(3):
            reforge_match = reforge_regex.match(stat_match.group(3))
            if reforge_match is not None:
                reforge_value = reforge_match.group(2)

                if reforge_value:
                    reforge_value = float(reforge_value)
                    reforge_stats[stat_type] = reforge_value

            if dungeon:
                dungeon_match = dungeon_regex.match(stat_match.group(3))
                if dungeon_match is None:
                    continue

                dungeon_stat = dungeon_match.group(1)
                if not dungeon_stat:
                    continue
                dungeon_stat = float(dungeon_stat)

                if dungeon_stat < stat_value:
                    continue  # if the matched stat is less than main stat

                dungeon_bonus = float(dungeon_stat / stat_value)

    return stats, reforge_stats, dungeon_bonus


def closest(lst, k):
    """
    Find closest number in the given list.
    Return the number and the index in that list
    """
    num = min(range(len(lst)), key=lambda i: abs(lst[i] - k))
    return lst[num], num


async def ask_for_skyblock_profiles(ctx, player, profile, *, session, hypixel_api_client, auto_set=False,
                                    get_guild=False):
    if not player:
        player = await ctx.ask(message=f'{ctx.author.mention}, What is your minecraft username?')

    player_name, player_uuid = await get_uuid_from_name(player, session=session)
    player = await hypixel_api_client.get_player(player_uuid, uname=player_name)

    if profile:
        await player.get_skyblock_profiles(selected_profile=profile)
    else:
        await player.get_skyblock_profiles()

    if auto_set:
        player.profile.set_pet_armor_automatically()

    if get_guild:
        await player.get_player_guild()

    return player


async def ask_for_guild(ctx, guild, *, hypixel_api_client, load_members=False):
    if not guild:
        guild = await ctx.ask(message=f'{ctx.author.mention}, What is the guild you want to check?')

    await ctx.send(f'{ctx.author.mention}, I am getting the guild information, please wait a little bit!')
    guild_data = await hypixel_api_client.get_guild(params={'name': quote(guild)})
    if guild_data is None:
        raise BadGuildError(guild)

    guild = Guild(guild_data)

    if load_members:
        await guild.load_all_members(hypixel_api_client=hypixel_api_client)

    return guild
