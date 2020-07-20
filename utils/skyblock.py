from discord.ext import commands

from lib import Player


class PlayerConverter(commands.Converter):
    async def convert(self, ctx, arg):
        api_keys = ctx.bot.config.keys
        return await Player(api_keys, uname=arg)


def colorize(s, color):
    language, point = color
    s = str(s)

    if s:
        return f'```{language}\n{point}' + s.replace('\n', f'\n{point}') + '\n```'
    else:
        return ''


def format_pet(pet):
    """Returns a pretty string repersenting a pet"""
    return f'{pet.title} |{pet.rarity.upper()}|' if pet else ''
