from pyomo.environ import *

damage_reforges = {
	'sword': {
		'legendary': {
			'common': {'strength': 3, 'crit chance': 10, 'crit damage': 5, 'intelligence': 5, 'attack speed': 3},
			'uncommon': {'strength': 7, 'crit chance': 12, 'crit damage': 10, 'intelligence': 8, 'attack speed': 5},
			'rare': {'strength': 14, 'crit chance': 14, 'crit damage': 15, 'intelligence': 12, 'attack speed': 7},
			'epic': {'strength': 18, 'crit chance': 17, 'crit damage': 22, 'intelligence': 18, 'attack speed': 10},
			'legendary': {'strength': 25, 'crit chance': 20, 'crit damage': 30, 'intelligence': 25, 'attack speed': 15},
			'mythic': {'strength': 40, 'crit chance': 25, 'crit damage': 40, 'intelligence': 35, 'attack speed': 20},
			'blacksmith': True
		},
		'spicy': {
			'common': {'strength': 2, 'crit chance': 1, 'crit damage': 25, 'attack speed': 1},
			'uncommon': {'strength': 3, 'crit chance': 1, 'crit damage': 35, 'attack speed': 2},
			'rare': {'strength': 4, 'crit chance': 1, 'crit damage': 45, 'attack speed': 4},
			'epic': {'strength': 7, 'crit chance': 1, 'crit damage': 60, 'attack speed': 7},
			'legendary': {'strength': 10, 'crit chance': 1, 'crit damage': 80, 'attack speed': 10},
			'mythic': {'strength': 12, 'crit chance': 1, 'crit damage': 100, 'attack speed': 15},
			'blacksmith': True
		},
		'epic': {
			'common': {'strength': 15, 'crit damage': 5, 'attack speed': 1},
			'uncommon': {'strength': 20, 'crit damage': 10, 'attack speed': 2},
			'rare': {'strength': 25, 'crit damage': 15, 'attack speed': 4},
			'epic': {'strength': 32, 'crit damage': 22, 'attack speed': 7},
			'legendary': {'strength': 40, 'crit damage': 30, 'attack speed': 10},
			'mythic': {'strength': 50, 'crit damage': 40, 'attack speed': 15},
			'blacksmith': True
		},
		'odd': {
			'rare': {'crit chance': 15, 'crit damage': 15, 'intelligence': -18},
			'epic': {'crit chance': 20, 'crit damage': 22, 'intelligence': -32},
			'legendary': {'crit chance': 25, 'crit damage': 30, 'intelligence': -50},
			'mythic': {'crit chance': 30, 'crit damage': 40, 'intelligence': -75},
			'blacksmith': True
		},
		'gentle': {
			'common': {'strength': -2, 'attack speed': 10},
			'uncommon': {'strength': -4, 'attack speed': 20},
			'rare': {'strength': -6, 'attack speed': 30},
			'epic': {'strength': -8, 'attack speed': 40},
			'legendary': {'strength': -10, 'attack speed': 50},
			'mythic': {'strength': -12, 'attack speed': 60},
			'blacksmith': True
		},
		'fast': {
			'common': {'strength': 3, 'attack speed': 8},
			'uncommon': {'strength': 5, 'attack speed': 10},
			'rare': {'strength': 7, 'attack speed': 15},
			'epic': {'strength': 10, 'attack speed': 20},
			'legendary': {'strength': 15, 'attack speed': 25},
			'mythic': {'strength': 20, 'attack speed': 30},
			'blacksmith': True
		},
		'fabled': {
			'common': {'strength': 30, 'crit damage': 35},
			'uncommon': {'strength': 35, 'crit damage': 40},
			'rare': {'strength': 40, 'crit damage': 50},
			'epic': {'strength': 50, 'crit damage': 60},
			'legendary': {'strength': 60, 'crit damage': 80},
			'mythic': {'strength': 75, 'crit damage': 100},
			'blacksmith': False
		}
	},
	'bow': {
		'awkward': {
			'epic': {'crit chance': 20, 'crit damage': 22, 'intelligence': -32},
			'legendary': {'crit chance': 25, 'crit damage': 30, 'intelligence': -50},
			'mythic': {'crit chance': 30, 'crit damage': 40, 'intelligence': -60},
			'blacksmith': True
		},
		'fine': {
			'mythic': {'strength': 40, 'crit chance': 20, 'crit damage': 20},
			'blacksmith': True
		},
		'neat': {
			'common': {'crit chance': 10, 'crit damage': 5},
			'uncommon': {'crit chance': 13, 'crit damage': 10},
			'rare': {'crit chance': 16, 'crit damage': 18},
			'epic': {'crit chance': 19, 'crit damage': 32},
			'legendary': {'crit chance': 22, 'crit damage': 50},
			'mythic': {'crit chance': 25, 'crit damage': 75},
			'blacksmith': True
		},
		'hasty': {
			'common': {'strength': 3, 'crit chance': 20},
			'uncommon': {'strength': 5, 'crit chance': 25},
			'rare': {'strength': 7, 'crit chance': 30},
			'epic': {'strength': 10, 'crit chance': 40},
			'legendary': {'strength': 15, 'crit chance': 50},
			'mythic': {'strength': 20, 'crit chance': 60},
			'blacksmith': True
		},
		'grand': {
			'common': {'strength': 15},
			'uncommon': {'strength': 20},
			'rare': {'strength': 25},
			'epic': {'strength': 32},
			'legendary': {'strength': 40},
			'mythic': {'strength': 50},
			'blacksmith': True
		},
		'rapid': {
			'common': {'strength': 2, 'crit damage': 35},
			'uncommon': {'strength': 3, 'crit damage': 45},
			'rare': {'strength': 4, 'crit damage': 55},
			'epic': {'strength': 7, 'crit damage': 65},
			'legendary': {'strength': 10, 'crit damage': 75},
			'mythic': {'strength': 12, 'crit damage': 90},
			'blacksmith': True
		},
		'deadly': {
			'uncommon': {'strength': 3, 'crit chance': 12, 'crit damage': 2, 'intelligence': 25},
			'rare': {'strength': 4, 'crit chance': 14, 'crit damage': 4, 'intelligence': 30},
			'epic': {'strength': 7, 'crit chance': 17, 'crit damage': 7, 'intelligence': 40},
			'legendary': {'strength': 10, 'crit chance': 20, 'crit damage': 10, 'intelligence': 50},
			'mythic': {'strength': 12, 'crit chance': 25, 'crit damage': 15, 'intelligence': 75},
			'blacksmith': True
		},
		'unreal': {
			'common': {'strength': 3, 'crit chance': 10, 'crit damage': 5},
			'uncommon': {'strength': 7, 'crit chance': 11, 'crit damage': 10},
			'rare': {'strength': 12, 'crit chance': 12, 'crit damage': 18},
			'epic': {'strength': 18, 'crit chance': 13, 'crit damage': 32},
			'legendary': {'strength': 25, 'crit chance': 15, 'crit damage': 50},
			'mythic': {'strength': 40, 'crit chance': 17, 'crit damage': 75},
			'blacksmith': True
		}
	},
	'armor': {
		'fierce': {
			'common': {'strength': 2, 'crit chance': 1, 'crit damage': 3, 'intelligence': 4},
			'uncommon': {'strength': 4, 'crit chance': 2, 'crit damage': 6, 'intelligence': 5},
			'rare': {'strength': 6, 'crit chance': 3, 'crit damage': 9, 'intelligence': 7},
			'epic': {'strength': 8, 'crit chance': 4, 'crit damage': 12, 'intelligence': 10},
			'legendary': {'strength': 10, 'crit chance': 5, 'crit damage': 15, 'intelligence': 15},
			'mythic': {'strength': 12, 'crit chance': 6, 'crit damage': 20, 'intelligence': 20},
			'blacksmith': True
		},
		'pure': {
			'common': {'strength': 2, 'defense': 2, 'speed': 1, 'health': 2, 'crit chance': 2, 'crit damage': 2, 'intelligence': 2, 'attack speed': 1},
			'uncommon': {'strength': 4, 'defense': 4, 'speed': 1, 'health': 4, 'crit chance': 4, 'crit damage': 4, 'intelligence': 4, 'attack speed': 2},
			'rare': {'strength': 6, 'defense': 6, 'speed': 1, 'health': 6, 'crit chance': 6, 'crit damage': 6, 'intelligence': 6, 'attack speed': 3},
			'epic': {'strength': 8, 'defense': 8, 'speed': 1, 'health': 8, 'crit chance': 9, 'crit damage': 8, 'intelligence': 8, 'attack speed': 4},
			'legendary': {'strength': 10, 'defense': 10, 'speed': 1, 'health': 10, 'crit chance': 10, 'crit damage': 10, 'intelligence': 10, 'attack speed': 5},
			'mythic': {'strength': 12, 'defense': 12, 'speed': 1, 'health': 12, 'crit chance': 12, 'crit damage': 12, 'intelligence': 12, 'attack speed': 6},
			'blacksmith': True
		},
		'renowned': {
			'common': {'strength': 3, 'defense': 3, 'speed': 2, 'health': 3, 'crit chance': 3, 'crit damage': 3, 'intelligence': 3, 'attack speed': 1},
			'uncommon': {'strength': 5, 'defense': 5, 'speed': 2, 'health': 5, 'crit chance': 5, 'crit damage': 5, 'intelligence': 5, 'attack speed': 2},
			'rare': {'strength': 7, 'defense': 7, 'speed': 2, 'health': 7, 'crit chance': 7, 'crit damage': 7, 'intelligence': 7, 'attack speed': 3},
			'epic': {'strength': 9, 'defense': 9, 'speed': 2, 'health': 9, 'crit chance': 9, 'crit damage': 9, 'intelligence': 9, 'attack speed': 4},
			'legendary': {'strength': 12, 'defense': 12, 'speed': 2, 'health': 12, 'crit chance': 12, 'crit damage': 12, 'intelligence': 12, 'attack speed': 5},
			'mythic': {'strength': 15, 'defense': 15, 'speed': 2, 'health': 15, 'crit chance': 15, 'crit damage': 15, 'intelligence': 15, 'attack speed': 6},
			'blacksmith': False
		}
	},
	'talisman': {
		'itchy': {
			'common': {'strength': 1, 'crit damage': 3, 'attack speed': 0},
			'uncommon': {'strength': 1, 'crit damage': 4, 'attack speed': 0},
			'rare': {'strength': 1, 'crit damage': 5, 'attack speed': 1},
			'epic': {'strength': 2, 'crit damage': 7, 'attack speed': 1},
			'legendary': {'strength': 3, 'crit damage': 10, 'attack speed': 1},
			'mythic': {'strength': 4, 'crit damage': 15, 'attack speed': 1},
			'blacksmith': True
		},
		'unpleasant': {
			'common': {'crit chance': 1},
			'uncommon': {'crit chance': 1},
			'rare': {'crit chance': 1},
			'epic': {'crit chance': 2},
			'legendary': {'crit chance': 2},
			'mythic': {'crit chance': 3},
			'blacksmith': True
		},
		'superior': {
			'common': {'strength': 2, 'crit damage': 2},
			'uncommon': {'strength': 3, 'crit damage': 2},
			'rare': {'strength': 4, 'crit damage': 2},
			'blacksmith': True
		},
		'forceful': {
			'common': {'strength': 4},
			'uncommon': {'strength': 5},
			'rare': {'strength': 7},
			'epic': {'strength': 10},
			'legendary': {'strength': 15},
			'mythic': {'strength': 20},
			'blacksmith': True
		},
		'hurtful': {
			'common': {'crit damage': 4},
			'uncommon': {'crit damage': 5},
			'rare': {'crit damage': 7},
			'epic': {'crit damage': 10},
			'legendary': {'crit damage': 15},
			'mythic': {'crit damage': 20},
			'blacksmith': True
		},
		'strong': {
			'epic': {'strength': 5, 'crit damage': 5, 'defense': 2},
			'legendary': {'strength': 8, 'crit damage': 8, 'defense': 3},
			'mythic': {'strength': 12, 'crit damage': 12, 'defense': 4},
			'blacksmith': True
		},
		'godly/strong': {
			'rare': {'strength': 3, 'crit damage': 3, 'intelligence': 1},
			'blacksmith': True
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
			'blacksmith': True
		},
		'spicy': {
			'common': {'strength': 2, 'crit chance': 1, 'crit damage': 25, 'attack speed': 1},
			'uncommon': {'strength': 3, 'crit chance': 1, 'crit damage': 35, 'attack speed': 2},
			'rare': {'strength': 4, 'crit chance': 1, 'crit damage': 45, 'attack speed': 4},
			'epic': {'strength': 7, 'crit chance': 1, 'crit damage': 60, 'attack speed': 7},
			'legendary': {'strength': 10, 'crit chance': 1, 'crit damage': 80, 'attack speed': 10},
			'mythic': {'strength': 12, 'crit chance': 1, 'crit damage': 100, 'attack speed': 15},
			'blacksmith': True
		},
		'epic': {
			'common': {'strength': 15, 'crit damage': 5, 'attack speed': 1},
			'uncommon': {'strength': 20, 'crit damage': 10, 'attack speed': 2},
			'rare': {'strength': 25, 'crit damage': 15, 'attack speed': 4},
			'epic': {'strength': 32, 'crit damage': 22, 'attack speed': 7},
			'legendary': {'strength': 40, 'crit damage': 30, 'attack speed': 10},
			'mythic': {'strength': 50, 'crit damage': 40, 'attack speed': 15},
			'blacksmith': True
		},
		'odd': {
			'rare': {'crit chance': 15, 'crit damage': 15, 'intelligence': -18},
			'epic': {'crit chance': 20, 'crit damage': 22, 'intelligence': -32},
			'legendary': {'crit chance': 25, 'crit damage': 30, 'intelligence': -50},
			'mythic': {'crit chance': 30, 'crit damage': 40, 'intelligence': -75},
			'blacksmith': True
		},
		'gentle': {
			'common': {'strength': -2, 'attack speed': 10},
			'uncommon': {'strength': -4, 'attack speed': 20},
			'rare': {'strength': -6, 'attack speed': 30},
			'epic': {'strength': -8, 'attack speed': 40},
			'legendary': {'strength': -10, 'attack speed': 50},
			'mythic': {'strength': -12, 'attack speed': 60},
			'blacksmith': True
		},
		'fast': {
			'common': {'strength': 3, 'attack speed': 8},
			'uncommon': {'strength': 5, 'attack speed': 10},
			'rare': {'strength': 7, 'attack speed': 15},
			'epic': {'strength': 10, 'attack speed': 20},
			'legendary': {'strength': 15, 'attack speed': 25},
			'mythic': {'strength': 20, 'attack speed': 30},
			'blacksmith': True
		}
	}
}

