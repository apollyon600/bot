import aiohttp
import asyncio

from lib import ExternalAPIError, BadNameError
from constants import MOBS_RELEVANT_ENCHANTS, ENCHANTMENT_BONUS
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
    item_name = item_name.replace(' ', '%20')
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
