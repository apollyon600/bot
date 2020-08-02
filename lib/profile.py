from datetime import datetime

from . import ProfileStats, Pet, decode_inventory_data
from . import HypixelLanguageError
from utils import safe_list_get, level_from_xp_table
from constants import *


class Profile:
    def __init__(self, *, player, profile_data, load_all):
        self.player = player
        self.profile_data = profile_data['members'][player.uuid]
        self.id = profile_data['profile_id']
        self.name = profile_data['cute_name'].lower()
        self.last_save = datetime.fromtimestamp(self.profile_data.get('last_save', 0) / 1000.0)
        self.join_date = datetime.fromtimestamp(self.profile_data.get('first_join', 0) / 1000.0)
        self.purse = float(f'{self.profile_data.get("coin_purse", 0.00):.2f}')

        # Get coop members uuid if there is
        self.coop_members = []
        if len(profile_data['members']) > 1:
            for member in profile_data['members'].keys():
                if member != player.uuid:
                    self.coop_members.append(member)

        self.enabled_api = {'skills': False, 'collection': False, 'inventory': False, 'banking': False}
        self.current_armor = {'helmet': None, 'chestplate': None, 'leggings': None, 'boots': None}
        self.armor = {'helmet': None, 'chestplate': None, 'leggings': None, 'boots': None}
        self.weapon = None
        self.pet = None

        # Dungeon skill level, will be set if there is a dungeon item
        self.dungeon_skill = 0

        # Load profile's bank data if banking api is enabled
        self.bank_balance = 0.00
        self.bank_transactions = None
        if 'banking' in profile_data:
            self.enabled_api['banking'] = True
            self.bank_balance = float(f'{profile_data["banking"].get("balance", 0.00):.2f}')
            self.bank_transactions = profile_data['banking'].get('transactions', [])

        # Loads profile's skill skills api is enabled
        self.skills_xp = {}
        self.skills = {}
        for skill in SKILL_NAMES:
            if f'experience_skill_{skill}' in self.profile_data:
                self.enabled_api['skills'] = True
                xp = int(self.profile_data.get(f'experience_skill_{skill}', 0))
                self.skills_xp[skill] = xp
                self.skills[skill] = level_from_xp_table(
                    xp,
                    RUNECRAFTING_LEVEL_REQUIREMENT if skill == 'runecrafting' else SKILL_LEVEL_REQUIREMENT
                )
        self.skill_average = sum(
            skill_level for skill, skill_level in self.skills.items() if skill not in COSMETIC_SKILL_NAMES) / (
                                     len(SKILL_NAMES) - len(COSMETIC_SKILL_NAMES))

        # Load profile's slayer data
        self.slayers_xp = {}
        self.slayers = {}
        for slayer_name in SLAYERS:
            xp = self.profile_data.get('slayer_bosses', {}).get(slayer_name, {}).get('xp', 0)
            self.slayers_xp[slayer_name] = xp
            self.slayers[slayer_name] = level_from_xp_table(xp, SLAYER_LEVEL_REQUIREMENT[slayer_name])
        self.total_slayer_xp = sum(self.slayers_xp.values())

        # Loads profile's kills and deaths
        self.kills = int(self.profile_data.get('stats', {'kills': 0}).get('kills', 0))
        self.specifc_kills = {name.replace('kills_', '').replace('_', ' '): int(amount)
                              for name, amount in self.profile_data['stats'].items() if re.match('kills_', name)}

        self.deaths = int(self.profile_data.get('stats', {'deaths': 0}).get('deaths', 0))
        self.specifc_deaths = {name.replace('deaths_', '').replace('_', ' '): int(amount)
                               for name, amount in self.profile_data['stats'].items() if re.match('deaths_', name)}

        # Loads profile's collections if collection api is enabled
        try:
            # TODO: revise to get exactly collection name instead of collection's icon name
            self.collections = {collection.lower().replace('_', ' '): amount for collection, amount in
                                self.profile_data['collection'].items()}
            self.enabled_api['collection'] = True
        except KeyError:
            self.collections = {}

        # Load profile's minion slots
        self.unlocked_collections = self._parse_collection(self.profile_data, 'unlocked_coll_tiers')

        self.minions = self._parse_collection(self.profile_data, 'crafted_generators')
        self.unique_minions = sum(self.minions.values())
        self.minion_slots = level_from_xp_table(self.unique_minions, MINION_SLOT_REQUIREMENT)

        self.loaded_all = load_all
        if load_all:
            # Load profile stats
            self.stats = ProfileStats(BASE_PLAYER_STATS.copy(), profile=self)

            self.stats.combat_bonus = self.skills.get('combat', 0) * 4

            self.fairy_souls = self.profile_data.get('fairy_souls_collected', 0)
            self.stats.add_stat('health', FAIRY_SOUL_HP_BONUS[self.fairy_souls // 5])
            self.stats.add_stat('defense', self.fairy_souls // 5 + self.fairy_souls // 25)
            self.stats.add_stat('strength', self.fairy_souls // 5 + self.fairy_souls // 25)
            self.stats.add_stat('speed', self.fairy_souls // 50)

            for slayer_name, slayer_level in self.slayers.items():
                self.stats += ProfileStats(SLAYER_REWARDS[slayer_name][slayer_level])

            for skill_name, skill_level in self.skills.items():
                self.stats += ProfileStats(SKILL_REWARDS[skill_name][skill_level])

            # Load profile's current equipped armor
            for armor in self._parse_inventory(self.profile_data, ['inv_armor', 'data']):
                # check for special type
                if armor.type == 'hatccessory':
                    self.current_armor['helmet'] = armor
                else:
                    self.current_armor[armor.type] = armor

            # Load profile's inventories
            self.inventory = self._parse_inventory(self.profile_data, ['inv_contents', 'data'])
            self.echest = self._parse_inventory(self.profile_data, ['ender_chest_contents', 'data'])
            self.talisman_bag = self._parse_inventory(self.profile_data, ['talisman_bag', 'data'])
            # Comment out unnecessary inventories for now
            # self.candy_bag = self._parse_inventory(self.profile_raw_data, ['candy_inventory_contents', 'data'])
            # self.potion_bag = self._parse_inventory(self.profile_raw_data, ['potion_bag', 'data'])
            # self.fish_bag = self._parse_inventory(self.profile_raw_data, ['fishing_bag', 'data'])
            # self.quiver = self._parse_inventory(self.profile_raw_data, ['quiver', 'data'])
            if self.inventory or self.echest or self.talisman_bag:
                self.enabled_api['inventory'] = True

            # Load profile's weapon from inventory and ender chest
            self.weapons = [item for item in self.inventory + self.echest if item.type in ('sword', 'bow')]

            # Load profile's wardrobe
            self.wardrobe = []
            wardrobe = self._parse_inventory(self.profile_data, ['wardrobe_contents', 'data'], index_empty=True)
            for wardrobe_page in range(0, 2 * 36, 36):  # 2 for current max 2 pages of wardrobe
                for i in range(wardrobe_page, wardrobe_page + 9):
                    armor_set = {
                        'helmet': safe_list_get(wardrobe, i),
                        'chestplate': safe_list_get(wardrobe, i + 9),
                        'leggings': safe_list_get(wardrobe, i + 18),
                        'boots': safe_list_get(wardrobe, i + 27)
                    }
                    if all(item is None for item in armor_set.values()):
                        continue
                    self.wardrobe.append(armor_set)

            # Check if player has dungeon armor/wep items
            self.has_dungeon_items = False
            for item in self.inventory + self.echest + wardrobe:
                if not item:
                    continue
                if item.dungeon:
                    self.has_dungeon_items = True
                    break

            # Load profile's talismans from inventory + talisman bag and talisman counts
            self.talismans = [talisman for talisman in self.inventory + self.talisman_bag if
                              talisman.type in ('accessory', 'hatccessory')]
            self.talisman_counts = {'common': 0, 'uncommon': 0, 'rare': 0, 'epic': 0, 'legendary': 0, 'mythic': 0}
            talismans_dup = []

            for talisman in self.talismans:
                talisman.active = True
                # Check for talisman families
                if talisman.internal_name in TIERED_TALISMANS:
                    for other_fam_member in TIERED_TALISMANS[talisman.internal_name]:
                        if other_fam_member in self.talismans:
                            talisman.active = False
                            continue

                # Check for duplicate talismans
                if self.talismans.count(talisman) > 1:
                    talisman.active = False
                    if talisman not in talismans_dup:
                        talismans_dup.append(talisman)  # append the reference to a list to set active true later

            # Set one of the talisman dup to active true
            for talisman in talismans_dup:
                talisman.active = True

            # Load talisman stats
            self.stats.childrens.extend([talisman.stats for talisman in self.talismans if talisman.active])

            # Load talisman counts
            for taliman in self.talismans:
                if taliman.active:
                    # Check for hypixel language because it's most reliable here
                    try:
                        self.talisman_counts[taliman.rarity] += 1
                    except KeyError:
                        raise HypixelLanguageError from None

            # Loads profile's pets
            self.pets = []
            if 'pets' in self.profile_data:
                for pet_data in self.profile_data['pets']:
                    self.pets.append(Pet(pet_data, profile=self))

    def __str__(self):
        return self.name

    def set_weapon(self, weapon):
        """
        Set profile weapon.
        """
        if weapon and self.loaded_all:
            self.weapon = weapon

            self.stats.childrens.append(self.weapon.stats)

    def set_armor(self, armor, *, dungeon=False):
        """
        Set profile armor.
        """
        if armor and self.loaded_all:
            self.armor = armor

            self.stats.childrens.extend([piece.stats for piece in self.armor.values() if piece is not None])

            # Armor passive/set bonus
            if self.armor == {'helmet': 'SUPERIOR_DRAGON_HELMET', 'chestplate': 'SUPERIOR_DRAGON_CHESTPLATE',
                              'leggings': 'SUPERIOR_DRAGON_LEGGINGS', 'boots': 'SUPERIOR_DRAGON_BOOTS'}:
                self.stats.multiplier += 0.05
            elif self.armor['helmet'] == 'TARANTULA_HELMET':
                self.stats.add_modifier('crit damage',
                                        lambda stat: stat + self.stats.get_stat('strength', dungeon=dungeon) / 10)
            elif self.armor == {'helmet': 'MUSHROOM_HELMET', 'chestplate': 'MUSHROOM_CHESTPLATE',
                                'leggings': 'MUSHROOM_LEGGINGS', 'boots': 'MUSHROOM_BOOTS'}:
                for piece in self.armor.values():
                    piece.stats.multiplier *= 3
            elif self.armor == {'helmet': 'END_HELMET', 'chestplate': 'END_CHESTPLATE',
                                'leggings': 'END_LEGGINGS', 'boots': 'END_BOOTS'}:
                for piece in self.armor.values():
                    piece.stats.multiplier *= 2
            elif self.armor == {'helmet': 'BAT_PERSON_HELMET', 'chestplate': 'BAT_PERSON_CHESTPLATE',
                                'leggings': 'BAT_PERSON_LEGGINGS', 'boots': 'BAT_PERSON_BOOTS'}:
                for piece in self.armor.values():
                    piece.stats.multiplier *= 3
            elif self.armor == {'helmet': 'SNOW_SUIT_HELMET', 'chestplate': 'SNOW_SUIT_CHESTPLATE',
                                'leggings': 'SNOW_SUIT_LEGGINGS', 'boots': 'SNOW_SUIT_BOOTS'}:
                for piece in self.armor.values():
                    piece.stats.multiplier *= 2
            elif self.armor == {'helmet': 'YOUNG_DRAGON_HELMET', 'chestplate': 'YOUNG_DRAGON_CHESTPLATE',
                                'leggings': 'YOUNG_DRAGON_LEGGINGS', 'boots': 'YOUNG_DRAGON_BOOTS'}:
                self.stats.add_stat('speed cap', 100)
            elif self.armor == {'helmet': 'MASTIFF_HELMET', 'chestplate': 'MASTIFF_CHESTPLATE',
                                'leggings': 'MASTIFF_LEGGINGS', 'boots': 'MASTIFF_BOOTS'}:
                self.stats.add_modifier('crit damage', lambda stat: stat / 2)
                self.stats.add_modifier('health',
                                        lambda stat: stat + self.stats.get_stat('crit damage', dungeon=dungeon) * 50)
            elif self.weapon == 'POOCH_SWORD':
                self.weapon.stats.add_modifier('damage',
                                               lambda stat: stat + self.stats.get_stat('health', dungeon=dungeon) // 50)

    def set_pet(self, pet, *, dungeon=False):
        """
        Set profile pet.
        """
        if pet and self.loaded_all:
            self.pet = pet

            self.stats.childrens.append(self.pet.stats)

            pet_ability = PETS[self.pet.internal_name]['ability']
            if callable(pet_ability):
                pet_ability(self, dungeon=dungeon)

    def set_pet_armor_automatically(self):
        if not self.loaded_all:
            return

        self.set_armor(self.current_armor)

        for pet in self.pets:
            if pet.active:
                self.set_pet(pet)

    async def get_profile_auctions(self):
        """
        Get profile's active auctions.
        """
        # call hypixel auction endpoint.
        raise NotImplementedError

    def get_skills_from_achievements(self):
        """
        Set profile's skill base on player's achievements
        """
        # only when profile's skill api disabled
        # not implement for now due to unreliable: which profile achieved those achievements
        raise NotImplementedError

    def _parse_inventory(self, profile_raw_data, path, *, index_empty=False):
        try:
            raw_data = profile_raw_data
            for key in path:
                raw_data = raw_data[key]
            return decode_inventory_data(raw_data, self, index_empty=index_empty)
        except KeyError:
            return []

    # TODO: revise this aswell
    # noinspection PyTypeChecker,PyShadowingNames
    @staticmethod
    def _parse_collection(raw_data, path):
        try:
            tuples = []
            for s in raw_data[path]:
                temp = re.split('_(?!.*_)', s, maxsplit=1)
                temp[1] = int(temp[1])
                tuples.append(temp)
            dictionary = {}
            for s in set(name for name, level in tuples):
                max_level = 0
                for name, level in tuples:
                    if name == s and level > max_level:
                        max_level = level
                dictionary[s.lower().replace('_', ' ')] = max_level
            return dictionary
        except KeyError:
            return {}
