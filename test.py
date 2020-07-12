from lib.Player import Player
import asyncio
import os

if os.environ.get('API_KEY') is None:
    import dotenv

    dotenv.load_dotenv()

keys = os.getenv('API_KEY')


async def main():
    player = await Player(keys, uname='craftedfury', uuid='f33f51a796914076abdaf66e3d047a71')
    await player.set_profile(list(player.profiles.values())[0])
    print('done')
    # for item in player.talismans:
    #     pprint(item.__nbt__)
    #     print('\n--------------------------------\n')


try:
    asyncio.run(main())
except RuntimeError:
    pass
