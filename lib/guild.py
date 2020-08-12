import asyncio
from datetime import datetime
import copy

from lib import NeverPlayedSkyblockError
from constants import GUILD_LEVEL_REQUIREMENT


class Guild:
    def __init__(self, guild_data, player=None):
        self.guild_data = guild_data
        self.player = player
        self.hypixel_api_client = None

        self.id = guild_data.get('_id', None)
        self.name = guild_data.get('name', '')
        self.description = guild_data.get('description', '')
        self.xp = guild_data.get('exp', 0)
        self.tag = guild_data.get('tag', None)
        self.tag_color = guild_data.get('tagColor', None)
        self.created_at = datetime.fromtimestamp(guild_data.get('created', 0) / 1000.0)
        self.publicly_listed = guild_data.get('publiclyListed', False)
        self.owner = None

        # Calc guild lvl
        xp = self.xp
        for level, requirement in enumerate(GUILD_LEVEL_REQUIREMENT):
            if xp >= requirement:
                xp -= requirement
            else:
                break
        # noinspection PyUnboundLocalVariable
        level += xp // GUILD_LEVEL_REQUIREMENT[-1]
        self.level = level

        # Load guild ranks
        self.rank_amount = len(guild_data.get('ranks', []))
        self.ranks = []
        max_priority = 0
        for rank_data in guild_data.get('ranks', []):
            if rank_data is None:
                continue
            guild_rank = GuildRank(rank_data, self)
            if guild_rank.priority > max_priority:
                max_priority = guild_rank.priority
            self.ranks.append(GuildRank(rank_data, self))
        # Add guild master rank
        self.ranks.append(GuildRank({
            'name': 'Guild Master',
            'created': guild_data.get('created', 0),
            'priority': max_priority + 1
        }, self))

        # Load guild members
        self.member_amount = len(guild_data.get('members', []))
        self.guild_members = []
        for member_data in guild_data.get('members', []):
            if member_data is None:
                continue
            self.guild_members.append(GuildMember(member_data, self))

        # Guild stats
        self.achievements = guild_data.get('achievements', {})
        self.max_online_members = self.achievements.get('ONLINE_PLAYERS', 0)
        self.current_online = 0

        self.average_deaths = 0
        self.average_money = 0
        self.average_skills = 0
        self.minion_slot = 0
        self.unique_minions = 0
        self.skills = {}
        self.skills_xp = {}
        self.slayers = {}
        self.slayers_xp = {}

        self.all_members_skill_average = {}
        self.all_members_unique_minions = {}
        self.all_members_minion_slots = {}
        self.all_members_skills = {}
        self.all_members_skills_xp = {}
        self.all_members_slayers = {}
        self.all_members_slayers_xp = {}
        self.all_members_total_slayers_xp = {}
        self.all_members_dungeon_level = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    async def load_all_members(self, *, hypixel_api_client):
        self.hypixel_api_client = hypixel_api_client

        await asyncio.gather(
            *[self.load_member_data(member, hypixel_api_client=hypixel_api_client) for member in self.guild_members])

        self.load_skyblock_stats()

    async def load_member_data(self, member, *, hypixel_api_client):
        if member.uuid is None:
            return

        member.player = await hypixel_api_client.get_player(member.uuid, guild=self)
        try:
            await member.player.load_skyblock_profiles(load_all=False)
        except NeverPlayedSkyblockError:
            pass

    def load_skyblock_stats(self):
        total_deaths = 0
        total_money = 0
        total_average_skills = 0.00
        total_minion_slots = 0
        total_unique_minions = 0

        total_skills = {'farming': 0, 'mining': 0, 'combat': 0, 'foraging': 0, 'fishing': 0, 'enchanting': 0,
                        'alchemy': 0, 'taming': 0, 'carpentry': 0, 'runecrafting': 0}
        total_skills_xp = {'farming': 0, 'mining': 0, 'combat': 0, 'foraging': 0, 'fishing': 0, 'enchanting': 0,
                           'alchemy': 0, 'taming': 0, 'carpentry': 0, 'runecrafting': 0}

        total_slayers = {'zombie': 0, 'spider': 0, 'wolf': 0}
        total_slayers_xp = {'zombie': 0, 'spider': 0, 'wolf': 0}
        for member in self.guild_members:
            player = member.player
            profile = player.profile
            if profile is None:
                continue  # for those guild member doesn't player skyblock

            self.all_members_skill_average.update({player.uname: profile.skill_average})
            self.all_members_unique_minions.update({player.uname: profile.unique_minions})
            self.all_members_minion_slots.update({player.uname: profile.minion_slots})
            self.all_members_skills.update({player.uname: profile.skills.copy()})
            self.all_members_skills_xp.update({player.uname: profile.skills_xp.copy()})
            self.all_members_slayers.update({player.uname: copy.deepcopy(profile.slayers)})
            self.all_members_slayers_xp.update({player.uname: copy.deepcopy(profile.slayers_xp)})
            self.all_members_total_slayers_xp.update({player.uname: profile.total_slayer_xp})
            self.all_members_dungeon_level.update({player.uname: profile.dungeon_skill})

            self.current_online += player.online
            total_deaths += profile.deaths
            total_money += profile.bank_balance + profile.purse
            total_average_skills += profile.skill_average
            total_minion_slots += profile.minion_slots
            total_unique_minions += profile.unique_minions

            for skill in total_skills.keys():
                total_skills[skill] += profile.skills.get(skill, 0)
                total_skills_xp[skill] += profile.skills_xp.get(skill, 0)

            for slayer in total_slayers.keys():
                total_slayers[slayer] += profile.slayers.get(slayer, 0)
                total_slayers_xp[slayer] += profile.slayers_xp.get(slayer, 0)

        self.average_deaths = total_deaths // self.member_amount
        self.average_money = total_money / self.member_amount
        self.average_skills = total_average_skills / self.member_amount
        self.minion_slot = total_minion_slots // self.member_amount
        self.unique_minions = total_unique_minions // self.member_amount

        for skill in total_skills.keys():
            self.skills[skill] = total_skills[skill] // self.member_amount
            self.skills_xp[skill] = total_skills_xp[skill] / self.member_amount

        for slayer in total_slayers.keys():
            self.slayers[slayer] = total_slayers[slayer] // self.member_amount
            self.slayers_xp[slayer] = total_slayers_xp[slayer] / self.member_amount


class GuildMember:
    def __init__(self, member_data, guild):
        self.member_data = member_data
        self.guild = guild
        self.player = None

        self.uuid = member_data.get('uuid', None)
        self.joined_at = datetime.fromtimestamp(member_data.get('joined', 0) / 1000.0)

        # Load guild member's rank
        self.rank = member_data.get('rank', None)
        if self.rank is not None:
            for rank in guild.ranks:
                if rank.name.lower() == self.rank.lower():
                    self.rank = rank
                    if rank.name.lower() == 'guild master':
                        self.guild.owner = self
                    break

        self.quest_completed = member_data.get('questParticipation', 0)
        self.xp_history = member_data.get('expHistory', {})

    def __str__(self):
        return self.uuid

    def __repr__(self):
        return self.uuid


class GuildRank:
    def __init__(self, rank_data, guild):
        self.rank_data = rank_data
        self.guild = guild

        self.name = rank_data.get('name', '')
        self.default = rank_data.get('default', False)
        self.tag = rank_data.get('tag', None)
        self.created_at = datetime.fromtimestamp(rank_data.get('created', 0) / 1000.0)
        self.priority = rank_data.get('priority', 0)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
