import aiohttp
from typing import Optional
from discord.ext.commands import UserInputError, CheckFailure


class SkyblockCommandError(UserInputError):
    """
    The base exception type for errors regarding user wrong skyblock-related input.
    """
    pass


class BadNameError(SkyblockCommandError):
    """
    Exception raised when a user enters invalid player name.
    """

    def __init__(self, uname):
        self.uname = uname


class BadProfileError(SkyblockCommandError):
    """
    Exception raised when a user enters invalid profile name.
    """

    def __init__(self, profile_name):
        self.profile_name = profile_name


class NeverPlayedSkyblockError(SkyblockCommandError):
    """
    Exception raised when a user enters a player name/uuid that has never played skyblock before.
    """

    def __init__(self, uname_or_uuid):
        self.uname = uname_or_uuid


class APIDisabledError(SkyblockCommandError):
    """
    Exception raised when a user enters a player name/uuid that has their api disabled.
    """

    def __init__(self, uname_or_uuid, profile_name):
        self.uname = uname_or_uuid
        self.profile_name = profile_name


class BadGuildError(SkyblockCommandError):
    """
    Exception raised when a user enters invalid guild name.
    """

    def __init__(self, guild_name):
        self.guild_name = guild_name


class PlayerOnlineError(SkyblockCommandError):
    """
    Exception raised when the player is online in hypixel.
    """
    pass


class NoArmorError(SkyblockCommandError):
    """
    Exception raised when the player doesn't have any armors
    """
    pass


class NoWeaponError(SkyblockCommandError):
    """
    Exception raised when the player doesn't have any weapon
    """
    pass


class HypixelLanguageError(SkyblockCommandError):
    """
    Exception raised when the player's hypixel language is not english.
    """
    pass


class NotStaff(CheckFailure):
    """
    Exception raised when the user is not a sbs staff.
    """
    pass


class SessionTimeout(Exception):
    """
    Exception raised when the current message session timed out.
    """
    pass


class SkyblockLibError(Exception):
    """
    The base exception type for errors regarding skyblock library.
    """

    def __str__(self):
        return self.reason


class DataError(SkyblockLibError):
    """
    Exception raised when something is wrong while processing the data.
    """

    def __init__(self, reason=''):
        self.reason = reason


class APIError(Exception):
    """
    The base exception type for errors regarding API.
    """


class ExternalAPIError(APIError):
    """
    Exception raised when something is wrong while calling API.
    """

    def __init__(self, reason=''):
        self.reason = reason

    def __str__(self):
        return self.reason


class HypixelAPIRateLimitError(APIError):
    """
    Exception raised when hypixel api ratelimit is reached.
    """
    pass


class HypixelAPINoSuccess(APIError):
    """
    Exception raised when hypixel api return not success.
    """
    pass


class HypixelAPITimeout(APIError):
    """
    Exception raised when hypixel api request timed out.
    """
    pass


class HypixelResponseCodeError(APIError):
    """
    Exception raised when a non-OK HTTP response from hypixel is received.
    """

    def __init__(
            self,
            response: aiohttp.ClientResponse,
            response_json: Optional[dict] = None,
            response_text: str = ""
    ):
        self.status = response.status
        self.response_json = response_json or {}
        self.response_text = response_text
        self.response = response

    def __str__(self):
        response = self.response_json if self.response_json else self.response_text
        return f"Status: {self.status} Response: {response}"


class APIKeyError(APIError):
    """
    Exception raised when the API key is invalid.
    """

    def __init__(self, key, reason=''):
        self.key = key
        self.reason = reason

    def __str__(self):
        return f'{self.reason}: {self.key}'
