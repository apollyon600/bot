timeout_emoji = ['🇹', '🇮', '🇲', '🇪', '🇴', '🇺', '✝️']

optimizers = [
    {'emoji': '💯', 'name': 'perfect crit chance'},
    {'emoji': '💥', 'name': 'maximum damage'}
]

white = ('', '')
gray = ('bf', '')
puke = ('css', '')
green = ('yaml', '')
blue = ('md', '#')
yellow = ('fix', '')
orange = ('glsl', '#')
red = ('diff', '-')
rarity_colors = {'common': gray, 'uncommon': green, 'rare': blue, 'epic': orange, 'legendary': yellow, 'mythic': red}

pet_emojis = {
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
    'GOLEM': '🗿',
}

damage_potions = {
    'dungeon': {
        'stats': {'strength': [0, 20, 20, 20], 'crit chance': [0, 10, 10, 15], 'crit damage': [0, 10, 10, 20],
                  'speed': [0, 5, 10, 10], 'defense': [0, 5, 5, 10]},
        'levels': [0, 1, 3]
    },
    'critical': {
        'stats': {'crit chance': [0, 10, 15, 20, 25], 'crit damage': [0, 10, 20, 30, 40]},
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

support_items = {
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

number_emojis = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
