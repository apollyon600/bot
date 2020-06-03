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
	'wolf': [10, 25, 250, 1500, 5000, 20000, 100000, 400000, 1000000]
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
