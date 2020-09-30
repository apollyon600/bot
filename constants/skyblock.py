import re

SWORD_ENCHANTS = [
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

BOW_ENCHANTS = [
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

ROD_ENCHANTS = [
    'angler',
    'blessing',
    'caster',
    'frail',
    'luck_of_the_sea',
    'lure',
    'magnet',
    'looting'
]

SKILL_REWARDS = {
    'farming': [{'health': 0}, {'health': 2}, {'health': 4}, {'health': 6}, {'health': 8}, {'health': 10},
                {'health': 12}, {'health': 14}, {'health': 16}, {'health': 18}, {'health': 20}, {'health': 22},
                {'health': 24}, {'health': 26}, {'health': 28}, {'health': 31}, {'health': 34}, {'health': 37},
                {'health': 40}, {'health': 43}, {'health': 47}, {'health': 51}, {'health': 55}, {'health': 59},
                {'health': 63}, {'health': 67}, {'health': 72}, {'health': 77}, {'health': 82}, {'health': 87},
                {'health': 92}, {'health': 97}, {'health': 102}, {'health': 107}, {'health': 112}, {'health': 117},
                {'health': 122}, {'health': 127}, {'health': 132}, {'health': 137}, {'health': 142}, {'health': 147},
                {'health': 152}, {'health': 157}, {'health': 162}, {'health': 167}, {'health': 172}, {'health': 177},
                {'health': 182}, {'health': 187}, {'health': 192}],
    'mining': [{'defense': 0}, {'defense': 1}, {'defense': 2}, {'defense': 3}, {'defense': 4}, {'defense': 5},
               {'defense': 6}, {'defense': 7}, {'defense': 8}, {'defense': 9}, {'defense': 10}, {'defense': 11},
               {'defense': 12}, {'defense': 13}, {'defense': 14}, {'defense': 16}, {'defense': 18}, {'defense': 20},
               {'defense': 22}, {'defense': 24}, {'defense': 26}, {'defense': 28}, {'defense': 30}, {'defense': 32},
               {'defense': 34}, {'defense': 36}, {'defense': 38}, {'defense': 40}, {'defense': 42}, {'defense': 44},
               {'defense': 46}, {'defense': 48}, {'defense': 50}, {'defense': 52}, {'defense': 54}, {'defense': 56},
               {'defense': 58}, {'defense': 60}, {'defense': 62}, {'defense': 64}, {'defense': 66}, {'defense': 68},
               {'defense': 70}, {'defense': 72}, {'defense': 74}, {'defense': 76}, {'defense': 78}, {'defense': 80},
               {'defense': 82}, {'defense': 84}, {'defense': 86}],
    'combat': [{'crit chance': 0}, {'crit chance': 0.5}, {'crit chance': 1.0}, {'crit chance': 1.5},
               {'crit chance': 2.0}, {'crit chance': 2.5}, {'crit chance': 3.0}, {'crit chance': 3.5},
               {'crit chance': 4.0}, {'crit chance': 4.5}, {'crit chance': 5.0}, {'crit chance': 5.5},
               {'crit chance': 6.0}, {'crit chance': 6.5}, {'crit chance': 7.0}, {'crit chance': 7.5},
               {'crit chance': 8.0}, {'crit chance': 8.5}, {'crit chance': 9.0}, {'crit chance': 9.5},
               {'crit chance': 10.0}, {'crit chance': 10.5}, {'crit chance': 11.0}, {'crit chance': 11.5},
               {'crit chance': 12.0}, {'crit chance': 12.5}, {'crit chance': 13.0}, {'crit chance': 13.5},
               {'crit chance': 14.0}, {'crit chance': 14.5}, {'crit chance': 15.0}, {'crit chance': 15.5},
               {'crit chance': 16.0}, {'crit chance': 16.5}, {'crit chance': 17.0}, {'crit chance': 17.5},
               {'crit chance': 18.0}, {'crit chance': 18.5}, {'crit chance': 19.0}, {'crit chance': 19.5},
               {'crit chance': 20.0}, {'crit chance': 20.5}, {'crit chance': 21.0}, {'crit chance': 21.5},
               {'crit chance': 22.0}, {'crit chance': 22.5}, {'crit chance': 23.0}, {'crit chance': 23.5},
               {'crit chance': 24.0}, {'crit chance': 24.5}, {'crit chance': 25.0}],
    'foraging': [{'strength': 0}, {'strength': 1}, {'strength': 2}, {'strength': 3}, {'strength': 4}, {'strength': 5},
                 {'strength': 6}, {'strength': 7}, {'strength': 8}, {'strength': 9}, {'strength': 10}, {'strength': 11},
                 {'strength': 12}, {'strength': 13}, {'strength': 14}, {'strength': 16}, {'strength': 18},
                 {'strength': 20}, {'strength': 22}, {'strength': 24}, {'strength': 26}, {'strength': 28},
                 {'strength': 30}, {'strength': 32}, {'strength': 34}, {'strength': 36}, {'strength': 38},
                 {'strength': 40}, {'strength': 42}, {'strength': 44}, {'strength': 46}, {'strength': 48},
                 {'strength': 50}, {'strength': 52}, {'strength': 54}, {'strength': 56}, {'strength': 58},
                 {'strength': 60}, {'strength': 62}, {'strength': 64}, {'strength': 66}, {'strength': 68},
                 {'strength': 70}, {'strength': 72}, {'strength': 74}, {'strength': 76}, {'strength': 78},
                 {'strength': 80}, {'strength': 82}, {'strength': 84}, {'strength': 86}],
    'fishing': [{'health': 0}, {'health': 2}, {'health': 4}, {'health': 6}, {'health': 8}, {'health': 10},
                {'health': 12}, {'health': 14}, {'health': 16}, {'health': 18}, {'health': 20}, {'health': 22},
                {'health': 24}, {'health': 26}, {'health': 28}, {'health': 31}, {'health': 34}, {'health': 37},
                {'health': 40}, {'health': 43}, {'health': 47}, {'health': 51}, {'health': 55}, {'health': 59},
                {'health': 63}, {'health': 67}, {'health': 72}, {'health': 77}, {'health': 82}, {'health': 87},
                {'health': 92}, {'health': 97}, {'health': 102}, {'health': 107}, {'health': 112}, {'health': 117},
                {'health': 122}, {'health': 127}, {'health': 132}, {'health': 137}, {'health': 142}, {'health': 147},
                {'health': 152}, {'health': 157}, {'health': 162}, {'health': 167}, {'health': 172}, {'health': 177},
                {'health': 182}, {'health': 187}, {'health': 192}],
    'enchanting': [{'intelligence': 0}, {'intelligence': 1}, {'intelligence': 2}, {'intelligence': 3},
                   {'intelligence': 4}, {'intelligence': 5}, {'intelligence': 6}, {'intelligence': 7},
                   {'intelligence': 8}, {'intelligence': 9}, {'intelligence': 10}, {'intelligence': 11},
                   {'intelligence': 12}, {'intelligence': 13}, {'intelligence': 14}, {'intelligence': 16},
                   {'intelligence': 18}, {'intelligence': 20}, {'intelligence': 22}, {'intelligence': 24},
                   {'intelligence': 26}, {'intelligence': 28}, {'intelligence': 30}, {'intelligence': 32},
                   {'intelligence': 34}, {'intelligence': 36}, {'intelligence': 38}, {'intelligence': 40},
                   {'intelligence': 42}, {'intelligence': 44}, {'intelligence': 46}, {'intelligence': 48},
                   {'intelligence': 50}, {'intelligence': 52}, {'intelligence': 54}, {'intelligence': 56},
                   {'intelligence': 58}, {'intelligence': 60}, {'intelligence': 62}, {'intelligence': 64},
                   {'intelligence': 66}, {'intelligence': 68}, {'intelligence': 70}, {'intelligence': 72},
                   {'intelligence': 74}, {'intelligence': 76}, {'intelligence': 78}, {'intelligence': 80},
                   {'intelligence': 82}, {'intelligence': 84}, {'intelligence': 86}],
    'alchemy': [{'intelligence': 0}, {'intelligence': 1}, {'intelligence': 2}, {'intelligence': 3}, {'intelligence': 4},
                {'intelligence': 5}, {'intelligence': 6}, {'intelligence': 7}, {'intelligence': 8}, {'intelligence': 9},
                {'intelligence': 10}, {'intelligence': 11}, {'intelligence': 12}, {'intelligence': 13},
                {'intelligence': 14}, {'intelligence': 16}, {'intelligence': 18}, {'intelligence': 20},
                {'intelligence': 22}, {'intelligence': 24}, {'intelligence': 26}, {'intelligence': 28},
                {'intelligence': 30}, {'intelligence': 32}, {'intelligence': 34}, {'intelligence': 36},
                {'intelligence': 38}, {'intelligence': 40}, {'intelligence': 42}, {'intelligence': 44},
                {'intelligence': 46}, {'intelligence': 48}, {'intelligence': 50}, {'intelligence': 52},
                {'intelligence': 54}, {'intelligence': 56}, {'intelligence': 58}, {'intelligence': 60},
                {'intelligence': 62}, {'intelligence': 64}, {'intelligence': 66}, {'intelligence': 68},
                {'intelligence': 70}, {'intelligence': 72}, {'intelligence': 74}, {'intelligence': 76},
                {'intelligence': 78}, {'intelligence': 80}, {'intelligence': 82}, {'intelligence': 84},
                {'intelligence': 86}],
    'taming': [{'pet luck': 0}, {'pet luck': 1}, {'pet luck': 2}, {'pet luck': 3}, {'pet luck': 4}, {'pet luck': 5},
               {'pet luck': 6}, {'pet luck': 7}, {'pet luck': 8}, {'pet luck': 9}, {'pet luck': 10}, {'pet luck': 11},
               {'pet luck': 12}, {'pet luck': 13}, {'pet luck': 14}, {'pet luck': 15}, {'pet luck': 16},
               {'pet luck': 17}, {'pet luck': 18}, {'pet luck': 19}, {'pet luck': 20}, {'pet luck': 21},
               {'pet luck': 22}, {'pet luck': 23}, {'pet luck': 24}, {'pet luck': 25}, {'pet luck': 26},
               {'pet luck': 27}, {'pet luck': 28}, {'pet luck': 29}, {'pet luck': 30}, {'pet luck': 31},
               {'pet luck': 32}, {'pet luck': 33}, {'pet luck': 34}, {'pet luck': 35}, {'pet luck': 36},
               {'pet luck': 37}, {'pet luck': 38}, {'pet luck': 39}, {'pet luck': 40}, {'pet luck': 41},
               {'pet luck': 42}, {'pet luck': 43}, {'pet luck': 44}, {'pet luck': 45}, {'pet luck': 46},
               {'pet luck': 47}, {'pet luck': 48}, {'pet luck': 49}, {'pet luck': 50}],
    'carpentry': [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
                  {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
                  {}],
    'runecrafting': [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
                     {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
                     {}]
}

TALISMANS = {re.compile(k): v for k, v in {
    'POTATO_TALISMAN': 'Potato Talisman',
    'FARMING_TALISMAN': 'Farming Talisman',
    'VACCINE_TALISMAN': 'Vaccine Talisman',
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
    'PIGS_FOOT': 'Pig\'s Foot',
    'FROZEN_CHICKEN': 'Frozen Chicken',
    'FISH_AFFINITY_TALISMAN': 'Fish Affinity Talisman',
    'FARMER_ORB': 'Farmer Orb',
    '(BROKEN_|CRACKED_)?PIGGY_BANK': 'Piggy Bank',
    'FEATHER_ARTIFACT': 'Feather Artifact',
    'HASTE_RING': 'Haste Ring',
    'NIGHT_CRYSTAL': 'Night Crystal',
    'DAY_CRYSTAL': 'Day Crystal',
    'NEW_YEAR_CAKE_BAG': 'New Year Cake Bag',
    'HEALING_RING': 'Healing Ring',
    'ARTIFACT_POTION_AFFINITY': 'Potion Affinity Artifact',
    'SEA_CREATURE_ARTIFACT': 'Sea Creature Artifact',
    'CANDY_ARTIFACT': 'Candy Artifact',
    'MELODY_HAIR': '♪ Melody\'s Hair ♪',
    'EXPERIENCE_ARTIFACT': 'Experience Artifact',
    'PARTY_HAT_CRAB': 'Crab Hat of Celebration',
    'INTIMIDATION_ARTIFACT': 'Intimidation Artifact',
    'WOLF_RING': 'Wolf Ring',
    'CHEETAH_TALISMAN': 'Cheetah Talisman',
    'DEVOUR_RING': 'Devour Ring',
    'BAT_ARTIFACT': 'Bat Artifact',
    'CAMPFIRE_TALISMAN_(21|22|23|24|25|26|27|28|29)': 'Campfire God Badge',
    'SURVIVOR_CUBE': 'Survivor Cube',
    'ZOMBIE_ARTIFACT': 'Zombie Artifact',
    'SPIDER_ARTIFACT': 'Spider Artifact',
    'SPEED_ARTIFACT': 'Speed Artifact',
    'PERSONAL_COMPACTOR_6000': 'Personal Compactor 6000',
    'TARANTULA_TALISMAN': 'Tarantula Talisman',
    'WEDDING_RING_9': 'Legendary Ring of Love',
    'RED_CLAW_ARTIFACT': 'Red Claw Artifact',
    'BAIT_RING': 'Bait Ring',
    'ENDER_ARTIFACT': 'Ender Artifact',
    'WITHER_ARTIFACT': 'Wither Artifact',
    'SCARF_GRIMOIRE': 'Scarf\'s Grimoire',
    'HUNTER_RING': 'Hunter Ring',
    'SEAL_OF_THE_FAMILY': 'Seal of the Family',
    'TREASURE_ARTIFACT': 'Treasure Artifact'
}.items()}

SKILL_NAMES = ['farming', 'mining', 'combat', 'foraging', 'fishing', 'enchanting', 'alchemy', 'taming', 'carpentry',
               'runecrafting']

COSMETIC_SKILL_NAMES = ['carpentry', 'runecrafting']

BASE_PLAYER_STATS = {
    'damage': 0,
    'strength': 0,
    'crit chance': 30,
    'crit damage': 50,
    'attack speed': 0,
    'health': 100,
    'defense': 0,
    'speed': 100,
    'intelligence': 0,
    'speed cap': 400
}

PROFILE_NAMES = [
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

FAIRY_SOUL_HP_BONUS = [0, 3, 6, 10, 14, 19, 24, 30, 36, 43, 50, 58, 66, 75, 84, 94, 104, 115, 126, 138, 150, 163, 176,
                       190, 204, 219, 234, 250, 266, 283, 300, 318, 336, 355, 374, 394, 414, 435, 456, 478, 500, 523]

SKILL_LEVEL_REQUIREMENT = [50, 175, 375, 675, 1175, 1925, 2925, 4425, 6425, 9925, 14925, 22425, 32425, 47425, 67425,
                           97425, 147425, 222425, 322425, 522425, 822425, 1222425, 1722425, 2322425, 3022425, 3822425,
                           4722425, 5722425, 6822425, 8022425, 9322425, 10722425, 12222425, 13822425, 15522425,
                           17322425, 19222425, 21222425, 23322425, 25522425, 27822425, 30222425, 32722425, 35322425,
                           38022425, 40822425, 43922425, 47322425, 51022425, 55022425]

DUNGEON_SKILL_LEVEL_REQUIREMENT = [50, 125, 235, 295, 635, 955, 1425, 2095, 3045, 4385, 6275, 8940, 12700, 17960, 25340, 
                                   25640, 50040, 70040, 97640, 135640, 188140, 259640, 356640, 488640, 668640, 911640, 1239640, 
                                   1684640, 2284640, 3084640, 4149640, 5559640, 7459640, 9959640, 13259640, 17559640, 23159640
                                   30359640, 39559640, 51559640, 66559640, 85559640, 109559640, 139559640, 177559640, 225559640,
                                   285559640, 360559640, 453559640, 569809640]

RUNECRAFTING_LEVEL_REQUIREMENT = [50, 150, 275, 435, 635, 885, 1200, 1600, 2100, 2725, 3510, 4510, 5760, 7360, 9360,
                                  11825, 14950, 18950, 23950, 30150, 37950, 47750, 59950, 
                                  75250]

MINION_SLOT_REQUIREMENT = [0, 0, 0, 0, 0, 5, 15, 30, 50, 75, 100, 125, 150, 175, 200, 225, 250, 275, 300, 350, 400,
                           450, 500, 550]

GUILD_LEVEL_REQUIREMENT = [100000, 150000, 250000, 500000, 750000, 1000000, 1250000, 1500000, 2000000, 2500000,
                           3000000]  # every level after 2.5 mil needs 3mil

# generated by [x//5 for x in range(4*5, 4*5+50)]
CATACOMB_LEVEL_REWARDS = {
    'dungeon bonus': [0, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 9, 9, 9, 9, 9, 10,
                      10, 10, 10, 10, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13]
}

ACCUMULATED_CATACOMB_LEVEL_REWARDS = {
    'dungeon bonus': [0, 4, 8, 12, 16, 20, 25, 30, 35, 40, 45, 51, 57, 63, 69, 75, 82, 89, 96, 103, 110, 118, 126, 134,
                      142, 150, 159, 168, 177, 186, 195, 205, 215, 225, 235, 245, 256, 267, 278, 289, 300, 312, 324,
                      336, 348, 360, 373, 386, 399, 412, 425]
}

TIERED_TALISMANS = {
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
    'SPEED_TALISMAN': ['SPEED_RING', 'SPEED_ARTIFACT'],
    'PERSONAL_COMPACTOR_4000': ['PERSONAL_COMPACTOR_5000', 'PERSONAL_COMPACTOR_6000'],
    'PERSONAL_COMPACTOR_5000': ['PERSONAL_COMPACTOR_6000'],
    'CAT_TALISMAN': ['LYNX_TALISMAN', 'CHEETAH_TALISMAN'],
    'LYNX_TALISMAN': ['CHEETAH_TALISMAN'],
    'SCARF_STUDIES': ['SCARF_THESIS', 'SCARF_GRIMOIRE'],
    'SCARF_THESIS': ['SCARF_GRIMOIRE'],
    'TREASURE_RING': ['TREASURE_ARTIFACT'],
    'TREASURE_TALISMAN': ['TREASURE_RING', 'TREASURE_ARTIFACT']
}

ENCHANTMENT_BONUS = {
    # sword always
    'sharpness': 5,
    'giant_killer': lambda level: 25 if level > 0 else 0,
    # sword sometimes
    'smite': 8,
    'bane_of_arthropods': 8,
    'first_strike': 25,
    'ender_slayer': 12,
    'cubism': 10,
    'execute': 10,
    'impaling': 12.5,
    # bow always
    'power': 8,
    # bow sometimes
    'dragon_hunter': 8,
    'snipe': 5,  # Would be lower except I only use this for drags and magma bosses
    # rod always
    'spiked_hook': 5
}

MOBS_RELEVANT_ENCHANTS = {
    'slayer bosses': [
        'giant_killer',
        'sharpness',
        'power',
        'spiked_hook',
        'smite',
        'bane_of_arthropods',
        'execute'
    ],
    'zealots': [
        'giant_killer',
        'sharpness',
        'power',
        'spiked_hook',
        'ender_slayer',
        'first_strike'
    ],
    'base': [
        'giant_killer',
        'sharpness',
        'first_strike',
        'power',
        'spiked_hook'
    ]
}

ENCHANTED_BOOK_6 = {
    'sharpness': 6,
    'giant_killer': 6,
    'smite': 6,
    'bane_of_arthropods': 6,
    'first_strike': 4,
    'ender_slayer': 6,
    'cubism': 5,
    'execute': 5,
    'impaling': 3,
    'power': 6,
    'dragon_hunter': 5,
    'snipe': 3,
    'spiked_hook': 6
}

ENCHANTED_BOOK_5 = {
    'sharpness': 5,
    'giant_killer': 5,
    'smite': 5,
    'bane_of_arthropods': 5,
    'first_strike': 4,
    'ender_slayer': 5,
    'cubism': 5,
    'execute': 5,
    'impaling': 3,
    'power': 5,
    'dragon_hunter': 0,
    'snipe': 3,
    'spiked_hook': 5
}

RARITIES = ['common', 'uncommon', 'rare', 'epic', 'legendary', 'mythic']

STAT_NAMES = ['damage', 'health', 'defense', 'strength', 'speed', 'crit chance', 'crit damage', 'bonus attack speed',
              'intelligence', 'sea creature chance', 'magic find', 'pet luck', 'gear score', 'true defense']

DAMAGE_REFORGES = {
    'sword': {
        'legendary': {
            'common': {'strength': 3, 'crit chance': 5, 'crit damage': 5, 'intelligence': 5, 'attack speed': 2},
            'uncommon': {'strength': 7, 'crit chance': 7, 'crit damage': 10, 'intelligence': 8, 'attack speed': 3},
            'rare': {'strength': 12, 'crit chance': 9, 'crit damage': 15, 'intelligence': 12, 'attack speed': 5},
            'epic': {'strength': 18, 'crit chance': 12, 'crit damage': 22, 'intelligence': 18, 'attack speed': 7},
            'legendary': {'strength': 25, 'crit chance': 15, 'crit damage': 28, 'intelligence': 25, 'attack speed': 10},
            'mythic': {'strength': 32, 'crit chance': 18, 'crit damage': 36, 'intelligence': 35, 'attack speed': 15},
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
            'common': {'strength': 15, 'crit damage': 10, 'attack speed': 1},
            'uncommon': {'strength': 20, 'crit damage': 15, 'attack speed': 2},
            'rare': {'strength': 25, 'crit damage': 20, 'attack speed': 4},
            'epic': {'strength': 32, 'crit damage': 27, 'attack speed': 7},
            'legendary': {'strength': 40, 'crit damage': 35, 'attack speed': 10},
            'mythic': {'strength': 50, 'crit damage': 45, 'attack speed': 15},
            'blacksmith': True
        },
        'odd': {
            'common': {'crit chance': 12, 'crit damage': 10, 'intelligence': -5},
            'uncommon': {'crit chance': 15, 'crit damage': 15, 'intelligence': -10},
            'rare': {'crit chance': 15, 'crit damage': 15, 'intelligence': -18},
            'epic': {'crit chance': 20, 'crit damage': 22, 'intelligence': -32},
            'legendary': {'crit chance': 25, 'crit damage': 30, 'intelligence': -36},
            'mythic': {'crit chance': 30, 'crit damage': 40, 'intelligence': -50},
            'blacksmith': True
        },
        'gentle': {
            'common': {'strength': 3, 'attack speed': 8},
            'uncommon': {'strength': 5, 'attack speed': 10},
            'rare': {'strength': 7, 'attack speed': 15},
            'epic': {'strength': 10, 'attack speed': 20},
            'legendary': {'strength': 15, 'attack speed': 25},
            'mythic': {'strength': 20, 'attack speed': 30},
            'blacksmith': True
        },
        'fast': {
            'common': {'attack speed': 10},
            'uncommon': {'attack speed': 20},
            'rare': {'attack speed': 30},
            'epic': {'attack speed': 40},
            'legendary': {'attack speed': 50},
            'mythic': {'attack speed': 60},
            'blacksmith': True
        },
        'fair': {
            'common': {'strength': 2, 'crit chance': 2, 'crit damage': 2, 'intelligence': 2, 'attack speed': 2},
            'uncommon': {'strength': 3, 'crit chance': 3, 'crit damage': 3, 'intelligence': 3, 'attack speed': 3},
            'rare': {'strength': 4, 'crit chance': 4, 'crit damage': 4, 'intelligence': 4, 'attack speed': 4},
            'epic': {'strength': 7, 'crit chance': 7, 'crit damage': 7, 'intelligence': 7, 'attack speed': 7},
            'legendary': {'strength': 10, 'crit chance': 10, 'crit damage': 10, 'intelligence': 10, 'attack speed': 10},
            'mythic': {'strength': 12, 'crit chance': 12, 'crit damage': 12, 'intelligence': 12, 'attack speed': 12},
            'blacksmith': True
        },
        'sharp': {
            'common': {'crit chance': 10, 'crit damage': 20},
            'uncommon': {'crit chance': 12, 'crit damage': 30},
            'rare': {'crit chance': 14, 'crit damage': 40},
            'epic': {'crit chance': 17, 'crit damage': 55},
            'legendary': {'crit chance': 20, 'crit damage': 75},
            'mythic': {'crit chance': 25, 'crit damage': 90},
            'blacksmith': True
        },
        'heroic': {
            'common': {'strength': 15, 'intelligence': 40, 'attack speed': 1},
            'uncommon': {'strength': 20, 'intelligence': 50, 'attack speed': 2},
            'rare': {'strength': 25, 'intelligence': 65, 'attack speed': 2},
            'epic': {'strength': 32, 'intelligence': 80, 'attack speed': 3},
            'legendary': {'strength': 40, 'intelligence': 100, 'attack speed': 5},
            'mythic': {'strength': 50, 'intelligence': 125, 'attack speed': 7},
            'blacksmith': True
        },
        'fabled': {
            # Your Critical hits have a chance to deal up to 20% extra damage (from 100% to 120%, randomly)
            'common': {'strength': 30, 'crit damage': 15},
            'uncommon': {'strength': 35, 'crit damage': 20},
            'rare': {'strength': 40, 'crit damage': 25},
            'epic': {'strength': 50, 'crit damage': 32},
            'legendary': {'strength': 60, 'crit damage': 40},
            'mythic': {'strength': 75, 'crit damage': 60},
            'blacksmith': False
        },
        'gilded': {
            'legendary': {'damage': 75, 'strength': 75},
            'mythic': {'damage': 90, 'strength': 90},
            'blacksmith': False
        },
        'warped': {
            'rare': {'damage': 165, 'strength': 165 },
            'epic': {'damage': 165, 'strength': 165 },
            'blacksmith': False
        },
        'suspicious': {
            'common': {'damage': 15, 'crit damage': 30, 'crit chance': 1},
            'uncommon': {'damage': 15, 'crit damage': 40, 'crit chance': 2},
            'rare': {'damage': 15, 'crit damage': 50, 'crit chance': 3},
            'epic': {'damage': 15, 'crit damage': 65, 'crit chance': 5},
            'legendary': {'damage': 15, 'crit damage': 85, 'crit chance': 7},
            'mythic': {'damage': 15, 'crit damage': 110, 'crit chance': 10},
            'blacksmith': False
        },
    },
    'bow': {
        'awkward': {
            'common': {'crit chance': 10, 'crit damage': 5, 'intelligence': -5},
            'uncommon': {'crit chance': 12, 'crit damage': 10, 'intelligence': -10},
            'rare': {'crit chance': 15, 'crit damage': 15, 'intelligence': -18},
            'epic': {'crit chance': 20, 'crit damage': 22, 'intelligence': -32},
            'legendary': {'crit chance': 25, 'crit damage': 30, 'intelligence': -50},
            'mythic': {'crit chance': 30, 'crit damage': 40, 'intelligence': -60},
            'blacksmith': True
        },
        'rich': {
            'common': {'strength': 2, 'crit chance': 10, 'crit damage': 1, 'intelligence': 20},
            'uncommon': {'strength': 3, 'crit chance': 12, 'crit damage': 2, 'intelligence': 25},
            'rare': {'strength': 4, 'crit chance': 14, 'crit damage': 4, 'intelligence': 30},
            'epic': {'strength': 7, 'crit chance': 17, 'crit damage': 7, 'intelligence': 40},
            'legendary': {'strength': 10, 'crit chance': 20, 'crit damage': 10, 'intelligence': 50},
            'mythic': {'strength': 12, 'crit chance': 25, 'crit damage': 15, 'intelligence': 75},
            'blacksmith': True
        },
        'fine': {
            'common': {'strength': 3, 'crit chance': 5, 'crit damage': 2},
            'uncommon': {'strength': 7, 'crit chance': 7, 'crit damage': 4},
            'rare': {'strength': 12, 'crit chance': 9, 'crit damage': 7},
            'epic': {'strength': 18, 'crit chance': 12, 'crit damage': 10},
            'legendary': {'strength': 25, 'crit chance': 15, 'crit damage': 15},
            'mythic': {'strength': 40, 'crit chance': 20, 'crit damage': 20},
            'blacksmith': True
        },
        'neat': {
            'common': {'crit chance': 10, 'crit damage': 4, 'intelligence': 3},
            'uncommon': {'crit chance': 12, 'crit damage': 8, 'intelligence': 6},
            'rare': {'crit chance': 14, 'crit damage': 14, 'intelligence': 10},
            'epic': {'crit chance': 17, 'crit damage': 20, 'intelligence': 15},
            'legendary': {'crit chance': 20, 'crit damage': 30, 'intelligence': 20},
            'mythic': {'crit chance': 25, 'crit damage': 40, 'intelligence': 30},
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
            'common': {'strength': 25},
            'uncommon': {'strength': 32},
            'rare': {'strength': 40},
            'epic': {'strength': 50},
            'legendary': {'strength': 60},
            'mythic': {'strength': 70},
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
            'common': {'crit chance': 10, 'crit damage': 5},
            'uncommon': {'crit chance': 13, 'crit damage': 10},
            'rare': {'crit chance': 16, 'crit damage': 18},
            'epic': {'crit chance': 19, 'crit damage': 32},
            'legendary': {'crit chance': 22, 'crit damage': 50},
            'mythic': {'crit chance': 25, 'crit damage': 70},
            'blacksmith': True
        },
        'unreal': {
            'common': {'strength': 3, 'crit chance': 8, 'crit damage': 5},
            'uncommon': {'strength': 7, 'crit chance': 9, 'crit damage': 10},
            'rare': {'strength': 12, 'crit chance': 10, 'crit damage': 18},
            'epic': {'strength': 18, 'crit chance': 11, 'crit damage': 32},
            'legendary': {'strength': 25, 'crit chance': 13, 'crit damage': 50},
            'mythic': {'strength': 34, 'crit chance': 15, 'crit damage': 75},
            'blacksmith': True
        },
        'spiritual': {
            'epic': {'strength': 20, 'crit chance': 10, 'crit damage': 37},
            'legendary': {'strength': 28, 'crit chance': 12, 'crit damage': 55},
            'mythic': {'strength': 38, 'crit chance': 14, 'crit damage': 75},
            'blacksmith': False
        }
    },
    'armor': {
        'warped': {
            'common': {'strength': 2, 'attack speed': 2, 'speed': 1},
            'uncommon': {'strength': 4, 'attack speed': 3, 'speed': 1},
            'rare': {'strength': 6, 'attack speed': 4, 'speed': 2},
            'epic': {'strength': 7, 'attack speed': 5, 'speed': 2},
            'legendary': {'strength': 10, 'attack speed': 6, 'speed': 3},
            'mythic': {'strength': 12, 'attack speed': 7, 'speed': 3},
            'blacksmith': False
        },
        'smart': {
            'common': {'defense': 4, 'health': 4, 'intelligence': 20},
            'uncommon': {'defense': 6, 'health': 6, 'intelligence': 40},
            'rare': {'defense': 9, 'health': 9, 'intelligence': 60},
            'epic': {'defense': 12, 'health': 12, 'intelligence': 80},
            'legendary': {'defense': 15, 'health': 15, 'intelligence': 100},
            'mythic': {'defense': 20, 'health': 20, 'intelligence': 120},
            'blacksmith': True
        },
        'clean': {
            'common': {'defense': 5, 'health': 5, 'crit chance': 2},
            'uncommon': {'defense': 7, 'health': 7, 'crit chance': 4},
            'rare': {'defense': 10, 'health': 10, 'crit chance': 6},
            'epic': {'defense': 15, 'health': 15, 'crit chance': 8},
            'legendary': {'defense': 20, 'health': 20, 'crit chance': 10},
            'mythic': {'defense': 25, 'health': 25, 'crit chance': 12},
            'blacksmith': True
        },
        'fierce': {
            'common': {'strength': 2, 'crit chance': 2, 'crit damage': 4},
            'uncommon': {'strength': 4, 'crit chance': 3, 'crit damage': 7},
            'rare': {'strength': 6, 'crit chance': 4, 'crit damage': 10},
            'epic': {'strength': 8, 'crit chance': 5, 'crit damage': 14},
            'legendary': {'strength': 10, 'crit chance': 6, 'crit damage': 18},
            'mythic': {'strength': 12, 'crit chance': 8, 'crit damage': 24},
            'blacksmith': True
        },
        'heavy': {
            'common': {'defense': 25, 'speed': -1, 'crit damage': -1},
            'uncommon': {'defense': 35, 'speed': -1, 'crit damage': -2},
            'rare': {'defense': 50, 'speed': -1, 'crit damage': -2},
            'epic': {'defense': 65, 'speed': -1, 'crit damage': -3},
            'legendary': {'defense': 80, 'speed': -1, 'crit damage': -5},
            'mythic': {'defense': 110, 'speed': -1, 'crit damage': -7},
            'blacksmith': True
        },
        'light': {
            'common': {'defense': 1, 'speed': 1, 'health': 5, 'crit chance': 1, 'attack speed': 1, 'crit damage': 1},
            'uncommon': {'defense': 2, 'speed': 2, 'health': 7, 'crit chance': 1, 'attack speed': 2, 'crit damage': 2},
            'rare': {'defense': 3, 'speed': 3, 'health': 10, 'crit chance': 2, 'attack speed': 3, 'crit damage': 3},
            'epic': {'defense': 4, 'speed': 4, 'health': 15, 'crit chance': 2, 'attack speed': 4, 'crit damage': 4},
            'legendary': {'defense': 5, 'speed': 5, 'health': 20, 'crit chance': 2, 'attack speed': 5,
                          'crit damage': 5},
            'mythic': {'defense': 6, 'speed': 6, 'health': 25, 'crit chance': 3, 'attack speed': 6, 'crit damage': 6},
            'blacksmith': True
        },
        'mythic': {
            'common': {'strength': 2, 'defense': 2, 'speed': 2, 'health': 2, 'crit chance': 1, 'intelligence': 20},
            'uncommon': {'strength': 4, 'defense': 4, 'speed': 2, 'health': 4, 'crit chance': 2, 'intelligence': 25},
            'rare': {'strength': 6, 'defense': 6, 'speed': 2, 'health': 6, 'crit chance': 3, 'intelligence': 30},
            'epic': {'strength': 8, 'defense': 8, 'speed': 2, 'health': 8, 'crit chance': 4, 'intelligence': 40},
            'legendary': {'strength': 10, 'defense': 10, 'speed': 2, 'health': 10, 'crit chance': 5,
                          'intelligence': 50},
            'mythic': {'strength': 12, 'defense': 12, 'speed': 2, 'health': 12, 'crit chance': 6, 'intelligence': 60},
            'blacksmith': True
        },
        'titanic': {
            'common': {'defense': 10, 'health': 10},
            'uncommon': {'defense': 15, 'health': 15},
            'rare': {'defense': 20, 'health': 20},
            'epic': {'defense': 25, 'health': 25},
            'legendary': {'defense': 35, 'health': 35},
            'mythic': {'defense': 50, 'health': 50},
            'blacksmith': True
        },
        'wise': {
            'common': {'speed': 1, 'health': 6, 'intelligence': 25},
            'uncommon': {'speed': 1, 'health': 8, 'intelligence': 50},
            'rare': {'speed': 1, 'health': 10, 'intelligence': 75},
            'epic': {'speed': 2, 'health': 12, 'intelligence': 100},
            'legendary': {'speed': 2, 'health': 15, 'intelligence': 125},
            'mythic': {'speed': 3, 'health': 20, 'intelligence': 150},
            'blacksmith': True
        },
        'pure': {
            'common': {'strength': 2, 'defense': 2, 'speed': 1, 'health': 2, 'crit chance': 2, 'crit damage': 2,
                       'intelligence': 2, 'attack speed': 1},
            'uncommon': {'strength': 3, 'defense': 3, 'speed': 1, 'health': 3, 'crit chance': 4, 'crit damage': 3,
                         'intelligence': 3, 'attack speed': 1},
            'rare': {'strength': 4, 'defense': 4, 'speed': 1, 'health': 4, 'crit chance': 6, 'crit damage': 4,
                     'intelligence': 4, 'attack speed': 2},
            'epic': {'strength': 6, 'defense': 6, 'speed': 1, 'health': 6, 'crit chance': 8, 'crit damage': 6,
                     'intelligence': 6, 'attack speed': 3},
            'legendary': {'strength': 8, 'defense': 8, 'speed': 1, 'health': 8, 'crit chance': 10, 'crit damage': 8,
                          'intelligence': 8, 'attack speed': 4},
            'mythic': {'strength': 10, 'defense': 10, 'speed': 1, 'health': 10, 'crit chance': 12, 'crit damage': 10,
                       'intelligence': 10, 'attack speed': 5},
            'blacksmith': True
        },
        'spiked': {
            'epic': {'strength': 8, 'defense': 6, 'speed': 1, 'health': 6, 'crit chance': 8, 'crit damage': 8,
                     'intelligence': 8, 'attack speed': 3},
            'legendary': {'strength': 10, 'defense': 8, 'speed': 1, 'health': 8, 'crit chance': 10, 'crit damage': 10,
                          'intelligence': 10, 'attack speed': 4},
            'mythic': {'strength': 12, 'defense': 10, 'speed': 1, 'health': 10, 'crit chance': 12, 'crit damage': 12,
                       'intelligence': 12, 'attack speed': 5},
            'blacksmith': False
        },
        'renowned': {
            # Increases all your stats by 1% (similar to Superior passive)
            'epic': {'strength': 8, 'defense': 6, 'speed': 1, 'health': 6, 'crit chance': 8, 'crit damage': 8,
                     'intelligence': 8, 'attack speed': 3},
            'legendary': {'strength': 10, 'defense': 8, 'speed': 1, 'health': 8, 'crit chance': 10, 'crit damage': 10,
                          'intelligence': 10, 'attack speed': 4},
            'mythic': {'strength': 12, 'defense': 10, 'speed': 1, 'health': 10, 'crit chance': 12, 'crit damage': 12,
                       'intelligence': 12, 'attack speed': 5},
            'blacksmith': False
        },
        'cubic': {
            # Decrease damage taken from nether mobs by 2% (needs more info if stacking)
            'common': {'strength': 3, 'health': 5},
            'uncommon': {'strength': 5, 'health': 7},
            'rare': {'strength': 7, 'health': 10},
            'epic': {'strength': 10, 'health': 15},
            'legendary': {'strength': 12, 'health': 20},
            'mythic': {'strength': 15, 'health': 30},
            'blacksmith': False
        },
        'reinforced': {
            'common': {'defense': 25},
            'uncommon': {'defense': 35},
            'rare': {'defense': 50},
            'epic': {'defense': 65},
            'legendary': {'defense': 80},
            'mythic': {'defense': 100},
            'blacksmith': False
        }
    },
    'talisman': {
        'bizarre': {
            'common': {'strength': 1, 'crit damage': -1, 'health': 1, 'intelligence': 6},
            'uncommon': {'strength': 2, 'crit damage': -2, 'health': 1, 'intelligence': 8},
            'rare': {'strength': 2, 'crit damage': -2, 'health': 1, 'intelligence': 10},
            'epic': {'strength': 3, 'crit damage': -3, 'health': 1, 'intelligence': 14},
            'legendary': {'strength': 5, 'crit damage': -5, 'health': 1, 'intelligence': 20},
            'mythic': {'strength': 7, 'crit damage': -7, 'health': 2, 'intelligence': 30},
            'blacksmith': True
        },
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
            'epic': {'strength': 5, 'crit damage': 3},
            'legendary': {'strength': 7, 'crit damage': 3},
            'mythic': {'strength': 10, 'crit damage': 5},
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
            'common': {'strength': 1, 'crit damage': 1, 'defense': 0},
            'uncommon': {'strength': 2, 'crit damage': 2, 'defense': 0},
            'rare': {'strength': 3, 'crit damage': 3, 'defense': 1},
            'epic': {'strength': 5, 'crit damage': 5, 'defense': 2},
            'legendary': {'strength': 8, 'crit damage': 8, 'defense': 3},
            'mythic': {'strength': 12, 'crit damage': 12, 'defense': 4},
            'blacksmith': True
        },
        'godly': {
            'common': {'strength': 1, 'crit damage': 2, 'intelligence': 1},
            'uncommon': {'strength': 2, 'crit damage': 2, 'intelligence': 1},
            'rare': {'strength': 3, 'crit damage': 3, 'intelligence': 1},
            'epic': {'strength': 5, 'crit damage': 4, 'intelligence': 2},
            'legendary': {'strength': 7, 'crit damage': 6, 'intelligence': 4},
            'mythic': {'strength': 10, 'crit damage': 8, 'intelligence': 6},
            'blacksmith': True
        },
        'demonic': {
            'common': {'strength': 1, 'intelligence': 5},
            'uncommon': {'strength': 2, 'intelligence': 7},
            'rare': {'strength': 2, 'intelligence': 9},
            'epic': {'strength': 3, 'intelligence': 12},
            'legendary': {'strength': 5, 'intelligence': 17},
            'mythic': {'strength': 7, 'intelligence': 24},
            'blacksmith': True
        },
        'zealous': {
            'common': {'strength': 1, 'speed': 0, 'crit damage': 1, 'intelligence': 1},
            'uncommon': {'strength': 2, 'speed': 0, 'crit damage': 2, 'intelligence': 2},
            'rare': {'strength': 2, 'speed': 1, 'crit damage': 2, 'intelligence': 3},
            'epic': {'strength': 3, 'speed': 1, 'crit damage': 3, 'intelligence': 5},
            'legendary': {'strength': 5, 'speed': 1, 'crit damage': 5, 'intelligence': 7},
            'mythic': {'strength': 7, 'speed': 2, 'crit damage': 7, 'intelligence': 10},
            'blacksmith': True
        },
        'strange': {
            'common': {'crit damage': 1, 'strength': 2, 'defense': 0, 'speed': 1, 'health': 0, 'intelligence': 1,
                       'attack speed': -1},
            'uncommon': {'crit damage': 2, 'strength': 1, 'defense': 3, 'speed': 0, 'health': 2, 'intelligence': -1,
                         'attack speed': 2},
            'rare': {'crit damage': 0, 'strength': -1, 'defense': 2, 'speed': 1, 'health': 1, 'intelligence': 2,
                     'attack speed': 0},
            'epic': {'crit damage': 1, 'strength': 3, 'defense': -1, 'speed': 0, 'health': 7, 'intelligence': 0,
                     'attack speed': 4},
            'legendary': {'crit damage': 7, 'strength': 0, 'defense': 1, 'speed': 3, 'health': -1, 'intelligence': 8,
                          'attack speed': 0},
            'mythic': {'crit damage': 9, 'strength': 4, 'defense': 1, 'speed': 3, 'health': 0, 'intelligence': 11,
                       'attack speed': 5},
            'blacksmith': True
        },
        'silky': {
            'common': {'crit damage': 5},
            'uncommon': {'crit damage': 6},
            'rare': {'crit damage': 8},
            'epic': {'crit damage': 10},
            'legendary': {'crit damage': 15},
            'mythic': {'crit damage': 20},
            'blacksmith': False
        },
        'bloody': {
            'common': {'strength': 1, 'crit damage': 3, 'attack speed': 1, 'speed': 1},
            'uncommon': {'strength': 1, 'crit damage': 4, 'attack speed': 1, 'speed': 1},
            'rare': {'strength': 1, 'crit damage': 5, 'attack speed': 1, 'speed': 1},
            'epic': {'strength': 2, 'crit damage': 6, 'attack speed': 2, 'speed': 1},
            'legendary': {'strength': 3, 'crit damage': 9, 'attack speed': 2, 'speed': 1},
            'mythic': {'strength': 4, 'crit damage': 14, 'attack speed': 2, 'speed': 1},
            'blacksmith': False
        },
        'shaded': {
            'common': {'strength': 2, 'crit damage': 3, 'crit chance': 0 },
            'uncommon': {'strength': 3, 'crit damage': 4, 'crit chance': 0 },
            'rare': {'strength': 4, 'crit damage': 5, 'crit chance': 0 },
            'epic': {'strength': 5, 'crit damage': 6, 'crit chance': 0 },
            'legendary': {'strength': 6, 'crit damage': 9, 'crit chance': 1 },
            'mythic': {'strength': 8, 'crit damage': 14, 'crit chance': 1 },
            'blacksmith': False
        }
    }
}

# List of all reforges
# REFORGES = {
#     'sword': {
#         'legendary': {
#             'common': {'strength': 3, 'crit chance': 5, 'crit damage': 5, 'intelligence': 5, 'attack speed': 2},
#             'uncommon': {'strength': 7, 'crit chance': 7, 'crit damage': 10, 'intelligence': 8, 'attack speed': 3},
#             'rare': {'strength': 12, 'crit chance': 9, 'crit damage': 15, 'intelligence': 12, 'attack speed': 5},
#             'epic': {'strength': 18, 'crit chance': 12, 'crit damage': 22, 'intelligence': 18, 'attack speed': 7},
#             'legendary': {'strength': 25, 'crit chance': 15, 'crit damage': 28, 'intelligence': 25, 'attack speed': 10},
#             'mythic': {'strength': 32, 'crit chance': 18, 'crit damage': 36, 'intelligence': 35, 'attack speed': 15},
#             'blacksmith': True
#         },
#         'spicy': {
#             'common': {'strength': 2, 'crit chance': 1, 'crit damage': 25, 'attack speed': 1},
#             'uncommon': {'strength': 3, 'crit chance': 1, 'crit damage': 35, 'attack speed': 2},
#             'rare': {'strength': 4, 'crit chance': 1, 'crit damage': 45, 'attack speed': 4},
#             'epic': {'strength': 7, 'crit chance': 1, 'crit damage': 60, 'attack speed': 7},
#             'legendary': {'strength': 10, 'crit chance': 1, 'crit damage': 80, 'attack speed': 10},
#             'mythic': {'strength': 12, 'crit chance': 1, 'crit damage': 100, 'attack speed': 15},
#             'blacksmith': True
#         },
#         'epic': {
#             'common': {'strength': 15, 'crit damage': 10, 'attack speed': 1},
#             'uncommon': {'strength': 20, 'crit damage': 15, 'attack speed': 2},
#             'rare': {'strength': 25, 'crit damage': 20, 'attack speed': 4},
#             'epic': {'strength': 32, 'crit damage': 27, 'attack speed': 7},
#             'legendary': {'strength': 40, 'crit damage': 35, 'attack speed': 10},
#             'mythic': {'strength': 50, 'crit damage': 45, 'attack speed': 15},
#             'blacksmith': True
#         },
#         'odd': {
#             'common': {'crit chance': 12, 'crit damage': 10, 'intelligence': -5},
#             'uncommon': {'crit chance': 15, 'crit damage': 15, 'intelligence': -10},
#             'rare': {'crit chance': 15, 'crit damage': 15, 'intelligence': -18},
#             'epic': {'crit chance': 20, 'crit damage': 22, 'intelligence': -32},
#             'legendary': {'crit chance': 25, 'crit damage': 30, 'intelligence': -36},
#             'mythic': {'crit chance': 30, 'crit damage': 40, 'intelligence': -50},
#             'blacksmith': True
#         },
#         'gentle': {
#             'common': {'strength': 3, 'attack speed': 8},
#             'uncommon': {'strength': 5, 'attack speed': 10},
#             'rare': {'strength': 7, 'attack speed': 15},
#             'epic': {'strength': 10, 'attack speed': 20},
#             'legendary': {'strength': 15, 'attack speed': 25},
#             'mythic': {'strength': 20, 'attack speed': 30},
#             'blacksmith': True
#         },
#         'fast': {
#             'common': {'attack speed': 10},
#             'uncommon': {'attack speed': 20},
#             'rare': {'attack speed': 30},
#             'epic': {'attack speed': 40},
#             'legendary': {'attack speed': 50},
#             'mythic': {'attack speed': 60},
#             'blacksmith': True
#         },
#         'fair': {
#             'common': {'strength': 2, 'crit chance': 2, 'crit damage': 2, 'intelligence': 2, 'attack speed': 2},
#             'uncommon': {'strength': 3, 'crit chance': 3, 'crit damage': 3, 'intelligence': 3, 'attack speed': 3},
#             'rare': {'strength': 4, 'crit chance': 4, 'crit damage': 4, 'intelligence': 4, 'attack speed': 4},
#             'epic': {'strength': 7, 'crit chance': 7, 'crit damage': 7, 'intelligence': 7, 'attack speed': 7},
#             'legendary': {'strength': 10, 'crit chance': 10, 'crit damage': 10, 'intelligence': 10, 'attack speed': 10},
#             'mythic': {'strength': 12, 'crit chance': 12, 'crit damage': 12, 'intelligence': 12, 'attack speed': 12},
#             'blacksmith': True
#         },
#         'sharp': {
#             'common': {'crit chance': 10, 'crit damage': 20},
#             'uncommon': {'crit chance': 12, 'crit damage': 30},
#             'rare': {'crit chance': 14, 'crit damage': 40},
#             'epic': {'crit chance': 17, 'crit damage': 55},
#             'legendary': {'crit chance': 20, 'crit damage': 75},
#             'mythic': {'crit chance': 25, 'crit damage': 90},
#             'blacksmith': True
#         },
#         'heroic': {
#             'common': {'strength': 15, 'intelligence': 40, 'attack speed': 1},
#             'uncommon': {'strength': 20, 'intelligence': 50, 'attack speed': 2},
#             'rare': {'strength': 25, 'intelligence': 65, 'attack speed': 2},
#             'epic': {'strength': 32, 'intelligence': 80, 'attack speed': 3},
#             'legendary': {'strength': 40, 'intelligence': 100, 'attack speed': 5},
#             'mythic': {'strength': 50, 'intelligence': 125, 'attack speed': 7},
#             'blacksmith': True
#         },
#         'fabled': {
#             # Your Critical hits have a chance to deal up to 20% extra damage (from 100% to 120%, randomly)
#             'common': {'strength': 30, 'crit damage': 15},
#             'uncommon': {'strength': 35, 'crit damage': 20},
#             'rare': {'strength': 40, 'crit damage': 25},
#             'epic': {'strength': 50, 'crit damage': 32},
#             'legendary': {'strength': 60, 'crit damage': 40},
#             'mythic': {'strength': 75, 'crit damage': 60},
#             'blacksmith': False
#         },
#         'gilded': {
#             'legendary': {'damage': 75, 'strength': 75},
#             'mythic': {'damage': 90, 'strength': 90},
#             'blacksmith': False
#         }
#     },
#     'bow': {
#         'awkward': {
#             'common': {'crit chance': 10, 'crit damage': 5, 'intelligence': -5},
#             'uncommon': {'crit chance': 12, 'crit damage': 10, 'intelligence': -10},
#             'rare': {'crit chance': 15, 'crit damage': 15, 'intelligence': -18},
#             'epic': {'crit chance': 20, 'crit damage': 22, 'intelligence': -32},
#             'legendary': {'crit chance': 25, 'crit damage': 30, 'intelligence': -50},
#             'mythic': {'crit chance': 30, 'crit damage': 40, 'intelligence': -60},
#             'blacksmith': True
#         },
#         'rich': {
#             'common': {'strength': 2, 'crit chance': 10, 'crit damage': 1, 'intelligence': 20},
#             'uncommon': {'strength': 3, 'crit chance': 12, 'crit damage': 2, 'intelligence': 25},
#             'rare': {'strength': 4, 'crit chance': 14, 'crit damage': 4, 'intelligence': 30},
#             'epic': {'strength': 7, 'crit chance': 17, 'crit damage': 7, 'intelligence': 40},
#             'legendary': {'strength': 10, 'crit chance': 20, 'crit damage': 10, 'intelligence': 50},
#             'mythic': {'strength': 12, 'crit chance': 25, 'crit damage': 15, 'intelligence': 75},
#             'blacksmith': True
#         },
#         'fine': {
#             'common': {'strength': 3, 'crit chance': 5, 'crit damage': 2},
#             'uncommon': {'strength': 7, 'crit chance': 7, 'crit damage': 4},
#             'rare': {'strength': 12, 'crit chance': 9, 'crit damage': 7},
#             'epic': {'strength': 18, 'crit chance': 12, 'crit damage': 10},
#             'legendary': {'strength': 25, 'crit chance': 15, 'crit damage': 15},
#             'mythic': {'strength': 40, 'crit chance': 20, 'crit damage': 20},
#             'blacksmith': True
#         },
#         'neat': {
#             'common': {'crit chance': 10, 'crit damage': 4, 'intelligence': 3},
#             'uncommon': {'crit chance': 12, 'crit damage': 8, 'intelligence': 6},
#             'rare': {'crit chance': 14, 'crit damage': 14, 'intelligence': 10},
#             'epic': {'crit chance': 17, 'crit damage': 20, 'intelligence': 15},
#             'legendary': {'crit chance': 20, 'crit damage': 30, 'intelligence': 20},
#             'mythic': {'crit chance': 25, 'crit damage': 40, 'intelligence': 30},
#             'blacksmith': True
#         },
#         'hasty': {
#             'common': {'strength': 3, 'crit chance': 20},
#             'uncommon': {'strength': 5, 'crit chance': 25},
#             'rare': {'strength': 7, 'crit chance': 30},
#             'epic': {'strength': 10, 'crit chance': 40},
#             'legendary': {'strength': 15, 'crit chance': 50},
#             'mythic': {'strength': 20, 'crit chance': 60},
#             'blacksmith': True
#         },
#         'grand': {
#             'common': {'strength': 25},
#             'uncommon': {'strength': 32},
#             'rare': {'strength': 40},
#             'epic': {'strength': 50},
#             'legendary': {'strength': 60},
#             'mythic': {'strength': 70},
#             'blacksmith': True
#         },
#         'rapid': {
#             'common': {'strength': 2, 'crit damage': 35},
#             'uncommon': {'strength': 3, 'crit damage': 45},
#             'rare': {'strength': 4, 'crit damage': 55},
#             'epic': {'strength': 7, 'crit damage': 65},
#             'legendary': {'strength': 10, 'crit damage': 75},
#             'mythic': {'strength': 12, 'crit damage': 90},
#             'blacksmith': True
#         },
#         'deadly': {
#             'common': {'crit chance': 10, 'crit damage': 5},
#             'uncommon': {'crit chance': 13, 'crit damage': 10},
#             'rare': {'crit chance': 16, 'crit damage': 18},
#             'epic': {'crit chance': 19, 'crit damage': 32},
#             'legendary': {'crit chance': 22, 'crit damage': 50},
#             'mythic': {'crit chance': 25, 'crit damage': 70},
#             'blacksmith': True
#         },
#         'unreal': {
#             'common': {'strength': 3, 'crit chance': 8, 'crit damage': 5},
#             'uncommon': {'strength': 7, 'crit chance': 9, 'crit damage': 10},
#             'rare': {'strength': 12, 'crit chance': 10, 'crit damage': 18},
#             'epic': {'strength': 18, 'crit chance': 11, 'crit damage': 32},
#             'legendary': {'strength': 25, 'crit chance': 13, 'crit damage': 50},
#             'mythic': {'strength': 34, 'crit chance': 15, 'crit damage': 75},
#             'blacksmith': True
#         },
#         'spiritual': {
#             'epic': {'strength': 20, 'crit chance': 10, 'crit damage': 37},
#             'legendary': {'strength': 28, 'crit chance': 12, 'crit damage': 55},
#             'mythic': {'strength': 38, 'crit chance': 14, 'crit damage': 75},
#             'blacksmith': False
#         }
#     },
#     'armor': {
#         'smart': {
#             'common': {'defense': 4, 'health': 4, 'intelligence': 20},
#             'uncommon': {'defense': 6, 'health': 6, 'intelligence': 40},
#             'rare': {'defense': 9, 'health': 9, 'intelligence': 60},
#             'epic': {'defense': 12, 'health': 12, 'intelligence': 80},
#             'legendary': {'defense': 15, 'health': 15, 'intelligence': 100},
#             'mythic': {'defense': 20, 'health': 20, 'intelligence': 120},
#             'blacksmith': True
#         },
#         'clean': {
#             'common': {'defense': 5, 'health': 5, 'crit chance': 2},
#             'uncommon': {'defense': 7, 'health': 7, 'crit chance': 4},
#             'rare': {'defense': 10, 'health': 10, 'crit chance': 6},
#             'epic': {'defense': 15, 'health': 15, 'crit chance': 8},
#             'legendary': {'defense': 20, 'health': 20, 'crit chance': 10},
#             'mythic': {'defense': 25, 'health': 25, 'crit chance': 12},
#             'blacksmith': True
#         },
#         'fierce': {
#             'common': {'strength': 2, 'crit chance': 2, 'crit damage': 4},
#             'uncommon': {'strength': 4, 'crit chance': 3, 'crit damage': 7},
#             'rare': {'strength': 6, 'crit chance': 4, 'crit damage': 10},
#             'epic': {'strength': 8, 'crit chance': 5, 'crit damage': 14},
#             'legendary': {'strength': 10, 'crit chance': 6, 'crit damage': 18},
#             'mythic': {'strength': 12, 'crit chance': 8, 'crit damage': 24},
#             'blacksmith': True
#         },
#         'heavy': {
#             'common': {'defense': 25, 'speed': -1, 'crit damage': -1},
#             'uncommon': {'defense': 35, 'speed': -1, 'crit damage': -2},
#             'rare': {'defense': 50, 'speed': -1, 'crit damage': -2},
#             'epic': {'defense': 65, 'speed': -1, 'crit damage': -3},
#             'legendary': {'defense': 80, 'speed': -1, 'crit damage': -5},
#             'mythic': {'defense': 110, 'speed': -1, 'crit damage': -7},
#             'blacksmith': True
#         },
#         'light': {
#             'common': {'defense': 1, 'speed': 1, 'health': 5, 'crit chance': 1, 'attack speed': 1, 'crit damage': 1},
#             'uncommon': {'defense': 2, 'speed': 2, 'health': 7, 'crit chance': 1, 'attack speed': 2, 'crit damage': 2},
#             'rare': {'defense': 3, 'speed': 3, 'health': 10, 'crit chance': 2, 'attack speed': 3, 'crit damage': 3},
#             'epic': {'defense': 4, 'speed': 4, 'health': 15, 'crit chance': 2, 'attack speed': 4, 'crit damage': 4},
#             'legendary': {'defense': 5, 'speed': 5, 'health': 20, 'crit chance': 2, 'attack speed': 5,
#                           'crit damage': 5},
#             'mythic': {'defense': 6, 'speed': 6, 'health': 25, 'crit chance': 3, 'attack speed': 6, 'crit damage': 6},
#             'blacksmith': True
#         },
#         'mythic': {
#             'common': {'strength': 2, 'defense': 2, 'speed': 2, 'health': 2, 'crit chance': 1, 'intelligence': 20},
#             'uncommon': {'strength': 4, 'defense': 4, 'speed': 2, 'health': 4, 'crit chance': 2, 'intelligence': 25},
#             'rare': {'strength': 6, 'defense': 6, 'speed': 2, 'health': 6, 'crit chance': 3, 'intelligence': 30},
#             'epic': {'strength': 8, 'defense': 8, 'speed': 2, 'health': 8, 'crit chance': 4, 'intelligence': 40},
#             'legendary': {'strength': 10, 'defense': 10, 'speed': 2, 'health': 10, 'crit chance': 5,
#                           'intelligence': 50},
#             'mythic': {'strength': 12, 'defense': 12, 'speed': 2, 'health': 12, 'crit chance': 6, 'intelligence': 60},
#             'blacksmith': True
#         },
#         'titanic': {
#             'common': {'defense': 10, 'health': 10},
#             'uncommon': {'defense': 15, 'health': 15},
#             'rare': {'defense': 20, 'health': 20},
#             'epic': {'defense': 25, 'health': 25},
#             'legendary': {'defense': 35, 'health': 35},
#             'mythic': {'defense': 50, 'health': 50},
#             'blacksmith': True
#         },
#         'wise': {
#             'common': {'speed': 1, 'health': 6, 'intelligence': 25},
#             'uncommon': {'speed': 1, 'health': 8, 'intelligence': 50},
#             'rare': {'speed': 1, 'health': 10, 'intelligence': 75},
#             'epic': {'speed': 2, 'health': 12, 'intelligence': 100},
#             'legendary': {'speed': 2, 'health': 15, 'intelligence': 125},
#             'mythic': {'speed': 3, 'health': 20, 'intelligence': 150},
#             'blacksmith': True
#         },
#         'pure': {
#             'common': {'strength': 2, 'defense': 2, 'speed': 1, 'health': 2, 'crit chance': 2, 'crit damage': 2,
#                        'intelligence': 2, 'attack speed': 1},
#             'uncommon': {'strength': 3, 'defense': 3, 'speed': 1, 'health': 3, 'crit chance': 4, 'crit damage': 3,
#                          'intelligence': 3, 'attack speed': 1},
#             'rare': {'strength': 4, 'defense': 4, 'speed': 1, 'health': 4, 'crit chance': 6, 'crit damage': 4,
#                      'intelligence': 4, 'attack speed': 2},
#             'epic': {'strength': 6, 'defense': 6, 'speed': 1, 'health': 6, 'crit chance': 8, 'crit damage': 6,
#                      'intelligence': 6, 'attack speed': 3},
#             'legendary': {'strength': 8, 'defense': 8, 'speed': 1, 'health': 8, 'crit chance': 10, 'crit damage': 8,
#                           'intelligence': 8, 'attack speed': 4},
#             'mythic': {'strength': 10, 'defense': 10, 'speed': 1, 'health': 10, 'crit chance': 12, 'crit damage': 10,
#                        'intelligence': 10, 'attack speed': 5},
#             'blacksmith': True
#         },
#         'necrotic': {
#             'common': {'intelligence': 50},
#             'uncommon': {'intelligence': 75},
#             'rare': {'intelligence': 100},
#             'epic': {'intelligence': 120},
#             'legendary': {'intelligence': 150},
#             'mythic': {'intelligence': 175},
#             'blacksmith': False
#         },
#         'perfect': {
#             'common': {'defense': 10},
#             'uncommon': {'defense': 15},
#             'rare': {'defense': 25},
#             'epic': {'defense': 50},
#             'legendary': {'defense': 75},
#             'mythic': {'defense': 100},
#             'blacksmith': False
#         },
#         'undead': {
#             'common': {'strength': 1, 'defense': 9, 'health': 9, 'attack speed': 1},
#             'uncommon': {'strength': 2, 'defense': 12, 'health': 12, 'attack speed': 2},
#             'rare': {'strength': 2, 'defense': 15, 'health': 15, 'attack speed': 3},
#             'epic': {'strength': 3, 'defense': 18, 'health': 18, 'attack speed': 4},
#             'legendary': {'strength': 5, 'defense': 23, 'health': 23, 'attack speed': 5},
#             'mythic': {'strength': 7, 'defense': 25, 'health': 25, 'attack speed': 6},
#             'blacksmith': False
#         },
#         'spiked': {
#             'common': {'strength': 3, 'defense': 2, 'speed': 1, 'health': 2, 'crit chance': 2, 'crit damage': 3,
#                        'intelligence': 3, 'attack speed': 1},
#             'uncommon': {'strength': 4, 'defense': 3, 'speed': 1, 'health': 3, 'crit chance': 4, 'crit damage': 4,
#                          'intelligence': 4, 'attack speed': 1},
#             'rare': {'strength': 6, 'defense': 4, 'speed': 1, 'health': 4, 'crit chance': 6, 'crit damage': 6,
#                      'intelligence': 6, 'attack speed': 2},
#             'epic': {'strength': 8, 'defense': 6, 'speed': 1, 'health': 6, 'crit chance': 8, 'crit damage': 8,
#                      'intelligence': 8, 'attack speed': 3},
#             'legendary': {'strength': 10, 'defense': 8, 'speed': 1, 'health': 8, 'crit chance': 10, 'crit damage': 10,
#                           'intelligence': 10, 'attack speed': 4},
#             'mythic': {'strength': 12, 'defense': 10, 'speed': 1, 'health': 10, 'crit chance': 12, 'crit damage': 12,
#                        'intelligence': 12, 'attack speed': 5},
#             'blacksmith': False
#         },
#         'renowned': {
#             # Increases all your stats by 1% (similar to Superior passive)
#             'common': {'strength': 3, 'defense': 3, 'speed': 2, 'health': 3, 'crit chance': 3, 'crit damage': 3,
#                        'intelligence': 3, 'attack speed': 1},
#             'uncommon': {'strength': 5, 'defense': 5, 'speed': 2, 'health': 5, 'crit chance': 5, 'crit damage': 5,
#                          'intelligence': 5, 'attack speed': 2},
#             'rare': {'strength': 7, 'defense': 7, 'speed': 2, 'health': 7, 'crit chance': 7, 'crit damage': 7,
#                      'intelligence': 7, 'attack speed': 3},
#             'epic': {'strength': 9, 'defense': 9, 'speed': 2, 'health': 9, 'crit chance': 9, 'crit damage': 9,
#                      'intelligence': 9, 'attack speed': 4},
#             'legendary': {'strength': 12, 'defense': 12, 'speed': 2, 'health': 12, 'crit chance': 12, 'crit damage': 12,
#                           'intelligence': 12, 'attack speed': 5},
#             'mythic': {'strength': 15, 'defense': 15, 'speed': 2, 'health': 15, 'crit chance': 15, 'crit damage': 15,
#                        'intelligence': 15, 'attack speed': 6},
#             'blacksmith': False
#         },
#         'cubic': {
#             # Decrease damage taken from nether mobs by 2% (needs more info if stacking)
#             'common': {'strength': 3, 'health': 5},
#             'uncommon': {'strength': 5, 'health': 7},
#             'rare': {'strength': 7, 'health': 10},
#             'epic': {'strength': 10, 'health': 15},
#             'legendary': {'strength': 12, 'health': 20},
#             'mythic': {'strength': 15, 'health': 30},
#             'blacksmith': False
#         },
#         'warped': {
#             # Gain +1/2/3/4/5 Speed icon Speed for 5s
#             'common': {'strength': 2, 'speed': 1, 'attack speed': 2},
#             'uncommon': {'strength': 4, 'speed': 1, 'attack speed': 3},
#             'rare': {'strength': 6, 'speed': 2, 'attack speed': 4},
#             'epic': {'strength': 7, 'speed': 2, 'attack speed': 5},
#             'legendary': {'strength': 10, 'speed': 3, 'attack speed': 6},
#             'mythic': {'strength': 12, 'speed': 4, 'attack speed': 7},
#             'blacksmith': False
#         },
#         'reinforced': {
#             'common': {'defense': 25},
#             'uncommon': {'defense': 35},
#             'rare': {'defense': 50},
#             'epic': {'defense': 65},
#             'legendary': {'defense': 80},
#             'mythic': {'defense': 100},
#             'blacksmith': False
#         }
#     },
#     'talisman': {
#         'bizzare': {
#             'common': {'strength': 1, 'crit damage': -1, 'health': 1, 'intelligence': 6},
#             'uncommon': {'strength': 2, 'crit damage': -2, 'health': 1, 'intelligence': 8},
#             'rare': {'strength': 2, 'crit damage': -2, 'health': 1, 'intelligence': 10},
#             'epic': {'strength': 3, 'crit damage': -3, 'health': 1, 'intelligence': 14},
#             'legendary': {'strength': 5, 'crit damage': -5, 'health': 1, 'intelligence': 20},
#             'mythic': {'strength': 7, 'crit damage': -7, 'health': 2, 'intelligence': 30},
#             'blacksmith': True
#         },
#         'ominous': {
#             'common': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 0},
#             'uncommon': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 1},
#             'rare': {'strength': 1, 'defense': 1, 'health': 2, 'crit damage': 1, 'intelligence': 2},
#             'epic': {'strength': 2, 'defense': 2, 'health': 3, 'crit damage': 1, 'intelligence': 3},
#             'legendary': {'strength': 3, 'defense': 3, 'health': 4, 'crit damage': 1, 'intelligence': 4},
#             'mythic': {'strength': 4, 'defense': 4, 'health': 5, 'crit damage': 1, 'intelligence': 5},
#             'blacksmith': True
#         },  # (tbd)
#         'simple': {
#             'common': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 1, 'speed': 1},
#             'uncommon': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 1, 'speed': 1},
#             'rare': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 1, 'speed': 1},
#             'epic': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 1, 'speed': 1},
#             'legendary': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 1, 'speed': 1},
#             'mythic': {'strength': 1, 'defense': 1, 'health': 1, 'crit damage': 1, 'intelligence': 1, 'speed': 1},
#             'blacksmith': True
#         },  # (tbd)
#         'pleasant': {
#             'common': {'defense': 4},
#             'uncommon': {'defense': 5},
#             'rare': {'defense': 7},
#             'epic': {'defense': 10},
#             'legendary': {'defense': 15},
#             'mythic': {'defense': 20},
#             'blacksmith': True
#         },  # (tbd)
#         'shiny': {
#             'common': {'health': 4, 'intelligence': 1},
#             'uncommon': {'health': 5, 'intelligence': 2},
#             'rare': {'health': 7, 'intelligence': 2},
#             'epic': {'health': 10, 'intelligence': 3},
#             'legendary': {'health': 15, 'intelligence': 5},
#             'mythic': {'health': 20, 'intelligence': 7},
#             'blacksmith': True
#         },  # (tbd)
#         'vivid': {
#             'common': {'speed': 1, 'health': 1},
#             'uncommon': {'speed': 2, 'health': 2},
#             'rare': {'speed': 3, 'health': 3},
#             'epic': {'speed': 4, 'health': 4},
#             'legendary': {'speed': 5, 'health': 5},
#             'mythic': {'speed': 6, 'health': 6},
#             'blacksmith': True
#         },  # (tbd)
#         'pretty': {
#             'common': {'speed': 0, 'health': 1, 'intelligence': 3, 'attack speed': 0},
#             'uncommon': {'speed': 0, 'health': 1, 'intelligence': 4, 'attack speed': 0},
#             'rare': {'speed': 0, 'health': 2, 'intelligence': 6, 'attack speed': 1},
#             'epic': {'speed': 1, 'health': 2, 'intelligence': 9, 'attack speed': 1},
#             'legendary': {'speed': 1, 'health': 3, 'intelligence': 13, 'attack speed': 1},
#             'mythic': {'speed': 2, 'health': 4, 'intelligence': 18, 'attack speed': 1},
#             'blacksmith': True
#         },  # (tbd)
#         'itchy': {
#             'common': {'strength': 1, 'crit damage': 3, 'attack speed': 0},
#             'uncommon': {'strength': 1, 'crit damage': 4, 'attack speed': 0},
#             'rare': {'strength': 1, 'crit damage': 5, 'attack speed': 1},
#             'epic': {'strength': 2, 'crit damage': 7, 'attack speed': 1},
#             'legendary': {'strength': 3, 'crit damage': 10, 'attack speed': 1},
#             'mythic': {'strength': 4, 'crit damage': 15, 'attack speed': 1},
#             'blacksmith': True
#         },
#         'keen': {
#             'common': {'defense': 1, 'health': 1, 'intelligence': 1},
#             'uncommon': {'defense': 2, 'health': 2, 'intelligence': 2},
#             'rare': {'defense': 3, 'health': 3, 'intelligence': 2},
#             'epic': {'defense': 4, 'health': 4, 'intelligence': 3},
#             'legendary': {'defense': 5, 'health': 5, 'intelligence': 4},
#             'mythic': {'defense': 7, 'health': 7, 'intelligence': 5},
#             'blacksmith': True
#         },  # (tbd)
#         'unpleasant': {
#             'common': {'crit chance': 1},
#             'uncommon': {'crit chance': 1},
#             'rare': {'crit chance': 1},
#             'epic': {'crit chance': 2},
#             'legendary': {'crit chance': 2},
#             'mythic': {'crit chance': 3},
#             'blacksmith': True
#         },
#         'superior': {
#             'common': {'strength': 2, 'crit damage': 2},
#             'uncommon': {'strength': 3, 'crit damage': 2},
#             'rare': {'strength': 4, 'crit damage': 2},
#             'epic': {'strength': 5, 'crit damage': 3},
#             'legendary': {'strength': 7, 'crit damage': 3},
#             'mythic': {'strength': 10, 'crit damage': 5},
#             'blacksmith': True
#         },
#         'forceful': {
#             'common': {'strength': 4},
#             'uncommon': {'strength': 5},
#             'rare': {'strength': 7},
#             'epic': {'strength': 10},
#             'legendary': {'strength': 15},
#             'mythic': {'strength': 20},
#             'blacksmith': True
#         },
#         'hurtful': {
#             'common': {'crit damage': 4},
#             'uncommon': {'crit damage': 5},
#             'rare': {'crit damage': 7},
#             'epic': {'crit damage': 10},
#             'legendary': {'crit damage': 15},
#             'mythic': {'crit damage': 20},
#             'blacksmith': True
#         },
#         'strong': {
#             'common': {'strength': 1, 'crit damage': 1, 'defense': 0},
#             'uncommon': {'strength': 2, 'crit damage': 2, 'defense': 0},
#             'rare': {'strength': 3, 'crit damage': 3, 'defense': 1},
#             'epic': {'strength': 5, 'crit damage': 5, 'defense': 2},
#             'legendary': {'strength': 8, 'crit damage': 8, 'defense': 3},
#             'mythic': {'strength': 12, 'crit damage': 12, 'defense': 4},
#             'blacksmith': True
#         },
#         'godly': {
#             'common': {'strength': 1, 'crit damage': 2, 'intelligence': 1},
#             'uncommon': {'strength': 2, 'crit damage': 2, 'intelligence': 1},
#             'rare': {'strength': 3, 'crit damage': 3, 'intelligence': 1},
#             'epic': {'strength': 5, 'crit damage': 4, 'intelligence': 2},
#             'legendary': {'strength': 7, 'crit damage': 6, 'intelligence': 4},
#             'mythic': {'strength': 10, 'crit damage': 8, 'intelligence': 6},
#             'blacksmith': True
#         },
#         'demonic': {
#             'common': {'strength': 1, 'intelligence': 5},
#             'uncommon': {'strength': 2, 'intelligence': 7},
#             'rare': {'strength': 2, 'intelligence': 9},
#             'epic': {'strength': 3, 'intelligence': 12},
#             'legendary': {'strength': 5, 'intelligence': 17},
#             'mythic': {'strength': 7, 'intelligence': 24},
#             'blacksmith': True
#         },
#         'zealous': {
#             'common': {'strength': 1, 'speed': 0, 'crit damage': 1, 'intelligence': 1},
#             'uncommon': {'strength': 2, 'speed': 0, 'crit damage': 2, 'intelligence': 2},
#             'rare': {'strength': 2, 'speed': 1, 'crit damage': 2, 'intelligence': 3},
#             'epic': {'strength': 3, 'speed': 1, 'crit damage': 3, 'intelligence': 5},
#             'legendary': {'strength': 5, 'speed': 1, 'crit damage': 5, 'intelligence': 7},
#             'mythic': {'strength': 7, 'speed': 2, 'crit damage': 7, 'intelligence': 10},
#             'blacksmith': True
#         },
#         'strange': {
#             'common': {'crit damage': 1, 'strength': 2, 'defense': 0, 'speed': 1, 'health': 0, 'intelligence': 1,
#                        'attack speed': -1},
#             'uncommon': {'crit damage': 2, 'strength': 1, 'defense': 3, 'speed': 0, 'health': 2, 'intelligence': -1,
#                          'attack speed': 2},
#             'rare': {'crit damage': 0, 'strength': -1, 'defense': 2, 'speed': 1, 'health': 1, 'intelligence': 2,
#                      'attack speed': 0},
#             'epic': {'crit damage': 1, 'strength': 3, 'defense': -1, 'speed': 0, 'health': 7, 'intelligence': 0,
#                      'attack speed': 4},
#             'legendary': {'crit damage': 7, 'strength': 0, 'defense': 1, 'speed': 3, 'health': -1, 'intelligence': 8,
#                           'attack speed': 0},
#             'mythic': {'crit damage': 9, 'strength': 4, 'defense': 1, 'speed': 3, 'health': 0, 'intelligence': 11,
#                        'attack speed': 5},
#             'blacksmith': True
#         },
#         'silky': {
#             'common': {'crit damage': 5},
#             'uncommon': {'crit damage': 6},
#             'rare': {'crit damage': 8},
#             'epic': {'crit damage': 10},
#             'legendary': {'crit damage': 15},
#             'mythic': {'crit damage': 20},
#             'blacksmith': False
#         },
#         'bloody': {
#             'common': {'strength': 1, 'crit damage': 3, 'attack speed': 1, 'speed': 1},
#             'uncommon': {'strength': 1, 'crit damage': 4, 'attack speed': 1, 'speed': 1},
#             'rare': {'strength': 1, 'crit damage': 5, 'attack speed': 1, 'speed': 1},
#             'epic': {'strength': 2, 'crit damage': 6, 'attack speed': 2, 'speed': 1},
#             'legendary': {'strength': 3, 'crit damage': 9, 'attack speed': 2, 'speed': 1},
#             'mythic': {'strength': 4, 'crit damage': 14, 'attack speed': 2, 'speed': 1},
#             'blacksmith': False
#         },
#     },
#     'fishing rod': {
#         'salty': {
#             'common': {'sea creature chance': 1},
#             'uncommon': {'sea creature chance': 2},
#             'rare': {'sea creature chance': 2},
#             'epic': {'sea creature chance': 3},
#             'legendary': {'sea creature chance': 5},
#             'mythic': {'sea creature chance': 7},
#             'blacksmith': False
#         },
#         'treacherous': {
#             'common': {'sea creature chance': 1, 'strength': 5},
#             'uncommon': {'sea creature chance': 2, 'strength': 10},
#             'rare': {'sea creature chance': 2, 'strength': 15},
#             'epic': {'sea creature chance': 3, 'strength': 20},
#             'legendary': {'sea creature chance': 5, 'strength': 25},
#             'mythic': {'sea creature chance': 7, 'strength': 30},
#             'blacksmith': False
#         }
#     }
# }
