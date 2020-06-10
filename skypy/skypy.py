from skypy.constants.pets import *
from skypy.constants.constants import *
from skypy.constants.slayer import *
from skypy.exceptions import *

# API Calls
import aiohttp
import asyncio
from datetime import datetime
import time
# --------

_session = None

async def session():
	global _session
	if _session is None:
		_session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=3), raise_for_status=True)
	return _session

# Inventory parsing
from base64 import b64decode as one
from gzip import decompress as two
from io import BytesIO as three
from struct import unpack
import re
# -----------------

def decode_inventory_data(raw):
	"""Takes a raw string representing inventory data.
	Returns a json object with the inventory's contents"""

	raw = three(two(one(raw)))	# Unzip raw string from the api

	def read(type, length):
		if type in 'chil':
			return int.from_bytes(raw.read(length), byteorder='big')
		if type == 's':
			return raw.read(length).decode('utf-8')
		return unpack('>' + type, raw.read(length))[0]

	def parse_list():
		subtype = read('c', 1)
		payload = []
		for _ in range(read('i', 4)):
			parse_next_tag(payload, subtype)
		return payload

	def parse_compound():
		payload = {}
		while parse_next_tag(payload) != 0:	 # Parse tags until we find an endcap (type == 0)
			pass  # Nothing needs to happen here
		return payload

	payloads = {
		1: lambda: read('c', 1),  # Byte
		2: lambda: read('h', 2),  # Short
		3: lambda: read('i', 4),  # Int
		4: lambda: read('l', 8),  # Long
		5: lambda: read('f', 4),  # Float
		6: lambda: read('d', 8),  # Double
		7: lambda: raw.read(read('i', 4)),	# Byte Array
		8: lambda: read('s', read('h', 2)),	 # String
		9: parse_list,	# List
		10: parse_compound,	 # Compound
		11: lambda: [read('i', 4) for _ in range(read('i', 4))],  # Int Array
		12: lambda: [read('l', 8) for _ in range(read('i', 4))]	 # Long Array
	}

	def parse_next_tag(dictionary, tag_id=None):
		if tag_id is None:	# Are we inside a list?
			tag_id = read('c', 1)
			if tag_id == 0:	 # Is this the end of a compound?
				return 0
			name = read('s', read('h', 2))

		payload = payloads[tag_id]()
		if isinstance(dictionary, dict):
			dictionary[name] = payload
		else:
			dictionary.append(payload)

	raw.read(3)	 # Remove file header (we ingore footer)
	root = {}
	parse_next_tag(root)
	return [Item(x, i) for i, x in enumerate(root['i']) if x]

def level_from_xp_table(xp, table):
	"""Takes a list of xp requirements and a xp value.
	Returns whatever level the thing should be at"""

	for level, requirement in enumerate(table):
		if requirement > xp:
			break
	else:
		level += 1
	return level

