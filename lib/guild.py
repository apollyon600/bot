from datetime import datetime


class Guild:
    def __init__(self, guild_data, player):
        self.guild_data = guild_data
        self.player = player

        self.id = guild_data.get('_id', None)
        self.name = guild_data.get('name', '')
        self.description = guild_data.get('description', '')
        self.xp = guild_data.get('exp', 0)
        self.tag = guild_data.get('tag', None)
        self.tag_color = guild_data.get('tagColor', None)
        self.created_at = datetime.fromtimestamp(guild_data.get('created', 0) / 1000.0)
        self.publicly_listed = guild_data.get('publiclyListed', False)
        self.owner = None

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
        self.members = []
        for member_data in guild_data.get('members', []):
            if member_data is None:
                continue
            self.members.append(GuildMember(member_data, self))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class GuildMember:
    def __init__(self, member_data, guild):
        self.member_data = member_data
        self.guild = guild

        self.uuid = member_data.get('uuid', None)
        self.joined_at = datetime.fromtimestamp(member_data.get('joined', 0) / 1000.0)

        # Load guild member's rank
        self.rank = member_data.get('rank', None)
        if self.rank is not None:
            for rank in guild.ranks:
                if rank.name.lower() == self.rank.lower():
                    self.rank = rank
                    if rank.name.lower() == 'guild master':
                        self.owner = self
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
