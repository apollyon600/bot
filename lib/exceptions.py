from discord.ext.commands import UserInputError


class SkyblockCommandError(UserInputError):
    """
    The base exception type for errors regarding user wrong skyblock-related input.
    """
    pass


class BadNameError(SkyblockCommandError):
    """
    Exception raised when a user enters invalid player name/uuid.
    """

    def __init__(self, uname_or_uuid):
        self.uname = uname_or_uuid


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

    def __str__(self):
        return self.reason


class ExternalAPIError(APIError):
    """
    Exception raised when something is wrong while calling API.
    """

    def __init__(self, reason=''):
        self.reason = reason


class HypixelAPIError(APIError):
    """
    Exception raised when something is wrong while calling Hypixel API.
    """

    def __init__(self, reason=''):
        self.reason = reason


class APIKeyError(APIError):
    """
    Exception raised when the API key is invalid.
    """

    def __init__(self, key, reason=''):
        self.key = key
        self.reason = reason

    def __str__(self):
        return f'{self.reason}: {self.key}'
