TIMEOUT_EMOJIS = ['🇹', '🇮', '🇲', '🇪', '🇴', '🇺', '✝️']

OPTIMIZER_GOALS = [
    {'emoji': '💯', 'name': 'Perfect crit chance'},
    {'emoji': '💥', 'name': 'Maximum damage'}
]

WHITE = ('', '')
GRAY = ('bf', '')
PUKE = ('css', '')
GREEN = ('yaml', '')
BLUE = ('md', '#')
YELLOW = ('fix', '')
ORANGE = ('glsl', '#')
RED = ('diff', '-')
RARITY_COLORS = {'common': GRAY, 'uncommon': GREEN, 'rare': BLUE, 'epic': ORANGE, 'legendary': YELLOW, 'mythic': RED}

PET_EMOJIS = {
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

DAMAGE_POTIONS = {
    'dungeon': {
        'stats': {'strength': [0, 20, 20, 20, 30], 'crit chance': [0, 10, 10, 15, 15],
                  'crit damage': [0, 10, 10, 20, 20], 'speed': [0, 5, 10, 10, 10], 'defense': [0, 5, 5, 10, 15],
                  'archery bonus': [0, 0, 0, 0, 12.5]},
        'levels': [0, 1, 3, 4]
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
        'stats': {'archery bonus': [0, 17.5, 30, 55, 80]},
        'levels': [0, 3, 4]
    }
}

SUPPORT_ITEMS = {
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

NUMBER_EMOJIS = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

SKILL_EMOJIS = {
    'skill': '📈',
    'minion slots': '⛓',
    'farming': '🌾',
    'mining': '⛏',
    'combat': '⚔',
    'foraging': '🪓',
    'enchanting': '📖',
    'alchemy': '⚗',
    'fishing': '🎣',
    'taming': '🐣',
    'carpentry': '🪑',
    'runecrafting': '⚜️',
    'zombie': '🧟',
    'spider': '🕸️',
    'wolf': '🐺',
    'slayers': '☠️',
    'dungeons': '⚔️'
}

SKYBLOCK_EVENTS = {
    "magmaBoss": {
        'name': 'Magma Boss',
        'endpoint': 'skyblock/bosstimer/magma/estimatedSpawn',
        'emoji': '🌋'
    },
    "darkAuction": {
        'name': 'Dark Auction',
        'endpoint': 'skyblock/darkauction/estimate',
        'emoji': '🕵️'
    },
    "bankInterest": {
        'name': 'Bank Interest',
        'endpoint': 'skyblock/bank/interest/estimate',
        'emoji': '💸'
    },
    "newYear": {
        'name': 'New Year Celebration',
        'endpoint': 'skyblock/newyear/estimate',
        'emoji': '🍰'
    },
    "zoo": {
        'name': 'Travelling Zoo',
        'endpoint': 'skyblock/zoo/estimate',
        'emoji': '🐵'
    },
    "spookyFestival": {
        'name': 'Spooky Festival',
        'endpoint': 'skyblock/spookyFestival/estimate',
        'emoji': '🍬'
    },
    "winterEvent": {
        'name': 'Winter Event',
        'endpoint': 'skyblock/winter/estimate',
        'emoji': '❄️'
    },
    "jerryWorkshopEvent": {
        'name': 'Jerry Event',
        'endpoint': 'skyblock/jerryWorkshop/estimate',
        'emoji': '☃️'
    },
}
