import aiohttp
import asyncio

from . import ExternalAPIError, BadNameError

_session = None


async def session():
    global _session
    if _session is None:
        _session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=3), raise_for_status=True)
    return _session


# noinspection PyAssignmentToLoopOrWithParameter
async def fetch_uuid_uname(uname_or_uuid):
    s = await session()

    try:
        async with s.get(f'https://api.mojang.com/users/profiles/minecraft/{uname_or_uuid}') as r:

            json = await r.json(content_type=None)
            if json is None:

                async with s.get(f'https://api.mojang.com/user/profiles/{uname_or_uuid}/names') as r:
                    json = await r.json(content_type=None)
                    if json is None:
                        raise BadNameError(uname_or_uuid, 'Malformed uuid or username') from None

                    return json[-1]['name'], uname_or_uuid

            return json['name'], json['id']
    except asyncio.TimeoutError:
        raise ExternalAPIError('Could not connect to https://api.mojang.com') from None
    except aiohttp.ClientResponseError:
        raise BadNameError(uname_or_uuid, 'Can\'t get player name or uuid')


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


def damage(weapon_dmg, strength, crit_dmg, ench_modifier):
    return (5 + weapon_dmg + strength // 5) * (1 + strength / 100) * (1 + crit_dmg / 100) * (1 + ench_modifier / 100)
