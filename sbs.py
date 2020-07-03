import concurrent.futures
from aiohttp import ClientError
import random
import re
import itertools
import traceback
import math
import asyncio
import discord
import os
import skypy.skypy as skypy
from optimizer import damage_optimizer, ehp_optimizer, mastiff_ehp_optimizer, intelligence_optimizer, speed_optimizer

if os.environ.get('API_KEY') is None:
	import dotenv
	dotenv.load_dotenv()

keys = os.getenv('API_KEY').split()
prefix = os.getenv('TOKEN', 'sbs')

class EndSession(Exception):
	def __init__(self, message=''):
		self.message = message

	def __str__(self):
		return self.message

damage_potions = {
	'critical': {
		'stats': {'crit chance': [0, 10, 15, 20, 25], 'crit damage': [0, 10, 20, 30, 40]},
		'levels': [0, 3, 4]
	},
	'strength': {
		# Assume cola
		'stats': {'strength': [0, 5.25, 13.125, 21, 31.5, 42, 52.5, 63, 78.75]},
		'levels': [0, 5, 6, 7, 8]
	},
	'spirit': {
		'stats': {'crit damage': [0, 10, 20, 30, 40]},
		'levels': [0, 3, 4]
	},
	'archery': {
		'stats': {'enchantment modifier': [0, 17.5, 30, 55, 80]},
		'levels': [0, 3, 4]
	}
}

ehp_potions = {
	'strength': {
		# Assume tea
		'stats': {'defense': [0, 5.5, 11, 16.5, 22, 33, 44, 55, 66]},
		'levels': [0, 5, 6, 7, 8]
	}
}

orbs = {
	'weird tuba': {
		'internal': 'WEIRD_TUBA',
		'stats': {'strength': 30}
	},
	'mana flux': {
		'internal': 'MANA_FLUX_POWER_ORB',
		'stats': {'strength': 10}
	},
	'overflux': {
		'internal': 'OVERFLUX_POWER_ORB',
		'stats': {'strength': 25}
	}
}

profile_emojis = {
	'Apple': '🍎',
	'Banana': '🍌',
	'blueberry': '🔵',
	'Coconut': '🥥',
	'Cucumber': '🥒',
	'Grapes': '🍇',
	'Kiwi': '🥝',
	'Lemon': '🍋',
	'Lime': '🍏',
	'Mango': '🥭',
	'orange': '🍊',
	'Papaya': '🍈',
	'Peach': '🍑',
	'Pear': '🍐',
	'Pineapple': '🍍',
	'Pomegranate': '👛',
	'Raspberry': '🍒',
	'Strawberry': '🍓',
	'Tomato': '🍅',
	'Watermelon': '🍉',
	'Zucchini': '🥬'
}

number_emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

# list of all enchantment powers per level. can be a function or a number
enchantment_effects = {
	# sword always
	'sharpness': 5,
	'giant_killer': lambda level: 25 if level > 0 else 0,
	# sword sometimes
	'smite': 8,
	'bane_of_arthropods': 8,
	'first_strike': 25,
	'ender_slayer': 12,
	'cubism': 10,
	'execute': 10,
	'impaling': 12.5,
	# bow always
	'power': 8,
	# bow sometimes
	'dragon_hunter': 8,
	'snipe': 5,	 # Would be lower except I only use this for drags and magma bosses
	# rod always
	'spiked_hook': 5
}

# list of relevant enchants for common mobs
relavant_enchants = {
	'slayer bosses': [
		'giant_killer',
		'sharpness',
		'power',
		'spiked_hook',
		'smite',
		'bane_of_arthropods',
		'execute'
	],
	'zealots': [
		'giant_killer',
		'sharpness',
		'power',
		'spiked_hook',
		'ender_slayer',
		'first_strike'
	],
	'base': [
		'giant_killer',
		'sharpness',
		'first_strike',
		'power',
		'spiked_hook'
	]
}

close_message = '\n> _use **exit** to close the session_'

