import re
import math

sword_enchants = [
	'sharpness',
	'critical',
	'ender_slayer',
	'execute',
	'first_strike',
	'giant_killer',
	'lethality',
	'life_steal',
	'looting',
	'luck',
	'scavenger',
	'vampirism',
	'bane_of_arthropods',
	'smite',
	'dragon_hunter'
]

bow_enchants = [
	'power',
	'aiming',
	'dragon_hunter',
	'infinite_quiver',
	'power',
	'snipe',
	'punch',
	'flame',
	'piercing'
]

rod_enchants = [
	'angler',
	'blessing',
	'caster',
	'frail',
	'luck_of_the_sea',
	'lure',
	'magnet',
	'looting'
]

skill_rewards = {
	'foraging': {
		0: {
			'strength': 1
		},
		15: {
			'strength': 2
		}
	},
	'combat': {
		0: {
			'crit chance': 1,
			'ench modifier': 4
		}
	}
}

talismans = {re.compile(k): v for k, v in {
	'FARMING_TALISMAN': 'Farming Talisman',
	'VACCINE_TALISMAN': 'Vaccine Talisman',
	'SPEED_TALISMAN': 'Speed Talisman',
	'SPEED_RING': 'Speed Ring',
	'SPEED_ARTIFACT': 'Speed Artifact',
	'WOOD_TALISMAN': 'Wood Affinity Talisman',
	'SKELETON_TALISMAN': 'Skeleton Talisman',
	'COIN_TALISMAN': 'Talisman of Coins',
	'MAGNETIC_TALISMAN': 'Magnetic Talisman',
	'GRAVITY_TALISMAN': 'Gravity Talisman',
	'VILLAGE_TALISMAN': 'Village Affinity Talisman',
	'MINE_TALISMAN': 'Mine Affinity Talisman',
	'NIGHT_VISION_CHARM': 'Night Vision Charm',
	'LAVA_TALISMAN': 'Lava Talisman',
	'SCAVENGER_TALISMAN': 'Scavenger Talisman',
	'WOLF_PAW': 'Wolf Paw',
	'FIRE_TALISMAN': 'Fire Talisman',
	'BROKEN_PIGGY_BANK': 'Broken Piggy Bank',
	'CRACKED_PIGGY_BANK': 'Cracked Piggy Bank',
	'PIGGY_BANK': 'Piggy Bank',
	'PIGS_FOOT': 'Pig\'s Foot',
	'FROZEN_CHICKEN': 'Frozen Chicken',
	'FISH_AFFINITY_TALISMAN': 'Fish Affinity Talisman',
	'FARMER_ORB': 'Farmer Orb',
	'HASTE_RING': 'Haste Ring',
	'NEW_YEAR_CAKE_BAG': 'New Year Cake Bag',
	'NIGHT_CRYSTAL': 'Night Crystal',
	'DAY_CRYSTAL': 'Day Crystal',
	'FEATHER_ARTIFACT': 'Feather Artifact',
	'ARTIFACT_POTION_AFFINITY': 'Potion Affinity Artifact',
	'HEALING_RING': 'Healing Ring',
	'CANDY_ARTIFACT': 'Candy Artifact',
	'EXPERIENCE_ARTIFACT': 'Experience Artifact',
	'MELODY_HAIR': '♪ Melody\'s Hair ♪',
	'SEA_CREATURE_ARTIFACT': 'Sea Creature Artifact',
	'INTIMIDATION_ARTIFACT': 'Intimidation Artifact',
	'WOLF_RING': 'Wolf Ring',
	'BAT_ARTIFACT': 'Bat Artifact',
	'DEVOUR_RING': 'Devour Ring',
	'ZOMBIE_ARTIFACT': 'Zombie Artifact',
	'SPIDER_ARTIFACT': 'Spider Artifact',
	'ENDER_ARTIFACT': 'Ender Artifact',
	'TARANTULA_TALISMAN': 'Tarantula Talisman',
	'SURVIVOR_CUBE': 'Survivor Cube',
	'WITHER_ARTIFACT': 'Wither Artifact',
	'WEDDING_RING_9': 'Legendary Ring of Love',
	'RED_CLAW_ARTIFACT': 'Red Claw Artifact',
	'BAIT_RING': 'Bait Ring',
	'SEAL_OF_THE_FAMILY': 'Seal of the Family',
	'HUNTER_RING': 'Hunter Ring',
	'CAMPFIRE_TALISMAN_(21|22|23|24|25|26|27|28|29)': 'Campfire God Badge',
}.items()}

skills = ['farming', 'mining', 'combat', 'foraging', 'fishing', 'enchanting', 'alchemy', 'taming', 'carpentry', 'runecrafting']
cosmetic_skills = ['carpentry', 'runecrafting']
slayers = ['zombie', 'spider', 'wolf']

slayer_rewards = {
	'zombie': (('health', 2), ('health', 2), ('health', 3), ('health', 3), ('health', 4), ('health', 4),
			   ('health', 5), ('health', 5), ('health', 6)),
	'spider': (('crit damage', 1), ('crit damage', 1), ('crit damage', 1), ('crit damage', 1), ('crit damage', 2),
			   ('crit damage', 2), ('crit chance', 1), ('crit damage', 3), ('crit damage', 3)),
	'wolf': (('speed', 1), ('health', 2), ('speed', 1), ('health', 2), ('crit damage', 1), ('health', 3),
			 ('crit damage', 2), ('speed', 1), ('health', 5))
}

slayer_level_requirements = {
	'zombie': [5, 15, 200, 1000, 5000, 20000, 100000, 400000, 1000000],
	'spider': [5, 15, 200, 1000, 5000, 20000, 100000, 400000, 1000000],
	'wolf': [5, 15, 200, 1500, 5000, 20000, 100000, 400000, 1000000]
}

base_stats = {
	'damage': 0,
	'strength': 0,
	'crit chance': 20,
	'crit damage': 50,
	'attack speed': 100,
	'health': 100,
	'defense': 0,
	'speed': 100,
	'intelligence': 0
}

profile_names = [
	'Apple',
	'Banana',
	'Blueberry',
	'Coconut',
	'Cucumber',
	'Grapes',
	'Kiwi',
	'Lemon',
	'Lime',
	'Mango',
	'Orange',
	'Papaya',
	'Peach',
	'Pear',
	'Pineapple',
	'Pomegranate',
	'Raspberry',
	'Strawberry',
	'Tomato',
	'Watermelon',
	'Zucchini'
]

'''
pet_xp = [0, 100, 210, 330, 460, 605, 765, 940, 1130, 1340, 1570, 1820, 2095, 2395, 2725, 3085, 3485, 3925, 4415, 4955, 5555, 6215, 6945, 7745, 8625, 9585, 10635, 11785, 13045, 14425, 15935, 17585, 19385, 21345, 23475, 25785, 28285, 30985, 33905, 37065, 40485, 44185, 48185, 52535, 57285, 62485, 68185, 74485, 81485, 89285, 97985, 107685, 118485, 130485, 143785, 158485, 174685, 192485, 211985, 233285, 256485, 281685, 309085, 338885, 371285, 406485, 444685, 486085, 530885, 579285, 631485, 687685, 748085, 812885, 882285, 956485, 1035685, 1120385, 1211085, 1308285, 1412485, 1524185, 1643885, 1772085, 1909285, 2055985, 2212685, 2380385, 2560085, 2752785, 2959485, 3181185, 3418885, 3673585, 3946285, 4237985, 4549685, 4883385, 5241085, 5624785, 6036485, 6478185, 6954885, 7471585, 8033285, 8644985, 9311685, 10038385, 10830085, 11691785, 12628485, 13645185, 14746885, 15938585, 17225285, 18611985, 20108685, 21725385, 23472085, 25358785]

def xp_slice(start):
	diff = pet_xp[start - 1]
	return [xp - diff for xp in pet_xp[start-1:start+99]]

pet_xp = {'common': xp_slice(1), 'uncommon': xp_slice(7), 'rare': xp_slice(12), 'epic': xp_slice(17), 'legendary': xp_slice(21)}
'''