ehp_reforges = {
	'armor': {
		'heavy': {
			'common': {'defense': 25, 'speed': -1, 'crit damage': -1},
			'uncommon': {'defense': 35, 'speed': -1, 'crit damage': -2},
			'rare': {'defense': 50, 'speed': -1, 'crit damage': -3},
			'epic': {'defense': 65, 'speed': -1, 'crit damage': -3},
			'legendary': {'defense': 80, 'speed': -1, 'crit damage': -5},
			'mythic': {'defense': 110, 'speed': -1, 'crit damage': -7},
			'blacksmith': True
		},
		'titanic': {
			'common': {'defense': 10, 'health': 10},
			'uncommon': {'defense': 15, 'health': 15},
			'rare': {'defense': 20, 'health': 20},
			'epic': {'defense': 25, 'health': 25},
			'legendary': {'defense': 25, 'health': 35},
			'mythic': {'defense': 50, 'health': 50},
			'blacksmith': True
		}
	},
	'talisman': {
		'simple': {
			'common': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 1, 'speed': 1},
			'blacksmith': True
		},
		'pleasant': {
			'common': {'defense': 4},
			'uncommon': {'defense': 5},
			'rare': {'defense': 7},
			'epic': {'defense': 10},
			'legendary': {'defense': 15},
			'mythic': {'defense': 20},
			'blacksmith': True
		},
		'shiny': {
			'common': {'health': 4, 'intelligence': 1},
			'uncommon': {'health': 5, 'intelligence': 2},
			'rare': {'health': 7, 'intelligence': 2},
			'epic': {'health': 10, 'intelligence': 3},
			'legendary': {'health': 15, 'intelligence': 5},
			'mythic': {'health': 20, 'intelligence': 7},
			'blacksmith': True
		},
		'keen': {
			'uncommon': {'defense': 2, 'health': 2, 'intelligence': 2},
			'rare': {'defense': 3, 'health': 3, 'intelligence': 2},
			'epic': {'defense': 4, 'health': 4, 'intelligence': 3},
			'legendary': {'defense': 5, 'health': 5, 'intelligence': 4},
			'mythic': {'defense': 7, 'health': 7, 'intelligence': 5},
			'blacksmith': True
		}
	}
}

