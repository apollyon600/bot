from skypy import *
import asyncio
import os
from pprint import pprint

if os.environ.get('API_KEY') is None:
    import dotenv
    dotenv.load_dotenv()
	
keys = os.getenv('API_KEY').split()

async def main():
	player = await skypy.Player(keys, uname='craftedfury')
	await player.set_profile(list(player.profiles.values())[0])
	for item in player.talismans:
		pprint(item.__nbt__)
		print('\n--------------------------------\n')
	
try:
	asyncio.run(main())
except RuntimeError:
	pass