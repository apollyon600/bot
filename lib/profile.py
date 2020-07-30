from datetime import datetime

from . import Stats, Pet, decode_inventory_data
from . import HypixelLanguageError
from utils import safe_list_get, level_from_xp_table
from constants import *


class Profile:
    def __init__(self, *, player, profile):
        self.player = player
        self.profile_raw_data = profile['members'][player.uuid]
        self.profile_id = profile['profile_id']
        self.profile_name = profile['cute_name'].lower()
        self.last_save = datetime.fromtimestamp(self.profile_raw_data.get('last_save', 0) / 1000.0)
        self.join_date = datetime.fromtimestamp(self.profile_raw_data.get('first_join', 0) / 1000.0)
        self.purse = float(f'{self.profile_raw_data.get("coin_purse", 0.00):.2f}')

        # Get coop members uuid if there is
        self.coop_members = []
        if len(profile['members']) > 1:
            for member in profile['members'].keys():
                if member != player.uuid:
                    self.coop_members.append(member)

        self.enabled_api = {'skills': False, 'collection': False, 'inventory': False, 'banking': False}
        self.current_armor = {'helmet': None, 'chestplate': None, 'leggings': None, 'boots': None}
        self.armor = {'helmet': None, 'chestplate': None, 'leggings': None, 'boots': None}
        self.weapon = None
        self.pet = None

        # Load profile's bank data if banking api is enabled
        self.bank_balance = 0.00
        self.bank_transactions = None
        if 'banking' in profile:
            self.enabled_api['banking'] = True
            self.bank_balance = float(f'{profile["banking"].get("balance", 0.00):.2f}')
            self.bank_transactions = profile['banking'].get('transactions', [])

        # Loads profile's skill skills api is enabled
        self.skills_xp = {}
        self.skills = {}
        for skill in SKILL_NAMES:
            if f'experience_skill_{skill}' in self.profile_raw_data:
                self.enabled_api['skills'] = True
                xp = int(self.profile_raw_data.get(f'experience_skill_{skill}', 0))
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
            xp = self.profile_raw_data.get('slayer_bosses', {}).get(slayer_name, {}).get('xp', 0)
            self.slayers_xp[slayer_name] = xp
            self.slayers[slayer_name] = level_from_xp_table(xp, SLAYER_LEVEL_REQUIREMENT[slayer_name])
        self.total_slayer_xp = sum(self.slayers_xp.values())

        # Loads profile's kills and deaths
        self.kills = int(self.profile_raw_data.get('stats', {'kills': 0}).get('kills', 0))
        self.specifc_kills = {name.replace('kills_', '').replace('_', ' '): int(amount)
                              for name, amount in self.profile_raw_data['stats'].items() if re.match('kills_', name)}

        self.deaths = int(self.profile_raw_data.get('stats', {'deaths': 0}).get('deaths', 0))
        self.specifc_deaths = {name.replace('deaths_', '').replace('_', ' '): int(amount)
                               for name, amount in self.profile_raw_data['stats'].items() if re.match('deaths_', name)}

        # Load profile base stats
        self.stats = Stats(BASE_PLAYER_STATS.copy())

        self.fairy_souls = self.profile_raw_data.get('fairy_souls_collected', 0)
        self.stats.__iadd__('health', FAIRY_SOUL_HP_BONUS[self.fairy_souls // 5])
        self.stats.__iadd__('defense', self.fairy_souls // 5 + self.fairy_souls // 25)
        self.stats.__iadd__('strength', self.fairy_souls // 5 + self.fairy_souls // 25)
        self.stats.__iadd__('speed', self.fairy_souls // 50)

        for slayer_name, slayer_level in self.slayers.items():
            self.stats += Stats(SLAYER_REWARDS[slayer_name][slayer_level])

        for skill_name, skill_level in self.skills.items():
            self.stats += Stats(SKILL_REWARDS[skill_name][skill_level])

        # Load profile's current equipped armor
        for armor in self._parse_inventory(self.profile_raw_data, ['inv_armor', 'data']):
            # check for special type
            if armor.type == 'hatccessory':
                self.current_armor['helmet'] = armor
            else:
                self.current_armor[armor.type] = armor

        # Load profile's inventories
        self.inventory = self._parse_inventory(self.profile_raw_data, ['inv_contents', 'data'])
        self.echest = self._parse_inventory(self.profile_raw_data, ['ender_chest_contents', 'data'])
        self.talisman_bag = self._parse_inventory(self.profile_raw_data, ['talisman_bag', 'data'])
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
        wardrobe = self._parse_inventory(self.profile_raw_data, ['wardrobe_contents', 'data'], index_empty=True)
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

        # Load profile's talismans from inventory + talisman bag and talisman counts
        self.talismans = [talisman for talisman in self.inventory + self.talisman_bag if
                          talisman.type in ('accessory', 'hatccessory')]
        self.talisman_counts = {'common': 0, 'uncommon': 0, 'rare': 0, 'epic': 0, 'legendary': 0, 'mythic': 0}
        talismans_dup = []

        for talisman in self.talismans:
            talisman.active = True
            # Check for duplicate talismans
            if self.talismans.count(talisman) > 1:
                talisman.active = False
                if talisman not in talismans_dup:
                    talismans_dup.append(talisman)  # append the reference to a list to set active true later
                continue  # no need to check for families

            # Check for talisman families
            if talisman.internal_name in TIERED_TALISMANS:
                for other_fam_member in TIERED_TALISMANS[talisman.internal_name]:
                    if other_fam_member in self.talismans:
                        talisman.active = False
                        break

        # Set one of the talisman dup to active true
        for talisman in talismans_dup:
            talisman.active = True

        # Load talisman stats
        self.stats.children.extend([('accessory', talisman.stats) for talisman in self.talismans if talisman.active])
        self.stats.base_children.extend(
            [('accessory', talisman.base_stats) for talisman in self.talismans if talisman.active])

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
        if 'pets' in self.profile_raw_data:
            for pet_data in self.profile_raw_data['pets']:
                self.pets.append(Pet(pet_data))

        # Loads profile's collections if collection api is enabled
        try:
            # TODO: revise to get exactly collection name instead of collection's icon name
            self.collections = {collection.lower().replace('_', ' '): amount for collection, amount in
                                self.profile_raw_data['collection'].items()}
            self.enabled_api['collection'] = True
        except KeyError:
            self.collections = {}

        # Load profile's minion slots
        self.unlocked_collections = self._parse_collection(self.profile_raw_data, 'unlocked_coll_tiers')

        self.minions = self._parse_collection(self.profile_raw_data, 'crafted_generators')
        self.unique_minions = sum(self.minions.values())
        self.minion_slots = level_from_xp_table(self.unique_minions, MINION_SLOT_REQUIREMENT)

    def __str__(self):
        return self.profile_name

    def set_weapon(self, weapon):
        """
        Set profile weapon.
        """
        if weapon:
            self.weapon = weapon

            self.stats.children.append((self.weapon.type, self.weapon.stats))
            self.stats.base_children.append((self.weapon.type, self.weapon.base_stats))

    def set_armor(self, armor):
        """
        Set profile armor.
        """
        if armor:
            self.armor = armor

            self.stats.children.extend([(type, piece.stats) for type, piece in self.armor.items() if piece is not None])
            self.stats.base_children.extend(
                [(type, piece.base_stats) for type, piece in self.armor.items() if piece is not None])

            # Armor passive/set bonus
            if self.armor == {'helmet': 'SUPERIOR_DRAGON_HELMET', 'chestplate': 'SUPERIOR_DRAGON_CHESTPLATE',
                              'leggings': 'SUPERIOR_DRAGON_LEGGINGS', 'boots': 'SUPERIOR_DRAGON_BOOTS'}:
                self.stats.multiplier += 0.05
            elif self.armor['helmet'] == 'TARANTULA_HELMET':
                self.stats.modifiers['crit damage'].insert(0, lambda stat: stat + self.stats['strength'] / 10)
            # These are not supported for now
            # elif self.armor == {'helmet': 'YOUNG_HELMET', 'chestplate': 'YOUNG_CHESTPLATE', 'leggings': 'YOUNG_LEGGINGS', 'boots': 'YOUNG_BOOTS'}: #name maybe wrong check later
            # 	self.stats.__iadd__('speed cap', 100)
            # elif self.armor == {'helmet': 'MASTIFF_HELMET', 'chestplate': 'MASTIFF_CHESTPLATE', 'leggings': 'MASTIFF_LEGGINGS', 'boots': 'MASTIFF_BOOTS'}:
            # 	self.stats.modifiers['crit damage'].append(lambda stat: stat / 2)
            # 	self.stats.modifiers['health'].append(lambda stat: stat + self.stats['crit damage'] * 50)

    def set_pet(self, pet):
        """
        Set profile pet.
        """
        if pet:
            self.pet = pet

            self.stats.children.append((self.pet.internal_name, self.pet.stats))
            self.stats.base_children.append((self.pet.internal_name, self.pet.stats))

            pet_ability = PETS[self.pet.internal_name]['ability']
            if callable(pet_ability):
                pet_ability(self)

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
