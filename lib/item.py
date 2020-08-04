import re
from base64 import b64decode as one
from gzip import decompress as two
from io import BytesIO as three
from struct import unpack

from . import ItemStats
from utils import get_stats_from_description, closest
from constants import ACCUMULATED_CATACOMB_LEVEL_REWARDS


class Item:
    def __init__(self, raw_data, profile, *, slot_number=0):
        self._raw_data = raw_data
        self.profile = profile

        tag = raw_data.get('tag', {})
        extras = tag.get('ExtraAttributes', {})

        self.slot_number = slot_number
        self.stack_size = self._raw_data.get('Count', 1)

        # Load item name and description
        self.name = re.sub('§.', '', tag.get('display', {}).get('Name', ''))
        self.internal_name = extras.get('id', '')

        self.description = tag.get('display', {}).get('Lore', [])
        self.description_clean = [re.sub('§.', '', line) for line in self.description]

        # Load item extra attributes
        self.hot_potatos = extras.get('hot_potato_count', 0)
        self.anvil_uses = extras.get('anvil_uses', 0) - self.hot_potatos
        self.collection_date = extras.get('timestamp', '')  # ex: 'timestamp': '2/16/20 9:24 PM'
        self.runes = extras.get('runes', {})  # ex: 'runes': {'ZOMBIE_SLAYER': 3}
        self.enchantments = extras.get('enchantments', {})
        self.reforge = extras.get('modifier', None)
        self.recombobulation = False
        if 'rarity_upgrades' in extras:
            if extras['rarity_upgrades'] == 1:
                self.recombobulation = True
        self.dungeon = 'dungeon_item_level' in extras
        self.dungeon_level = None
        if self.dungeon:
            self.dungeon_level = extras['dungeon_item_level']

        # Load item rarity and item from last line of description clean
        self.rarity = None
        self.type = None
        if self.description_clean:
            last_line = self.description_clean[-1].split()
            # remove extra 'a' from recombobulated item description last line
            if self.recombobulation:
                last_line.pop(0)
                last_line.pop(-1)

            self.rarity = last_line[0].lower()
            if len(last_line) > 1:
                self.type = last_line[1].lower()
                if (self.dungeon or last_line[1].lower() == 'dungeon') and len(last_line) > 2:
                    # In case some dungeon item doesnt have 'dungeon_item_level' attribute
                    if not self.dungeon:
                        self.dungeon = True
                        self.dungeon_level = 0
                    self.type = last_line[2].lower()

        # Load item from backpacks
        self.contents = None
        if self.internal_name == 'NEW_YEAR_CAKE_BAG' or self.internal_name.endswith('_BACKPACK'):
            for key, value in extras.items():
                if key == 'new_year_cake_bag_data' or key.endswith('_backpack_data'):
                    self.contents = decode_inventory_data(value, profile, backpack=True)
                    break

        # Load item stats
        stats, reforge_stat, dungeon_bonus = get_stats_from_description(self.description_clean, dungeon=self.dungeon)
        self.stats = ItemStats(stats, item=self, dungeon=self.dungeon)
        self.stats.reforge_stat = reforge_stat
        if self.dungeon:
            self.stats.dungeon_bonus += self.dungeon_level / 10

        # Check and get profile's catacomb dungeon bonus + level based on dungeon bonus from description.
        # Only when the item is a dungeon item + there's a dungeon bonus from item and profile dungeon level hasn't been set.
        if self.dungeon and dungeon_bonus > 1.00 and self.profile.dungeon_skill == 0:
            relative_dungeon_bonus = (dungeon_bonus - (1 + self.dungeon_level / 10)) * 100
            total_dungeon_bonus, dungeon_level = closest(ACCUMULATED_CATACOMB_LEVEL_REWARDS['dungeon bonus'],
                                                         relative_dungeon_bonus)
            self.profile.dungeon_skill = dungeon_level
            self.profile.stats.dungeon_bonus += total_dungeon_bonus / 100

        self.get_item_stats_extra()

    def get_item_stats_extra(self):
        """
        Get extra stats from some specific item
        """
        name = self.internal_name
        if name:
            if name == 'RECLUSE_FANG':
                self.stats.add_stat('strength', 370)
            elif name == 'POOCH_SWORD':
                self.stats.add_stat('strength', 150)
            elif name == 'THE_SHREDDER':
                self.stats.add_stat('damage', 115)
                self.stats.add_stat('strength', 15)
            elif name == 'NIGHT_CRYSTAL' or name == 'DAY_CRYSTAL':
                self.stats.add_stat('strength', 2.5)
                self.stats.add_stat('defense', 2.5)
            elif name == 'NEW_YEAR_CAKE_BAG':
                self.stats.add_stat('health', len(self.contents) if self.contents else 0)
            elif name == 'GRAVITY_TALISMAN':
                self.stats.add_stat('strength', 10)
                self.stats.add_stat('defense', 10)
            elif name == 'SPEED_TALISMAN':
                self.stats.add_stat('speed', 1)
            elif name == 'SPEED_RING':
                self.stats.add_stat('speed', 3)
            elif name == 'SPEED_ARTIFACT':
                self.stats.add_stat('speed', 5)
            elif name == 'CHEETAH_TALISMAN':
                self.stats.add_stat('speed', 3)
            elif name == 'PIGMAN_SWORD':
                self.stats.add_stat('defense', 50)

        if self.reforge == 'renowned':
            self.profile.stats.multiplier += 0.01

    def __getitem__(self, key):
        if isinstance(key, str):
            return self._raw_data.get(key, None)
        else:
            raise KeyError

    def __eq__(self, other):
        if isinstance(other, str):
            return self.internal_name == other
        elif isinstance(other, Item):
            return self.internal_name == other.internal_name
        else:
            raise TypeError

    def __str__(self):
        return self.name


