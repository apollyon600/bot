import asyncio
import discord
from discord.ext import commands

from lib.exceptions import *


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            await self.handle_user_input_error(ctx, error)
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f'{ctx.author.mention}, This command is on cooldown for you! Please try again after {error.retry_after:.2f}s.')
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send(
                f'{ctx.author.mention}, Someone is already using this command in this channel! Please try again later or DM me directly.')
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(f'{ctx.author.mention}, Did you make a typo? There is no command: `{ctx.invoked_with}`.')
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.author.mention}, This command: `{ctx.invoked_with}` is currently disabled.')
        elif isinstance(error, commands.CheckFailure):
            await self.handle_check_failure(ctx, error)
        elif isinstance(error, (commands.CommandInvokeError, commands.ConversionError)):
            ctx.command.reset_cooldown(ctx)
            original = error.original
            if isinstance(original, discord.errors.Forbidden):
                try:
                    await ctx.send(
                        f'{ctx.author.mention}, Sorry, it looks like I don\'t have the permissions or roles to do that.\n'
                        f'Try enabling your DMS or contract the server owner to give me more permissions.')
                except:
                    # in case the server disable bot's message permission
                    pass
            elif isinstance(original, (asyncio.TimeoutError, SessionTimeout)):
                await ctx.send(f'{ctx.author.mention}, Session closed!')
            elif isinstance(original, APIError):
                await self.handle_api_error(ctx, original)
            else:
                await self.handle_unexpected_error(ctx, original)
        else:
            ctx.command.reset_cooldown(ctx)
            await self.handle_unexpected_error(ctx, error)

    @staticmethod
    async def send_default_error_message(ctx: commands.Context):
        await ctx.send(f'{ctx.author.mention}, Something went wrong while running your command.\n'
                       'The error has been automatically reported to SBS devs.')

    @staticmethod
    async def get_help_command(ctx: commands.Context):
        if ctx.command:
            await ctx.send_help(ctx.command)
        else:
            await ctx.send_help()

    async def handle_user_input_error(self, ctx: commands.Context, error: commands.UserInputError):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'{ctx.author.mention}, This command requires arguments: `{error.param.name}`.')
            await self.get_help_command(ctx)
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send(f'{ctx.author.mention}, You provided too many arugments for this command.')
            await self.get_help_command(ctx)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                f'{ctx.author.mention}, Bad argument: Please double-check your input arguments and try again.')
            await self.get_help_command(ctx)
        elif isinstance(error, commands.BadUnionArgument):
            await ctx.send(f'{ctx.author.mention}, Bad argument: {error}\n```{error.errors[-1]}```')
            await self.get_help_command(ctx)
        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(f'{ctx.author.mention}, Argument parsing error: {error}.')
            await self.get_help_command(ctx)
        elif isinstance(error, SkyblockCommandError):
            await self.handle_skyblock_input_error(ctx, error)
        else:
            await ctx.send("Something about your input seems off. Please check the command usage.")
            await self.get_help_command(ctx)

    @staticmethod
    async def handle_check_failure(ctx: commands.Context, error: commands.CheckFailure):
        bot_missing_errors = (
            commands.BotMissingPermissions,
            commands.BotMissingRole,
            commands.BotMissingAnyRole
        )

        user_missing_errors = (
            commands.CheckAnyFailure,
            commands.NotOwner,
            commands.MissingPermissions,
            commands.MissingRole,
            commands.MissingAnyRole,
        )

        if isinstance(error, bot_missing_errors):
            await ctx.send(
                f'{ctx.author.mention}, Sorry, it looks like I don\'t have the permissions or roles to do that.\n'
                f'Try enabling your DM or contract the server owner to give me more permissions.')
        elif isinstance(error, user_missing_errors):
            await ctx.send(
                f'{ctx.author.mention}, Sorry, it looks like you don\'t have the permissions or roles to use this command.')
        else:
            # other unimplemented check exceptions
            pass

    async def handle_unexpected_error(self, ctx: commands.Context, error):
        await self.send_default_error_message(ctx)
        raise error from None

    async def handle_api_error(self, ctx: commands.Context, error: APIError):
        if isinstance(error, ExternalAPIError):
            await ctx.send(f'{ctx.author.mention}, {error}')
        elif isinstance(error, HypixelAPIError):
            await ctx.send(f'{ctx.author.mention}, Something went wrong while calling Hypixel API.\n'
                           f'This error usually goes away after about a minute. If not then Hypixel API is down.')
        else:
            await self.handle_unexpected_error(ctx, error)

    @staticmethod
    async def handle_skyblock_input_error(ctx: commands.Context, error: SkyblockCommandError):
        if isinstance(error, BadNameError):
            await ctx.send(f'{ctx.author.mention}, Invalid player\'s name/uuid: {error.uname}.')
        elif isinstance(error, BadProfileError):
            await ctx.send(f'{ctx.author.mention}, Invalid profile\'s name: {error.profile_name}.')
        elif isinstance(error, NeverPlayedSkyblockError):
            await ctx.send(f'{ctx.author.mention}, This player {error.uname} has never played skyblock before.')
        elif isinstance(error, APIDisabledError):
            await ctx.send(
                f'{ctx.author.mention}, This player {error.uname} has disabled API on profile {error.profile_name}.\n'
                f'Please re-enable them with [skyblock menu > settings > api settings].')
        elif isinstance(error, BadGuildError):
            await ctx.send(f'{ctx.author.mention}, Invalid guild\'s name: {error.guild_name}.')


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