class Item:
	def __init__(self, nbt, slot_number=0, player=None):
		self._nbt = nbt

		self.stack_size = self._nbt.get('Count', 1)
		self.slot_number = slot_number

		tag = nbt.get('tag', {})
		extras = tag.get('ExtraAttributes', {})

		self.description = tag.get('display', {}).get('Lore', [])
		self.description_clean = [re.sub('§.', '', line) for line in self.description]
		self.description = '\n'.join(self.description)
		self.internal_name = extras.get('id', None)
		self.hot_potatos = extras.get('hot_potato_count', 0)
		self.collection_date = extras.get('timestamp', '') # 'timestamp': '2/16/20 9:24 PM',
		self.runes = extras.get('runes', {}) # 'runes': {'ZOMBIE_SLAYER': 3},
		self.enchantments = extras.get('enchantments', {})
		self.reforge = extras.get('modifier', None)

		if self.description_clean:
			rarity_type = self.description_clean[-1].split()
			self.rarity = rarity_type[0].lower()
			self.type = rarity_type[1].lower() if len(rarity_type) > 1 else None

			if self.internal_name != 'ENCHANTED_BOOK':
				for type, list in {'sword': sword_enchants, 'bow': bow_enchants, 'fishing rod': rod_enchants}.items():
					for e in list:
						if e in self.enchantments:
							self.type = type
							break
		else:
			self.rarity = None
			self.type = None

		self.name = re.sub('§.', '', self['tag']['display']['Name'])

	def __getitem__(self, name):
		return self._nbt[name]

	def __eq__(self, other):
		return self.internal_name == (other if isinstance(other, str) else other.internal_name)

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.name

	# Why do we have to sift the lorestring for this?
	# Can't it just be in the nbt data?
	def stats(self, use_reforge=True):
		results = {}
		name = self.internal_name

		reforge_multiplier = 1

		# §7Attack Speed: §c+2% §8(Itchy +2%)
		# §7Intelligence: §a+9 §c(Godly +3)
		reg = re.compile(
			'(Damage|'
			'Strength|'
			'Crit Chance|'
			'Crit Damage|'
			'Attack Speed|'
			'Health|'
			'Defense|'
			'Speed|'
			'Intelligence)'
			': \+(\d+).*'
		)
		for line in self.description_clean:
			match = reg.match(line)
			if match:
				results[match[1].lower()] = int(match[2])

		def add(stat, amount):
			results[stat] = results.get(stat, 0) + amount

		end_defence = {'END_HELMET': 35, 'END_CHESTPLATE': 60, 'END_LEGGINGS': 50, 'END_BOOTS': 25}

		if name == 'RECLUSE_FANG':
			self.stats['strength'] += 370
		if name == 'POOCH_SWORD':
			self.stats['strength'] += 150
		elif name == 'THE_SHREDDER':
			self.stats['damage'] += 115
			self.stats['strength'] += 15
		elif name == 'NIGHT_CRYSTAL' or name == 'DAY_CRYSTAL':
			self.stats['strength'] += 2.5
			self.stats['defense'] += 2.5
		elif name == 'CAKE_BAG':
			# add('health', len(decode_inventory_data(self[][][])))
			pass
		elif name == 'GRAVITY_TALISMAN':
			self.stats['strength'] += 10
			self.stats['defense'] += 10
		elif name in ('MUSHROOM_HELMET', 'MUSHROOM_CHESTPLATE', 'MUSHROOM_LEGGINGS', 'MUSHROOM_BOOTS'):
			if self.player and self.player.armor == {'helmet': 'MUSHROOM_HELMET', 'chestplate': 'MUSHROOM_CHESTPLATE', 'leggings': 'MUSHROOM_LEGGINGS', 'boots': 'MUSHROOM_BOOTS'}:
				self.stats.multiplier = 3
		elif name in ('END_HELMET', 'END_CHESTPLATE', 'END_LEGGINGS', 'END_BOOTS'):
			if self.player and self.player.armor == {'helmet': 'END_HELMET', 'chestplate': 'END_CHESTPLATE', 'leggings': 'END_LEGGINGS', 'boots': 'END_BOOTS'}:
				self.stats.multiplier = 2
		elif name in ('BAT_PERSON_HELMET', 'BAT_PERSON_CHESTPLATE', 'BAT_PERSON_LEGGINGS', 'BAT_PERSON_BOOTS'):
			if self.player and self.player.armor == {'helmet': 'BAT_PERSON_HELMET', 'chestplate': 'BAT_PERSON_CHESTPLATE', 'leggings': 'BAT_PERSON_LEGGINGS', 'boots': 'BAT_PERSON_BOOTS'}:
				self.stats.multiplier = 3
		elif name in ('SNOW_SUIT_HELMET', 'SNOW_SUIT_CHESTPLATE', 'SNOW_SUIT_LEGGINGS', 'SNOW_SUIT_BOOTS'):
			if self.player and self.player.armor == {'helmet': 'SNOW_SUIT_HELMET', 'chestplate': 'SNOW_SUIT_CHESTPLATE', 'leggings': 'SNOW_SUIT_LEGGINGS', 'boots': 'SNOW_SUIT_BOOTS'}:
				self.stats.multiplier = 2

		if use_reforge is False:
			if self.reforge:
				for stat, amount in reforges[self.reforge][self.rarity_level()].items():
					if stat in results:
						results[stat] -= amount * reforge_multiplier
		return results

