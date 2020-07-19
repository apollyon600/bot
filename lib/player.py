import asyncio
from datetime import datetime

from . import Pet, Stats, HypixelApiInterface, HypixelAPIError, DataError, NeverPlayedSkyblockError, \
    decode_inventory_data, fetch_uuid_uname, level_from_xp_table
from constants import *


# noinspection PyUnusedLocal
class Player(HypixelApiInterface):
    """
    A class representing a Skyblock player.
    Instantiate the class with Player(api_key, username) or Player(api_key, uuid)
    Use set_profile() to define the profile data.
    Use set_weapon() to set the player's weapon.
    """

    async def __init__(self, api_keys, *, uname=None, uuid=None, guild=False, _profiles=None, _achivements=None):
        if uname and uuid:
            self.uname = uname
            self.uuid = uuid
        elif uname and not uuid:
            self.uname, self.uuid = await fetch_uuid_uname(uname)
        elif uuid and not uname:
            self.uname, self.uuid = await fetch_uuid_uname(uuid)
        else:
            raise DataError('You need to provide either a minecraft username or uuid!')
        self.online = False

        if _profiles and _achivements:
            self.profiles = _profiles
            self.achievements = _achivements
        else:
            try:
                self.profiles = {}
                player = await self.__call_api__('/player', uuid=self.uuid)
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
            guild_id = (await self.__call_api__('/findGuild', byUuid=self.uuid))['guild']
            if guild_id:
                self.guild_id = guild_id
                self.guild_info = (await self.__call_api__('/guild', id=self.guild_id))['guild']
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

    async def set_profile_automatically(self, attribute=lambda player: player.total_slayer_xp, threshold=None):
        """
        Sets a player profile automatically
        <attribute> is a function that takes a <Player> class and returns whatever value you want to set it based on
        example: player.set_profile_automatically(lambda player: player.skill_xp['combat'])
        """
        best = None
        max_value = 0

        profile_ids = list(self.profiles.values())

        if threshold:
            best = profile_ids[0]
            for profile in reversed(profile_ids):
                try:
                    canidate = await self._create_canadate(self, profile)
                except HypixelAPIError:
                    continue

                if attribute(canidate) >= threshold:
                    best = profile
                    break
        else:
            for canidate in asyncio.as_completed([self._create_canadate(self, profile) for profile in profile_ids]):
                try:
                    canidate = await canidate
                    current = attribute(canidate)
                    if best is None or current > max_value:
                        max_value = current
                        best = canidate.profile
                except HypixelAPIError:
                    pass

        await self.set_profile(best)

    # noinspection PyAttributeOutsideInit
    async def set_profile(self, profile):
        """
        Sets a player's profile based on the provided profile ID
        """

        if self._profile_set:
            raise DataError('This player already has their profile set!')
        self._profile_set = True

        self.profile = profile
        for cute_name, profile_id in self.profiles.items():
            if profile_id == profile:
                self.profile_name = cute_name
                break
        else:
            raise DataError('Bad profile ID!')

        # Get player's inventories nbt data
        self._nbt = (await self.__call_api__('/skyblock/profile', profile=self.profile))['profile']
        if not self._nbt:
            raise DataError('Something\'s wrong with player\'s items nbt data')
        v = self._nbt['members'][self.uuid]

        self.enabled_api = {'skills': False, 'collection': False, 'inventory': False, 'banking': False}
        self.armor = {'helmet': None, 'chestplate': None, 'leggings': None, 'boots': None}

        # Loads a player's numeric stats
        self.stats = Stats(base_player_stats.copy())

        # Check for special armor type
        for armor in self._parse_inventory(self, v, 'inv_armor', 'data'):
            if armor.type == 'hatccessory':
                self.armor['helmet'] = armor
            else:
                self.armor[armor.type] = armor

        # Loads all of a player's inventories
        self.inventory = self._parse_inventory(self, v, 'inv_contents', 'data')
        self.echest = self._parse_inventory(self, v, 'ender_chest_contents', 'data')
        self.weapons = [item for item in self.inventory + self.echest if item.type in ('sword', 'bow', 'fishing rod')]
        self.candy_bag = self._parse_inventory(self, v, 'candy_inventory_contents', 'data')
        self.talisman_bag = self._parse_inventory(self, v, 'talisman_bag', 'data')
        self.potion_bag = self._parse_inventory(self, v, 'potion_bag', 'data')
        self.fish_bag = self._parse_inventory(self, v, 'fishing_bag', 'data')
        self.quiver = self._parse_inventory(self, v, 'quiver', 'data')
        self.wardrobe = self._parse_inventory(self, v, 'wardrobe_contents', 'data')

        if self.inventory or self.echest or self.talisman_bag:
            self.enabled_api['inventory'] = True

        self.talismans = [talisman for talisman in self.inventory + self.talisman_bag if
                          talisman.type in ('accessory', 'hatccessory')]

        for talisman in self.talismans:
            talisman.active = True
            # Check for duplicate talismans
            if self.talismans.count(talisman) > 1:
                talisman.active = False
                continue

            # Check for talisman families
            if talisman.internal_name in tiered_talismans:
                for other in tiered_talismans[talisman.internal_name]:
                    if other in self.talismans:
                        talisman.active = False
                        break

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

        self.stats.children = [(p.type, p.stats) for p in self.armor.values() if p] + [(t.type, t.stats) for t in
                                                                                       self.talismans if t.active]
        self.stats.base_children = [(p.type, p.base_stats) for p in self.armor.values() if p] \
                                   + [(t.type, t.base_stats) for t in self.talismans if t.active]

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

        # Loads all of a player's pets
        self.pets = []
        self.pet = None
        if 'pets' in v:
            for data in v['pets']:
                pet = Pet(data)
                self.pets.append(pet)
                if pet.active:
                    self.pet = pet

        if self.pet:
            self.stats.children.append((self.pet.internal_name, self.pet.stats))
            self.stats.base_children.append((self.pet.internal_name, self.pet.stats))

    # noinspection PyAttributeOutsideInit
    def set_weapon(self, weapon):
        self.weapon = weapon
        self.stats.children.append((weapon.type, weapon.stats))
        self.stats.base_children.append((weapon.type, weapon.base_stats))

        if self.pet:
            pet_ability = pets[self.pet.internal_name]['ability']
            if callable(pet_ability):
                pet_ability(self)

    async def is_online(self):
        player_data = (await self.__call_api__('/status', uuid=self.uuid))['session']
        return player_data['online']

    async def auctions(self):
        r = await self.__call_api__('/skyblock/auction', uuid=self.uuid, profile=self.profile)

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
            _achivements=self.achievements
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
    def _parse_inventory(self, v, *path):
        try:
            result = v
            for key in path:
                result = result[key]
            return decode_inventory_data(result, self)
        except KeyError:
            return []