pet_emojis = {
	'SKELETON_HORSE': '🦓',
	'SNOWMAN': '⛄',
	'BAT': '🦇',
	'SHEEP': '🐑',
	'CHICKEN': '🐔',
	'WITHER_SKELETON': '🏴‍☠️',
	'SILVERFISH': '🐁',
	'RABBIT': '🐇',
	'HORSE': '🐴',
	'PIGMAN': '🐽',
	'WOLF': '🐺',
	'OCELOT': '🐆',
	'LION': '🦁',
	'ENDER_DRAGON': '🐲',
	'GUARDIAN': '🛡️',
	'ENDERMAN': '😈',
	'blue_WHALE': '🐳',
	'GIRAFFE': '🦒',
	'PHOENIX': '🐦',
	'BEE': '🐝',
	'MAGMA_CUBE': '🌋',
	'FLYING_FISH': '🐟',
	'SQUID': '🦑',
	'PARROT': '🦜',
	'TIGER': '🐯',
	'TURTLE': '🐢',
	'SPIDER': '🕷️',
	'BLAZE': '🔥',
	'JERRY': '🤡',
	'PIG': '🐽',
	'BLACK_CAT': '🐱',
	'JELLYFISH': '🎐',
	'MONKEY': '🐒',
	'ELEPHANT': '🐘',
	'ZOMBIE': '🧟',
	'SKELETON': '💀',
	'ENDERMITE': '🦠',
	'ROCK': '🥌',
	'DOLPHIN': '🐬',
	'HOUND': '🐶',
	'GHOUL': '🧟‍♀️',
	'TARANTULA': '🕸️',
	'GOLEM': '🗿'
}

class Embed(discord.Embed):
	nbst = '\u200b'

	def __init__(self, channel, *, user=None, **kwargs):
		self.channel = channel
		self.user = user

		super().__init__(
			color=self.color(channel),
			**kwargs
		)

	@staticmethod
	def color(channel):
		default = 0xbf2158

		if hasattr(channel, 'guild'):
			color = channel.guild.me.color
			return discord.Color(default) if color == 0x000000 else color
		else:
			return discord.Color(default)

	def add_field(self, *, name, value, inline=True):
		return super().add_field(name=f'**{name}**' if name else self.nbst, value=value or self.nbst, inline=inline)

	def set_image(self, url):
		return super().set_image(url=url)

	async def send(self):
		return await self.channel.send(self.user.mention if self.user else None, embed=self)


def format_pet(pet):
	"""Returns a pretty string repersenting a pet"""
	return f'{pet.title} |{pet.rarity.upper()}|' if pet else ''


white = ('', '')
gray = ('bf', '')
puke = ('css', '')
green = ('yaml', '')
blue = ('md', '#')
yellow = ('fix', '')
orange = ('glsl', '#')
red = ('diff', '-')
rarity_colors = {'common': gray, 'uncommon': green, 'rare': blue, 'epic': orange, 'legendary': yellow, 'mythic': red}


def colorize(s, color):
	language, point = color
	s = str(s)

	if s:
		return f'```{language}\n{point}' + s.replace('\n', f'\n{point}') + '\n```'
	else:
		return ''


def chunks(lst, n):
	"""Yield successive n-sized chunks from lst."""
	lst = list(lst)
	for i in range(0, len(lst), n):
		yield lst[i:i + n]
		
