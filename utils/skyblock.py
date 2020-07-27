from discord.ext import commands

from lib import Player
from constants import relavant_enchants, enchantment_effects
from constants.discord import timeout_emoji


class PlayerConverter(commands.Converter):
    async def convert(self, ctx, arg):
        api_keys = ctx.bot.config.keys
        return await Player(api_keys, uname=arg, session=ctx.bot.session)


def colorize(s, color):
    language, point = color
    s = str(s)
    if not s:
        return ''
    return f'```{language}\n{point}' + s.replace('\n', f'\n{point}') + '\n```'


def format_pet(pet):
    return f'{pet.title} |{pet.rarity.upper()}|' if pet else ''


async def embed_timeout_handler(ctx, emoji_list, message=None):
    message = message or ctx.message
    try:
        for (emoji, _) in emoji_list:
            await message.remove_reaction(emoji, ctx.bot.user)
        for emoji in timeout_emoji:
            await message.add_reaction(emoji)
    except:
        pass


def emod(activity, weapon):
    result = 0
    for enchantment in relavant_enchants[activity]:
        if enchantment in weapon.enchantments:
            value = enchantment_effects[enchantment]
            if callable(value):
                result += value(weapon.enchantments[enchantment])
            else:
                result += value * weapon.enchantments[enchantment]
    return result
