from datetime import datetime

from . import Profile
from . import NeverPlayedSkyblockError, BadProfileError, BadNameError


class Player:
    def __init__(self, *, uname, uuid, player_data, hypixel_api_client):
        self.hypixel_api_client = hypixel_api_client
        self.uname = uname
        self.uuid = uuid
        if not player_data:
            raise BadNameError(self.uname)
        self.player_data = player_data
        self.online = player_data.get('lastLogout', 0) < player_data.get('lastLogin', 0)
        self.achievements = player_data.get('achievements', {})

        self.profiles = []
        self.profile = None

        self.guild = None

    def __str__(self):
        return self.uname

    async def get_set_skyblock_profiles(self, *, selected_profile='', **kwargs):
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
                profile=profile_data
            )
            self.profiles.append(profile)
            if selected_profile.lower() == profile.profile_name:
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
        # call hypixel guild endpoint using player uuid.
        raise NotImplementedError