def decode_inventory_data(raw, profile=None, *, backpack=False, index_empty=False):
    """
	Takes a raw string representing inventory data.
	Returns a json object with the inventory's contents.
	"""

    if backpack:
        raw = three(two(raw))
    else:
        raw = three(two(one(raw)))  # Unzip raw string from the api

    def read(type, length):
        if type in 'chil':
            return int.from_bytes(raw.read(length), byteorder='big')
        if type == 's':
            return raw.read(length).decode('utf-8')
        return unpack(f'>{type}', raw.read(length))[0]

    def parse_list():
        subtype = read('c', 1)
        payload = []
        for _ in range(read('i', 4)):
            parse_next_tag(payload, subtype)
        return payload

    def parse_compound():
        payload = {}
        while parse_next_tag(payload) != 0:  # Parse tags until we find an endcap (type == 0)
            pass  # Nothing needs to happen here
        return payload

    payloads = {
        1: lambda: read('c', 1),  # Byte
        2: lambda: read('h', 2),  # Short
        3: lambda: read('i', 4),  # Int
        4: lambda: read('l', 8),  # Long
        5: lambda: read('f', 4),  # Float
        6: lambda: read('d', 8),  # Double
        7: lambda: raw.read(read('i', 4)),  # Byte Array
        8: lambda: read('s', read('h', 2)),  # String
        9: parse_list,  # List
        10: parse_compound,  # Compound
        11: lambda: [read('i', 4) for _ in range(read('i', 4))],  # Int Array
        12: lambda: [read('l', 8) for _ in range(read('i', 4))]  # Long Array
    }

    def parse_next_tag(dictionary, tag_id=None):
        name = None
        if tag_id is None:  # Are we inside a list?
            tag_id = read('c', 1)
            if tag_id == 0:  # Is this the end of a compound?
                return 0
            name = read('s', read('h', 2))

        payload = payloads[tag_id]()
        if isinstance(dictionary, dict):
            dictionary[name] = payload
        else:
            dictionary.append(payload)

    raw.read(3)  # Remove file header (we ingore footer)
    root = {}
    parse_next_tag(root)

    items = []
    for i, x in enumerate(root['i']):
        if x and 'tag' in x and 'ExtraAttributes' in x['tag']:
            items.append(Item(x, profile, slot_number=i))
        elif index_empty:
            items.append(None)

    return items
