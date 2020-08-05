from datetime import datetime

from . import Profile, Guild
from . import NeverPlayedSkyblockError, BadProfileError, BadNameError


class Player:
    def __init__(self, *, uname=None, uuid, player_data, hypixel_api_client, guild=None):
        self.hypixel_api_client = hypixel_api_client
        self.uname = uname
        self.uuid = uuid
        if not player_data:
            raise BadNameError(self.uname)
        self.player_data = player_data
        self.online = player_data.get('lastLogout', 0) < player_data.get('lastLogin', 0)
        self.achievements = player_data.get('achievements', {})
        if self.uname is None:
            self.uname = player_data.get('playername', '')

        self.profiles = []
        self.profile = None

        self.guild = guild

    def __str__(self):
        return self.uname

    async def load_skyblock_profiles(self, *, selected_profile='', load_all=True, **kwargs):
        """
        Get player's skyblock profiles and set the selected profile, if not it will set the last save profile.
        """
        profiles = await self.hypixel_api_client.get_skyblock_profiles(self.uuid, **kwargs)

        if not profiles:
            raise NeverPlayedSkyblockError(self.uname)

        latest_profile = None
        latest_logout = datetime.fromtimestamp(0)
        for profile_data in profiles:
            profile = Profile(
                player=self,
                raw_profile_data=profile_data,
                load_all=load_all
            )
            self.profiles.append(profile)
            if selected_profile.lower() == profile.name:
                self.profile = profile
            if profile.last_save > latest_logout:
                latest_logout = profile.last_save
                latest_profile = profile

        if selected_profile and self.profile is None:
            raise BadProfileError(selected_profile)
        elif not selected_profile:
            self.profile = latest_profile

    async def get_player_guild(self):
        """
        Get player's guild data
        """
        if self.guild is None:
            guild_data = await self.hypixel_api_client.get_guild(params={'player': self.uuid})
            if guild_data is not None:
                self.guild = Guild(guild_data, self)

    def get_avatar_url(self, *, size=None):
        if size:
            return f'https://mc-heads.net/avatar/{self.uuid}/{size}'
        else:
            return f'https://mc-heads.net/avatar/{self.uuid}'
