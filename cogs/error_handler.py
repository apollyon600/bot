import asyncio
import discord
from discord.ext import commands

from lib.exceptions import *
from utils import Embed


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            await self.handle_user_input_error(ctx, error)
        elif isinstance(error, commands.CommandOnCooldown):
            await CommandErrorEmbed(
                ctx,
                description=f'This command is on cooldown for you! Please try again in {error.retry_after:.2f}s.'
            ).send()
        elif isinstance(error, commands.MaxConcurrencyReached):
            await CommandErrorEmbed(
                ctx,
                description='Someone is already using this command in this channel! Please try again later or DM me directly.'
            ).send()
        elif isinstance(error, commands.CommandNotFound):
            await CommandErrorEmbed(
                ctx,
                description=f'Did you make a typo? There is no command: `{ctx.invoked_with}`.'
            ).send()
        elif isinstance(error, commands.DisabledCommand):
            await CommandErrorEmbed(
                ctx,
                description=f'This command: `{ctx.invoked_with}` is currently disabled.'
            ).send()
        elif isinstance(error, commands.CheckFailure):
            await self.handle_check_failure(ctx, error)
        elif isinstance(error, (commands.CommandInvokeError, commands.ConversionError)):
            ctx.command.reset_cooldown(ctx)
            original = error.original
            if isinstance(original, discord.errors.Forbidden):
                try:
                    await CommandErrorEmbed(
                        ctx,
                        description=f'Sorry, it looks like I don\'t have the permissions or roles to do that.\n'
                                    f'Try enabling your DMS or contact the server owner to give me more permissions.'
                    ).send()
                except:
                    # in case the server disable bot's message permission
                    pass
            elif isinstance(original, (asyncio.TimeoutError, SessionTimeout)):
                await ctx.send(f'{ctx.author.mention}\nSession closed!')
            elif isinstance(original, APIError):
                await self.handle_api_error(ctx, original)
            else:
                await self.handle_unexpected_error(ctx, original)
        else:
            ctx.command.reset_cooldown(ctx)
            await self.handle_unexpected_error(ctx, error)

    @staticmethod
    async def send_default_error_message(ctx: commands.Context):
        await CommandErrorEmbed(
            ctx,
            description='Something went wrong while running your command.\n'
                        'The error has been automatically reported to SBS devs.'
        ).send()

    @staticmethod
    async def get_help_command(ctx: commands.Context):
        if ctx.command:
            await ctx.send_help(ctx.command)
        else:
            await ctx.send_help()

    async def handle_user_input_error(self, ctx: commands.Context, error: commands.UserInputError):
        if isinstance(error, commands.MissingRequiredArgument):
            await CommandErrorEmbed(
                ctx,
                description=f'This command requires arguments: `{error.param.name}`.'
            ).send()
            await self.get_help_command(ctx)
        elif isinstance(error, commands.TooManyArguments):
            await CommandErrorEmbed(
                ctx,
                description='You provided too many arugments for this command.'
            ).send()
            await self.get_help_command(ctx)
        elif isinstance(error, commands.BadArgument):
            await CommandErrorEmbed(
                ctx,
                description='Bad argument: Please double-check your input arguments and try again.'
            ).send()
            await self.get_help_command(ctx)
        elif isinstance(error, commands.BadUnionArgument):
            await CommandErrorEmbed(
                ctx,
                description=f'Bad argument: {error}\n```{error.errors[-1]}```'
            ).send()
            await self.get_help_command(ctx)
        elif isinstance(error, commands.ArgumentParsingError):
            await CommandErrorEmbed(
                ctx,
                description=f'Argument parsing error: {error}.'
            ).send()
            await self.get_help_command(ctx)
        elif isinstance(error, SkyblockCommandError):
            await self.handle_skyblock_input_error(ctx, error)

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
            await CommandErrorEmbed(
                ctx,
                description='Sorry, it looks like I don\'t have the permissions or roles to do that.\n'
                            'Try enabling your DM or contact the server owner to give me more permissions.'
            ).send()
        elif isinstance(error, user_missing_errors):
            await CommandErrorEmbed(
                ctx,
                description='Sorry, it looks like you don\'t have the permissions or roles to use this command.'
            ).send()
        elif isinstance(error, commands.NoPrivateMessage):
            await CommandErrorEmbed(
                ctx,
                description='You can\'t use this command in DM! Please try again it again in a server.'
            ).send()
        elif isinstance(error, NotVerified):
            await CommandErrorEmbed(
                ctx,
                description='You need to be verified to use this command.\nVerify yourself by using command `sbs verify`.'
            ).send()
        else:
            # other unimplemented check exceptions
            raise error

    async def handle_unexpected_error(self, ctx: commands.Context, error):
        await self.send_default_error_message(ctx)
        raise error from None

    async def handle_api_error(self, ctx: commands.Context, error: APIError):
        if isinstance(error, ExternalAPIError):
            await CommandErrorEmbed(
                ctx,
                description=f'{error}'
            ).send()
        elif isinstance(error, HypixelAPIRateLimitError):
            await CommandErrorEmbed(
                ctx,
                description='Hypixel API ratelimit has been reached!'
            ).send()
        elif isinstance(error, (HypixelAPINoSuccess, HypixelAPITimeout, HypixelResponseCodeError)):
            await CommandErrorEmbed(
                ctx,
                description='Something went wrong while calling Hypixel API.\n'
                            'This error usually goes away after about a minute. If not then Hypixel API is down.'
            ).send()
            if isinstance(error, HypixelResponseCodeError):
                raise error from None
        else:
            await self.handle_unexpected_error(ctx, error)

    @staticmethod
    async def handle_skyblock_input_error(ctx: commands.Context, error: SkyblockCommandError):
        ctx.command.reset_cooldown(ctx)
        if isinstance(error, BadNameError):
            await CommandErrorEmbed(
                ctx,
                description=f'Invalid player\'s name: {error.uname}.'
            ).send()
        elif isinstance(error, BadProfileError):
            await CommandErrorEmbed(
                ctx,
                description=f'Invalid profile\'s name: {error.profile_name}.'
            ).send()
        elif isinstance(error, NeverPlayedSkyblockError):
            await CommandErrorEmbed(
                ctx,
                description=f'This player {error.uname} has never played skyblock before.'
            ).send()
        elif isinstance(error, APIDisabledError):
            await CommandErrorEmbed(
                ctx,
                description=f'This player {error.uname} has disabled API on profile {error.profile_name}.\n'
                            'Please re-enable them with [skyblock menu > settings > api settings].'
            ).send()
        elif isinstance(error, BadGuildError):
            await CommandErrorEmbed(
                ctx,
                description=f'Invalid guild\'s name: {error.guild_name}.'
            ).send()
        elif isinstance(error, PlayerOnlineError):
            await CommandErrorEmbed(
                ctx,
                description='You need to be offline in hypixel to use this command!'
            ).send()
        elif isinstance(error, NoWeaponError):
            await CommandErrorEmbed(
                ctx,
                description='You have no weapons in your inventory.'
            ).send()
        elif isinstance(error, NoArmorError):
            await CommandErrorEmbed(
                ctx,
                description='You have no armors equipped or in wardrobe.'
            ).send()
        elif isinstance(error, HypixelLanguageError):
            await CommandErrorEmbed(
                ctx,
                description='I only support english at the moment!\n'
                            'Please change your hypixel language to English and try again.'
            ).send()


def setup(bot):
    bot.add_cog(ErrorHandler(bot))


class CommandErrorEmbed(Embed):
    def __init__(self, ctx, **kwargs):
        super().__init__(ctx=ctx, title='Command Error', **kwargs)
