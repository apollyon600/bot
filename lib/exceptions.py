from discord.ext.commands import UserInputError


class SkyblockCommandError(UserInputError):
    pass


class BadNameError(SkyblockCommandError):
    """This uuid or username is invalid"""

    def __init__(self, uname_or_uuid, reason='', *args):
        if not reason:
            super().__init__(f'Invalid player\'s name/uuid: {uname_or_uuid}', *args)
        else:
            super().__init__(f'{reason}: {uname_or_uuid}', *args)


class NeverPlayedSkyblockError(SkyblockCommandError):
    """This user has never played skyblock before"""

    def __init__(self, uname_or_uuid, *args):
        super().__init__(f'This player {uname_or_uuid} has never played skyblock before.', *args)


class BadGuildError(SkyblockCommandError):
    """This guild name is invalid"""

    def __init__(self, guild, *args):
        super().__init__(f'Invalid guild\'s name: {guild}', *args)


class SkyblockLibError(Exception):
    """A general exception from the skyblock library"""

    def __str__(self):
        return self.reason


class DataError(SkyblockLibError):
    """You entered wrong data"""

    def __init__(self, reason=''):
        self.reason = reason


class APIError(Exception):
    """A general exception from the skyblock library"""

    def __str__(self):
        return self.reason

class ExternalAPIError(APIError):
    """There was an issue connecting to the API"""

    def __init__(self, reason=''):
        self.reason = reason


class HypixelAPIError(APIError):
    """The Hypixel API had some error"""

    def __init__(self, reason=''):
        self.reason = reason


class APIKeyError(APIError):
    """You used an invalid API key"""

    def __init__(self, key, reason=''):
        self.key = key
        self.reason = reason

    def __str__(self):
        return f'{self.reason}: {self.key}'
