from config import keys
from lib import Player


async def args_to_player(player, profile):
    player = await Player(keys, uname=player)

    if not profile:
        await player.set_profile_automatically()
    else:
        await player.set_profile(player.profiles[profile.capitalize()])

    return player