def damage(weapon_dmg, strength, crit_dmg, ench_modifier):
	return (5 + weapon_dmg + strength // 5) * (1 + strength / 100) * (1 + crit_dmg / 100) * (1 + ench_modifier / 100)


async def fetch_uuid_uname(uname_or_uuid, _depth=0):
	s = await session()

	class TryNormal(Exception):
		#A simple exception that lets us exit mcheads
		pass

	try:
		async with s.get(f'https://mc-heads.net/minecraft/profile/{uname_or_uuid}') as r:
			if r.status == 204:
				raise BadNameError(uname_or_uuid, 'Malformed uuid or username')
			json = await r.json(content_type=None)
			if json is None:
				raise TryNormal
			return json['name'], json['id']

	except (asyncio.TimeoutError, TryNormal):
		# if mcheads fails, we try the normal minecraft API
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
			raise ExternalAPIError('Could not connect to https://mc-heads.net') from None
	except aiohttp.client_exceptions.ClientResponseError as e:
		if e.status == 429:
			await asyncio.sleep(15)
			if _depth <= 5:
				return fetch_uuid_uname(uname_or_uuid, _depth + 1)
			else:
				raise ExternalAPIError('You are being ratelimited by https://api.mojang.com') from None
		else:
			raise BadNameError(uname_or_uuid, 'Malformed uuid or username') from None

class Pet:
	def __init__(self, nbt):
		self._nbt = nbt
		self.xp = nbt.get('exp', 0)
		self.active = nbt.get('active', False)
		self.rarity = nbt.get('tier', 'COMMON').lower()
		self.internal_name = nbt.get('type', 'BEE')
		self.level = level_from_xp_table(self.xp, pet_xp[self.rarity])
		self.name = pets[self.internal_name]['name']
		self.title = f'[Lvl {self.level}] {self.name}'
		self.xp_remaining = pet_xp[self.rarity][-1] - self.xp
		self.candy_used = nbt.get('candyUsed', 0)
		self.item = nbt.get('heldItem', None)
		if self.item:
			self.item = PetItem(self.item)
		self.stats = {stat: function(self.level) for stat, function in pets[self.internal_name]['stats'].items()}

	def __str__(self):
		return self.name

	def __repr__(self):
		return self.name

class PetItem:
	def __init__(self, internal_name):
		self.internal_name = internal_name
		self.name = ' '.join([
			s.capitalize() for s in
			re.sub('_COMMON|_UNCOMMON|_RARE|_EPIC|_LEGENDARY', '', internal_name[9:]).split('_')
		])
			
	def __str__(self):
		return self.name
		
	def __repr__(self):
		return self.name
		
	def apply(self, pet):
		name = self.name
		if name == 'Textbook':
			pet.stats['intelligence'] *= 2
		elif name == 'Hardened Scales':
			pet.stats['defense'] += 25
		elif name == 'Iron Claws':
			pet.stats['crit chance'] = int(pet.stats['crit chance'] * 1.4)
			pet.stats['crit damage'] = int(pet.stats['crit damage'] * 1.4)
		elif name == 'Sharpened Claws':
			pet.stats['crit damage'] += 15
		elif name == 'Big Teeth':
			pet.stats['crit chance'] += 5
		elif name == 'Lucky Clover':
			pet.stats['magic find'] += 7

class Stats:
	def __init__(self, dict={}):
		self._dict = dict
		self.multiplier = 1
		
	def __add__(self, other):
		self = Stats(self._dict.copy())
		if isinstance(other, Stats):
			for k, v in other:
				self[k] += v
		else:
			raise NotImplementedError
		return self
			
	def __sub__(self, other):
		self = Stats(self._dict.copy())
		if isinstance(other, Stats):
			for k, v in other:
				self[k] -= v
		else:
			raise NotImplementedError
		return self
		
	def __iadd__(self, other):
		if isinstance(other, Stats):
			for k, v in other._dict:
				self[k] += k
		else:
			raise NotImplementedError
			
	def __isub__(self, other):
		if isinstance(other, Stats):
			for k, v in other._dict:
				self[k] -= v
		else:
			raise NotImplementedError
			
	def __getitem__(self, key):
		if isinstance(key, str):
			return self._dict.get(key, 0) * self.multiplier
		else:
			raise TypeError
			
	def __setitem__(self, key, value):
		if isinstance(value, (int, float)):
			self._dict[key] = value
		else:
			raise ValueError
		
	def __str__(self):
		return str(self._dict)
		
	def __repr__(self):
		return str(self._dict)
		
	def __iter__(self):
		return ((k, v * self.multiplier) for k, v in self._dict.items())

class ApiInterface:
	def __next_key__(self):
		self.__key_id__ += 1
		if self.__key_id__ == len(self._api_keys):
			self.__key_id__ = 0
		return self._api_keys[self.__key_id__]

	async def __call_api__(self, api, **kwargs):
		kwargs['key'] = self.__next_key__()
		url = f'https://api.hypixel.net{api}'

		try:
			async with (await session()).get(url, params=kwargs) as data:
				data = await data.json(content_type=None)

				if data['success']:
					return data

				elif data['cause'] == 'Invalid API key!':
					raise APIKeyError(kwargs["key"], f'Invalid API key!')

				else:
					raise ExternalAPIError(data['cause'])

		except asyncio.TimeoutError:
			return await self.__call_api__(api, **kwargs)

		except aiohttp.client_exceptions.ClientResponseError as e:
			if e.code == 403:
				raise HypixelError(f'Your request to {url} was not granted')
				
			elif e.code == 429:
				raise HypixelError('You are being ratelimited')

			elif e.code == 500:
				raise HypixelError('Hypixel\'s servers could not complete your request')
		
			elif e.code == 502:
				raise HypixelError('Hypixel\'s API is currently not working. Please try again in a few minutes.')

			else:
				raise e from None

	async def __new__(cls, keys, *args, **kwargs):
		instance = super().__new__(cls)

		if isinstance(keys, str):
			instance._api_keys = [keys]
		else:
			instance._api_keys = keys

		instance.__key_id__ = 0

		await instance.__init__(*args, **kwargs)
		return instance

class Player(ApiInterface):
	"""A class representing a Skyblock player.
	Instantiate the class with Player(api_key, username) or Player(api_key, uuid)
	Use profiles() and set_profile() to retrieve and define all the profile data.
	Use weapons() and set_weapon() to retrieve and set the player's weapon."""

	async def __init__(self, *, uname=None, uuid=None, guild=False, _profiles=None, _achivements=None):
		if uname and uuid:
			self.uname, self.uuid = await fetch_uuid_uname(uuid)
		elif uname:
			self.uname, self.uuid = await fetch_uuid_uname(uname)
		elif uuid:
			self.uname, self.uuid = await fetch_uuid_uname(uuid)
		else:
			raise DataError('You need to provide either a minecraft username or uuid!')

		if _profiles and _achivements:
			self.profiles = _profiles
			self.achievements = _achivements
		else:
			try:
				self.profiles = {}
				player = await self.__call_api__('/player', uuid=self.uuid)
				profile_ids = player['player']['stats']['SkyBlock']['profiles']

				self.achievements = player['player']['achievements']

				for k, v in profile_ids.items():
					self.profiles[v['cute_name']] = k

			except (KeyError, TypeError):
				raise NeverPlayedSkyblockError(self.uname) from None
			if not self.profiles:
				raise NeverPlayedSkyblockError(self.uname)

		if guild:
			id = (await self.__call_api__('/findGuild', byUuid=self.uuid))['guild']
			if id:
				self.guild_id = id
				self.guild_info = (await self.__call_api__('/guild', id=self.guild_id))['guild']
				self.guild = self.guild_info['name']
			else:
				self.guild_id = None
				self.guild_info = None
				self.guild = None

		self._profile_set = False

	def __str__(self):
		return self.uname

	def __repr__(self):
		return self.uname

	def avatar(self, size=None):
		if size:
			return f'https://mc-heads.net/avatar/{self.uuid}/{size}'
		else:
			return f'https://mc-heads.net/avatar/{self.uuid}'

	async def set_profile_automatically(self, attribute=lambda player: player.total_slayer_xp, threshold=None):
		"""Sets a player profile automatically
		<attribute> is a function that takes a <Player> class and returns whatever value you want to set it based on
		example: player.set_profile_automatically(lambda player: player.skill_xp['combat'])"""
		best = None
		max = 0

		async def create_canidate(profile):
			player = await Player(
				self._api_keys,
				uname=self.uname,
				uuid=self.uuid,
				_profiles=self.profiles,
				_achivements=self.achievements
			)
			await player.set_profile(profile)
			return player

		profile_ids = list(self.profiles.values())

		if threshold:
			best = profile_ids[0]
			for profile in reversed(profile_ids):
				try:
					canidate = await create_canidate(profile)
				except HypixelError:
					continue

				if attribute(canidate) >= threshold:
					best = profile
					break
		else:
			for canidate in asyncio.as_completed([create_canidate(profile) for profile in profile_ids]):
				try:
					canidate = await canidate
					current = attribute(canidate)
					if best is None or current > max:
						max = current
						best = canidate.profile
				except HypixelError:
					pass

		await self.set_profile(best)

	@staticmethod
	def _parse_inventory(v, *path):
		try:
			result = v
			for key in path:
				result = result[key]
			return decode_inventory_data(result)
		except KeyError:
			return []

	@staticmethod
	def _parse_collection(v, data):
		try:
			tuples = []
			for s in v[data]:
				temp = re.split('_(?!.*_)', s, maxsplit=1)
				temp[1] = int(temp[1])
				tuples.append(temp)
			dictionary = {}
			for s in set(name for name, level in tuples):
				max = 0
				for name, level in tuples:
					if name == s and level > max:
						max = level
				dictionary[s.lower().replace('_', ' ')] = max
			return dictionary
		except KeyError:
			return {}

	async def set_profile(self, profile):
		"""Sets a player's profile based on the provided profile ID"""
		
		if self._profile_set == True:
			raise DataError('This player already has their profile set!')
		self._profile_set = True

		self.profile = profile
		for cute_name, id in self.profiles.items():
			if id == profile:
				self.profile_name = cute_name
				break
		else:
			raise DataError('Bad profile ID!')

		self._nbt = (await self.__call_api__('/skyblock/profile', profile=self.profile))['profile']
		self.enabled_api = {'skills': False, 'collection': False, 'inventory': False, 'banking': False}
		
		v = self._nbt['members'][self.uuid]
		
		#Loads all of a player's pets
		self.pets = []
		self.pet = None
		if 'pets' in v:
			for data in v['pets']:
				pet = Pet(data)
				self.pets.append(pet)
				if pet.active:
					self.pet = pet
					
		#Loads all of a player's inventories
		self.inventory = Player._parse_inventory(v, 'inv_contents', 'data')
		self.echest = Player._parse_inventory(v, 'ender_chest_contents', 'data')
		self.weapons = [item for item in self.inventory + self.echest if item.type in ('sword', 'bow', 'fishing rod')]
		self.candy_bag = Player._parse_inventory(v, 'candy_inventory_contents', 'data')
		self.talisman_bag = Player._parse_inventory(v, 'talisman_bag', 'data')
		self.potion_bag = Player._parse_inventory(v, 'potion_bag', 'data')
		self.fish_bag = Player._parse_inventory(v, 'fishing_bag', 'data')
		self.quiver = Player._parse_inventory(v, 'quiver', 'data')
		self.armor = {'helmet': None, 'chestplate': None, 'leggings': None, 'boots': None}
		for armor in Player._parse_inventory(v, 'inv_armor', 'data'):
			self.armor[armor.type] = armor

		if self.inventory or self.echest or self.talisman_bag:
			self.enabled_api['inventory'] = True

		self.talismans = [talisman for talisman in self.inventory + self.talisman_bag if talisman.type == 'accessory']

		for talisman in self.talismans:
			talisman.active = True
			# Check for duplicate talismans
			if self.talismans.count(talisman) > 1:
				talisman.active = False
				continue

			# Check for talisman families
			if talisman.internal_name in tiered_talismans:
				for other in tiered_talismans[talisman.internal_name]:
					if other in self.talismans:
						talisman.active = False
						break
						
		#Loads a player's minion slots and collections
		try:
			self.collections = {name.lower().replace('_', ' '): level for name, level in v['collection'].items()}
			self.enabled_api['collection'] = True

		except KeyError:
			self.collections = {}

		self.unlocked_collections = Player._parse_collection(v, 'unlocked_coll_tiers')
		self.minions = Player._parse_collection(v, 'crafted_generators')

		self.unique_minions = max(
			self.achievements.get('skyblock_minion_lover', 0),
			sum(self.minions.values())
		)

		self.minion_slots = level_from_xp_table(self.unique_minions, minion_slot_requirements)
		
		#Loads a player's skill and slayer data
		if 'experience_skill_farming' in v:
			self.enabled_api['skills'] = True

			self.skill_xp = {}
			self.skills = {}

			for skill in skills:
				xp = int(v.get(f'experience_skill_{skill}', 0))
				self.skill_xp[skill] = xp
				self.skills[skill] = level_from_xp_table(
					xp,
					runecrafting_xp_requirements if skill == 'runecrafting' else skill_xp_requirements
				)
		else:
			self.enabled_api['skills'] = False

			self.skill_xp = {
				'carpentry': 0,
				'runecrafting': 0
			}
			self.skills = {
				'carpentry': 0,
				'runecrafting': 0
			}

			for skill, achievement in [
					('farming', 'skyblock_harvester'),
					('mining', 'skyblock_excavator'),
					('foraging', 'skyblock_gatherer'),
					('combat', 'skyblock_combat'),
					('enchanting', 'skyblock_augmentation'),
					('alchemy', 'skyblock_concoctor'),
					('fishing', 'skyblock_angler'),
					('taming', '')
				]:

				level = self.achievements.get(achievement, 0)
				self.skills[skill] = level
				self.skill_xp[skill] = 0 if level == 0 else skill_xp_requirements[level - 1]

		self.skill_average = sum(self.skills[skill] for skill in skills if skill not in cosmetic_skills) / (len(skills) - len(cosmetic_skills))

		self.slayer_xp = {}
		self.slayers = {}
		for slayer in slayers:
			xp = v.get('slayer_bosses', {}).get(slayer, {}).get('xp', 0)
			self.slayer_xp[slayer] = xp
			self.slayers[slayer] = level_from_xp_table(xp, slayer_level_requirements[slayer])

		self.total_slayer_xp = sum(self.slayer_xp.values())

		#Loads a player's kills and deaths
		self.kills = int(v.get('stats', {'kills': 0}).get('kills', 0))
		self.specifc_kills = {name.replace('kills_', '').replace('_', ' '): int(amount)
							  for name, amount in v['stats'].items() if re.match('kills_', name)}
		self.deaths = int(v.get('stats', {'deaths': 0}).get('deaths', 0))
		self.specifc_deaths = {name.replace('deaths_', '').replace('_', ' '): int(amount)
							   for name, amount in v['stats'].items() if re.match('deaths_', name)}

		#Loads a player's bank balance and purse
		if 'banking' in self._nbt:
			self.enabled_api['banking'] = True
			self.bank_balance = float(self._nbt['banking'].get('balance', 0))
		else:
			self.bank_balance = 0

		self.purse = float(self._nbt['members'][self.uuid].get('coin_purse', 0))

		#Loads a player's misc stats
		self.join_date = datetime.fromtimestamp(v.get('first_join', 0) / 1000.0)
		self.fairy_souls = v.get('fairy_souls', 0)
		
		#Loads a player's numeric stats
		self.stats = Stats(base_stats)
		
		for slayer, level in self.slayers.items():
			self.stats += Stats(slayer_rewards[slayer][level])
			
		for skill, level in self.skills.items():
			self.stats += Stats(skill_rewards[skill][level])
			
		self.stats['health'] += fairy_soul_hp_bonus[self.fairy_souls]
		self.stats['defense'] += self.fairy_souls // 5 + self.fairy_souls // 25
		self.stats['strength'] += self.fairy_souls // 5 + self.fairy_souls // 25
		self.stats['speed'] += self.fairy_souls // 50

	async def is_online(self):
		player_data = (await self.__call_api__('/player', name=self.uname))['player']
		return player_data['lastLogout'] < player_data['lastLogin']

	def talisman_counts(self):
		counts = {'common': 0, 'uncommon': 0, 'rare': 0, 'epic': 0, 'legendary': 0}
		for tali in self.talismans:
			if tali.active:
				counts[tali.rarity] += 1
		return counts

	async def auctions(self):
		r = await self.__call_api__('/skyblock/auction', uuid=self.uuid, profile=self.profile)

		return [
			{
				'item': decode_inventory_data(auction['item_bytes']['data'])[0],
				'start': auction['start'],
				'end': auction['end'],
				'starting_bid': auction['starting_bid'],
				'highest_bid': auction['highest_bid_amount'],
				'bids': auction['bids'],
				'buyer': auction['bids'][-1]['bidder'] if auction['bids'] else None
			}
			for auction in r['auctions']
			if auction['claimed'] is False
		]
