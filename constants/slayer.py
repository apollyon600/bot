SLAYER_NAMES = ['zombie', 'spider', 'wolf']

SLAYER_REWARDS = {
    'zombie': [{'health': 0}, {'health': 2}, {'health': 4}, {'health': 7}, {'health': 10}, {'health': 14}, {'health': 18},
               {'health': 23}, {'health': 28}, {'health': 34}],
    'spider': [{'crit damage': 0}, {'crit damage': 1}, {'crit damage': 2}, {'crit damage': 3}, {'crit damage': 4}, {'crit damage': 6},
               {'crit damage': 8}, {'crit damage': 8, 'crit chance': 1}, {'crit damage': 11, 'crit chance': 1},
               {'crit damage': 14, 'crit chance': 1}],
    'wolf': [{'speed': 0}, {'speed': 1}, {'speed': 1, 'health': 2}, {'speed': 2, 'health': 2}, {'speed': 2, 'health': 4},
             {'speed': 2, 'health': 4, 'crit damage': 1}, {'speed': 2, 'health': 7, 'crit damage': 1},
             {'speed': 2, 'health': 7, 'crit damage': 3}, {'speed': 3, 'health': 7, 'crit damage': 3},
             {'speed': 3, 'health': 12, 'crit damage': 3}]
}

SLAYER_LEVEL_REQUIREMENT = {
    'zombie': [5, 15, 200, 1000, 5000, 20000, 100000, 400000, 1000000],
    'spider': [5, 15, 200, 1000, 5000, 20000, 100000, 400000, 1000000],
    'wolf': [10, 25, 250, 1500, 5000, 20000, 100000, 400000, 1000000]
}
