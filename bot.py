import concurrent.futures
from aiohttp import ClientError
import cloudscraper
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from statistics import mean, median, mode, pstdev, StatisticsError
import random
import re
import itertools
import motor.motor_asyncio
import traceback
import math
import asyncio
import discord
import os
import skypy
from constants import skills, cosmetic_skills

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

potions = {
	'critical': {
		'stats': {
			'crit chance': [0, 10, 15, 20, 25],
			'crit damage': [0, 10, 20, 30, 40]
		},
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
	'Blueberry': '🔵',
	'Coconut': '🥥',
	'Cucumber': '🥒',
	'Grapes': '🍇',
	'Kiwi': '🥝',
	'Lemon': '🍋',
	'Lime': '🍏',
	'Mango': '🥭',
	'Orange': '🍊',
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

max_book_levels = {
	'sharpness': 6,
	'giant_killer': 6,
	'smite': 7,
	'bane_of_arthropods': 6,
	'first_strike': 4,
	'ender_slayer': 6,
	'cubism': 5,
	'execute': 5,
	'impaling': 3,
	'power': 6,
	'dragon_hunter': 5,
	'snipe': 3,
	'spiked_hook': 6
}

max_book_levels_cheap = {
	'sharpness': 5,
	'giant_killer': 5,
	'smite': 5,
	'bane_of_arthropods': 5,
	'first_strike': 4,
	'ender_slayer': 5,
	'cubism': 5,
	'execute': 5,
	'impaling': 3,
	'power': 5,
	'dragon_hunter': 0,
	'snipe': 3,
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
	]
	'zealots': [
		'giant_killer',
		'sharpness',
		'power',
		'spiked_hook',
		'ender_slayer',
		'first_strike'
	]
}

RELEVANT_REFORGES = {
	'forceful': (None, None, (7, 0, 0), None, None),
	'itchy': ((1, 0, 3), (2, 0, 5), (2, 0, 8), (3, 0, 12), (5, 0, 15)),
	'strong': (None, None, (4, 0, 4), (7, 0, 7), (10, 0, 10)),
	'godly': ((1, 1, 1), (2, 2, 2), (4, 2, 3), (7, 3, 6), (10, 5, 8))
}
reforges_list = list(RELEVANT_REFORGES.values())

CLOSE_MESSAGE = '\n> _use **exit** to close the session_'

PET_EMOJIS = {
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
	'BLUE_WHALE': '🐳',
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

damage_reforges = {
	'sword': {
		'legendary': ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic'],
		'spicy': ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic'],
		'epic': ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic'],
		'odd': ['rare', 'epic', 'legendary', 'mythic'],
		'gentle': ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic'],
		'fast': ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic'],
		'fabled': ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic']
	},
	'bows': {
		'awkward': ['epic', 'legendary', 'mythic'],
		'fine': ['mythic'],
		'neat': ['uncommon', 'rare', 'epic', 'legendary', 'mythic'],
		'hasty': ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic'],
		'grand': ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic'],
		'rapid': ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic'],
		'deadly': ['uncommon', 'rare', 'epic', 'legendary', 'mythic'],
		'unreal': ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic']
	}
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


WHITE = ('', '')
GRAY = ('bf', '')
GREY = GRAY
PUKE = ('css', '')
GREEN = ('yaml', '')
BLUE = ('md', '#')
YELLOW = ('fix', '')
ORANGE = ('glsl', '#')
RED = ('diff', '-')
RARITY_COLORS = {'common': GREY, 'uncommon': GREEN, 'rare': BLUE, 'epic': ORANGE, 'legendary': YELLOW}


def colorize(s, color):
	language, point = color
	s = str(s)

	if s:
		return f'```{language}\n{point}' + s.replace('\n', f'\n{point}') + '\n```'
	else:
		return ''


def optimizer(opt_goal, player, weapon_damage, base_str, base_cc, base_cd):
	best = 0
	best_route = []
	best_str = 0
	best_cc = 0
	best_cd = 0

	stat_modifiers = player.stat_modifiers()
	str_mod = stat_modifiers.get('strength', lambda x: x)
	cc_mod = stat_modifiers.get('crit chance', lambda x: x)
	cd_mod = stat_modifiers.get('crit damage', lambda x, y: x)

	counts = player.talisman_counts()

	if opt_goal == 1 or cc_mod(base_cc) > 100:
		for c, u, r, e, l in itertools.product(
				*[Route.routes(counts[key], 4, rarity_num) for rarity_num, key in enumerate(counts.keys())]):
			strength = str_mod(base_str + c.strength + u.strength +
							   r.strength + e.strength + l.strength)
			crit_damage = cd_mod(
				base_cd + c.crit_damage + u.crit_damage + r.crit_damage + e.crit_damage + l.crit_damage, strength)

			d = (5 + weapon_damage + strength // 5) * \
				 (1 + strength / 100) * (1 + crit_damage / 100)

			if d > best:
				best = d
				best_route = [c, u, r, e, l]
				best_str = strength
				best_cc = cc_mod(
					base_cc + c.crit_chance + u.crit_chance + r.crit_chance + e.crit_chance + l.crit_chance)
				best_cd = crit_damage
	else:
		cc_mod = stat_modifiers.get('crit chance', None)
		if cc_mod:
			for c, u, r, e, l in itertools.product(
					*[Route.routes(counts[key], 4, rarity_num) for rarity_num, key in enumerate(counts.keys())]):
				crit_chance = cc_mod(
					base_cc + c.crit_chance + u.crit_chance + r.crit_chance + e.crit_chance + l.crit_chance) // 1
				if crit_chance >= 100:
					strength = str_mod(base_str + c.strength + u.strength +
									   r.strength + e.strength + l.strength)
					crit_damage = cd_mod(
						base_cd + c.crit_damage + u.crit_damage +
							r.crit_damage + e.crit_damage + l.crit_damage,
						strength)

					d = (5 + weapon_damage + strength // 5) * \
						 (1 + strength / 100) * (1 + crit_damage / 100)

					if d > best:
						best = d
						best_route = [c, u, r, e, l]
						best_str = strength
						best_cc = crit_chance
						best_cd = crit_damage
		else:
			for c, u, r, e, l in itertools.product(
					*[Route.routes(counts[key], 4, rarity_num) for rarity_num, key in enumerate(counts.keys())]):
				crit_chance = base_cc + c.crit_chance + u.crit_chance + \
					r.crit_chance + e.crit_chance + l.crit_chance
				if crit_chance >= 100:
					strength = str_mod(base_str + c.strength + u.strength +
									   r.strength + e.strength + l.strength)
					crit_damage = cd_mod(base_cd + c.crit_damage + u.crit_damage + r.crit_damage + e.crit_damage + l.crit_damage,
						strength)

					d = (5 + weapon_damage + strength // 5) * \
						 (1 + strength / 100) * (1 + crit_damage / 100)

					if d > best:
						best = d
						best_route = [c, u, r, e, l]
						best_str = strength
						best_cc = crit_chance
						best_cd = crit_damage

	return best, best_route, best_str, best_cc, best_cd


class Route:
	def __init__(self, talismans, rarity):
		self.strength, self.crit_chance, self.crit_damage = [
			sum(reforges_list[y][rarity][x] * talismans[y]
				for y in range(len(reforges_list)) if reforges_list[y][rarity])
			for x in range(3)
		]
		self.counts = talismans
		self.rarity = rarity
		self.rarity_str = ['common', 'uncommon', 'rare', 'epic', 'legendary'][self.rarity]

	def __str__(self):
		return ' ߸ '.join(f'{c} '
						  f'{"godly/zealous" if self.rarity < 2 and name == "godly" else name} '
						  f'{Route.rarity_grammar(self.rarity_str, c)}'
						  for name, c in zip(RELEVANT_REFORGES.keys(), self.counts) if c != 0)

	@staticmethod
	def routes(count, size, rarity):
		def helper(count, idx, current):
			if count == 0:
				yield Route(current, rarity)
			elif idx == size - 1:
				new = current.copy()
				new[idx] += count
				yield Route(new, rarity)
			else:
				if reforges_list[idx][rarity]:
					new = current.copy()
					new[idx] += 1
					for x in helper(count - 1, idx, new):
						yield x
				for x in helper(count, idx + 1, current):
					yield x

		return helper(count, 0, [0] * size)

	@staticmethod
	def rarity_grammar(rarity, count=0):
		if count == 1:
			return rarity
		return f'{rarity[:-1]}ies' if rarity[-1] == 'y' else f'{rarity}s'


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
						'function': self.optimize_talismans,
						'desc': 'Optimizes your talismans to their best reforges',
						'session': True
					},
					'missing': {
						'args': '[username] (profile)',
						'function': self.view_missing_talismans,
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
		await self.get_user(270352691924959243).send(f'```{error[-1900:]}```')
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
		command[0] = command[0].casefold()
		if command[0] == f'<@!{self.user.id}>' or command[0] == f'<@{self.user.id}>':
			command = command[1:]
		elif command[0] == prefix:
			command = command[1:]
		elif not dm:
			return

		if not command:
			return

		name = command[0].casefold()
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
		player = await skypy.Player(keys, uname=args[0], guild=True)

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

	async def optimize_talismans(self, message, *args):
		user = message.author
		channel = message.channel

		valid = False
		while valid is False:
			await channel.send(f'{user.mention} what is your Minecraft username?')
			msg = await self.respond(user, channel)

			msg = msg.content.casefold()

			player = await skypy.Player(keys, uname=msg)
			if len(player.profiles) == 0:
				await embed(
					channel,
					user=user,
					title=f'{user.name}, the Hypixel API has returned invalid information'
				).add_field(
					name=None,
					value='You can usually solve this issue by simply retrying in a few minutes, contact melon if otherwise'
				).set_footer(
					text='This error is rare, about the same chance as getting an overflux! Congratulations!'
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
				value='\n\n'.join(f'> {PROFILE_EMOJIS[profile]}\n`{profile}`' for profile in player.profiles.keys())
			)

			result = await self.reaction_menu(await embed.send(), user, {PROFILE_EMOJIS[profile]: profile for profile in player.profiles.keys()})
			await player.set_profile(player.profiles[result])

		if player.enabled_api['skills'] is False or player.enabled_api['inventory'] is False:
			await self.api_disabled(f'{user.name}, your API is disabled!', channel, user)
			return

		if len(player.weapons) == 0:
			await channel.send(f'{user.mention}, you have `no weapons` in your inventory. If you have any items in your inventory or backpacks with no rarity, this will stop sbs from finding your weapons. If you do not have any, DM uwu your profile.')
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

				msg = (await self.respond(user, channel)).content.casefold()

				names = [weapon.name.casefold() for weapon in player.weapons]

				if msg in names:
					weapon = player.weapons[names.index(msg)]
					valid = True
				else:
					try:
						weapon = player.weapons[int(msg) - 1]
						valid = True
					except (IndexError, TypeError, ValueError):
						await channel.send(f'Invalid weapon! Did you make a typo?{CLOSE_MESSAGE}')

		pet = player.pet

		embed = Embed(
			channel,
			user=user,
			title='Is this the correct equipment?'
		).add_field(
			name=f'⚔️\tWeapon',
			value=f'```{weapon.name}```',
			inline=False
		).add_field(
			name=f'{PET_EMOJIS[pet.internal_name] if pet else "🐣"}\tPet',
			value=f'```{format_pet(pet) if pet else None}```',
			inline=False
		)

		for piece, emoji in [('helmet', '⛑️'), ('chestplate', '👚'), ('leggings', '👖'), ('boots', '👞')]:
			embed.add_field(
				name=f'{emoji}\t{piece.capitalize()}',
				value='```' + str(next((a.name for a in player.armor if a.type == piece), None)) + '```',
				inline=False
			)

		embed.add_field(
			name='🏺\tTalismans',
			value=''.join(
				colorize(
					f'{amount} {Route.rarity_grammar(name).capitalize()}',
					RARITY_COLORS[name]
				)
				for name, amount in player.talisman_counts().items())
		)

		if not await self.yesno(await embed.send(), user):
			await channel.send(f'{user.mention} session ended')
			return

		numbers = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

		stats = {'crit damage': 0, 'crit chance': 0, 'strength': 0, 'enchantment modifier': 0, 'damage': 0}

		for name, pot in DAMAGING_POTIONS.items():
			buff = pot['stats']
			levels = pot['levels']

			if weapon.type != 'bow' and name == 'archery':
				continue

			msg = await channel.send(f'{user.mention} what level of `{name} potion` do you use?')

			emojis = {numbers[level]: level for level in levels}

			level = await self.reaction_menu(msg, user, emojis)

			for name1, amount in buff.items():
				stats[name1] += amount[level]

		for name, orb in ORBS.items():
			internal_name = orb['internal']
			buff = orb['stats']

			if internal_name in player.inventory or internal_name in player.echest:
				msg = await channel.send(f'{user.mention} will you be using your `{name}`?')
				yn = await self.yesno(msg, user)

				if yn is True:
					for name, amount in buff.items():
						stats[name] += amount

		potion_cc = stats['crit chance']

		optimizers = [
			('💯', 'perfect crit chance'),
			('⚔️', 'maximum damage')
		]

		embed = Embed(
			channel,
			user=user,
			title='You are almost done!'
		).add_field(
			name='What would you like to optimize for?',
			value='\n\n'.join(f'> {emoji}\n`{value}`' for emoji, value in optimizers)
		)

		optimizers = {emoji: index for index, (emoji, _) in enumerate(optimizers)}
		opt_goal = await self.reaction_menu(await embed.send(), user, optimizers)

		def apply_stats(additional, reverse=False):
			for key, value in additional.items():
				if key in stats:
					if reverse:
						stats[key] -= value
					else:
						stats[key] += value

		apply_stats(player.base_stats())
		apply_stats(player.fairy_soul_stats())
		apply_stats(player.armor_stats())
		apply_stats(player.slayer_stats())
		apply_stats(player.skill_stats())
		apply_stats(weapon.stats())
		if pet:
			apply_stats(pet.stats())
		weapon_damage = stats['damage']

		apply_stats(player.talisman_stats(include_reforges=True))
		cur_str = stats['strength']
		cur_cc = stats['crit chance']
		cur_cd = stats['crit damage']
		apply_stats(player.talisman_stats(include_reforges=True), reverse=True)
		apply_stats(player.talisman_stats(include_reforges=False))

		stat_modifiers = player.stat_modifiers()
		str_mod = stat_modifiers.get('strength', lambda x: x)
		cc_mod = stat_modifiers.get('crit chance', lambda x: x)
		cd_mod = stat_modifiers.get('crit damage', lambda x, y: x)

		cur_str = str_mod(cur_str)
		cur_cc = cc_mod(cur_cc)
		cur_cd = cd_mod(cur_cd, cur_str)

		base_str = stats['strength']
		base_cc = stats['crit chance']
		base_cd = stats['crit damage']

		# print(*(f"({n} {v})" for n, v in locals().items()))

		best, best_route, best_str, best_cc, best_cd = await self.loop.run_in_executor(None,
			optimizer,
			opt_goal,
			player,
			weapon_damage,
			base_str,
			base_cc,
			base_cd
		)

		if not best_route:
			await Embed(
				channel,
				user=user,
				title='There is no possible setup that will give you 100% crit chance',
				description='Collect more talismans or raise your combat level before trying again'
			).send()
			return

		embed = Embed(
			channel,
			user=user,
			title='Success!'
		)
		for route, color in zip(best_route, [GRAY, GREEN, BLUE, ORANGE, YELLOW]):
			if str(route):
				embed.add_field(
					name=f'**{route.rarity_str.title()}**',
					value=colorize(route, color),
					inline=False
				)
			else:
				embed.add_field(
					name=f'**{route.rarity_str.title()}**',
					value=r'```¯\_(ツ)_/¯```',
					inline=False
				)

		def emod(activity):
			result = 0
			for enchantment in ACTIVITIES[activity]:
				if enchantment in weapon.enchantments:
					value = ENCHANTMENT_VALUES[enchantment]
					if callable(value):
						result += value(weapon.enchantments[enchantment])
					else:
						result += value * weapon.enchantments[enchantment]
			return result

		base_mod = stats['enchantment modifier'] + player.skills['combat'] * 4
		zealot_mod = emod('zealots') + base_mod
		slayer_mod = emod('slayer bosses') + base_mod

		if weapon.internal_name == 'REAPER_SWORD':
			slayer_mult = 3
		elif weapon.internal_name == 'SCORPION_FOIL':
			slayer_mult = 2.5
		else:
			slayer_mult = 1

		zealot_damage = skypy.damage(weapon_damage, cur_str, cur_cd, zealot_mod)
		slayer_damage = skypy.damage(weapon_damage, cur_str, cur_cd, slayer_mod)
		slayer_damage *= slayer_mult

		zealot_damage_after = skypy.damage(weapon_damage, best_str, best_cd, zealot_mod)
		slayer_damage_after = skypy.damage(weapon_damage, best_str, best_cd, slayer_mod)
		slayer_damage_after *= slayer_mult

		embed.add_field(
			name='**Before**',
			value=f'```{cur_str:.0f} strength\n{cur_cd:.0f} crit damage\n{cur_cc - potion_cc:.0f} crit chance```'
				  f'```{zealot_damage:,.0f} to zealots\n{slayer_damage:,.0f} to slayers```'
		)

		embed.add_field(
			name='**After**',
			value=f'```{best_str:.0f} strength\n{best_cd:.0f} crit damage\n{best_cc - potion_cc:.0f} crit chance```'
				  f'```{zealot_damage_after:,.0f} to zealots\n{slayer_damage_after:,.0f} to slayers```'
		)

		if zealot_damage > zealot_damage_after or slayer_damage > slayer_damage_after:
			embed.set_footer(
				text=f'Even though you will be dealing less damage, you will gain {best_cc - cur_cc} crit chance'
			)

		await embed.send()

	async def view_missing_talismans(self, message, *args):
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

		inactive = [talisman for talisman in player.talismans if talisman.active is False]

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
			description='Welcome to Skyblock Simplified, a Skyblock bot designed to streamline gameplay\n[Click me](https://discord.com/oauth2/authorize?client_id=671040150251372569&permissions=8&scope=bot) to invite the bot to your server\n'
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
		shards = []
		for x in range(self.shard_count): shards.append([0,0,0])
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
			name='Heartbeat',
			value=f'This message was delivered in {self.latency * 1000:.0f} milliseconds',
			inline=False
		)
		await _embed.send()

	async def respond(self, user, channel):
		msg = None

		try:
			msg = await self.wait_for('message',
									  check=lambda message: message.author == user and message.channel == channel,
									  timeout=60 * 3)
		except asyncio.TimeoutError:
			raise EndSession
		if msg.content.casefold() == 'exit':
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

	async def book(self, user, channel, pages):
		page_num = 0
		backward = {'⬅️': -1}
		forward = {'➡️': 1}
		both = {'⬅️': -1, '➡️': 1}

		if channel.type != discord.ChannelType.private and channel.guild.me.permissions_in(channel).manage_messages:
			r = await pages(page_num)
			embed, last_page = r

			msg = await embed.send()
			while True:
				if page_num == 0 and last_page is True:
					return

				if page_num == 0:
					result = await self.reaction_menu(msg, user, forward, edit=True)
				elif last_page is True:
					result = await self.reaction_menu(msg, user, backward, edit=True)
				else:
					result = await self.reaction_menu(msg, user, both, edit=True)
				page_num += result

				r = await pages(page_num)
				embed, last_page = r

				await msg.edit(embed=embed)
		else:
			while True:
				r = await pages(page_num)
				embed, last_page = r

				msg = await embed.send()
				if page_num == 0 and last_page is True:
					return

				if page_num == 0:
					result = await self.reaction_menu(msg, user, forward, edit=False)
				elif last_page is True:
					result = await self.reaction_menu(msg, user, backward, edit=False)
				else:
					result = await self.reaction_menu(msg, user, both, edit=False)
				await msg.delete()
				page_num += result

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
			description='[Click me to invite the bot](https://discord.com/oauth2/authorize?client_id=671040150251372569&permissions=8&scope=bot)'
		).send()

discord.Embed = None  # Disable default discord Embed
