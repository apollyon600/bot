import asyncio
import discord
from discord.ext import commands

from constants.bot import timeout_emoji


class Context(commands.Context):
    def __init__(self, **kwargs):
        self.bot_message = None
        super().__init__(**kwargs)

    async def prompt(self, message=None, *, embed=None, timeout=60.0, emoji_list=None):
        if not emoji_list:
            emoji_list = [
                ('✅', True),
                ('❌', False)
            ]

        self.bot.loop.create_task(self.send_in_task(message, emoji_list, embed=embed))

        answer = None

        def check(payload):
            nonlocal answer

            if payload.user_id != self.author.id:
                return False

            if payload.message_id != self.bot_message.id:
                return False

            to_check = str(payload.emoji)
            for (_emoji, _ans) in emoji_list:
                if to_check == _emoji:
                    answer = _ans
                    return True
            return False

        try:
            await self.bot.wait_for('raw_reaction_add', check=check, timeout=timeout)
        except asyncio.TimeoutError as e:
            self.bot.loop.create_task(self.timeout_handler(emoji_list))
            raise e

        return answer

    async def prompt_with_list(self, *, timeout=60.0, prompt_list, embed):
        embed.add_field(
            value=''.join([f'```{i + 1} > ' + item + '```' for i, item in enumerate(prompt_list)])
        )
        await embed.send()

        def check(m):
            return m.content.isdigit() and m.author.id == self.author.id and m.channel.id == self.channel.id

        valid_index = [i + 1 for i, _ in enumerate(prompt_list)]

        while True:
            msg = await self.bot.wait_for('message', check=check, timeout=timeout)
            if int(msg.clean_content) in valid_index:
                return msg.clean_content
            else:
                await self.send(f'{self.author.mention}, Invalid number! Did you make a typo?')

    async def timeout_handler(self, emoji_list):
        try:
            for (emoji, _) in emoji_list:
                await self.bot_message.remove_reaction(emoji, self.bot.user)
            for emoji in timeout_emoji:
                await self.bot_message.add_reaction(emoji)
        except:
            pass

    async def send_in_task(self, message, emoji_list, *, embed):
        try:
            if embed:
                self.bot_message = await embed.send()
            else:
                self.bot_message = await self.send(f'{self.author.mention}, {message}')

            for (emoji, _) in emoji_list:
                await self.bot_message.add_reaction(emoji)
        except discord.errors.Forbidden:
            try:
                await self.send(
                    f'{self.author.mention}, Sorry, it looks like I don\'t have the permissions or roles to do that.\n'
                    f'Try enabling your DMS or contract the server owner to give me more permissions.')
            except:
                pass