class Bot(discord.AutoShardedClient):
	def __init__(self, *args, **kwargs):
		self.callables = {}
		self.commands = {
			'bot': {
				'emoji': '🤖',
				'desc': 'View bot stats, visit the support server, and other status commands',
				'commands': {
					'stats': {
						'function': self.stats,
						'desc': 'Displays stats about the bot including number of servers and users'
					},
					'help': {
						'function': self.help,
						'desc': 'Opens the menu that you are looking at now'
					},
					'support': {
						'function': self.support_server,
						'desc': 'Have an question about the bot? Use this command'
					}
				}
			},
			'damage': {
				'emoji': '💪',
				'desc': 'A collection of tools designed to optimize your damage and talismans',
				'commands': {
					'optimizer': {
						'function': self.optimize_reforges,
						'desc': 'Optimizes your talismans to their best reforges',
						'session': True
					},
					'missing': {
						'args': '[username] (profile)',
						'function': self.view_missing,
						'desc': 'Displays a list of your missing talismans. Also displays inactive/unnecessary talismans if you have them'
					}
				}
			}
		}
		self.hot_channels = {}
		self.ready = False
		self.args_message = '`[] signifies a required argument, while () signifies an optional argument`'

		super().__init__(*args, **kwargs)

	async def log(self, *args):
		print(*args, sep='')

	async def on_error(self, *args, **kwargs):
		error = traceback.format_exc().replace('```', '"""')
		await self.get_user(270352691924959243).send(f'```{error[-1950:]}```')
		print(error)

	async def on_ready(self):
		await self.log(f'Logged on as {self.user}!')

		for data in self.commands.values():
			self.callables.update(data['commands'])

		await self.change_presence(activity=discord.Game(f'| 🍤 {prefix} help'))

		self.ready = True

	async def on_message(self, message):
		if self.ready is False:
			return

		user = message.author

		if user.bot:
			return

		channel = message.channel
		dm = channel.type == discord.ChannelType.private

		if channel in self.hot_channels and self.hot_channels[channel] == user:
			return

		command = message.content[1:] if message.content.startswith('!') else message.content

		if command == f'<@!{self.user.id}>' or command == f'<@{self.user.id}>':
			await self.help(message)
			return

		command = re.split('\s+', command)
		command[0] = command[0].lower()
		if command[0] == f'<@!{self.user.id}>' or command[0] == f'<@{self.user.id}>':
			command = command[1:]
		elif command[0] == prefix:
			command = command[1:]
		elif not dm:
			return

		if not command:
			return

		name = command[0].lower()
		args = command[1:]

		if name not in self.callables:
			return

		data = self.callables[name]
		security = data['security'] if 'security' in data else 0
		session = 'session' in data and data['session']
		function = data['function']

		if session and channel in self.hot_channels:
			await channel.send(
				f'{user.mention} someone else is currently using me in this channel! Try sending me a DM with your command instead')
			return

		if security == 1 and not channel.permissions_for(user).manage_messages:
			await channel.send(
				f'{user.mention} you do not have permission to use this command here! Try using it on your own discord server')
			return

		await self.log(f'{str(user)} used {name} {args} in {"a DM" if dm else channel.guild.name}')

		if session:
			self.hot_channels[channel] = user

		error = None

		try:
			await function(message, *args)
		except EndSession:
			await channel.send(f'{user.mention} session closed')
		except skypy.NeverPlayedSkyblockError:
			await Embed(
				channel,
				user=user,
				title='No Profiles!',
				description='This user has never played Skyblock'
			).send()
		except skypy.BadGuildError as e:
			await Embed(
				channel,
				user=user,
				description=f'Invalid guild name: {e.guild}'
			).send()
		except skypy.BadNameError as e:
			await Embed(
				channel,
				user=user,
				description=f'Invalid username: {e.uname_or_uuid}'
			).send()
		except skypy.HypixelError:
			await Embed(
				channel,
				user=user,
				title='Hypixel API Error!',
				description='The Hypixel API did not respond to your command'
			).set_footer(
				text='This error usually goes away after about a minute.\nIf not, the Hypixel API is down'
			).send()
		except skypy.ExternalAPIError as e:
			await Embed(
				channel,
				user=user,
				title='API Error!',
				description=str(e)
			).send()
		except discord.errors.Forbidden as e:
			if channel.permissions_for(channel.guild.me).send_messages:
				if channel.permissions_for(channel.guild.me).embed_links:
					await Embed(
						channel,
						user=user,
						title='Insufficient Permissions',
						description='I do not have permissions to do this. Try enabling your DMS or giving me admin'
					).send()
				else:
					await channel.send(
						'Insufficient Permissions: I do not have permissions to do this. Try enabling your DMS or giving me admin')
		except Exception as e:
			await Embed(
				channel,
				user=user,
				title='Error!',
				description='Something terrible happened while running your command\n'
				'The error has been automatically reported to SBS devs'
			).send()
			error = e

		if session:
			self.hot_channels.pop(channel)

		if error:
			raise error from None

	async def args_to_player(self, user, channel, *args):
		player = await skypy.Player(keys, uname=args[0])

		if len(args) == 1:
			await player.set_profile_automatically()
		else:
			try:
				await player.set_profile(player.profiles[args[1].capitalize()])
			except KeyError:
				await channel.send(f'{user.mention} invalid profile!')
				return None

		# await update_top_players(player)

		return player

	async def no_args(self, command, user, channel):
		data = self.callables[command]
		usage = f'sbs {command} {data["args"]}' if 'args' in data else command

		await Embed(
			channel,
			user=user,
			title='This command requires arguments!',
			description=f'Correct usage is `{usage}`\n{self.args_message}'
		).send()

	@staticmethod
	async def unimplemented(message):
		await message.channel.send(f'{message.author.mention} this command is unimplemented')

	async def optimize_reforges(self, message, *args):
		user = message.author
		channel = message.channel

		optimizers = [
			{'emoji': '💯', 'name': 'perfect crit chance', 'potions': damage_potions},
			{'emoji': '💥', 'name': 'maximum damage', 'potions': damage_potions},
			{'emoji': '🛡️', 'name': 'effective health', 'potions': ehp_potions},
			{'emoji': '🧠', 'name': 'intelligence', 'text': intelligence_optimizer},
			{'emoji': '💨', 'name': 'speed', 'text': speed_optimizer}
		]

		embed = Embed(
			channel,
			user=user,
			title='What would you like to optimize for?'
		).add_field(
			name=None,
			value='\n\n'.join(f'> {o["emoji"]}\n`{o["name"]}`' for o in optimizers)
		).set_footer(
			text='Effective health is a way to measure your\ntotal survivablity by combining health and defense'
		)

		optimizer = await self.reaction_menu(await embed.send(), user, {o['emoji']: o for o in optimizers})

		blacksmith = await self.reaction_menu(await Embed(
			channel,
			user=user,
			title='Select Reforge Prices'
		).add_field(
			name=None,
			value='> 🔨\n`only optimize with reforges`\n`from the blacksmith`\n\n> 🌈\n`include all reforges`'
		).send(), user, {'🔨': True, '🌈': False})

		if 'text' in optimizer:
			split = '``````'.join(optimizer['text'](blacksmith).split('\n'))
			await Embed(
				channel,
				user=user,
				title=f'Best {optimizer["name"].capitalize()} Reforges'
			).add_field(
				name=None,
				value=f'```{split}```'
			).send()
			return

		valid = False
		while valid is False:
			await Embed(
				channel,
				user=user,
				title=f'What is your Minecraft Username?'
			).send()
			msg = await self.respond(user, channel)

			msg = msg.content.lower()

			player = await skypy.Player(keys, uname=msg)
			if len(player.profiles) == 0:
				await embed(
					channel,
					user=user,
					title=f'{user.name}, the Hypixel API has returned invalid information'
				).add_field(
					name=None,
					value='This is a bug with Hypixel API. Retry after 30 seconds'
				).send()
				return

			else:
				valid = True

		if len(player.profiles) == 1:
			await player.set_profile(list(player.profiles.values())[0])

		else:
			embed = Embed(
				channel,
				user=user,
				title='Which profile would you like to use?',
				description='**[Sorted by date created]**'
			).add_field(
				name=None,
				value='\n\n'.join(f'> {profile_emojis[profile]}\n`{profile}`' for profile in player.profiles.keys())
			)

			result = await self.reaction_menu(await embed.send(), user, {profile_emojis[profile]: profile for profile in player.profiles.keys()})
			await player.set_profile(player.profiles[result])

		if player.enabled_api['skills'] is False or player.enabled_api['inventory'] is False:
			await self.api_disabled(f'{user.name}, your API is disabled!', channel, user)
			return

		talisman_counts = {'common': 0, 'uncommon': 0, 'rare': 0, 'epic': 0, 'legendary': 0, 'mythic': 0}
		for tali in player.talismans:
			if tali.active:
				talisman_counts[tali.rarity] += 1

		if optimizer['name'] == 'effective health' and player.armor == {'boots': 'MASTIFF_BOOTS', 'chestplate': 'MASTIFF_CHESTPLATE', 'helmet': 'MASTIFF_HELMET', 'leggings': 'MASTIFF_LEGGINGS'}:
			split = '``````'.join(mastiff_ehp_optimizer(blacksmith).split('\n'))
			await Embed(
				channel,
				user=user,
				title=f'Best Effective Health Reforges with Mastiff'
			).add_field(
				name=None,
				value=f'```{split}```'
			).send()
			return

		if len(player.weapons) == 0:
			await channel.send(f'{user.mention}, you have `no weapons` in your inventory')
			return

		if len(player.weapons) == 1:
			weapon = player.weapons[0]
		else:
			valid = False

			while valid is False:
				await Embed(
					channel,
					user=user,
					title='Which weapon would you like to use?'
				).set_footer(
					text='You may use either the weapon name or the weapon number'
				).add_field(
					name=None,
					value=''.join([f'```{i + 1} > ' + weapon.name + '```' for i, weapon in enumerate(player.weapons)])
				).send()

				msg = (await self.respond(user, channel)).content.lower()

				names = [weapon.name.lower() for weapon in player.weapons]

				if msg in names:
					weapon = player.weapons[names.index(msg)]
					valid = True
				else:
					try:
						weapon = player.weapons[int(msg) - 1]
						valid = True
					except (IndexError, TypeError, ValueError):
						await channel.send(f'Invalid weapon! Did you make a typo?{close_message}')
						
		player.set_weapon(weapon)

		pet = player.pet

		embed = Embed(
			channel,
			user=user,
			title='Is this the correct equipment?'
		).add_field(
			name='⚔️\tWeapon',
			value=f'```{weapon.name}```',
			inline=False
		).add_field(
			name=f'{pet_emojis[pet.internal_name] if pet else "🐣"}\tPet',
			value=f'```{format_pet(pet) if pet else None}```',
			inline=False
		).add_field(
			name='💎\tPet Item',
			value=f'```{pet.item_name if pet else None}```',
			inline=False
		).add_field(
			name='⛑️\tHelmet',
			value=f'```{player.armor["helmet"]}```',
			inline=False
		).add_field(
			name='👚\tChestplate',
			value=f'```{player.armor["chestplate"]}```',
			inline=False
		).add_field(
			name='👖\tLeggings',
			value=f'```{player.armor["leggings"]}```',
			inline=False
		).add_field(
			name='👞\tBoots',
			value=f'```{player.armor["boots"]}```',
			inline=False
		)

		embed.add_field(
			name='🏺\tTalismans',
			value=''.join(
				colorize(f'{amount} {name.capitalize()}', rarity_colors[name])
				for name, amount in talisman_counts.items()
			)
		)

		if not await self.yesno(await embed.send(), user):
			await channel.send(f'{user.mention} session ended')
			return

		for name, pot in optimizer['potions'].items():
			buff = pot['stats']
			levels = pot['levels']

			if weapon.type != 'bow' and name == 'archery':
				continue

			msg = await channel.send(f'{user.mention} what level of `{name} potion` do you use?')

			emojis = {number_emojis[level]: level for level in levels}

			level = await self.reaction_menu(msg, user, emojis)

			for name1, amount in buff.items():
				player.stats.__iadd__(name1, amount[level])

		if optimizer['name'] in ('perfect crit chance', 'maximum damage'):
			for name, orb in orbs.items():
				internal_name = orb['internal']
				buff = orb['stats']

				if internal_name in player.inventory or internal_name in player.echest:
					msg = await channel.send(f'{user.mention} will you be using your `{name}`?')
					yn = await self.yesno(msg, user)

					if yn is True:
						for name, amount in buff.items():
							player.stats.__iadd__(name, amount)
			
			include_attack_speed = await self.yesno(await Embed(
				channel,
				user=user,
				title='Do you want to include attack speed?'
			).send(), user)

			for enchantment in relavant_enchants['zealots']:
				if enchantment in weapon.enchantments:
					value = enchantment_effects[enchantment]
					if callable(value):
						player.stats.__iadd__('enchantment modifier', value(weapon.enchantments[enchantment]))
					else:
						player.stats.__iadd__('enchantment modifier', value * weapon.enchantments[enchantment])
		
			await channel.send(str(damage_optimizer(
				player,
				perfect_crit_chance=optimizer['name'] == 'perfect crit chance',
				include_attack_speed=include_attack_speed,
				only_blacksmith_reforges=blacksmith
			)))
		else:
			await channel.send(str(
				ehp_optimizer(player, talisman_counts, armor_counts, only_blacksmith_reforges=blacksmith)
			))

	async def view_missing(self, message, *args):
		user = message.author
		channel = message.channel

		if not args:
			await self.no_args('missing', user, channel)
			return

		player = await self.args_to_player(user, channel, *args)

		if player.enabled_api['inventory'] is False:
			await self.api_disabled(f'{player.uname}, your inventory API is disabled on {player.profile_name.title()}!', channel, user)
			return

		talismans = skypy.talismans.copy()
		for talisman in player.talismans:
			if talisman.active:
				for regex in skypy.talismans.keys():
					if regex.match(talisman.internal_name):
						talismans.pop(regex)

		embed = Embed(
			channel,
			user=user,
			title=f'{user.name}, you are missing {len(talismans)}/{len(skypy.talismans)} talisman{"" if len(talismans) == 1 else "s"}!',
			description='Only counting talismans in your bag or inventory'
		)

		if talismans:
			embed.add_field(
				name='[Roughly sorted by price]',
				value='```' + '\n'.join(talismans.values()) + '```',
				inline=False
			)

		inactive = [talisman for talisman in player.talismans if talisman.active is False and talisman.internal_name != 'PERSONAL_COMPACTOR_6000']

		if inactive:
			embed.add_field(
				name=f'You also have {len(inactive)} unnecessary talismans',
				value='```' + '\n'.join(map(str, inactive)) + '``````An unnecessary talisman is any talisman is\nduplicated or part of a talisman family```'
			)

		await embed.send()

	async def help(self, message, *args):
		user = message.author
		channel = message.channel

		dm = user.dm_channel or await user.create_dm()

		embed = Embed(
			dm,
			user=user,
			title='Skyblock Simplified',
			description='Welcome to Skyblock Simplified, a Skyblock bot designed to streamline gameplay\n[Click me to invite the bot to your server!](https://discord.com/oauth2/authorize?client_id=671040150251372569&permissions=8&scope=bot)\n'
						f'**React to this message with any of the emojis to view commands**\n{self.args_message}\n'
		).set_footer(
			text='Skyblock Simplified for Hypixel Skyblock | Created by notnotmelon#7218'
		)

		for category, data in self.commands.items():
			embed.add_field(
				name=f'{data["emoji"]}	{category}',
				value=f'```{data["desc"]}```'
			)

		boxes = {}
		for category, data in self.commands.items():
			category_data = self.commands[category]

			def command_desc(name, data):
				security = data['security'] if 'security' in data else 0
				args = f' {data["args"]}' if 'args' in data else ''

				moderators = "\n\t*Can only be used by moderators*" if security == 1 else ""
				return f'> {self.user.mention} {name}{args}\n{data["desc"]}{moderators}'

			boxes[data['emoji']] = Embed(
				dm,
				user=user,
				title=category.capitalize(),
				description=f'{self.args_message}\n```{category_data["desc"]}```'
			).add_field(
				name=None,
				value='\n\n'.join([command_desc(name, data) for name, data in category_data['commands'].items()])
			).set_footer(
				text='Skyblock Simplified for Hypixel Skyblock | Created by notnotmelon#7218'
			)

		if channel.type != discord.ChannelType.private:
			await channel.send(f'Sent you a DM with the information {user.mention}!')

		while True:
			msg = await embed.send()

			box = await self.reaction_menu(msg, user, boxes)
			if await self.back(await box.send(), user) is False:
				return

	async def stats(self, message, *args):
		channel = message.channel
		user = message.author

		server_rankings = sorted(self.guilds, key=lambda guild: len(guild.members), reverse=True)[:10]
		server_rankings = f'{"Top Servers".ljust(28)} | Users\n' + '\n'.join(
			[f'{guild.name[:28].ljust(28)} | {len(guild.members)}' for guild in server_rankings])

		_embed = Embed(
			channel,
			user=user,
			title='Discord Stats',
			description=f'This Command was run on shard {(message.guild.shard_id if message.guild else 0) + 1} / {self.shard_count}\n```{server_rankings}```'
		).add_field(
			name='Servers',
			value=f'{self.user.name} is running in {len(self.guilds)} servers with {sum(len(guild.text_channels) for guild in self.guilds)} channels',
			inline=False
		).add_field(
			name='Users',
			value=f'There are currently {sum(len(guild.members) for guild in self.guilds)} users with access to the bot',
			inline=False
		)
		
		shards = [[0,0,0]] * self.shard_count
		for x in self.guilds:
			shards[x.shard_id][0] += 1
			shards[x.shard_id][1] += len(x.text_channels)
			shards[x.shard_id][2] += len(x.members)
			
		for x in range(self.shard_count):
			_embed.add_field(
				name=f'Shard {x + 1}',
				value=f'{shards[x][0]} servers\n{shards[x][1]} channels\n{shards[x][2]} members',
				inline=True
			)
		_embed.add_field(
			name='Latency',
			value=f'This message was delivered in {self.latency * 1000:.0f} milliseconds',
			inline=False
		)
		await _embed.send()

	async def respond(self, user, channel):
		msg = None

		try:
			msg = await self.wait_for('message', check=lambda message: message.author == user and message.channel == channel, timeout=60 * 3)
		except asyncio.TimeoutError:
			raise EndSession
		if msg.content.lower() == 'exit':
			raise EndSession

		return msg

	async def reaction_menu(self, message, user, reactions, edit=False):
		if edit:
			await message.clear_reactions()

		for reaction in reactions.keys():
			await message.add_reaction(reaction)

		check = lambda reaction, u: u == user and reaction.message.id == message.id and str(reaction) in reactions

		try:
			reaction, _ = await self.wait_for('reaction_add', check=check, timeout=45)
			return reactions[str(reaction)]
		except asyncio.TimeoutError:
			for reaction in reactions.keys():
				await message.remove_reaction(reaction, self.user)
			for reaction in ['🇹', '🇮', '🇲', '🇪', '🇴', '🇺', '✝️']:
				await message.add_reaction(reaction)
			raise EndSession

	async def back(self, message, user):
		return True if await self.reaction_menu(message, user, {'⬅️': True}) else False

	async def yesno(self, message, user):
		return await self.reaction_menu(message, user, {'✅': True, '❌': False})

	async def api_disabled(self, title, channel, user):
		await Embed(
			channel,
			user=user,
			title=title,
			description='Re-enable them with [skyblock menu > settings > api settings]'
		).set_footer(
			text='Sometimes this message appears even if your API settings are enabled. If so, exit Hypixel and try again. It\'s also possible that Hypixel\'s API servers are down'
		).send()

	async def support_server(self, message, *args):
		await Embed(
			message.channel,
			user=message.author,
			title='Here\'s a link to my support server',
			description='[https://discord.gg/sbs]'
		).set_footer(
			text='(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧'
		).send()

	async def invite(self, message, *args):
		await Embed(
			message.channel,
			user=message.author,
			title='Here\'s an invite link',
			description='[Click me to invite the bot](https://tinyurl.com/add-sbs)'
		).send()

discord.Embed = None  # Disable default discord Embed