pet_xp = {
	'common': [
		0, 100, 210, 330, 460, 605, 765, 940, 1130, 1340, 1570, 1820, 2095,
		2395, 2725, 3085, 3485, 3925, 4415, 4955, 5555, 6215, 6945, 7745,
		8625, 9585, 10635, 11785, 13045, 14425, 15935, 17585, 19385, 21345,
		23475, 25785, 28285, 30985, 33905, 37065, 40485, 44185, 48185,
		52535, 57285, 62485, 68185, 74485, 81485, 89285, 97985, 107685,
		118485, 130485, 143785, 158485, 174685, 192485, 211985, 233285,
		256485, 281685, 309085, 338885, 371285, 406485, 444685, 486085,
		530885, 579285, 631485, 687685, 748085, 812885, 882285, 956485,
		1035685, 1120385, 1211085, 1308285, 1412485, 1524185, 1643885,
		1772085, 1909285, 2055985, 2212685, 2380385, 2560085, 2752785,
		2959485, 3181185, 3418885, 3673585, 3946285, 4237985, 4549685,
		4883385, 5241085, 5624785
	],
	'uncommon': [
		0, 175, 365, 575, 805, 1055, 1330, 1630, 1960, 2320, 2720, 3160,
		3650, 4190, 4790, 5450, 6180, 6980, 7860, 8820, 9870, 11020,
		12280, 13660, 15170, 16820, 18620, 20580, 22710, 25020, 27520,
		30220, 33140, 36300, 39720, 43420, 47420, 51770, 56520, 61720,
		67420, 73720, 80720, 88520, 97220, 106920, 117720, 129720, 143020,
		157720, 173920, 191720, 211220, 232520, 255720, 280920, 308320,
		338120, 370520, 405720, 443920, 485320, 530120, 578520, 630720,
		686920, 747320, 812120, 881520, 955720, 1034920, 1119620, 1210320,
		1307520, 1411720, 1523420, 1643120, 1771320, 1908520, 2055220,
		2211920, 2379620, 2559320, 2752020, 2958720, 3180420, 3418120,
		3672820, 3945520, 4237220, 4548920, 4882620, 5240320, 5624020,
		6035720, 6477420, 6954120, 7470820, 8032520, 8644220
	],
	'rare': [
		0, 275, 575, 905, 1265, 1665, 2105, 2595, 3135, 3735, 4395, 5125,
		5925, 6805, 7765, 8815, 9965, 11225, 12605, 14115, 15765, 17565,
		19525, 21655, 23965, 26465, 29165, 32085, 35245, 38665, 42365, 46365,
		50715, 55465, 60665, 66365, 72665, 79665, 87465, 96165, 105865,
		116665, 128665, 141965, 156665, 172865, 190665, 210165, 231465,
		254665, 279865, 307265, 337065, 369465, 404665, 442865, 484265,
		529065, 577465, 629665, 685865, 746265, 811065, 880465, 954665,
		1033865, 1118565, 1209265, 1306465, 1410665, 1522365, 1642065,
		1770265, 1907465, 2054165, 2210865, 2378565, 2558265, 2750965,
		2957665, 3179365, 3417065, 3671765, 3944465, 4236165, 4547865,
		4881565, 5239265, 5622965, 6034665, 6476365, 6953065, 7469765,
		8031465, 8643165, 9309865, 10036565, 10828265, 11689965, 12626665
	],
	'epic': [
		0, 440, 930, 1470, 2070, 2730, 3460, 4260, 5140, 6100, 7150, 8300,
		9560, 10940, 12450, 14100, 15900, 17860, 19990, 22300, 24800, 27500,
		30420, 33580, 37000, 40700, 44700, 49050, 53800, 59000, 64700, 71000,
		78000, 85800, 94500, 104200, 115000, 127000, 140300, 155000, 171200,
		189000, 208500, 229800, 253000, 278200, 305600, 335400, 367800,
		403000, 441200, 482600, 527400, 575800, 628000, 684200, 744600,
		809400, 878800, 953000, 1032200, 1116900, 1207600, 1304800, 1409000,
		1520700, 1640400, 1768600, 1905800, 2052500, 2209200, 2376900,
		2556600, 2749300, 2956000, 3177700, 3415400, 3670100, 3942800,
		4234500, 4546200, 4879900, 5237600, 5621300, 6033000, 6474700,
		6951400, 7468100, 8029800, 8641500, 9308200, 10034900, 10826600,
		11688300, 12625000, 13641700, 14743400, 15935100, 17221800,
		18608500
	],
	'legendary': [
		0, 660, 1390, 2190, 3070, 4030, 5080, 6230, 7490, 8870, 10380,
		12030, 13830, 15790, 17920, 20230, 22730, 25430, 28350, 31510,
		34930, 38630, 42630, 46980, 51730, 56930, 62630, 68930, 75930,
		83730, 92430, 102130, 112930, 124930, 138230, 152930, 169130,
		186930, 206430, 227730, 250930, 276130, 303530, 333330, 365730,
		400930, 439130, 480530, 525330, 573730, 625930, 682130, 742530,
		807330, 876730, 950930, 1030130, 1114830, 1205530, 1302730,
		1406930, 1518630, 1638330, 1766530, 1903730, 2050430, 2207130,
		2374830, 2554530, 2747230, 2953930, 3175630, 3413330, 3668030,
		3940730, 4232430, 4544130, 4877830, 5235530, 5619230, 6030930,
		6472630, 6949330, 7466030, 8027730, 8639430, 9306130, 10032830,
		10824530, 11686230, 12622930, 13639630, 14741330, 15933030,
		17219730, 18606430, 20103130, 21719830, 23466530, 25353230
	]
}

def none():
	pass

def pigman(player, stats, pet):
	# Buffs the Pigman sword by (Pet lvl * 0.4) damage and (Pet lvl * 0.25) strength. (All)
	# Deal (Pet lvl * 0.2%) extra damage to monsters level 100 and up. (Legendary)
	if player.weapon == 'PIGMAN_SWORD':
		stats['weapon damage'] += int(pet.level * 0.4)
		stats['strength'] += int(pet.level * 0.25)


def sheep(player, stats, pet):
	# Increases your total  Mana by (Pet lvl * 0.25%) while in dungeons. (Legendary)
	pass


def witherskeleton(player, stats, pet):
	# Deal (Pet lvl * 0.5%) more damage against wither mobs. (All) - tbd
	# Upon hitting an enemy inflict the wither effect for (Pet lvl * 2%) damage over 3 seconds (No stack). (Legendary)
	pass


def horse(player, stats, pet):
	# While riding your horse, gain (Pet lvl * 0.25%) bow damage. (Legendary)
	pass


def lion(player, stats, pet):
	# Adds (Pet lvl * 0.03) damage to your weapons. (Common) (0.05 on Uncommon) (0.1 on Rare) (0.15 on Epic) (0.2 on Legendary)
	# Increases damage dealt by (Pet lvl * 0.3%) on your first hit on a mob. (Rare) (0.4% on Epic) (0.5% on Legendary)
	# Deal (Pet lvl * 0.3%) weapon damage against mobs below level 80. (Legendary)
	pass


def wolf(player, stats, pet):
	# Gain (Pet lvl * 0.1%) crit damage for every nearby wolf (max 10). (Rare) (0.15% for Epic, Legendary)
	pass


def enderdragon(player, pet):
	# Deal (Pet lvl * 0.25%) more damage to end mobs. (All)
	# Buffs the Aspect of the Dragon sword by (Pet lvl * 0.5) damage and (Pet lvl * 0.3) strength. (All)
	# Increases all stats by (Pet lvl * 0.1%). (Legendary)
	if player.weapon == 'ASPECT_OF_THE_DRAGONS':
		player.stats.weapon['damage'] += pet.level // 2
		player.stats.weapon['strength'] += int(pet.level * 0.3)
	if pet.rarity == 'legendary':
		boost = 1 + (pet.level * 0.1)
		stats = {name: int(stat * boost) for name, stat in player.stats.items()}


def giraffe(player, stats, pet):
	# Grants (Pet lvl * 0.4) strength and (20 + (Pet lvl * 0.1)) crit damage when mid air. (Rare)
	# ((Pet lvl * 0.5) strength and (20 + (Pet lvl * 0.25)) crit damage on Epic)
	# ((Pet lvl * 0.5) strength and (20 + (Pet lvl * 0.4)) crit damage on Legendary)
	pass


def phoenix(player, stats, pet):
	# Before death, become immune and gain (10 + (Pet lvl * 0.1)) strength on (2 + (Pet lvl * 0.02)) seconds (3 minutes cooldown). (Epic) ((10 + (Pet lvl * 0.2) STR on (2 + (Pet lvl * 0.02)) seconds on Legendary)
	# On 4th melee strike, ignite mobs, dealing (1 + (Pet lvl * 0.14)) your crit damage each second for (2 + (Pet lvl/25)) seconds. (Epic, Legendary)
	pass


def bee(player, stats, pet):
	# Gain (1 + (Pet lvl * 0.02)) Intelligence and (1 + (Pet lvl * 0.02)) Strength for each nearby bee. (Max 15) (Common)
	# (1+ (Pet lvl * 0.09) INT and (1 + (Pet lvl * 0.07)) STR on Rare)
	# (1+ (Pet lvl * 0.14) INT and (1 + (Pet lvl * 0.11)) STR on Epic)
	# (1+ (Pet lvl * 0.19) INT and (1 + (Pet lvl * 0.14)) STR on Legendary)
	pass


def squid(player, stats, pet):
	# Buffs the Ink Wand by (Pet lvl * 0.3) damage and (Pet lvl * 0.1) strength. (Rare) (0.4 DMG and 0.2 STR on Epic, Legendary)
	pass


def parrot(player, stats, pet):
	# Gives (5 + (Pet lvl * 0.25)) strength to players within 20 Blocks (No stack). (Legendary)
	pass


def tiger(player, stats, pet):
	# Attacks have a (Pet lvl * 0.05%) chance to strike twice. (Common) (0.1% on Uncommon, Rare) (0.2% on Epic, Legendary)
	# Deal (Pet lvl * 0.2%) more damage against targets with no other mobs within 15 blocks. (Legendary)
	pass


def blaze(player, stats, pet):
	# Upgrades Blaze Armor stats and ability by (Pet lvl * 0.4%). (All)
	# Double effects of Hot Potato Books. (Legendary)
	pass


def zombie(player, stats, pet):
	# Deal (Pet lvl * 0.2%) more damage to zombies. (Epic, Legendary)
	pass


def skeleton(player, stats, pet):
	# Increase arrow damage by (Pet lvl * 0.1%), which is tripled while in dungeons. (Common, Uncommon, Rare) (0.2% on Epic, Legendary)
	# Gain a combo stack for every bow hit granting +3 Strength. Max (Pet lvl * 0.1) stacks, stacks disappear after 8 seconds. (Rare) (0.2 on Epic, Legendary)
	pass


def yeti(player, stats, pet):
	# Buff the Yeti sword by 1 (+1 per level) Damage and  Intelligence
	if pet.rarity == 'legendary' and player.weapon == 'YETI_SWORD':
		player.weapon.stats['damage'] += pet.level
		player.weapon.stats['intelligence'] += pet.level


def flyingfish(player, stats, pet):
	# Gives (Pet lvl * 0.4) strength when near water. (Rare) (0.5 on Epic, Legendary)
	# Increases the stats of Diver's Armor by (Pet lvl * 0.3%). (Legendary)
	pass

def magmacube(player, stats, pet):
	# Deal (Pet lvl * 0.25%) more damage to slimes. (Rare, Epic, Legendary)
	# Buffs the stats of Ember Armor by (Pet lvl * 1%). (Legendary)
	pass

def spider(player, stats, pet):
	# Gain (Pet lvl * 0.1) strength for every nearby spider (Max 10). (All)
	pass

def rock(player, stats, pet):
	# While sitting on your rock, gain (Pet lvl * 0.3%) more damage. (Legendary)
	pass