def format_counts(counts):
	result = {}
	for (equipment_type, rarity, reforge), count in counts.get_values().items():
		count = round(count)
		if count > 0:
			if equipment_type not in result:
				result[equipment_type] = {}
			if rarity not in result[equipment_type]:
				result[equipment_type][rarity] = {}
				
			result[equipment_type][rarity][reforge] = count
			
	return result

def solve(m):
	SolverFactory('scip', executable='scip').solve(m)

def create_model(counts, reforge_set, only_blacksmith_reforges):
	m = ConcreteModel()
	m.reforge_set = Set(
		initialize=[
			(i, j, k) for i, count in counts.items() for j in rarities for k, stats in damage_reforges[i].items()
			if j in stats and count[j] > 0 and (only_blacksmith_reforges is False or stats['blacksmith'] is True)
		], ordered=True
	)
	m.reforge_counts = Var(m.reforge_set, domain=NonNegativeIntegers, initialize=0)
	m.eqn = ConstraintList()
	return m

rarities = ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic']

def damage_optimizer(player, talisman_rarity_counts, *, perfect_crit_chance, include_attack_speed, only_blacksmith_reforges):
	armor_types = [type for type, piece in player.armor.items() if piece]
	equipment_types = ['talisman', player.weapon.type] + armor_types
	counts = {'talisman': talisman_rarity_counts, player.weapon.type: {rarity: int(player.weapon.rarity == rarity) for rarity in rarities}}
	for name in player.armor.keys():
		counts[name] = {rarity: int(player.armor[name].rarity == rarity) for rarity in rarities}
		
	m = create_model(counts, damage_reforges, only_blacksmith_reforges)
	
	for equipment_type in equipment_types:
		reforges = damage_reforges[equipment_type]
		sums = {rarity: [] for rarity in rarities}
		for reforge in reforges.keys():
			for rarity in reforges[reforge].keys():
				sums[rarity].append(m.reforge_counts[equipment_type, rarity, reforge])
		for rarity in rarities:
			m.eqn.add(quicksum(sums[rarity]) == counts[equipment_type][rarity])

	if only_blacksmith_reforges is False:
		player.stats.multiplier += quicksum(m.reforge_counts[piece, rarity, 'renowned'] for piece in armor_types for rarity in rarities) / 100

	for stat in ['strength', 'crit damage'] + ['crit chance'] * perfect_crit_chance + ['attack speed'] * include_attack_speed:
		player.stats.modifiers[stat].insert(0, 
			lambda stat: stat + quicksum(damage_reforges[i][k][j].get(stat, 0) * m.reforge_counts[i, j, k] for i, j, k in m.reforge_set)
		)
	
	if perfect_crit_chance:
		m.eqn.add(100 <= player.stats['crit damage'])

	m.damage = Var(domain=Reals)
	m.floored_strength = Var(domain=Integers, initialize=60)
	m.eqn.add(m.floored_strength >= player.stats['strength'] / 5 - 0.9999)
	m.eqn.add(m.floored_strength <= player.stats['strength'] / 5)
	m.eqn.add(m.damage == (5 + player.stats['damage'] + m.floored_strength) * (1 + m.s / 100) * (1 + m.cd / 100))

	m.objective = Objective(expr=m.damage if include_attack_speed else m.damage * player.stats['attack speed'] / 100, sense=maximize)
	solve(m)
	
	result = {'damage': m.damage() * (1 + player.stats['enchantment modifier'] / 100), 'strength': player.stats['strength'](), 'crit damage': player.stats['crit damage']()}
	if perfect_crit_chance:
		result['crit chance'] = player.stats['crit chance']()
	if include_attack_speed:
		result['attack speed'] = player.stats['attack speed']()
	return result, format_counts(m.reforge_counts)

