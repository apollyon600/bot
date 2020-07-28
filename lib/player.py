import asyncio
import copy
from datetime import datetime

from . import Pet, Stats, HypixelApiInterface, HypixelAPIError, DataError, NeverPlayedSkyblockError, \
    decode_inventory_data, fetch_uuid_uname, level_from_xp_table, BadProfileError, safe_list_get, HypixelLanguageError
from constants import *


# noinspection PyUnusedLocal,PyShadowingNames
class Player(HypixelApiInterface):
    """
    A class representing a Skyblock player.
    Instantiate the class with Player(api_key, username) or Player(api_key, uuid)
    Use set_profile() to define the profile data.
    Use set_weapon() to set the player's weapon.
    Use set_pet() to set the player's pet.
    Use set_armor() to set the player's armor.
    """

    async def __init__(self, api_keys, *, uname=None, uuid=None, guild=False, _profiles=None, _achivements=None,
                       session=None):
        self.session = session
        if uname and uuid:
            self.uname = uname
            self.uuid = uuid
        elif uname and not uuid:
            self.uname, self.uuid = await fetch_uuid_uname(uname, self.session)
        elif uuid and not uname:
            self.uname, self.uuid = await fetch_uuid_uname(uuid, self.session)
        else:
            raise DataError('You need to provide either a minecraft username or uuid!')
        self.online = False

        if _profiles and _achivements:
            self.profiles = _profiles
            self.achievements = _achivements
        else:
            try:
                self.profiles = {}
                player = await self.__call_api__('/player', self.session, uuid=self.uuid)
                player_data = player['player']
                profile_ids = player_data['stats']['SkyBlock']['profiles']

                self.online = player_data['lastLogout'] < player_data['lastLogin']
                self.achievements = player['player']['achievements']

                for k, v in profile_ids.items():
                    self.profiles[v['cute_name']] = k

            except (KeyError, TypeError):
                raise NeverPlayedSkyblockError(self.uname) from None
            if not self.profiles:
                raise NeverPlayedSkyblockError(self.uname) from None

        if guild:
            guild_id = (await self.__call_api__('/findGuild', self.session, byUuid=self.uuid))['guild']
            if guild_id:
                self.guild_id = guild_id
                self.guild_info = (await self.__call_api__('/guild', self.session, id=self.guild_id))['guild']
                self.guild = self.guild_info['name']
            else:
                self.guild_id = None
                self.guild_info = None
                self.guild = None

        self._profile_set = False

    def __str__(self):
        return self.uname

    def __repr__(self):
        return f"'{self.uname}'"

    def avatar(self, size=None):
        if size:
            return f'https://mc-heads.net/avatar/{self.uuid}/{size}'
        else:
            return f'https://mc-heads.net/avatar/{self.uuid}'

    # TODO: set profile automatically is kinda api expensive, need a revise
    async def set_profile_automatically(self, attribute=lambda player: player.total_slayer_xp, threshold=None):
        """
        Sets a player profile automatically
        <attribute> is a function that takes a <Player> class and returns whatever value you want to set it based on
        example: player.set_profile_automatically(lambda player: player.skill_xp['combat'])
        """
        best = None
        max_value = 0

        profile_names = list(self.profiles.keys())

        if threshold:
            best = profile_names[0]
            for profile in reversed(profile_names):
                try:
                    canidate = await self._create_canadate(self, profile)
                except HypixelAPIError:
                    continue

                if attribute(canidate) >= threshold:
                    best = profile
                    break
        else:
            for canidate in asyncio.as_completed([self._create_canadate(self, profile) for profile in profile_names]):
                try:
                    canidate = await canidate
                    current = attribute(canidate)
                    if best is None or current > max_value:
                        max_value = current
                        best = canidate.profile_name
                except HypixelAPIError:
                    pass

        await self.set_profile(best)

    # noinspection PyAttributeOutsideInit
    async def set_profile(self, profile_name):
        """
        Sets a player's profile based on the provided profile ID
        """

        if self._profile_set:
            raise DataError('This player already has their profile set!')
        self._profile_set = True

        try:
            self.profile = self.profiles[profile_name.capitalize()]
        except KeyError:
            raise BadProfileError(profile_name)
        self.profile_name = profile_name.capitalize()

        # Get player's inventories nbt data
        self._nbt = (await self.__call_api__('/skyblock/profile', self.session, profile=self.profile))['profile']
        if not self._nbt or not self._nbt['members'][self.uuid]:
            raise DataError('Something\'s wrong with player\'s items nbt data')
        v = self._nbt['members'][self.uuid]

        self.enabled_api = {'skills': False, 'collection': False, 'inventory': False, 'banking': False}
        self.armor = {'helmet': None, 'chestplate': None, 'leggings': None, 'boots': None}

        # Loads a player's numeric stats
        self.stats = Stats(copy.deepcopy(base_player_stats))

        self.current_armor = {'helmet': None, 'chestplate': None, 'leggings': None, 'boots': None}
        for armor in self._parse_inventory(self, v, path=['inv_armor', 'data']):
            if armor.type == 'hatccessory':
                self.current_armor['helmet'] = armor
            else:
                self.current_armor[armor.type] = armor

        # Loads all of a player's inventories
        self.inventory = self._parse_inventory(self, v, path=['inv_contents', 'data'])
        self.echest = self._parse_inventory(self, v, path=['ender_chest_contents', 'data'])
        self.weapons = [item for item in self.inventory + self.echest if item.type in ('sword', 'bow', 'fishing rod')]
        self.candy_bag = self._parse_inventory(self, v, path=['candy_inventory_contents', 'data'])
        self.talisman_bag = self._parse_inventory(self, v, path=['talisman_bag', 'data'])
        self.potion_bag = self._parse_inventory(self, v, path=['potion_bag', 'data'])
        self.fish_bag = self._parse_inventory(self, v, path=['fishing_bag', 'data'])
        self.quiver = self._parse_inventory(self, v, path=['quiver', 'data'])
        wardrobe = self._parse_inventory(self, v, index_empty=True, path=['wardrobe_contents', 'data'])
        self.wardrobe = []
        for wardrobe_page in range(0, 2 * 36, 36):
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

        if self.inventory or self.echest or self.talisman_bag:
            self.enabled_api['inventory'] = True

        # Loads player's talismans
        self.talismans = [talisman for talisman in self.inventory + self.talisman_bag if
                          talisman.type in ('accessory', 'hatccessory')]

        self.talisman_counts = {'common': 0, 'uncommon': 0, 'rare': 0, 'epic': 0, 'legendary': 0, 'mythic': 0}
        talismans_dup = []

        for talisman in self.talismans:
            talisman.active = True
            # Check for duplicate talismans
            if self.talismans.count(talisman) > 1:
                talisman.active = False
                if not talisman in talismans_dup:
                    talismans_dup.append(talisman)
                continue

            # Check for talisman families
            if talisman.internal_name in tiered_talismans:
                for other in tiered_talismans[talisman.internal_name]:
                    if other in self.talismans:
                        talisman.active = False
                        break

        for talisman in talismans_dup:
            talisman.active = True

        for tali in self.talismans:
            if tali.active:
                try:
                    self.talisman_counts[tali.rarity] += 1
                except KeyError:
                    raise HypixelLanguageError from None

        # Loads a player's minion slots and collections
        try:
            self.collections = {name.lower().replace('_', ' '): level for name, level in v['collection'].items()}
            self.enabled_api['collection'] = True
        except KeyError:
            self.collections = {}

        self.unlocked_collections = Player._parse_collection(v, 'unlocked_coll_tiers')
        self.minions = Player._parse_collection(v, 'crafted_generators')

        self.unique_minions = max(
            self.achievements.get('skyblock_minion_lover', 0),
            sum(self.minions.values())
        )

        self.minion_slots = level_from_xp_table(self.unique_minions, minion_slot_requirements)

        # Loads a player's skill and slayer data
        if 'experience_skill_farming' in v:
            self.enabled_api['skills'] = True

            self.skill_xp = {}
            self.skills = {}

            for skill in skills:
                xp = int(v.get(f'experience_skill_{skill}', 0))
                self.skill_xp[skill] = xp
                self.skills[skill] = level_from_xp_table(
                    xp,
                    runecrafting_xp_requirements if skill == 'runecrafting' else skill_xp_requirements
                )
        else:
            self.enabled_api['skills'] = False

            self.skill_xp = {
                'carpentry': 0,
                'runecrafting': 0
            }
            self.skills = {
                'carpentry': 0,
                'runecrafting': 0
            }

            for skill, achievement in [
                ('farming', 'skyblock_harvester'),
                ('mining', 'skyblock_excavator'),
                ('foraging', 'skyblock_gatherer'),
                ('combat', 'skyblock_combat'),
                ('enchanting', 'skyblock_augmentation'),
                ('alchemy', 'skyblock_concoctor'),
                ('fishing', 'skyblock_angler'),
                ('taming', '')
            ]:
                level = self.achievements.get(achievement, 0)
                self.skills[skill] = level
                self.skill_xp[skill] = 0 if level == 0 else skill_xp_requirements[level - 1]

        self.skill_average = sum(self.skills[skill] for skill in skills if skill not in cosmetic_skills) / (
                len(skills) - len(cosmetic_skills))

        self.slayer_xp = {}
        self.slayers = {}
        for s in slayers:
            xp = v.get('slayer_bosses', {}).get(s, {}).get('xp', 0)
            self.slayer_xp[s] = xp
            self.slayers[s] = level_from_xp_table(xp, slayer_level_requirements[s])

        self.total_slayer_xp = sum(self.slayer_xp.values())

        # Loads a player's kills and deaths
        self.kills = int(v.get('stats', {'kills': 0}).get('kills', 0))
        self.specifc_kills = {name.replace('kills_', '').replace('_', ' '): int(amount)
                              for name, amount in v['stats'].items() if re.match('kills_', name)}
        self.deaths = int(v.get('stats', {'deaths': 0}).get('deaths', 0))
        self.specifc_deaths = {name.replace('deaths_', '').replace('_', ' '): int(amount)
                               for name, amount in v['stats'].items() if re.match('deaths_', name)}

        # Loads a player's bank balance and purse
        if 'banking' in self._nbt:
            self.enabled_api['banking'] = True
            self.bank_balance = float(self._nbt['banking'].get('balance', 0))
        else:
            self.bank_balance = 0

        self.purse = float(self._nbt['members'][self.uuid].get('coin_purse', 0))

        # Loads a player's misc stats
        self.join_date = datetime.fromtimestamp(v.get('first_join', 0) / 1000.0)
        self.fairy_souls = v.get('fairy_souls_collected', 0)

        for s, level in self.slayers.items():
            self.stats += Stats(slayer_rewards[s][level])

        for skill, level in self.skills.items():
            self.stats += Stats(skill_rewards[skill][level])

        self.stats.__iadd__('health', fairy_soul_hp_bonus[self.fairy_souls // 5])
        self.stats.__iadd__('defense', self.fairy_souls // 5 + self.fairy_souls // 25)
        self.stats.__iadd__('strength', self.fairy_souls // 5 + self.fairy_souls // 25)
        self.stats.__iadd__('speed', self.fairy_souls // 50)

        # Loads all of a player's pets
        self.pets = []
        if 'pets' in v:
            for data in v['pets']:
                pet = Pet(data)
                self.pets.append(pet)

    # noinspection PyAttributeOutsideInit
    def set_armor(self, armor=None):
        self.armor = armor

        if self.armor:
            self.stats.children.extend(
                [(p.type, p.stats) for p in self.armor.values() if p] + [(t.type, t.stats) for t in
                                                                         self.talismans if t.active])
            self.stats.base_children.extend([(p.type, p.base_stats) for p in self.armor.values() if p] \
                                            + [(t.type, t.base_stats) for t in self.talismans if t.active])

            # Set Bonuses
            if self.armor == {'helmet': 'SUPERIOR_DRAGON_HELMET', 'chestplate': 'SUPERIOR_DRAGON_CHESTPLATE',
                              'leggings': 'SUPERIOR_DRAGON_LEGGINGS', 'boots': 'SUPERIOR_DRAGON_BOOTS'}:
                self.stats.multiplier += 0.05
            # elif self.armor == {'helmet': 'YOUNG_HELMET', 'chestplate': 'YOUNG_CHESTPLATE', 'leggings': 'YOUNG_LEGGINGS', 'boots': 'YOUNG_BOOTS'}: #name maybe wrong check later
            # 	self.stats.__iadd__('speed cap', 100)
            # elif self.armor == {'helmet': 'MASTIFF_HELMET', 'chestplate': 'MASTIFF_CHESTPLATE', 'leggings': 'MASTIFF_LEGGINGS', 'boots': 'MASTIFF_BOOTS'}:
            # 	self.stats.modifiers['crit damage'].append(lambda stat: stat / 2)
            # 	self.stats.modifiers['health'].append(lambda stat: stat + self.stats['crit damage'] * 50)
            elif self.armor['helmet'] == 'TARANTULA_HELMET':
                self.stats.modifiers['crit damage'].insert(0, lambda stat: stat + self.stats['strength'] / 10)

    # noinspection PyAttributeOutsideInit
    def set_weapon(self, weapon=None):
        self.weapon = weapon

        if self.weapon:
            self.stats.children.append((self.weapon.type, self.weapon.stats))
            self.stats.base_children.append((self.weapon.type, self.weapon.base_stats))

    # noinspection PyAttributeOutsideInit
    def set_pet(self, pet=None):
        self.pet = pet

        if self.pet:
            self.stats.children.append((self.pet.internal_name, self.pet.stats))
            self.stats.base_children.append((self.pet.internal_name, self.pet.stats))

            pet_ability = pets[self.pet.internal_name]['ability']
            if callable(pet_ability):
                pet_ability(self)

    async def is_online(self):
        player_data = (await self.__call_api__('/status', self.session, uuid=self.uuid))['session']
        return player_data['online']

    async def auctions(self):
        r = await self.__call_api__('/skyblock/auction', self.session, uuid=self.uuid, profile=self.profile)

        return [
            {
                'item': decode_inventory_data(auction['item_bytes']['data'])[0],
                'start': auction['start'],
                'end': auction['end'],
                'starting_bid': auction['starting_bid'],
                'highest_bid': auction['highest_bid_amount'],
                'bids': auction['bids'],
                'buyer': auction['bids'][-1]['bidder'] if auction['bids'] else None
            }
            for auction in r['auctions']
            if auction['claimed'] is False
        ]

    @staticmethod
    async def _create_canadate(self, profile):
        player = await Player(
            self._api_keys,
            uname=self.uname,
            uuid=self.uuid,
            _profiles=self.profiles,
            _achivements=self.achievements,
            session=self.session
        )
        await player.set_profile(profile)
        return player

    # noinspection PyTypeChecker
    @staticmethod
    def _parse_collection(v, data):
        try:
            tuples = []
            for s in v[data]:
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

    @staticmethod
    def _parse_inventory(self, v, *, index_empty=False, path):
        try:
            result = v
            for key in path:
                result = result[key]
            return decode_inventory_data(result, self, index_empty=index_empty)
        except KeyError:
            return []
