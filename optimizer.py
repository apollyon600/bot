from pyomo.environ import *

damage_reforges = {
	'sword': {
		'legendary': {
			'common': {'strength': 3, 'crit chance': 10, 'crit damage': 5, 'intelligence': 5, 'attack speed': 3},
			'uncommon': {'strength': 7, 'crit chance': 12, 'crit damage': 10, 'intelligence': 8, 'attack speed': 5},
			'rare': {'strength': 14, 'crit chance': 14, 'crit damage': 15, 'intelligence': 12, 'attack speed': 7},
			'epic': {'strength': 18, 'crit chance': 17, 'crit damage': 22, 'intelligence': 18, 'attack speed': 10},
			'legendary': {'strength': 25, 'crit chance': 20, 'crit damage': 30, 'intelligence': 25, 'attack speed': 15},
			'mythic': {'strength': 40, 'crit chance': 25, 'crit damage': 40, 'intelligence': 35, 'attack speed': 20}
		},
		'spicy': {
			'common': {'strength': 2, 'crit chance': 1, 'crit damage': 25, 'attack speed': 1},
			'uncommon': {'strength': 3, 'crit chance': 1, 'crit damage': 35, 'attack speed': 2},
			'rare': {'strength': 4, 'crit chance': 1, 'crit damage': 45, 'attack speed': 4},
			'epic': {'strength': 7, 'crit chance': 1, 'crit damage': 60, 'attack speed': 7},
			'legendary': {'strength': 10, 'crit chance': 1, 'crit damage': 80, 'attack speed': 10},
			'mythic': {'strength': 12, 'crit chance': 1, 'crit damage': 100, 'attack speed': 15}
		},
		'epic': {
			'common': {'strength': 15, 'crit damage': 5, 'attack speed': 1},
			'uncommon': {'strength': 20, 'crit damage': 10, 'attack speed': 2},
			'rare': {'strength': 25, 'crit damage': 15, 'attack speed': 4},
			'epic': {'strength': 32, 'crit damage': 22, 'attack speed': 7},
			'legendary': {'strength': 40, 'crit damage': 30, 'attack speed': 10},
			'mythic': {'strength': 50, 'crit damage': 40, 'attack speed': 15}
		},
		'odd': {
			'rare': {'crit chance': 15, 'crit damage': 15, 'intelligence': -18},
			'epic': {'crit chance': 20, 'crit damage': 22, 'intelligence': -32},
			'legendary': {'crit chance': 25, 'crit damage': 30, 'intelligence': -50},
			'mythic': {'crit chance': 30, 'crit damage': 40, 'intelligence': -75}
		},
		'gentle': {
			'common': {'strength': -2, 'attack speed': 10},
			'uncommon': {'strength': -4, 'attack speed': 20},
			'rare': {'strength': -6, 'attack speed': 30},
			'epic': {'strength': -8, 'attack speed': 40},
			'legendary': {'strength': -10, 'attack speed': 50},
			'mythic': {'strength': -12, 'attack speed': 60}
		},
		'fast': {
			'common': {'strength': 3, 'attack speed': 8},
			'uncommon': {'strength': 5, 'attack speed': 10},
			'rare': {'strength': 7, 'attack speed': 15},
			'epic': {'strength': 10, 'attack speed': 20},
			'legendary': {'strength': 15, 'attack speed': 25},
			'mythic': {'strength': 20, 'attack speed': 30}
		},
		'fabled': {
			'common': {'strength': 30, 'crit damage': 35},
			'uncommon': {'strength': 35, 'crit damage': 40},
			'rare': {'strength': 40, 'crit damage': 50},
			'epic': {'strength': 50, 'crit damage': 60},
			'legendary': {'strength': 60, 'crit damage': 80},
			'mythic': {'strength': 75, 'crit damage': 100}
		}
	},
	'bow': {
		'awkward': {
			'epic': {'crit chance': 20, 'crit damage': 22, 'intelligence': -32},
			'legendary': {'crit chance': 25, 'crit damage': 30, 'intelligence': -50},
			'mythic': {'crit chance': 30, 'crit damage': 40, 'intelligence': -60}
		},
		'fine': {
			'mythic': {'strength': 40, 'crit chance': 20, 'crit damage': 20}
		},
		'neat': {
			'common': {'crit chance': 10, 'crit damage': 5},
			'uncommon': {'crit chance': 13, 'crit damage': 10},
			'rare': {'crit chance': 16, 'crit damage': 18},
			'epic': {'crit chance': 19, 'crit damage': 32},
			'legendary': {'crit chance': 22, 'crit damage': 50},
			'mythic': {'crit chance': 25, 'crit damage': 75}
		},
		'hasty': {
			'common': {'strength': 3, 'crit chance': 20},
			'uncommon': {'strength': 5, 'crit chance': 25},
			'rare': {'strength': 7, 'crit chance': 30},
			'epic': {'strength': 10, 'crit chance': 40},
			'legendary': {'strength': 15, 'crit chance': 50},
			'mythic': {'strength': 20, 'crit chance': 60}
		},
		'grand': {
			'common': {'strength': 15},
			'uncommon': {'strength': 20},
			'rare': {'strength': 25},
			'epic': {'strength': 32},
			'legendary': {'strength': 40},
			'mythic': {'strength': 50}
		},
		'rapid': {
			'common': {'strength': 2, 'crit damage': 35},
			'uncommon': {'strength': 3, 'crit damage': 45},
			'rare': {'strength': 4, 'crit damage': 55},
			'epic': {'strength': 7, 'crit damage': 65},
			'legendary': {'strength': 10, 'crit damage': 75},
			'mythic': {'strength': 12, 'crit damage': 90}
		},
		'deadly': {
			'uncommon': {'strength': 3, 'crit chance': 12, 'crit damage': 2, 'intelligence': 25},
			'rare': {'strength': 4, 'crit chance': 14, 'crit damage': 4, 'intelligence': 30},
			'epic': {'strength': 7, 'crit chance': 17, 'crit damage': 7, 'intelligence': 40},
			'legendary': {'strength': 10, 'crit chance': 20, 'crit damage': 10, 'intelligence': 50},
			'mythic': {'strength': 12, 'crit chance': 25, 'crit damage': 15, 'intelligence': 75}
		},
		'unreal': {
			'common': {'strength': 3, 'crit chance': 10, 'crit damage': 5},
			'uncommon': {'strength': 7, 'crit chance': 11, 'crit damage': 10},
			'rare': {'strength': 12, 'crit chance': 12, 'crit damage': 18},
			'epic': {'strength': 18, 'crit chance': 13, 'crit damage': 32},
			'legendary': {'strength': 25, 'crit chance': 15, 'crit damage': 50},
			'mythic': {'strength': 40, 'crit chance': 17, 'crit damage': 75}
		}
	},
	'armor': {
		'fierce': {
			'common': {'strength': 2, 'crit chance': 1, 'crit damage': 3, 'intelligence': 4},
			'uncommon': {'strength': 4, 'crit chance': 2, 'crit damage': 6, 'intelligence': 5},
			'rare': {'strength': 6, 'crit chance': 3, 'crit damage': 9, 'intelligence': 7},
			'epic': {'strength': 8, 'crit chance': 4, 'crit damage': 12, 'intelligence': 10},
			'legendary': {'strength': 10, 'crit chance': 5, 'crit damage': 15, 'intelligence': 15},
			'mythic': {'strength': 12, 'crit chance': 6, 'crit damage': 20, 'intelligence': 20}
		},
		'pure': {
			'common': {'strength': 2, 'defense': 2, 'speed': 1, 'health': 2, 'crit chance': 2, 'crit damage': 2, 'intelligence': 2, 'attack speed': 1},
			'uncommon': {'strength': 4, 'defense': 4, 'speed': 1, 'health': 4, 'crit chance': 4, 'crit damage': 4, 'intelligence': 4, 'attack speed': 2},
			'rare': {'strength': 6, 'defense': 6, 'speed': 1, 'health': 6, 'crit chance': 6, 'crit damage': 6, 'intelligence': 6, 'attack speed': 3},
			'epic': {'strength': 8, 'defense': 8, 'speed': 1, 'health': 8, 'crit chance': 9, 'crit damage': 8, 'intelligence': 8, 'attack speed': 4},
			'legendary': {'strength': 10, 'defense': 10, 'speed': 1, 'health': 10, 'crit chance': 10, 'crit damage': 10, 'intelligence': 10, 'attack speed': 5},
			'mythic': {'strength': 12, 'defense': 12, 'speed': 1, 'health': 12, 'crit chance': 12, 'crit damage': 12, 'intelligence': 12, 'attack speed': 6}
		},
		'spiked': {
			'common': {'strength': 3, 'defense': 3, 'speed': 2, 'health': 3, 'crit chance': 3, 'crit damage': 3, 'intelligence': 3, 'attack speed': 1},
			'uncommon': {'strength': 5, 'defense': 5, 'speed': 2, 'health': 5, 'crit chance': 5, 'crit damage': 5, 'intelligence': 5, 'attack speed': 2},
			'rare': {'strength': 7, 'defense': 7, 'speed': 2, 'health': 7, 'crit chance': 7, 'crit damage': 7, 'intelligence': 7, 'attack speed': 3},
			'epic': {'strength': 9, 'defense': 9, 'speed': 2, 'health': 9, 'crit chance': 9, 'crit damage': 9, 'intelligence': 9, 'attack speed': 4},
			'legendary': {'strength': 12, 'defense': 12, 'speed': 2, 'health': 12, 'crit chance': 12, 'crit damage': 12, 'intelligence': 12, 'attack speed': 5},
			'mythic': {'strength': 15, 'defense': 15, 'speed': 2, 'health': 15, 'crit chance': 15, 'crit damage': 15, 'intelligence': 15, 'attack speed': 6}
		},
		'renowned': {
			'common': {'strength': 3, 'defense': 3, 'speed': 2, 'health': 3, 'crit chance': 3, 'crit damage': 3, 'intelligence': 3, 'attack speed': 1},
			'uncommon': {'strength': 5, 'defense': 5, 'speed': 2, 'health': 5, 'crit chance': 5, 'crit damage': 5, 'intelligence': 5, 'attack speed': 2},
			'rare': {'strength': 7, 'defense': 7, 'speed': 2, 'health': 7, 'crit chance': 7, 'crit damage': 7, 'intelligence': 7, 'attack speed': 3},
			'epic': {'strength': 9, 'defense': 9, 'speed': 2, 'health': 9, 'crit chance': 9, 'crit damage': 9, 'intelligence': 9, 'attack speed': 4},
			'legendary': {'strength': 12, 'defense': 12, 'speed': 2, 'health': 12, 'crit chance': 12, 'crit damage': 12, 'intelligence': 12, 'attack speed': 5},
			'mythic': {'strength': 15, 'defense': 15, 'speed': 2, 'health': 15, 'crit chance': 15, 'crit damage': 15, 'intelligence': 15, 'attack speed': 6}
		}
	},
	'talisman': {
		'itchy': {
			'common': {'strength': 1, 'crit damage': 3, 'attack speed': 0},
			'uncommon': {'strength': 1, 'crit damage': 4, 'attack speed': 0},
			'rare': {'strength': 1, 'crit damage': 5, 'attack speed': 1},
			'epic': {'strength': 2, 'crit damage': 7, 'attack speed': 1},
			'legendary': {'strength': 3, 'crit damage': 10, 'attack speed': 1},
			'mythic': {'strength': 4, 'crit damage': 15, 'attack speed': 1}
		},
		'unpleasant': {
			'common': {'crit chance': 1},
			'uncommon': {'crit chance': 1},
			'rare': {'crit chance': 1},
			'epic': {'crit chance': 2},
			'legendary': {'crit chance': 2},
			'mythic': {'crit chance': 3}
		},
		'superior': {
			'common': {'strength': 2, 'crit damage': 2},
			'uncommon': {'strength': 3, 'crit damage': 2},
			'rare': {'strength': 4, 'crit damage': 2}
		},
		'forceful': {
			'common': {'strength': 4},
			'uncommon': {'strength': 5},
			'rare': {'strength': 7},
			'epic': {'strength': 10},
			'legendary': {'strength': 15},
			'mythic': {'strength': 20}
		},
		'hurtful': {
			'common': {'crit damage': 4},
			'uncommon': {'crit damage': 5},
			'rare': {'crit damage': 7},
			'epic': {'crit damage': 10},
			'legendary': {'crit damage': 15},
			'mythic': {'crit damage': 20}
		},
		'strong': {
			'epic': {'strength': 5, 'crit damage': 5, 'defense': 2},
			'legendary': {'strength': 8, 'crit damage': 8, 'defense': 3},
			'mythic': {'strength': 12, 'crit damage': 12, 'defense': 4}
		},
		'godly/strong': {
			'rare': {'strength': 3, 'crit damage': 3, 'intelligence': 1}
		}
	},
	'fishing rod': {
		'legendary': {
			'common': {'strength': 3, 'crit chance': 10, 'crit damage': 5, 'intelligence': 5, 'attack speed': 3},
			'uncommon': {'strength': 7, 'crit chance': 12, 'crit damage': 10, 'intelligence': 8, 'attack speed': 5},
			'rare': {'strength': 14, 'crit chance': 14, 'crit damage': 15, 'intelligence': 12, 'attack speed': 7},
			'epic': {'strength': 18, 'crit chance': 17, 'crit damage': 22, 'intelligence': 18, 'attack speed': 10},
			'legendary': {'strength': 25, 'crit chance': 20, 'crit damage': 30, 'intelligence': 25, 'attack speed': 15},
			'mythic': {'strength': 40, 'crit chance': 25, 'crit damage': 40, 'intelligence': 35, 'attack speed': 20}
		},
		'spicy': {
			'common': {'strength': 2, 'crit chance': 1, 'crit damage': 25, 'attack speed': 1},
			'uncommon': {'strength': 3, 'crit chance': 1, 'crit damage': 35, 'attack speed': 2},
			'rare': {'strength': 4, 'crit chance': 1, 'crit damage': 45, 'attack speed': 4},
			'epic': {'strength': 7, 'crit chance': 1, 'crit damage': 60, 'attack speed': 7},
			'legendary': {'strength': 10, 'crit chance': 1, 'crit damage': 80, 'attack speed': 10},
			'mythic': {'strength': 12, 'crit chance': 1, 'crit damage': 100, 'attack speed': 15}
		},
		'epic': {
			'common': {'strength': 15, 'crit damage': 5, 'attack speed': 1},
			'uncommon': {'strength': 20, 'crit damage': 10, 'attack speed': 2},
			'rare': {'strength': 25, 'crit damage': 15, 'attack speed': 4},
			'epic': {'strength': 32, 'crit damage': 22, 'attack speed': 7},
			'legendary': {'strength': 40, 'crit damage': 30, 'attack speed': 10},
			'mythic': {'strength': 50, 'crit damage': 40, 'attack speed': 15}
		},
		'odd': {
			'rare': {'crit chance': 15, 'crit damage': 15, 'intelligence': -18},
			'epic': {'crit chance': 20, 'crit damage': 22, 'intelligence': -32},
			'legendary': {'crit chance': 25, 'crit damage': 30, 'intelligence': -50},
			'mythic': {'crit chance': 30, 'crit damage': 40, 'intelligence': -75}
		},
		'gentle': {
			'common': {'strength': -2, 'attack speed': 10},
			'uncommon': {'strength': -4, 'attack speed': 20},
			'rare': {'strength': -6, 'attack speed': 30},
			'epic': {'strength': -8, 'attack speed': 40},
			'legendary': {'strength': -10, 'attack speed': 50},
			'mythic': {'strength': -12, 'attack speed': 60}
		},
		'fast': {
			'common': {'strength': 3, 'attack speed': 8},
			'uncommon': {'strength': 5, 'attack speed': 10},
			'rare': {'strength': 7, 'attack speed': 15},
			'epic': {'strength': 10, 'attack speed': 20},
			'legendary': {'strength': 15, 'attack speed': 25},
			'mythic': {'strength': 20, 'attack speed': 30}
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
			'mythic': {'defense': 110, 'speed': -1, 'crit damage': -7}
		},
		'titanic': {
			'common': {'defense': 10, 'health': 10},
			'uncommon': {'defense': 15, 'health': 15},
			'rare': {'defense': 20, 'health': 20},
			'epic': {'defense': 25, 'health': 25},
			'legendary': {'defense': 25, 'health': 35},
			'mythic': {'defense': 50, 'health': 50}
		}
	},
	'talisman': {
		'simple': {
			'common': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 1, 'speed': 1}
		},
		'pleasant': {
			'common': {'defense': 4},
			'uncommon': {'defense': 5},
			'rare': {'defense': 7},
			'epic': {'defense': 10},
			'legendary': {'defense': 15},
			'mythic': {'defense': 20}
		},
		'shiny': {
			'common': {'health': 4, 'intelligence': 1},
			'uncommon': {'health': 5, 'intelligence': 2},
			'rare': {'health': 7, 'intelligence': 2},
			'epic': {'health': 10, 'intelligence': 3},
			'legendary': {'health': 15, 'intelligence': 5},
			'mythic': {'health': 20, 'intelligence': 7}
		},
		'keen': {
			'uncommon': {'defense': 2, 'health': 2, 'intelligence': 2},
			'rare': {'defense': 3, 'health': 3, 'intelligence': 2},
			'epic': {'defense': 4, 'health': 4, 'intelligence': 3},
			'legendary': {'defense': 5, 'health': 5, 'intelligence': 4},
			'mythic': {'defense': 7, 'health': 7, 'intelligence': 5}
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

rarities = ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic']

def damage_optimizer(player, talisman_rarity_counts, armor_rarity_counts, *, perfect_crit_chance, include_attack_speed):
	equipment_types = ['talisman', 'armor', player.weapon.type]

	m = ConcreteModel()

	m.reforge_set = Set(initialize=[(i, j, k) for i in equipment_types for j in rarities for k, stats in damage_reforges[i].items() if j in stats], ordered=True)
	m.reforge_counts = Var(m.reforge_set, domain=NonNegativeIntegers, initialize=0)
	m.s = Var(domain=NonNegativeIntegers, initialize=300)
	m.cd = Var(domain=NonNegativeIntegers, initialize=500)

	m.eqn = ConstraintList()
	m.eqn.add(m.s == quicksum([ehp_reforges[i][k][j].get('strength', 0) * m.reforge_counts[i, j, k] for i, j, k in m.reforge_set]))
	m.eqn.add(m.cd == quicksum([ehp_reforges[i][k][j].get('crit damage', 0) * m.reforge_counts[i, j, k] for i, j, k in m.reforge_set]))

	weapon_rarity_counts = {rarity: 0 for rarity in rarities}
	weapon_rarity_counts[player.weapon.rarity] = 1
	counts = {'talisman': talisman_rarity_counts, 'armor': armor_rarity_counts, player.weapon.type: weapon_rarity_counts}
	for equipment_type in equipment_types:
		reforges = damage_reforges[equipment_type]
		sums = {rarity: [] for rarity in rarities}
		for reforge in reforges.keys():
			for rarity in reforges[reforge].keys():
				sums[rarity].append(m.reforge_counts[equipment_type, rarity, reforge])
		for rarity in rarities:
			m.eqn.add(quicksum(quicksums[rarity]) == counts[equipment_type][rarity])

	if perfect_crit_chance:
		m.cc = Var(domain=NonNegativeIntegers, initialize=100)
		m.eqn.add(m.cc == quicksum([ehp_reforges[i][k][j].get('crit chance', 0) * m.reforge_counts[i, j, k] for i, j, k in m.reforge_set]) - 100)

	m.damage = Var(domain=Reals)
	weapon_dmg = 245
	ench_modifier = 500
	m.floored_strength = Var(domain=NonNegativeIntegers, initialize=60)
	m.eqn.add(m.floored_strength >= m.s / 5 - 0.9999)
	m.eqn.add(m.floored_strength <= m.s / 5)
	m.eqn.add(m.damage == (5 + weapon_dmg + m.floored_strength) * (1 + m.s / 100) * (1 + m.cd / 100))

	if include_attack_speed:
		m.a = Var(domain=NonNegativeIntegers, initialize=110)
		m.eqn.add(m.a == quicksum([ehp_reforges[i][k][j].get('attack speed', 0) * m.reforge_counts[i, j, k] for i, j, k in m.reforge_set]))
		m.objective = Objective(expr=(m.damage * (1 + m.a / 100)), sense=maximize)
	else:
		m.objective = Objective(expr=m.damage, sense=maximize)

	SolverFactory('scip', executable='scip').solve(m)
	
	result = {'damage': m.damage() * (1 + ench_modifier / 100), 'strength': m.s(), 'crit damage': m.cd(), 'crit chance': m.cc()}
	if include_attack_speed:
		result['attack speed'] = m.a()
	return result, format_counts(m.reforge_counts)

def ehp_optimizer(player, talisman_rarity_counts, armor_rarity_counts):
	equipment_types = ['talisman', 'armor']

	m = ConcreteModel()

	m.reforge_set = Set(initialize=[(i, j, k) for i in equipment_types for j in rarities for k, stats in ehp_reforges[i].items() if j in stats], ordered=True)
	m.reforge_counts = Var(m.reforge_set, domain=NonNegativeIntegers, initialize=0)
	m.hp = Var(domain=NonNegativeIntegers, initialize=1400)
	m.d = Var(domain=NonNegativeIntegers, initialize=700)

	m.eqn = ConstraintList()
	m.eqn.add(m.hp == quicksum([ehp_reforges[i][k][j].get('health', 0) * m.reforge_counts[i, j, k] for i, j, k in m.reforge_set]))
	m.eqn.add(m.d == quicksum([ehp_reforges[i][k][j].get('defense', 0) * m.reforge_counts[i, j, k] for i, j, k in m.reforge_set]))
	
	counts = {'talisman': talisman_rarity_counts, 'armor': armor_rarity_counts}
	for equipment_type in equipment_types:
		reforges = ehp_reforges[equipment_type]
		sums = {rarity: [] for rarity in rarities}
		for reforge in reforges.keys():
			for rarity in reforges[reforge].keys():
				sums[rarity].append(m.reforge_counts[equipment_type, rarity, reforge])
		for rarity in rarities:
			m.eqn.add(quicksum(quicksums[rarity]) == counts[equipment_type][rarity])

	m.objective = Objective(expr=(m.hp * (1 + m.d / 100)), sense=maximize)
	SolverFactory('scip', executable='scip').solve(m)
			
	return {'ehp': m.objective(), 'health': m.hp(), 'defense': m.d()}, format_counts(m.reforge_counts)