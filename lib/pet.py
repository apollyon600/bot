import re

from . import Stats
from utils import level_from_xp_table
from constants import PET_RARITIES, PET_XP, PETS


class Pet:
    def __init__(self, nbt):
        self._nbt = nbt
        self.xp = nbt.get('exp', 0)
        self.active = nbt.get('active', False)
        self.rarity = nbt.get('tier', 'COMMON').lower()
        self.item_internal_name = nbt.get('heldItem', None)
        if self.item_internal_name:
            self.item_name = ' '.join([
                s.capitalize() for s in
                re.sub('_COMMON|_UNCOMMON|_RARE|_EPIC|_LEGENDARY', '', self.item_internal_name[9:]).split('_')
            ])
            if self.item_name == 'Tier Boost':
                self.rarity = PET_RARITIES[PET_RARITIES.index(self.rarity) + 1]
        else:
            self.item_name = None
        self.internal_name = nbt.get('type', 'BEE')
        self.level = level_from_xp_table(self.xp, PET_XP[self.rarity])
        self.name = PETS[self.internal_name]['name']
        self.title = f'[Lvl {self.level}] {self.name}'
        self.xp_remaining = PET_XP[self.rarity][-1] - self.xp
        self.candy_used = nbt.get('candyUsed', 0)
        self.stats = Stats({stat: function(self.level) for stat, function in PETS[self.internal_name]['stats'].items()})

        if self.item_name:
            if self.item_name == 'Textbook':
                self.stats.modifiers['intelligence'].append(lambda stat: stat * 2)
            elif self.item_name == 'Hardened Scales':
                self.stats.__iadd__('defense', 25)
            elif self.item_name == 'Iron Claws':
                self.stats.modifiers['crit chance'].append(lambda stat: stat * 1.4)
                self.stats.modifiers['crit damage'].append(lambda stat: stat * 1.4)
            elif self.item_name == 'Sharpened Claws':
                self.stats.__iadd__('crit damage', 15)
            elif self.item_name == 'Big Teeth':
                self.stats.__iadd__('crit chance', 5)
            elif self.item_name == 'Lucky Clover':
                self.stats.__iadd__('magic find', 7)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"'{self.internal_name}'"
