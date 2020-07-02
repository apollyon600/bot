from skypy.constants.constants import reforges
result2 = {}
for n, d in reforges.items():
	result = {}

	questions = ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic']
	for reforge, rarities in d.items():
		for question in questions:
			add = True
			equals = []
			for other_reforge, other_rarities in d.items():
				if reforge != other_reforge and other_rarities['blacksmith'] == True:
					s1, s2 = rarities[question].get('strength', 0), other_rarities[question].get('strength', 0)
					cc1, cc2 = rarities[question].get('crit chance', 0), other_rarities[question].get('crit chance', 0)
					cd1, cd2 = rarities[question].get('crit damage', 0), other_rarities[question].get('crit damage', 0)
					a1, a2 = rarities[question].get('attack speed', 0), other_rarities[question].get('attack speed', 0)
					if s1 <= s2 and cc1 <= cc2 and cd1 <= cd2 and a1 <= a2:
						if s1 == s2 and cc1 == cc2 and cd1 == cd2 and a1 == a2:
							if s1 > 0 or cc1 > 0 or cd1 > 0 or a1 > 0:
								equals.append((reforge, other_reforge, question))
						else:
							add = False
							break
			if add:
				for reforge, other_reforge, question in equals:
					print(reforge, other_reforge, question, 'equal')
				if reforge in result:
					result[reforge][question] = rarities[question]
				else:
					result[reforge] = {question: rarities[question]}
					
	result2[n] = result
print(result2)
print()
print()
result2 = {}
for n, d in reforges.items():
	if n in ('sword', 'bow', 'fishing rod'):
		continue
	result = {}

	questions = ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic']
	for reforge, rarities in d.items():
		for question in questions:
			add = True
			equals = []
			for other_reforge, other_rarities in d.items():
				if reforge != other_reforge and other_rarities['blacksmith'] == True:
					s1, s2 = rarities[question].get('defense', 0), other_rarities[question].get('defense', 0)
					cc1, cc2 = rarities[question].get('health', 0), other_rarities[question].get('health', 0)
					if s1 <= s2 and cc1 <= cc2:
						if s1 == s2 and cc1 == cc2:
							if s1 > 0 or cc1 > 0:
								equals.append((reforge, other_reforge, question))
						else:
							add = False
							break
			if add:
				for reforge, other_reforge, question in equals:
					print(reforge, other_reforge, question, 'equal')
				if reforge in result:
					result[reforge][question] = rarities[question]
				else:
					result[reforge] = {question: rarities[question]}
					
	result2[n] = result
print(result2)
print()
print()
result2 = {}
for n, d in reforges.items():
	if n in ('sword', 'bow', 'fishing rod'):
		continue
	result = {}

	questions = ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic']
	for reforge, rarities in d.items():
		for question in questions:
			add = True
			equals = []
			for other_reforge, other_rarities in d.items():
				if reforge != other_reforge and other_rarities['blacksmith'] == True:
					s1, s2 = rarities[question].get('speed', 0), other_rarities[question].get('speed', 0)
					if s1 <= s2:
						if s1 == s2:
							if s1 > 0:
								equals.append((reforge, other_reforge, question))
						else:
							add = False
							break
			if add:
				for reforge, other_reforge, question in equals:
					print(reforge, other_reforge, question, 'equal')
				if reforge in result:
					result[reforge][question] = rarities[question]
				else:
					result[reforge] = {question: rarities[question]}
					
	result2[n] = result
print(result2)