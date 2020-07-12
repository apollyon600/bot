import re
from base64 import b64decode as one
from gzip import decompress as two
from io import BytesIO as three
from struct import unpack

from . import Stats
from constants import bow_enchants, rod_enchants, sword_enchants


class Item:
    def __init__(self, nbt, slot_number=0, player=None):
        self._nbt = nbt
        self.player = player

        self.stack_size = self._nbt.get('Count', 1)
        self.slot_number = slot_number

        tag = nbt.get('tag', {})
        extras = tag.get('ExtraAttributes', {})

        self.description = tag.get('display', {}).get('Lore', [])
        self.description_clean = [re.sub('§.[a-z]?', '', line) for line in self.description]
        self.description = '\n'.join(self.description)
        self.internal_name = extras.get('id', None)
        name = self.internal_name if self.internal_name else None
        self.hot_potatos = extras.get('hot_potato_count', 0)
        self.collection_date = extras.get('timestamp', '')  # ex: 'timestamp': '2/16/20 9:24 PM',
        self.runes = extras.get('runes', {})  # ex: 'runes': {'ZOMBIE_SLAYER': 3},
        self.enchantments = extras.get('enchantments', {})
        self.reforge = extras.get('modifier', None)
        self.dungeon = False

        if self.description_clean:
            rarity_type = self.description_clean[-1].split()
            self.rarity = rarity_type[0].lower()
            self.type = rarity_type[2].lower() if len(rarity_type) > 2 else rarity_type[1].lower() if len(
                rarity_type) > 1 else None
            self.dungeon = True if len(rarity_type) > 2 and rarity_type[1].lower() == 'dungeon' else False

            if self != 'ENCHANTED_BOOK':
                for type, enchant_list in {'fishing rod': rod_enchants, 'bow': bow_enchants,
                                           'sword': sword_enchants}.items():
                    for e in enchant_list:
                        if e in self.enchantments and e != 'looting' and e != 'dragon_hunter':
                            self.type = type
                            break
        else:
            self.rarity = None
            self.type = None

        self.name = re.sub('§.', '', self['tag']['display']['Name'])

        # Stats
        self.stats = Stats()
        self.base_stats = Stats()

        # Parse items from cake bag and backpacks
        self.contents = None
        if name:
            if name == 'NEW_YEAR_CAKE_BAG' or name.endswith('_BACKBACK'):
                for k, v in extras.items():
                    if k == 'new_year_cake_bag_data' or k.endswith('_backpack_data'):
                        self.contents = decode_inventory_data(v, player, backpack=True)
                        break

            if name == 'RECLUSE_FANG':
                self.stats.__iadd__('strength', 370)
            elif name == 'POOCH_SWORD':
                self.stats.__iadd__('strength', 150)
            elif name == 'THE_SHREDDER':
                self.stats.__iadd__('damage', 115)
                self.stats.__iadd__('strength', 15)
            elif name == 'NIGHT_CRYSTAL' or name == 'DAY_CRYSTAL':
                self.stats.__iadd__('strength', 2.5)
                self.stats.__iadd__('defense', 2.5)
            elif name == 'NEW_YEAR_CAKE_BAG':
                self.stats.__iadd__('health', len(self.contents) if self.contents else 0)
            elif name == 'GRAVITY_TALISMAN':
                self.stats.__iadd__('strength', 10)
                self.stats.__iadd__('defense', 10)
            elif name == 'SPEED_TALISMAN':
                self.stats.__iadd__('speed', 1)
            elif name == 'SPEED_RING':
                self.stats.__iadd__('speed', 3)
            elif name == 'SPEED_ARTIFACT':
                self.stats.__iadd__('speed', 5)
            elif name == 'CHEETAH_TALISMAN':
                self.stats.__iadd__('speed', 3)
            # elif name == 'PARTY_HAT_CRAB':
            # Get Intelligence base on how long player played (tbd)
            elif name == 'PIGMAN_SWORD':
                self.stats.__iadd__('defense', 50)
            elif self.player:
                # if name == 'POOCH_SWORD' and self.player.weapon == 'POOCH_SWORD':
                # 	self.stats.modifiers['damage'].insert(0, lambda stat: stat + player.stats['health'] // 50)
                if re.match('MUSHROOM_(HELMET|CHESTPLATE|LEGGINGS|BOOTS)', name) and self.player.armor == {
                    'helmet': 'MUSHROOM_HELMET', 'chestplate': 'MUSHROOM_CHESTPLATE', 'leggings': 'MUSHROOM_LEGGINGS',
                    'boots': 'MUSHROOM_BOOTS'}:
                    self.stats.multiplier *= 3
                elif re.match('END_(HELMET|CHESTPLATE|LEGGINGS|BOOTS)', name) and self.player.armor == {
                    'helmet': 'END_HELMET', 'chestplate': 'END_CHESTPLATE', 'leggings': 'END_LEGGINGS',
                    'boots': 'END_BOOTS'}:
                    self.stats.multiplier *= 2
                elif re.match('BAT_PERSON_(HELMET|CHESTPLATE|LEGGINGS|BOOTS)', name) and self.player.armor == {
                    'helmet': 'BAT_PERSON_HELMET', 'chestplate': 'BAT_PERSON_CHESTPLATE',
                    'leggings': 'BAT_PERSON_LEGGINGS', 'boots': 'BAT_PERSON_BOOTS'}:
                    self.stats.multiplier *= 3
                elif re.match('SNOW_SUIT_(HELMET|CHESTPLATE|LEGGINGS|BOOTS)', name) and self.player.armor == {
                    'helmet': 'SNOW_SUIT_HELMET', 'chestplate': 'SNOW_SUIT_CHESTPLATE',
                    'leggings': 'SNOW_SUIT_LEGGINGS', 'boots': 'SNOW_SUIT_BOOTS'}:
                    self.stats.multiplier *= 2

        if self.reforge == 'renowned' and player:
            player.stats.multiplier += 0.01

        r = re.compile('([\w ]*): \+(\d*\.?\d*)(.*)')
        r_r = re.compile('.*\(([\w ]*) \+(\d*)')

        for line in self.description_clean:
            match = r.match(line)
            if match:
                self.stats['attack speed' if match[1].lower() == 'bonus attack speed' else match[1].lower()] = float(
                    match[2])
                match_r = r_r.match(match.group(3))
                reforge_stat = float(match_r[2]) if match_r else 0
                if float(match[2]) - reforge_stat == 0:
                    continue
                self.base_stats[
                    'attack speed' if match[1].lower() == 'bonus attack speed' else match[1].lower()] = float(
                    match[2]) - reforge_stat

    def __getitem__(self, name):
        return self._nbt[name]

    def __eq__(self, other):
        return self.internal_name == (other if isinstance(other, str) else other.internal_name)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"'{self.internal_name}'"


def decode_inventory_data(raw, player=None, backpack=False):
    """
	Takes a raw string representing inventory data.
	Returns a json object with the inventory's contents
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

    return [Item(x, i, player) for i, x in enumerate(root['i']) if x and 'tag' in x and 'ExtraAttributes' in x['tag']]
