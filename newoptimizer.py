from pyomo.environ import *
from constants import reforges as _reforges
from pprint import pprint
import skypy

_reforges = _reforges['talismans']

def optimizer(rarity_counts):
	rarities = list(rarity_counts.keys())
	reforges = list(_reforges.keys())

	m = ConcreteModel()
	
	m.reforge_counts = Var(rarities, reforges, domain=Integers, bounds=lambda model, rarity, reforge: (0, rarity_counts[rarity]), initialize=0)
	m.s = Var(domain=NonNegativeIntegers, initialize=300)
	m.cd = Var(domain=NonNegativeIntegers, initialize=500)
	m.cc = Var(domain=NonNegativeIntegers, initialize=100)
	
	m.eqn = ConstraintList()
	m.eqn.add(m.s == sum([_reforges[j][i].get('strength', 0) * m.reforge_counts[i, j] for i in rarities for j in reforges]))
	m.eqn.add(m.cd == sum([_reforges[j][i].get('crit damage', 0) * m.reforge_counts[i, j] for i in rarities for j in reforges]))
	m.eqn.add(m.cc == sum([_reforges[j][i].get('crit chance', 0) * m.reforge_counts[i, j] for i in rarities for j in reforges]) - 100)
	for rarity in rarities:
		m.eqn.add(sum([m.reforge_counts[rarity, i] for i in reforges]) == rarity_counts[rarity])
	
	m.damage = Var(domain=Reals)
	weapon_dmg = 245
	ench_modifier = 500
	m.floored_strength = Var(domain=NonNegativeIntegers, initialize=60)
	m.eqn.add(m.floored_strength >= m.s / 5 - 0.9999)
	m.eqn.add(m.floored_strength <= m.s / 5)
	m.eqn.add(m.damage == (5 + weapon_dmg + m.floored_strength) * (1 + m.s / 100) * (1 + m.cd / 100) * (1 + ench_modifier / 100))
		
	m.objective = Objective(expr=m.damage, sense=maximize)
	SolverFactory('scip', executable='scip').solve(m)
	
	for i in rarities:
		for j in reforges:
			k = m.reforge_counts[i, j]()
			if k:
				print(i, j, round(k))
				
	print('will give', m.objective(), 'damage')
	print(m.s(), 'strength')
	print(m.cd(), 'crit damage')
	print(m.cc() + 100, 'crit chance')
	print(m.floored_strength())

optimizer({'common': 16, 'uncommon': 6, 'rare': 10, 'epic': 15, 'legendary': 10, 'mythic': 40})