def ehp_optimizer(player, talisman_rarity_counts, *, only_blacksmith_reforges):
	equipment_types = ['talisman', 'armor']

	m = create_model(equipment_types, ehp_reforges)
	
	m.m = 1 + player.stats['multiplier'] / 100
	
	m.hp = Var(domain=Reals, initialize=1400)
	m.eqn.add(m.hp == max(0, m.m * (quicksum(ehp_reforges[i][k][j].get('health', 0) * m.reforge_counts[i, j, k] for i, j, k in m.reforge_set) + player.stats['health'])))
	m.d = Var(domain=Reals, initialize=700)
	m.eqn.add(m.d == max(0, m.m * (quicksum(ehp_reforges[i][k][j].get('defense', 0) * m.reforge_counts[i, j, k] for i, j, k in m.reforge_set) + player.stats['defense'])))
	
	counts = {'talisman': talisman_rarity_counts, 'armor': armor_rarity_counts}
	for equipment_type in equipment_types:
		reforges = ehp_reforges[equipment_type]
		sums = {rarity: [] for rarity in rarities}
		for reforge in reforges.keys():
			for rarity in reforges[reforge].keys():
				sums[rarity].append(m.reforge_counts[equipment_type, rarity, reforge])
		for rarity in rarities:
			m.eqn.add(quicksum(sums[rarity]) == counts[equipment_type][rarity])

	m.objective = Objective(expr=(m.hp * (1 + m.d / 100)), sense=maximize)
	solve(m)
			
	return {'ehp': m.objective(), 'health': m.hp(), 'defense': m.d()}, format_counts(m.reforge_counts)
	
