import aiohttp
import asyncio

from . import ExternalAPIError, BadNameError


# noinspection PyAssignmentToLoopOrWithParameter
async def fetch_uuid_uname(uname_or_uuid, s):
    try:
        async with s.get(f'https://api.mojang.com/users/profiles/minecraft/{uname_or_uuid}') as r:

            json = await r.json(content_type=None)
            if not json:

                async with s.get(f'https://api.mojang.com/user/profiles/{uname_or_uuid}/names') as r:
                    json = await r.json(content_type=None)

                    if not json:
                        raise BadNameError(uname_or_uuid) from None

                    return json[-1]['name'], uname_or_uuid

            return json['name'], json['id']
    except asyncio.TimeoutError:
        raise ExternalAPIError('Could not connect to https://api.mojang.com.') from None
    except aiohttp.ClientResponseError:
        raise BadNameError(uname_or_uuid) from None


# noinspection PyUnboundLocalVariable
def level_from_xp_table(xp, table):
    """
    Takes a list of xp requirements and a xp value.
    Returns whatever level the thing should be at
    """

    for level, requirement in enumerate(table):
        if requirement > xp:
            break
    else:
        level += 1
    return level


def safe_list_get(lst, i):
    try:
        return lst[i]
    except IndexError:
        return None


def damage(weapon_dmg, strength, crit_dmg, ench_modifier):
    return (5 + weapon_dmg + strength // 5) * (1 + strength / 100) * (1 + crit_dmg / 100) * (1 + ench_modifier / 100)


async def get_item_price_stats(item_id, *, session):
    try:
        async with session.get(f'https://auctions.craftlink.xyz/api/items/{item_id}/quickStats') as response:
            json = await response.json(content_type=None)
            if not json:
                return None
            if not json['success']:
                return None
            return json['data']
    except asyncio.TimeoutError:
        raise ExternalAPIError('Could not connect to https://auctions.craftlink.xyz.') from None


async def get_item_id(item_name, *, session):
    item_name = item_name.replace(' ', '%20')
    try:
        async with session.get(f'https://auctions.craftlink.xyz/api/items/search?name={item_name}') as response:
            json = await response.json(content_type=None)
            if not json:
                return None
            if not json['success']:
                return None
            return json['data']
    except asyncio.TimeoutError:
        raise ExternalAPIError('Could not connect to https://auctions.craftlink.xyz.') from None