def golem(player, stats, pet):
	# While less than 15% HP, deal (Pet lvl * 0.3%) more damage. (All)
	pass

pet = {
	'SKELETON_HORSE': {
		'name': 'Skeleton Horse',
		'stats': {
			'intelligent': lambda lvl: lvl,
			'speed': lambda lvl: lvl // 2
		},
		'ability': none,
		'type': 'combat',
		'icon': '/head/47effce35132c86ff72bcae77dfbb1d22587e94df3cbc2570ed17cf8973a'
	},
	'SNOWMAN': {
		'name': 'Snowman',
		'stats': {
			'damage': lambda lvl: lvl // 4,
			'strength': lambda lvl: lvl // 4,
			'crit damage': lambda lvl: lvl // 4
		},
		'ability': none,
		'type': 'combat',
		'icon': '/head/11136616d8c4a87a54ce78a97b551610c2b2c8f6d410bc38b858f974b113b208'
	},
	'BAT': {
		'name': 'Bat',
		'stats': {
			'intelligent': lambda lvl: lvl,
			'speed': lambda lvl: lvl // 20
		},
		'ability': none,
		'type': 'mining',
		'icon': '/head/382fc3f71b41769376a9e92fe3adbaac3772b999b219c9d6b4680ba9983e527'
	},
	'SHEEP': {
		'name': 'Sheep',
		'stats': {
			'intelligent': lambda lvl: lvl,
			'ability damage': lambda lvl: lvl // 2,
		},
		# Increases your total  Mana by (Pet lvl * 0.25%) while in dungeons. (Legendary)
		'ability': sheep,
		'type': 'alchemy',
		'icon': '/head/64e22a46047d272e89a1cfa13e9734b7e12827e235c2012c1a95962874da0'
	},
	'CHICKEN': {
		'name': 'Chicken',
		'stats': {
			'health': lambda lvl: lvl * 2
		},
		'ability': none,
		'type': 'farming',
		'icon': '/head/7f37d524c3eed171ce149887ea1dee4ed399904727d521865688ece3bac75e'
	},
	'WITHER_SKELETON': {
		'name': 'Wither Skeleton',
		'stats': {
			'strength': lambda lvl: lvl // 4,
			'crit chance': lambda lvl: lvl // 20,
			'crit damage': lambda lvl: lvl // 4,
			'defense': lambda lvl: lvl // 4,
			'intelligent': lambda lvl: lvl // 4
		},
		# Deal (Pet lvl * 0.5%) more damage against wither mobs. (All)
		# Upon hitting an enemy inflict the wither effect for (Pet lvl * 2%) damage over 3 seconds (No stack). (Legendary)
		'ability': witherskeleton,
		'type': 'combat',
		'icon': '/head/f5ec964645a8efac76be2f160d7c9956362f32b6517390c59c3085034f050cff'
	},
	'SILVERFISH': {
		'name': 'Silverfish',
		'stats': {
			'defense': lambda lvl: lvl,
			'health': lambda lvl: lvl // 5,
		},
		'ability': none,
		'type': 'mining',
		'icon': '/head/da91dab8391af5fda54acd2c0b18fbd819b865e1a8f1d623813fa761e924540'
	},
	'RABBIT': {
		'name': 'Rabbit',
		'stats': {
			'health': lambda lvl: lvl,
			'speed': lambda lvl: lvl // 5
		},
		'ability': none,
		'type': 'farming',
		'icon': '/head/117bffc1972acd7f3b4a8f43b5b6c7534695b8fd62677e0306b2831574b'
	},
	'HORSE': {
		'name': 'Horse',
		'stats': {
			'intelligent': lambda lvl: lvl // 2,
			'speed': lambda lvl: lvl // 4
		},
		# While riding your horse, gain (Pet lvl * 0.25%) bow damage. (Legendary)
		'ability': horse,
		'type': 'combat',
		'icon': '/head/36fcd3ec3bc84bafb4123ea479471f9d2f42d8fb9c5f11cf5f4e0d93226'
	},
	'PIGMAN': {
		'name': 'Pigman',
		'stats': {
			'strength': lambda lvl: lvl // 2,
			'defense': lambda lvl: lvl // 2
		},
		# Buffs the Pigman sword by (Pet lvl * 0.4) damage and (Pet lvl * 0.25) strength. (All)
		# Deal (Pet lvl * 0.2%) extra damage to monsters level 100 and up. (Legendary)
		'ability': pigman,
		'type': 'combat',
		'icon': '/head/63d9cb6513f2072e5d4e426d70a5557bc398554c880d4e7b7ec8ef4945eb02f2'
	},
	'WOLF': {
		'name': 'Wolf',
		'stats': {
			'crit damage': lambda lvl: lvl // 10,
			'true defense': lambda lvl: lvl // 10,
			'speed': lambda lvl: lvl // 5,
			'health': lambda lvl: lvl // 2
		},
		# Gain (Pet lvl * 0.1%) crit damage for every nearby wolf (max 10). (Rare) (0.15% for Epic, Legendary)
		'ability': wolf,
		'type': 'combat',
		'icon': '/head/dc3dd984bb659849bd52994046964c22725f717e986b12d548fd169367d494'
	},
	'OCELOT': {
		'name': 'Ocelot',
		'stats': {
			'speed': lambda lvl: lvl // 2
		},
		'ability': none,
		'type': 'foraging',
		'icon': '/head/5657cd5c2989ff97570fec4ddcdc6926a68a3393250c1be1f0b114a1db1'
	},
	'LION': {
		'name': 'Lion',
		'stats': {
			'strength': lambda lvl: lvl // 2,
			'speed': lambda lvl: lvl // 4
		},
		# Adds (Pet lvl * 0.03) damage to your weapons. (Common) (0.05 on Uncommon) (0.1 on Rare) (0.15 on Epic) (0.2 on Legendary)
		# Increases damage dealt by (Pet lvl * 0.3%) on your first hit on a mob. (Rare) (0.4% on Epic) (0.5% on Legendary)
		# Deal (Pet lvl * 0.3%) weapon damage against mobs below level 80. (Legendary)
		'ability': lion,
		'type': 'foraging',
		'icon': '/head/38ff473bd52b4db2c06f1ac87fe1367bce7574fac330ffac7956229f82efba1'
	},
	'ENDER_DRAGON': {
		'name': 'Dragon',
		'stats': {
			'strength': lambda lvl: lvl // 2,
			'crit chance': lambda lvl: lvl // 10,
			'crit damage': lambda lvl: lvl // 2
		},
		# Deal (Pet lvl * 0.25%) more damage to end mobs. (All)
		# Buffs the Aspect of the Dragon sword by (Pet lvl * 0.5) damage and (Pet lvl * 0.3) strength. (All)
		# Increases all stats by (Pet lvl * 0.1%). (Legendary)
		'ability': enderdragon,
		'type': 'combat',
		'icon': '/head/aec3ff563290b13ff3bcc36898af7eaa988b6cc18dc254147f58374afe9b21b9'
	},
	'GUARDIAN': {
		'name': 'Guardian',
		'stats': {
			'intelligent': lambda lvl: lvl,
			'defense': lambda lvl: lvl // 2
		},
		'ability': none,
		'type': 'fishing',
		'icon': '/head/221025434045bda7025b3e514b316a4b770c6faa4ba9adb4be3809526db77f9d'
	},
	'ENDERMAN': {
		'name': 'Enderman',
		'stats': {
			'crit damage': lambda lvl: lvl * 0.75
		},
		'ability': none,
		'type': 'combat',
		'icon': '/head/6eab75eaa5c9f2c43a0d23cfdce35f4df632e9815001850377385f7b2f039ce1'
	},
	'BLUE_WHALE': {
		'name': 'Whale',
		'stats': {
			'health': lambda lvl: lvl * 2
		},
		'ability': none,
		'type': 'fishing',
		'icon': '/head/dab779bbccc849f88273d844e8ca2f3a67a1699cb216c0a11b44326ce2cc20'
	},
	'GIRAFFE': {
		'name': 'Giraffe',
		'stats': {
			'health': lambda lvl: lvl,
			'crit chance': lambda lvl: lvl // 20
		},
		# Grants (Pet lvl * 0.4) strength and (20 + (Pet lvl * 0.1)) crit damage when mid air. (Rare)
		# ((Pet lvl * 0.5) strength and (20 + (Pet lvl * 0.25)) crit damage on Epic)
		# ((Pet lvl * 0.5) strength and (20 + (Pet lvl * 0.4)) crit damage on Legendary)
		'ability': giraffe,
		'type': 'foraging',
		'icon': '/head/6eab75eaa5c9f2c43a0d23cfdce35f4df632e9815001850377385f7b2f039ce1'
	},
	'PHOENIX': {
		'name': 'Phoenix',
		'stats': {
			'strength': lambda lvl: (lvl // 2) + 10,
			'intelligent': lambda lvl: lvl + 50
		},
		# Before death, become immune and gain (10 + (Pet lvl * 0.1)) strength on (2 + (Pet lvl * 0.02)) seconds (3 minutes cooldown). (Epic)
		# ((10 + (Pet lvl * 0.2) STR on (2 + (Pet lvl * 0.02)) seconds on Legendary)
		# On 4th melee strike, ignite mobs, dealing (1 + (Pet lvl * 0.14)) your crit damage each second for (2 + (Pet lvl/25)) seconds. (Epic, Legendary)
		'ability': phoenix,
		'type': 'combat',
		'icon': '/head/23aaf7b1a778949696cb99d4f04ad1aa518ceee256c72e5ed65bfa5c2d88d9e'
	},
	'BEE': {
		'name': 'Bee',
		'stats': {
			'intelligent': lambda lvl: lvl // 2,
			'strength': lambda lvl: (lvl // 4) + 5,
			'speed': lambda lvl: lvl // 10,
		},
		# Gain (1 + (Pet lvl * 0.02)) Intelligence and (1 + (Pet lvl * 0.02)) Strength for each nearby bee. (Max 15) (Common)
		# (1+ (Pet lvl * 0.09) INT and (1 + (Pet lvl * 0.07)) STR on Rare)
		# (1+ (Pet lvl * 0.14) INT and (1 + (Pet lvl * 0.11)) STR on Epic)
		# (1+ (Pet lvl * 0.19) INT and (1 + (Pet lvl * 0.14)) STR on Legendary)
		'ability': bee,
		'type': 'farming',
		'icon': '/head/7e941987e825a24ea7baafab9819344b6c247c75c54a691987cd296bc163c263'
	},
	'MAGMA_CUBE': {
		'name': 'Magma Cube',
		'stats': {
			'strength': lambda lvl: lvl // 5,
			'defense': lambda lvl: lvl // 3,
			'health': lambda lvl: lvl // 2
		},
		# Deal (Pet lvl * 0.25%) more damage to slimes. (Rare, Epic, Legendary)
		# Buffs the stats of Ember Armor by (Pet lvl * 1%). (Legendary)
		'ability': magmacube,
		'type': 'combat',
		'icon': '/head/38957d5023c937c4c41aa2412d43410bda23cf79a9f6ab36b76fef2d7c429'
	},
	'FLYING_FISH': {
		'name': 'Flying Fish',
		'stats': {
			'strength': lambda lvl: lvl // 2,
			'defense': lambda lvl: lvl // 2
		},
		# Gives (Pet lvl * 0.4) strength when near water. (Rare) (0.5 on Epic, Legendary)
		# Increases the stats of Diver's Armor by (Pet lvl * 0.3%). (Legendary)
		'ability': flyingfish,
		'type': 'fishing',
		'icon': '/head/40cd71fbbbbb66c7baf7881f415c64fa84f6504958a57ccdb8589252647ea'
	},
	'SQUID': {
		'name': 'Squid',
		'stats': {
			'intelligent': lambda lvl: lvl // 2,
			'health': lambda lvl: lvl // 2
		},
		# Buffs the Ink Wand by (Pet lvl * 0.3) damage and (Pet lvl * 0.1) strength. (Rare) (0.4 DMG and 0.2 STR on Epic, Legendary)
		'ability': squid,
		'type': 'fishing',
		'icon': '/head/01433be242366af126da434b8735df1eb5b3cb2cede39145974e9c483607bac'
	},
	'PARROT': {
		'name': 'Parrot',
		'stats': {
			'crit damage': lambda lvl: lvl // 10,
			'intelligent': lambda lvl: lvl
		},
		# Gives (5 + (Pet lvl * 0.25)) strength to players within 20 Blocks (No stack). (Legendary)
		'ability': parrot,
		'type': 'alchemy',
		'icon': '/head/5df4b3401a4d06ad66ac8b5c4d189618ae617f9c143071c8ac39a563cf4e4208'
	},
	'TIGER': {
		'name': 'Tiger',
		'stats': {
			'strength': lambda lvl: (lvl // 10) + 5,
			'crit chance': lambda lvl: lvl // 20,
			'crit damage': lambda lvl: lvl // 2
		},
		# Attacks have a (Pet lvl * 0.05%) chance to strike twice. (Common) (0.1% on Uncommon, Rare) (0.2% on Epic, Legendary)
		# Deal (Pet lvl * 0.2%) more damage against targets with no other mobs within 15 blocks. (Legendary)
		'ability': tiger,
		'type': 'combat',
		'icon': '/head/fc42638744922b5fcf62cd9bf27eeab91b2e72d6c70e86cc5aa3883993e9d84'
	},
	'TURTLE': {
		'name': 'Turtle',
		'stats': {
			'health': lambda lvl: lvl // 2,
			'defense': lambda lvl: lvl
		},
		'ability': none,
		'type': 'combat',
		'icon': '/head/212b58c841b394863dbcc54de1c2ad2648af8f03e648988c1f9cef0bc20ee23c'
	},
	'BLAZE': {
		'name': 'Blaze',
		'stats': {
			'intelligent': lambda lvl: lvl,
			'defense': lambda lvl: (lvl // 5) + 10
		},
		# Upgrades Blaze Armor stats and ability by (Pet lvl * 0.4%). (All)
		# Double effects of Hot Potato Books. (Legendary)
		'ability': blaze,
		'type': 'combat',
		'icon': '/head/b78ef2e4cf2c41a2d14bfde9caff10219f5b1bf5b35a49eb51c6467882cb5f0'
	},
	'JERRY': {
		'name': 'Jerry',
		'stats': {
			'intelligent': lambda lvl: -lvl
		},
		'ability': none,
		'type': 'combat',
		'icon': '/head/822d8e751c8f2fd4c8942c44bdb2f5ca4d8ae8e575ed3eb34c18a86e93b'
	},
	'ZOMBIE': {
		'name': 'Zombie',
		'stats': {
			'crit damage': lambda lvl: lvl * 0.3,
			'health': lambda lvl: lvl
		},
		# Deal (Pet lvl * 0.2%) more damage to zombies. (Epic, Legendary)
		'ability': zombie,
		'type': 'combat',
		'icon': '/head/822d8e751c8f2fd4c8942c44bdb2f5ca4d8ae8e575ed3eb34c18a86e93b'
	},
	'DOLPHIN': {
		'name': 'Dolphin',
		'stats': {
			'intelligent': lambda lvl: lvl,
			'sea creature chance': lambda lvl: lvl // 20
		},
		'ability': none,
		'type': 'fishing',
		'icon': '/head/6271bda308834d738faf194677090bc3'
	},
	'JELLYFISH': {
		'name': 'Jellyfish',
		'stats': {
			'health': lambda lvl: lvl * 2
		},
		'ability': none,
		'type': 'alchemy',
		'icon': '/head/913f086ccb56323f238ba3489ff2a1a34c0fdceeafc483acff0e5488cfd6c2f1'
	},
	'ELEPHANT': {
		'name': 'Elephant',
		'stats': {
			'health': lambda lvl: lvl,
			'intelligent': lambda lvl: lvl * 0.75
		},
		'ability': none,
		'type': 'farming',
		'icon': '/head/7071a76f669db5ed6d32b48bb2dba55d5317d7f45225cb3267ec435cfa514'
	},
	'MONKEY': {
		'name': 'Monkey',
		'stats': {
			'speed': lambda lvl: lvl // 5,
			'intelligent': lambda lvl: lvl // 2
		},
		'ability': none,
		'type': 'foraging',
		'icon': '/head/57ba53654c79265623b0aac6d2c611fe861b7fa22b392ef43674c11d8c8214c'
	},
	'SKELETON': {
		'name': 'Skeleton',
		'stats': {
			'crit chance': lambda lvl: lvl * 0.15,
			'crit damage': lambda lvl: lvl * 0.3
		},
		# Increase arrow damage by (Pet lvl * 0.1%), which is tripled while in dungeons. (Common, Uncommon, Rare) (0.2% on Epic, Legendary)
		# Gain a combo stack for every bow hit granting +3 Strength. Max (Pet lvl * 0.1) stacks, stacks disappear after 8 seconds. (Rare) (0.2 on Epic, Legendary)
		'ability': skeleton,
		'type': 'combat',
		'icon': '/head/301268e9c492da1f0d88271cb492a4b302395f515a7bbf77f4a20b95fc02eb2'
	},
	'SPIDER': {
		'name': 'Spider',
		'stats': {
			'strength': lambda lvl: lvl // 10,
			'crit chance': lambda lvl: lvl // 10
		},
		# Gain (Pet lvl * 0.1) strength for every nearby spider (Max 10). (All)
		'ability': spider,
		'type': 'combat',
		'icon': '/head/cd541541daaff50896cd258bdbdd4cf80c3ba816735726078bfe393927e57f1'
	},
	'ENDERMITE': {
		'name': 'Endermite',
		'stats': {
			'intelligent': lambda lvl: lvl
		},
		'ability': none,
		'type': 'mining',
		'icon': '/head/5a1a0831aa03afb4212adcbb24e5dfaa7f476a1173fce259ef75a85855'
	},
	'PIG': {
		'name': 'Pig',
		'stats': {
			'speed': lambda lvl: lvl // 4
		},
		'ability': none,
		'type': 'farming',
		'icon': '/head/621668ef7cb79dd9c22ce3d1f3f4cb6e2559893b6df4a469514e667c16aa4'
	},
	'ROCK': {
		'name': 'Rock',
		'stats': {
			'defense': lambda lvl: lvl * 2,
			'true defense': lambda lvl: lvl // 10
		},
		# While sitting on your rock, gain (Pet lvl * 0.3%) more damage. (Legendary)
		'ability': rock,
		'type': 'mining',
		'icon': '/head/ca979f76633f5dda89496511716948e9d7b8592f6e1e480c5de1c83238d3e32'
	},
	'HOUND': {
		'name': 'Hound',
		'stats': {
			'strength': lambda lvl: lvl * 0.4
		},
		'ability': none,
		'type': 'combat',
		'icon': '/head/b7c8bef6beb77e29af8627ecdc38d86aa2fea7ccd163dc73c00f9f258f9a1457'
	},
	'GHOUL': {
		'name': 'Ghoul',
		'stats': {
			'health': lambda lvl: lvl,
			'intelligent': lambda lvl: lvl * 7 // 10
		},
		'ability': none,
		'type': 'combat',
		'icon': '/head/87934565bf522f6f4726cdfe127137be11d37c310db34d8c70253392b5ff5b'
	},
	'TARANTULA': {
		'name': 'Tarantula',
		'stats': {
			'strength': lambda lvl: lvl // 10,
			'crit chance': lambda lvl: lvl // 10,
			'crit damage': lambda lvl: lvl * 1 // 3
		},
		'ability': none,
		'type': 'combat',
		'icon': '/head/8300986ed0a04ea79904f6ae53f49ed3a0ff5b1df62bba622ecbd3777f156df8'
	},
	'GOLEM': {
		'name': 'Golem',
		'stats': {
			'strength': lambda lvl: lvl // 2,
			'health': lambda lvl: lvl * 1.5
		},
		# While less than 15% HP, deal (Pet lvl * 0.3%) more damage. (All)
		'ability': golem,
		'type': 'combat',
		'icon': '/head/89091d79ea0f59ef7ef94d7bba6e5f17f2f7d4572c44f90f76c4819a714'
	},
	'BLACK_CAT': {
		'name': 'Black Cat',
		'stats': {
			'intelligent': lambda lvl: lvl,
			'speed': lambda lvl: lvl // 4
		},
		'ability': none,
		'type': 'combat',
		'icon': '/head/e4b45cbaa19fe3d68c856cd3846c03b5f59de81a480eec921ab4fa3cd81317'
	},
	'BABY_YETI': {
		'name': 'Baby Yeti',
		'stats': {
			'strength': lambda lvl: lvl * 2 // 5,
			'intelligent': lambda lvl: lvl * 3 // 4
		},
		'type': 'fishing',
		'ability': yeti,
		'icon': '/head/ab126814fc3fa846dad934c349628a7a1de5b415021a03ef4211d62514d5'
	},
}


fairy_soul_hp_bonus = [
	3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8,
	8, 9, 9, 10, 10, 11, 11, 12, 12,
	13, 13, 14, 14, 15, 15, 16, 16,
	17, 17, 18, 18, 19, 19, 20, 20, 21, 21
]

skill_xp_requirements = [
	50, 175, 375, 675, 1175, 1925, 2925, 4425,
	6425, 9925, 14925, 22425, 32425, 47425, 67425,
	97425, 147425, 222425, 322425, 522425, 822425,
	1222425, 1722425, 2322425, 3022425, 3822425,
	4722425, 5722425, 6822425, 8022425, 9322425,
	10722425, 12222425, 13822425, 15522425, 17322425,
	19222425, 21222425, 23322425, 25522425, 27822425,
	30222425, 32722425, 35322425, 38022425, 40822425,
	43922425, 47322425, 51022425, 55022425
]

tiered_talismans = {
	'BAT_RING': ['BAT_ARTIFACT'],
	'BAT_TALISMAN': ['BAT_RING', 'BAT_ARTIFACT'],
	'BROKEN_PIGGY_BANK': ['CRACKED_PIGGY_BANK', 'PIGGY_BANK'],
	'CANDY_RING': ['CANDY_ARTIFACT'],
	'CANDY_TALISMAN': ['CANDY_RING', 'CANDY_ARTIFACT'],
	'CRACKED_PIGGY_BANK': ['PIGGY_BANK'],
	'CROOKED_ARTIFACT': ['SEAL_OF_THE_FAMILY'],
	'FEATHER_RING': ['FEATHER_ARTIFACT'],
	'FEATHER_TALISMAN': ['FEATHER_RING', 'FEATHER_ARTIFACT'],
	'HEALING_TALISMAN': ['HEALING_RING'],
	'HUNTER_TALISMAN': ['HUNTER_RING'],
	'INTIMIDATION_RING': ['INTIMIDATION_ARTIFACT'],
	'INTIMIDATION_TALISMAN': ['INTIMIDATION_RING', 'INTIMIDATION_ARTIFACT'],
	'POTION_AFFINITY_TALISMAN': ['RING_POTION_AFFINITY', 'ARTIFACT_POTION_AFFINITY'],
	'RED_CLAW_RING': ['RED_CLAW_ARTIFACT'],
	'RED_CLAW_TALISMAN': ['RED_CLAW_RING', 'RED_CLAW_ARTIFACT'],
	'RING_POTION_AFFINITY': ['ARTIFACT_POTION_AFFINITY'],
	'SEA_CREATURE_RING': ['SEA_CREATURE_ARTIFACT'],
	'SEA_CREATURE_TALISMAN': ['SEA_CREATURE_RING', 'SEA_CREATURE_ARTIFACT'],
	'SHADY_RING': ['CROOKED_ARTIFACT', 'SEAL_OF_THE_FAMILY'],
	'SPIDER_RING': ['SPIDER_ARTIFACT'],
	'SPIDER_TALISMAN': ['SPIDER_RING', 'SPIDER_ARTIFACT'],
	'WOLF_TALISMAN': ['WOLF_RING'],
	'ZOMBIE_RING': ['ZOMBIE_ARTIFACT'],
	'ZOMBIE_TALISMAN': ['ZOMBIE_RING', 'ZOMBIE_ARTIFACT'],
	'SPEED_RING': ['SPEED_ARTIFACT'],
	'SPEED_TALISMAN': ['SPEED_RING', 'SPEED_ARTIFACT']
}

def clover(pet_stats):
	pet_stats['magic find'] += 7
	return pet_stats

def big_teeth(pet_stats):
	pet_stats['crit chance'] += 5
	return pet_stats

def sharp_claws(pet_stats):
	pet_stats['crit damage'] += 15
	return pet_stats

def iron_claws(pet_stats):
	pet_stats['crit chance'] = int(pet_stats['crit chance'] * 1.4)
	pet_stats['crit damage'] = int(pet_stats['crit damage'] * 1.4)
	return pet_stats

def scales(pet_stats):
	pet_stats['defense'] += 25
	return pet_stats

def textbook(pet_stats):
	pet_stats['intelligence'] *= 2
	return pet_stats

pet_items = {
	'PET_ITEM_LUCKY_CLOVER_EPIC': {
		'name': 'Lucky Clover',
		'effect': clover
	},
	'PET_ITEM_BIG_TEETH_COMMON': {
		'name': 'Big Teeth',
		'effect': big_teeth
	},
	'PET_ITEM_SHARPENED_CLAWS_COMMON': {
		'name': 'Sharpened Claws',
		'effect': sharp_claws
	},
	'PET_ITEM_IRON_CLAWS_COMMON': {
		'name': 'Iron Claws',
		'effect': iron_claws
	},
	'PET_ITEM_HARDENED_SCALES_UNCOMMON': {
		'name': 'Hardened Scales',
		'effect': scales
	},
	'PET_ITEM_TEXTBOOK_LEGENDARY': {
		'name': 'Textbook',
		'effect': textbook
	}
}

reforges = {
	'sword': {
		'legendary': {
			'common': {'strength': 3, 'crit chance': 10, 'crit damage': 5, 'intelligence': 5, 'attack speed': 3},
			'uncommon': {'strength': 7, 'crit chance': 12, 'crit damage': 10, 'intelligence': 8, 'attack speed': 5},
			'rare': {'strength': 14, 'crit chance': 14, 'crit damage': 15, 'intelligence': 12, 'attack speed': 7},
			'epic': {'strength': 18, 'crit chance': 17, 'crit damage': 22, 'intelligence': 18, 'attack speed': 10},
			'legendary': {'strength': 25, 'crit chance': 20, 'crit damage': 30, 'intelligence': 25, 'attack speed': 15},
			'mythic': {'strength': 40, 'crit chance': 25, 'crit damage': 40, 'intelligence': 35, 'attack speed': 20},
			'stone': False
		},
		'spicy': {
			'common': {'strength': 2, 'crit chance': 1, 'crit damage': 25, 'attack speed': 1},
			'uncommon': {'strength': 3, 'crit chance': 1, 'crit damage': 35, 'attack speed': 2},
			'rare': {'strength': 4, 'crit chance': 1, 'crit damage': 45, 'attack speed': 4},
			'epic': {'strength': 7, 'crit chance': 1, 'crit damage': 60, 'attack speed': 7},
			'legendary': {'strength': 10, 'crit chance': 1, 'crit damage': 80, 'attack speed': 10},
			'mythic': {'strength': 12, 'crit chance': 1, 'crit damage': 100, 'attack speed': 15},
			'stone': False
		},
		'epic': {
			'common': {'strength': 15, 'crit damage': 5, 'attack speed': 1},
			'uncommon': {'strength': 20, 'crit damage': 10, 'attack speed': 2},
			'rare': {'strength': 25, 'crit damage': 15, 'attack speed': 4},
			'epic': {'strength': 32, 'crit damage': 22, 'attack speed': 7},
			'legendary': {'strength': 40, 'crit damage': 30, 'attack speed': 10},
			'mythic': {'strength': 50, 'crit damage': 40, 'attack speed': 15},
			'stone': False
		},
		'odd': {
			'common': {'crit chance': 10, 'crit damage': 5, 'intelligence': -5},
			'uncommon': {'crit chance': 12, 'crit damage': 10, 'intelligence': -10},
			'rare': {'crit chance': 15, 'crit damage': 15, 'intelligence': -18},
			'epic': {'crit chance': 20, 'crit damage': 22, 'intelligence': -32},
			'legendary': {'crit chance': 25, 'crit damage': 30, 'intelligence': -50},
			'mythic': {'crit chance': 30, 'crit damage': 40, 'intelligence': -75},
			'stone': False
		},
		'gentle': {
			'common': {'strength': -2, 'attack speed': 10},
			'uncommon': {'strength': -4, 'attack speed': 20},
			'rare': {'strength': -6, 'attack speed': 30},
			'epic': {'strength': -8, 'attack speed': 40},
			'legendary': {'strength': -10, 'attack speed': 50},
			'mythic': {'strength': -12, 'attack speed': 60},
			'stone': False
		},
		'fast': {
			'common': {'strength': 3, 'attack speed': 8},
			'uncommon': {'strength': 5, 'attack speed': 10},
			'rare': {'strength': 7, 'attack speed': 15},
			'epic': {'strength': 10, 'attack speed': 20},
			'legendary': {'strength': 15, 'attack speed': 25},
			'mythic': {'strength': 20, 'attack speed': 30},
			'stone': False
		},
		'fair': {
			'common': {'strength': 2, 'crit chance': 2, 'crit damage': 2, 'intelligence': 2, 'attack speed': 2},
			'uncommon': {'strength': 3, 'crit chance': 3, 'crit damage': 3, 'intelligence': 3, 'attack speed': 3},
			'rare': {'strength': 4, 'crit chance': 4, 'crit damage': 4, 'intelligence': 4, 'attack speed': 4},
			'epic': {'strength': 7, 'crit chance': 7, 'crit damage': 7, 'intelligence': 7, 'attack speed': 7},
			'legendary': {'strength': 10, 'crit chance': 10, 'crit damage': 10, 'intelligence': 10, 'attack speed': 10},
			'mythic': {'strength': 12, 'crit chance': 12, 'crit damage': 12, 'intelligence': 12, 'attack speed': 12},
			'stone': False
		},
		'sharp': {
			'common': {'crit chance': 10, 'crit damage': 2, 'intelligence': 3},
			'uncommon': {'crit chance': 12, 'crit damage': 4, 'intelligence': 6},
			'rare': {'crit chance': 14, 'crit damage': 7, 'intelligence': 10},
			'epic': {'crit chance': 17, 'crit damage': 10, 'intelligence': 15},
			'legendary': {'crit chance': 20, 'crit damage': 15, 'intelligence': 20},
			'mythic': {'crit chance': 25, 'crit damage': 20, 'intelligence': 30},
			'stone': False
		},
		'heroic': {
			'common': {'strength': 15, 'intelligence': 15, 'attack speed': 1},
			'uncommon': {'strength': 20, 'intelligence': 20, 'attack speed': 2},
			'rare': {'strength': 25, 'intelligence': 25, 'attack speed': 4},
			'epic': {'strength': 32, 'intelligence': 32, 'attack speed': 7},
			'legendary': {'strength': 40, 'intelligence': 40, 'attack speed': 10},
			'mythic': {'strength': 50, 'intelligence': 50, 'attack speed': 15},
			'stone': False
		},
		'fabled': {
			'common': {'strength': 30, 'crit damage': 35},
			'uncommon': {'strength': 35, 'crit damage': 40},
			'rare': {'strength': 40, 'crit damage': 50},
			'epic': {'strength': 50, 'crit damage': 60},
			'legendary': {'strength': 60, 'crit damage': 80},
			'mythic': {'strength': 75, 'crit damage': 100},
			'stone': True
		}
	},
	'bows': {
		'awkward': {
			'common': {'crit chance': 10, 'crit damage': 5, 'intelligence': -5},
			'uncommon': {'crit chance': 12, 'crit damage': 10, 'intelligence': -10},
			'rare': {'crit chance': 15, 'crit damage': 15, 'intelligence': -18},
			'epic': {'crit chance': 20, 'crit damage': 22, 'intelligence': -32},
			'legendary': {'crit chance': 25, 'crit damage': 30, 'intelligence': -50},
			'mythic': {'crit chance': 30, 'crit damage': 40, 'intelligence': -60},
			'stone': False
		},
		'rich': {
			'common': {'crit chance': 10, 'crit damage': 2, 'intelligence': 3},
			'uncommon': {'crit chance': 12, 'crit damage': 4, 'intelligence': 6},
			'rare': {'crit chance': 15, 'crit damage': 7, 'intelligence': 10},
			'epic': {'crit chance': 20, 'crit damage': 10, 'intelligence': 15},
			'legendary': {'crit chance': 25, 'crit damage': 15, 'intelligence': 20},
			'mythic': {'crit chance': 30, 'crit damage': 20, 'intelligence': 30},
			'stone': False
		},
		'fine': {
			'common': {'strength': 3, 'crit chance': 5, 'crit damage': 2},
			'uncommon': {'strength': 7, 'crit chance': 7, 'crit damage': 4},
			'rare': {'strength': 12, 'crit chance': 9, 'crit damage': 7},
			'epic': {'strength': 18, 'crit chance': 12, 'crit damage': 10},
			'legendary': {'strength': 25, 'crit chance': 15, 'crit damage': 15},
			'mythic': {'strength': 40, 'crit chance': 20, 'crit damage': 20},
			'stone': False
		},
		'neat': {
			'common': {'crit chance': 10, 'crit damage': 5},
			'uncommon': {'crit chance': 13, 'crit damage': 10},
			'rare': {'crit chance': 16, 'crit damage': 18},
			'epic': {'crit chance': 19, 'crit damage': 32},
			'legendary': {'crit chance': 22, 'crit damage': 50},
			'mythic': {'crit chance': 25, 'crit damage': 75},
			'stone': False
		},
		'hasty': {
			'common': {'strength': 3, 'crit chance': 20},
			'uncommon': {'strength': 5, 'crit chance': 25},
			'rare': {'strength': 7, 'crit chance': 30},
			'epic': {'strength': 10, 'crit chance': 40},
			'legendary': {'strength': 15, 'crit chance': 50},
			'mythic': {'strength': 20, 'crit chance': 60},
			'stone': False
		},
		'grand': {
			'common': {'strength': 15},
			'uncommon': {'strength': 20},
			'rare': {'strength': 25},
			'epic': {'strength': 32},
			'legendary': {'strength': 40},
			'mythic': {'strength': 50},
			'stone': False
		},
		'rapid': {
			'common': {'strength': 2, 'crit damage': 35},
			'uncommon': {'strength': 3, 'crit damage': 45},
			'rare': {'strength': 4, 'crit damage': 55},
			'epic': {'strength': 7, 'crit damage': 65},
			'legendary': {'strength': 10, 'crit damage': 75},
			'mythic': {'strength': 12, 'crit damage': 80},
			'stone': False
		},
		'deadly': {
			'common': {'strength': 2, 'crit chance': 10, 'crit damage': 1, 'intelligence': 20},
			'uncommon': {'strength': 3, 'crit chance': 12, 'crit damage': 2, 'intelligence': 25},
			'rare': {'strength': 4, 'crit chance': 14, 'crit damage': 4, 'intelligence': 30},
			'epic': {'strength': 7, 'crit chance': 17, 'crit damage': 7, 'intelligence': 40},
			'legendary': {'strength': 10, 'crit chance': 20, 'crit damage': 10, 'intelligence': 50},
			'mythic': {'strength': 12, 'crit chance': 25, 'crit damage': 15, 'intelligence': 75},
			'stone': False
		},
		'unreal': {
			'common': {'strength': 3, 'crit chance': 10, 'crit damage': 5},
			'uncommon': {'strength': 7, 'crit chance': 11, 'crit damage': 10},
			'rare': {'strength': 12, 'crit chance': 12, 'crit damage': 18},
			'epic': {'strength': 18, 'crit chance': 13, 'crit damage': 32},
			'legendary': {'strength': 25, 'crit chance': 15, 'crit damage': 50},
			'mythic': {'strength': 40, 'crit chance': 17, 'crit damage': 75},
			'stone': False
		}
	},
	'armor': {
		'smart': {
			'common': {'defense': 4, 'speed': 4, 'intelligence': 20},
			'uncommon': {'defense': 5, 'speed': 5, 'intelligence': 40},
			'rare': {'defense': 6, 'speed': 6, 'intelligence': 60},
			'epic': {'defense': 8, 'speed': 8, 'intelligence': 80},
			'legendary': {'defense': 10, 'speed': 10, 'intelligence': 100},
			'mythic': {'defense': 14, 'speed': 14, 'intelligence': 120},
			'stone': False
		},
		'clean': {
			'common': {'defense': 5, 'speed': 5, 'health': 2},
			'uncommon': {'defense': 7, 'speed': 7, 'health': 4},
			'rare': {'defense': 10, 'speed': 10, 'health': 6},
			'epic': {'defense': 15, 'speed': 15, 'health': 8},
			'legendary': {'defense': 20, 'speed': 20, 'health': 10},
			'mythic': {'defense': 25, 'speed': 25, 'health': 12},
			'stone': False
		},
		'fierce': {
			'common': {'strength': 2, 'crit chance': 1, 'crit damage': 3, 'intelligence': 4},
			'uncommon': {'strength': 4, 'crit chance': 2,'crit damage': 6, 'intelligence': 5},
			'rare': {'strength': 6, 'crit chance': 3, 'crit damage': 9, 'intelligence': 7},
			'epic': {'strength': 8, 'crit chance': 4, 'crit damage': 12, 'intelligence': 10},
			'legendary': {'strength': 10, 'crit chance': 5, 'crit damage': 15, 'intelligence': 15},
			'mythic': {'strength': 12, 'crit chance': 6, 'crit damage': 20, 'intelligence': 20},
			'stone': False
		},
		'heavy': {
			'common': {'defense': 25, 'speed': -1, 'health': -1},
			'uncommon': {'defense': 35, 'speed': -1, 'health': -2},
			'rare': {'defense': 50, 'speed': -1, 'health': -3},
			'epic': {'defense': 65, 'speed': -1, 'health': -3},
			'legendary': {'defense': 80, 'speed': -1, 'health': -5},
			'mythic': {'defense': 110, 'speed': -1, 'health': -7},
			'stone': False
		},
		'light': {
			'common': {'defense': 1, 'speed': 1, 'health': 5, 'attack speed': 1, 'crit damage': 1},
			'uncommon': {'defense': 2, 'speed': 2, 'health': 7, 'attack speed': 2, 'crit damage': 2},
			'rare': {'defense': 3, 'speed': 3, 'health': 10, 'attack speed': 3, 'crit damage': 3},
			'epic': {'defense': 4, 'speed': 4, 'health': 15, 'attack speed': 4, 'crit damage': 4},
			'legendary': {'defense': 5, 'speed': 5, 'health': 20, 'attack speed': 5, 'crit damage': 5},
			'mythic': {'defense': 6, 'speed': 6, 'health': 25, 'attack speed': 6, 'crit damage': 6},
			'stone': False
		},
		'mythic': {
			'common': { 'strength': 2, 'defense': 2, 'speed': 2, 'health': 2, 'crit damage': 1, 'intelligence': 20},
			'uncommon': { 'strength': 4, 'defense': 4, 'speed': 2, 'health': 4, 'crit damage': 2, 'intelligence': 25},
			'rare': { 'strength': 6, 'defense': 6, 'speed': 2, 'health': 6, 'crit damage': 3, 'intelligence': 30},
			'epic': { 'strength': 8, 'defense': 8, 'speed': 2, 'health': 8, 'crit damage': 4, 'intelligence': 40},
			'legendary': { 'strength': 10, 'defense': 10, 'speed': 2, 'health': 10, 'crit damage': 5, 'intelligence': 50},
			'mythic': { 'strength': 12, 'defense': 12, 'speed': 2, 'health': 12, 'crit damage': 6, 'intelligence': 60},
			'stone': False
		},
		'titanic': {
			'common': {'defense': 10, 'health': 10},
			'uncommon': {'defense': 15, 'health': 15},
			'rare': {'defense': 20, 'health': 20},
			'epic': {'defense': 25, 'health': 25},
			'legendary': {'defense': 25, 'health': 35},
			'mythic': {'defense': 50, 'health': 50},
			'stone': False
		},
		'wise': {
			'common': {'speed': 1, 'health': 6, 'mana': 25},
			'uncommon': {'speed': 1, 'health': 8, 'mana': 50},
			'rare': {'speed': 1, 'health': 10, 'mana': 75},
			'epic': {'speed': 2, 'health': 12, 'mana': 100},
			'legendary': {'speed': 2, 'health': 15, 'mana': 125},
			'mythic': {'speed': 3, 'health': 20, 'mana': 150},
			'stone': False
		},
		'pure': {
			'common': {'strength': 2, 'defense': 2, 'speed': 1, 'health': 2, 'crit chance': 2, 'crit damage': 2, 'intelligence': 2, 'attack speed': 1},
			'uncommon': {'strength': 4, 'defense': 4, 'speed': 1, 'health': 4, 'crit chance': 4, 'crit damage': 4, 'intelligence': 4, 'attack speed': 2},
			'rare': {'strength': 6, 'defense': 6, 'speed': 1, 'health': 6, 'crit chance': 6, 'crit damage': 6, 'intelligence': 6, 'attack speed': 3},
			'epic': {'strength': 8, 'defense': 8, 'speed': 1, 'health': 8, 'crit chance': 9,'crit damage': 8, 'intelligence': 8, 'attack speed': 4},
			'legendary': {'strength': 10, 'defense': 10, 'speed': 1, 'health': 10, 'crit chance': 10, 'crit damage': 10, 'intelligence': 10, 'attack speed': 5},
			'mythic': {'strength': 12, 'defense': 12, 'speed': 1, 'health': 12, 'crit chance': 12, 'crit damage': 12, 'intelligence': 12, 'attack speed': 6},
			'stone': False
		},
		'necrotic': {
			'common': {'intelligence': 50},
			'uncommon': {'intelligence': 75},
			'rare': {'intelligence': 100},
			'epic': {'intelligence': 120},
			'legendary': {'intelligence': 150},
			'mythic': {'intelligence': 175},
			'stone': True
		},
		'perfect': {
			'common': {'defense': 10},
			'uncommon': {'defense': 15},
			'rare': {'defense': 25},
			'epic': {'defense': 50},
			'legendary': {'defense': 75},
			'mythic': {'defense': 100},
			'stone': True
		},
		'undead': {
			'common': {'strength': 1, 'defense': 9, 'health': 9, 'attack speed': 1},
			'uncommon': {'strength': 2, 'defense': 12, 'health': 12, 'attack speed': 2},
			'rare': {'strength': 2, 'defense': 15, 'health': 15, 'attack speed': 3},
			'epic': {'strength': 3, 'defense': 18, 'health': 18, 'attack speed': 4},
			'legendary': {'strength': 5, 'defense': 23, 'health': 23, 'attack speed': 5},
			'mythic': {'strength': 7, 'defense': 25, 'health': 25, 'attack speed': 6},
			'stone': True
		},
		'spiked': {
			'common': {'strength': 3, 'defense': 3, 'speed': 2, 'health': 3, 'crit chance': 3, 'crit damage': 3, 'intelligence': 3, 'attack speed': 1},
			'uncommon': {'strength': 5, 'defense': 5, 'speed': 2, 'health': 5, 'crit chance': 5, 'crit damage': 5, 'intelligence': 5, 'attack speed': 2},
			'rare': {'strength': 7, 'defense': 7, 'speed': 2, 'health': 7, 'crit chance': 7, 'crit damage': 7, 'intelligence': 7, 'attack speed': 3},
			'epic': {'strength': 9, 'defense': 9, 'speed': 2, 'health': 9, 'crit chance': 9, 'crit damage': 9, 'intelligence': 9, 'attack speed': 4},
			'legendary': {'strength': 12, 'defense': 12, 'speed': 2, 'health': 12, 'crit chance': 12, 'crit damage': 12, 'intelligence': 12, 'attack speed': 5},
			'mythic': {'strength': 15, 'defense': 15, 'speed': 2, 'health': 15, 'crit chance': 15, 'crit damage': 15, 'intelligence': 15, 'attack speed': 6},
			'stone': True
		},
		'renowned': {
			'common': {'strength': 3, 'defense': 3, 'speed': 2, 'health': 3, 'crit chance': 3, 'crit damage': 3, 'intelligence': 3, 'attack speed': 1},
			'uncommon': {'strength': 5, 'defense': 5, 'speed': 2, 'health': 5, 'crit chance': 5, 'crit damage': 5, 'intelligence': 5, 'attack speed': 2},
			'rare': {'strength': 7, 'defense': 7, 'speed': 2, 'health': 7, 'crit chance': 7, 'crit damage': 7, 'intelligence': 7, 'attack speed': 3},
			'epic': {'strength': 9, 'defense': 9, 'speed': 2, 'health': 9, 'crit chance': 9, 'crit damage': 9, 'intelligence': 9, 'attack speed': 4},
			'legendary': {'strength': 12, 'defense': 12, 'speed': 2, 'health': 12, 'crit chance': 12, 'crit damage': 12, 'intelligence': 12, 'attack speed': 5},
			'mythic': {'strength': 15, 'defense': 15, 'speed': 2, 'health': 15, 'crit chance': 15, 'crit damage': 15, 'intelligence': 15, 'attack speed': 6},
			'stone': True
		}
	},
	'talismans': {
		'bizzare': {
			'common': {'strength': 1, 'crit damage': 1, 'health': 1, 'intelligence': 3},
			'uncommon': {'strength': 2, 'crit damage': 2, 'health': 1, 'intelligence': 5},
			'rare': {'strength': 2, 'crit damage': 2, 'health': 1, 'intelligence': 8},
			'epic': {'strength': 3, 'crit damage': 3, 'health': 1, 'intelligence': 12},
			'legendary': {'strength': 5, 'crit damage': 5, 'health': 1, 'intelligence': 16},
			'mythic': {'strength': 7, 'crit damage': 7, 'health': 2, 'intelligence': 20},
			'stone': False
		},
		'ominus': {
			'common': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 0},
			'uncommon': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 1},
			'rare': {'strength': 1, 'defense': 1, 'health': 2, 'crit damage': 1, 'intelligence': 2},
			'epic': {'strength': 2, 'defense': 2, 'health': 3, 'crit damage': 1, 'intelligence': 3},
			'legendary': {'strength': 3, 'defense': 3, 'health': 4, 'crit damage': 1, 'intelligence': 4},
			'mythic': {'strength': 4, 'defense': 4, 'health': 5, 'crit damage': 1, 'intelligence': 5},
			'stone': False
		},
		'simple': {
			'common': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 1},
			'uncommon': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 1},
			'rare': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 1},
			'epic': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 1},
			'legendary': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 1},
			'mythic': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 1},
			'stone': False
		},
		'pleasant': {
			'common': {'defense': 4},
			'uncommon': {'defense': 5},
			'rare': {'defense': 7},
			'epic': {'defense': 10},
			'legendary': {'defense': 15},
			'mythic': {'defense': 20},
			'stone': False
		},
		'shiny': {
			'common': {'health': 4, 'intelligence': 1},
			'uncommon': {'health': 5, 'intelligence': 2},
			'rare': {'health': 7, 'intelligence': 2},
			'epic': {'health': 10, 'intelligence': 3},
			'legendary': {'health': 15, 'intelligence': 5},
			'mythic': {'health': 20, 'intelligence': 7},
			'stone': False
		},
		'vivid': {
			'common': {'speed': 1, 'health': 1, 'intelligence': 1},
			'uncommon': {'speed': 2, 'health': 2, 'intelligence': 2},
			'rare': {'speed': 3, 'health': 3, 'intelligence': 2},
			'epic': {'speed': 4, 'health': 4, 'intelligence': 3},
			'legendary': {'speed': 5, 'health': 5, 'intelligence': 5},
			'mythic': {'speed': 6, 'health': 6, 'intelligence': 7},
			'stone': False
		},
		'pretty': {
			'common': {'speed': 0, 'health': 1},
			'uncommon': {'speed': 0, 'health': 1},
			'rare': {'speed': 0, 'health': 2},
			'epic': {'speed': 1, 'health': 2},
			'legendary': {'speed': 1, 'health': 3},
			'mythic': {'speed': 2, 'health': 4},
			'stone': False
		},
		'itchy': {
			'common': {'strength': 1, 'crit damage': 3, 'intelligence': 3, 'attack speed': 0},
			'uncommon': {'strength': 1, 'crit damage': 4, 'intelligence': 4, 'attack speed': 0},
			'rare': {'strength': 1, 'crit damage': 5, 'intelligence': 6, 'attack speed': 1},
			'epic': {'strength': 2, 'crit damage': 7, 'intelligence': 9, 'attack speed': 1},
			'legendary': {'strength': 3, 'crit damage': 10, 'intelligence': 13, 'attack speed': 1},
			'mythic': {'strength': 4, 'crit damage': 15, 'intelligence': 18, 'attack speed': 1},
			'stone': False
		},
		'keen': {
			'common': {'defense': 1, 'health': 1, 'intelligence': 1},
			'uncommon': {'defense': 2, 'health': 2, 'intelligence': 2},
			'rare': {'defense': 3, 'health': 3, 'intelligence': 2},
			'epic': {'defense': 4, 'health': 4, 'intelligence': 3},
			'legendary': {'defense': 5, 'health': 5, 'intelligence': 4},
			'mythic': {'defense': 7, 'health': 7, 'intelligence': 5},
			'stone': False
		},
		'unpleasent': {
			'common': {'crit chance': 1},
			'uncommon': {'crit chance': 1},
			'rare': {'crit chance': 1},
			'epic': {'crit chance': 2},
			'legendary': {'crit chance': 2},
			'mythic': {'crit chance': 3},
			'stone': False
		},
		'superior': {
			'common': {'strength': 2, 'crit damage': 2},
			'uncommon': {'strength': 3, 'crit damage': 2},
			'rare': {'strength': 4, 'crit damage': 2},
			'epic': {'strength': 5, 'crit damage': 2},
			'legendary': {'strength': 7, 'crit damage': 3},
			'mythic': {'strength': 10, 'crit damage': 5},
			'stone': False
		},
		'forceful': {
			'common': {'strength': 4},
			'uncommon': {'strength': 5},
			'rare': {'strength': 7},
			'epic': {'strength': 10},
			'legendary': {'strength': 15},
			'mythic': {'strength': 20},
			'stone': False
		},
		'hurtful': {
			'common': {'crit damage': 4},
			'uncommon': {'crit damage': 5},
			'rare': {'crit damage': 7},
			'epic': {'crit damage': 10},
			'legendary': {'crit damage': 15},
			'mythic': {'crit damage': 20},
			'stone': False
		},
		'strong': {
			'common': {'strength': 1, 'crit damage': 1, 'defense': 0},
			'uncommon': {'strength': 2, 'crit damage': 2, 'defense': 0},
			'rare': {'strength': 3, 'crit damage': 3, 'defense': 1},
			'epic': {'strength': 5, 'crit damage': 5, 'defense': 2},
			'legendary': {'strength': 8, 'crit damage': 8, 'defense': 3},
			'mythic': {'strength': 12, 'crit damage': 12, 'defense': 4},
			'stone': False
		},
		'demonic': {
			'common': {'strength': 1, 'intelligence': 3},
			'uncommon': {'strength': 2, 'intelligence': 4},
			'rare': {'strength': 2, 'intelligence': 6},
			'epic': {'strength': 3, 'intelligence': 9},
			'legendary': {'strength': 5, 'intelligence': 13},
			'mythic': {'strength': 7, 'intelligence': 18},
			'stone': False
		},
		'zealous': {
			'common': {'strength': 1, 'speed': 0, 'crit damage': 1, 'intelligence': 1},
			'uncommon': {'strength': 1, 'speed': 0, 'crit damage': 2, 'intelligence': 2},
			'rare': {'strength': 1, 'speed': 1, 'crit damage': 2, 'intelligence': 2},
			'epic': {'strength': 1, 'speed': 1, 'crit damage': 3, 'intelligence': 3},
			'legendary': {'strength': 1, 'speed': 1, 'crit damage': 5, 'intelligence': 5},
			'mythic': {'strength': 1, 'speed': 2, 'crit damage': 7, 'intelligence': 7},
			'stone': False
		},
		'godly': {
			'common': {'strength': 1, 'crit damage': 2, 'intelligence': 1},
			'uncommon': {'strength': 2, 'crit damage': 2, 'intelligence': 1},
			'rare': {'strength': 3, 'crit damage': 3, 'intelligence': 1},
			'epic': {'strength': 5, 'crit damage': 4, 'intelligence': 2},
			'legendary': {'strength': 7, 'crit damage': 6, 'intelligence': 4},
			'mythic': {'strength': 10, 'crit damage': 8, 'intelligence': 6},
			'stone': False
		}
	},
	'fishing rod': {
		'legendary': {
			'common': {'strength': 3, 'crit chance': 10, 'crit damage': 5, 'intelligence': 5, 'attack speed': 3},
			'uncommon': {'strength': 7, 'crit chance': 12, 'crit damage': 10, 'intelligence': 8, 'attack speed': 5},
			'rare': {'strength': 14, 'crit chance': 14, 'crit damage': 15, 'intelligence': 12, 'attack speed': 7},
			'epic': {'strength': 18, 'crit chance': 17, 'crit damage': 22, 'intelligence': 18, 'attack speed': 10},
			'legendary': {'strength': 25, 'crit chance': 20, 'crit damage': 30, 'intelligence': 25, 'attack speed': 15},
			'mythic': {'strength': 40, 'crit chance': 25, 'crit damage': 40, 'intelligence': 35, 'attack speed': 20},
			'stone': False
		},
		'spicy': {
			'common': {'strength': 2, 'crit chance': 1, 'crit damage': 25, 'attack speed': 1},
			'uncommon': {'strength': 3, 'crit chance': 1, 'crit damage': 35, 'attack speed': 2},
			'rare': {'strength': 4, 'crit chance': 1, 'crit damage': 45, 'attack speed': 4},
			'epic': {'strength': 7, 'crit chance': 1, 'crit damage': 60, 'attack speed': 7},
			'legendary': {'strength': 10, 'crit chance': 1, 'crit damage': 80, 'attack speed': 10},
			'mythic': {'strength': 12, 'crit chance': 1, 'crit damage': 100, 'attack speed': 15},
			'stone': False
		},
		'epic': {
			'common': {'strength': 15, 'crit damage': 5, 'attack speed': 1},
			'uncommon': {'strength': 20, 'crit damage': 10, 'attack speed': 2},
			'rare': {'strength': 25, 'crit damage': 15, 'attack speed': 4},
			'epic': {'strength': 32, 'crit damage': 22, 'attack speed': 7},
			'legendary': {'strength': 40, 'crit damage': 30, 'attack speed': 10},
			'mythic': {'strength': 50, 'crit damage': 40, 'attack speed': 15},
			'stone': False
		},
		'odd': {
			'common': {'crit chance': 10, 'crit damage': 5, 'intelligence': -5},
			'uncommon': {'crit chance': 12, 'crit damage': 10, 'intelligence': -10},
			'rare': {'crit chance': 15, 'crit damage': 15, 'intelligence': -18},
			'epic': {'crit chance': 20, 'crit damage': 22, 'intelligence': -32},
			'legendary': {'crit chance': 25, 'crit damage': 30, 'intelligence': -50},
			'mythic': {'crit chance': 30, 'crit damage': 40, 'intelligence': -75},
			'stone': False
		},
		'gentle': {
			'common': {'strength': -2, 'attack speed': 10},
			'uncommon': {'strength': -4, 'attack speed': 20},
			'rare': {'strength': -6, 'attack speed': 30},
			'epic': {'strength': -8, 'attack speed': 40},
			'legendary': {'strength': -10, 'attack speed': 50},
			'mythic': {'strength': -12, 'attack speed': 60},
			'stone': False
		},
		'fast': {
			'common': {'strength': 3, 'attack speed': 8},
			'uncommon': {'strength': 5, 'attack speed': 10},
			'rare': {'strength': 7, 'attack speed': 15},
			'epic': {'strength': 10, 'attack speed': 20},
			'legendary': {'strength': 15, 'attack speed': 25},
			'mythic': {'strength': 20, 'attack speed': 30},
			'stone': False
		},
		'fair': {
			'common': {'strength': 2, 'crit chance': 2, 'crit damage': 2, 'intelligence': 2, 'attack speed': 2},
			'uncommon': {'strength': 3, 'crit chance': 3, 'crit damage': 3, 'intelligence': 3, 'attack speed': 3},
			'rare': {'strength': 4, 'crit chance': 4, 'crit damage': 4, 'intelligence': 4, 'attack speed': 4},
			'epic': {'strength': 7, 'crit chance': 7, 'crit damage': 7, 'intelligence': 7, 'attack speed': 7},
			'legendary': {'strength': 10, 'crit chance': 10, 'crit damage': 10, 'intelligence': 10, 'attack speed': 10},
			'mythic': {'strength': 12, 'crit chance': 12, 'crit damage': 12, 'intelligence': 12, 'attack speed': 12},
			'stone': False
		},
		'sharp': {
			'common': {'crit chance': 10, 'crit damage': 2, 'intelligence': 3},
			'uncommon': {'crit chance': 12, 'crit damage': 4, 'intelligence': 6},
			'rare': {'crit chance': 14, 'crit damage': 7, 'intelligence': 10},
			'epic': {'crit chance': 17, 'crit damage': 10, 'intelligence': 15},
			'legendary': {'crit chance': 20, 'crit damage': 15, 'intelligence': 20},
			'mythic': {'crit chance': 25, 'crit damage': 20, 'intelligence': 30},
			'stone': False
		},
		'heroic': {
			'common': {'strength': 15, 'intelligence': 15, 'attack speed': 1},
			'uncommon': {'strength': 20, 'intelligence': 20, 'attack speed': 2},
			'rare': {'strength': 25, 'intelligence': 25, 'attack speed': 4},
			'epic': {'strength': 32, 'intelligence': 32, 'attack speed': 7},
			'legendary': {'strength': 40, 'intelligence': 40, 'attack speed': 10},
			'mythic': {'strength': 50, 'intelligence': 50, 'attack speed': 15},
			'stone': False
		},
		'salty': {
			'common': {'sea creature chance': 1},
			'uncommon': {'sea creature chance': 2},
			'rare': {'sea creature chance': 2},
			'epic': {'sea creature chance': 3},
			'legendary': {'sea creature chance': 5},
			'mythic': {'sea creature chance': 7},
			'stone': False
		},
		'treacherous': {
			'common': {'sea creature chance': 1, 'strength': 5},
			'uncommon': {'sea creature chance': 2, 'strength': 10},
			'rare': {'sea creature chance': 2, 'strength': 15},
			'epic': {'sea creature chance': 3, 'strength': 20},
			'legendary': {'sea creature chance': 5, 'strength': 25},
			'mythic': {'sea creature chance': 7, 'strength': 30},
			'stone': False
		}
	}
}