def mastiff_ehp_optimizer(only_blacksmith_reforges):
	if only_blacksmith_reforges:
		return '''Reforge all your armor to fierce
Reforge all your talismans to hurtful
Reforge your sword/fishing rod to spicy
Reforge your bow to rapid'''
	else:
		return '''Reforge all your armor to fierce
Reforge all your talismans to hurtful
Reforge your sword/fishing rod to spicy or fabled
Reforge your bow to rapid'''

def intelligence_optimizer(only_blacksmith_reforges):
	if only_blacksmith_reforges:
		return '''Reforge all your armor to wise
Reforge all your common talismans to demonic
Reforge all your other talismans to bizzare
Reforge your sword/fishing rod to heroic
Reforge your bow to deadly'''
	else:
		return '''Reforge all your armor to necrotic
Reforge all your common talismans to demonic
Reforge all your other talismans to bizzare
Reforge your sword/fishing rod to heroic
Reforge your bow to deadly'''

def speed_optimizer(only_blacksmith_reforges):
	if only_blacksmith_reforges:
		return '''Reforge your common talismans to simple
Reforge your other talismans to vivid
Reforge your common and uncommon armor to mythic
Reforge your other armor to light
Sword/bow/fishing rod reforges don't matter'''
	else:
		return '''Reforge your common talismans to simple
Reforge your other talismans to vivid
Reforge your common and uncommon armor to renowned or spiked
Reforge your other armor to light
Sword/bow/fishing rod reforges don't matter'''