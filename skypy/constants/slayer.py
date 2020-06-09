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