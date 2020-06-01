d = {
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
			'common': {'defense': 1, 'health': 1, 'crit chance': 5, 'attack speed': 1},
			'uncommon': {'defense': 2, 'health': 2, 'crit chance': 7, 'attack speed': 2},
			'rare': {'defense': 3, 'health': 3, 'crit chance': 10, 'attack speed': 3},
			'epic': {'defense': 4, 'health': 4, 'crit chance': 15, 'attack speed': 4},
			'legendary': {'defense': 5, 'health': 5, 'crit chance': 20, 'attack speed': 5},
			'mythic': {'defense': 6, 'health': 6, 'crit chance': 25, 'attack speed': 6},
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
}

result = {}

questions = ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic']
for reforge, rarities in d.items():
	for question in questions:
		add = True
		for other_reforge, other_rarities in d.items():
			if reforge != other_reforge and other_rarities['stone'] == False:
				s1, s2 = rarities[question].get('strength', 0), other_rarities[question].get('strength', 0)
				cc1, cc2 = rarities[question].get('crit chance', 0), other_rarities[question].get('crit chance', 0)
				cd1, cd2 = rarities[question].get('crit damage', 0), other_rarities[question].get('crit damage', 0)
				a1, a2 = rarities[question].get('attack speed', 0), other_rarities[question].get('attack speed', 0)
				if s1 == s2 and cc1 == cc2 and cd1 == cd2 and a1 == a2:
					print(reforge, other_reforge, question, 'equal')
				if s1 <= s2 and cc1 <= cc2 and cd1 <= cd2 and a1 <= a2:
					print(question, reforge, 'beaten by', other_reforge)
					add = False
					break
		if add:
			if reforge in result:
				result[reforge].append(question)
			else:
				result[reforge] = [question]
				
print(result)

result = {}

questions = ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic']
for reforge, rarities in d.items():
	for question in questions:
		add = True
		for other_reforge, other_rarities in d.items():
			if reforge != other_reforge:
				s1, s2 = rarities[question].get('strength', 0), other_rarities[question].get('strength', 0)
				cc1, cc2 = rarities[question].get('crit chance', 0), other_rarities[question].get('crit chance', 0)
				cd1, cd2 = rarities[question].get('crit damage', 0), other_rarities[question].get('crit damage', 0)
				a1, a2 = rarities[question].get('attack speed', 0), other_rarities[question].get('attack speed', 0)
				if s1 == s2 and cc1 == cc2 and cd1 == cd2 and a1 == a2:
					print(reforge, other_reforge, question, 'equal')
				if s1 <= s2 and cc1 <= cc2 and cd1 <= cd2 and a1 <= a2:
					print(question, reforge, 'beaten by', other_reforge)
					add = False
					break
		if add:
			if reforge in result:
				result[reforge].append(question)
			else:
				result[reforge] = [question]
				
print(result)
input()