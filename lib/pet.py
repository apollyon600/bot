import re

from . import PetStats
from utils import level_from_xp_table
from constants import PET_RARITIES, PET_XP, PETS


class Pet:
    def __init__(self, raw_data, *, profile=None):
        self._nbt = raw_data
        self.profile = profile
        self.type = 'pet'

        self.active = raw_data.get('active', False)

        self.xp = raw_data.get('exp', 0)
        self.rarity = raw_data.get('tier', 'COMMON').lower()
        self.xp_remaining = PET_XP[self.rarity][-1] - self.xp
        self.level = level_from_xp_table(self.xp, PET_XP[self.rarity])

        self.internal_name = raw_data.get('type', 'PET')
        self.name = PETS[self.internal_name]['name']
        self.title = f'[Lvl {self.level}] {self.name}'

        self.candy_used = raw_data.get('candyUsed', 0)

        self.item_internal_name = raw_data.get('heldItem', None)
        self.item_name = None
        if self.item_internal_name:
            self.item_name = ' '.join([
                s.capitalize() for s in
                re.sub('_COMMON|_UNCOMMON|_RARE|_EPIC|_LEGENDARY', '', self.item_internal_name[9:]).split('_')
            ])

        # Load pet stats
        self.stats = PetStats(
            {stat: function(self.level) for stat, function in PETS[self.internal_name]['stats'].items()},
            pet=self
        )

        if self.item_name:
            if self.item_name == 'Tier Boost':
                self.rarity = PET_RARITIES[PET_RARITIES.index(self.rarity) + 1]
            elif self.item_name == 'Textbook':
                self.stats.add_modifier('intelligence', lambda stat: stat * 2)
            elif self.item_name == 'Hardened Scales':
                self.stats.add_stat('defense', 25)
            elif self.item_name == 'Iron Claws':
                self.stats.add_modifier('crit chance', lambda stat: stat * 1.4)
                self.stats.add_modifier('crit damage', lambda stat: stat * 1.4)
            elif self.item_name == 'Sharpened Claws':
                self.stats.add_stat('crit damage', 15)
            elif self.item_name == 'Big Teeth':
                self.stats.add_stat('crit chance', 5)
            elif self.item_name == 'Lucky Clover':
                self.stats.add_stat('magic find', 7)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.title
