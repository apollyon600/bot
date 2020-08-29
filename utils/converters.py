from discord.ext import commands
import re


class UserConverterSafe(commands.UserConverter):
    """
    Modified User Converter so it's return the ID (if the argument is user ID) if it can't find.
    """

    async def convert(self, ctx, argument):
        try:
            return await super().convert(ctx, argument)
        except commands.BadArgument as e:
            match = self._get_id_match(argument) or re.match(r'<@!?([0-9]+)>$', argument)
            if match is not None:
                return int(match.group(1))
            else:
                raise e
