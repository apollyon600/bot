import asyncio
import discord
from discord.ext import commands

from lib import SessionTimeout
from utils import embed_timeout_handler, Pages


class Context(commands.Context):
    def __init__(self, **kwargs):
        self.bot_message = None
        super().__init__(**kwargs)

    async def prompt(self, *, message=None, embed=None, timeout=60.0, emoji_list=None):
        if not emoji_list:
            emoji_list = [
                ('✅', True),
                ('❌', False)
            ]

        self.bot.loop.create_task(self.send_in_task(message, emoji_list, embed=embed))

        answer = None

        def reaction_check(payload):
            nonlocal answer
            if payload.user_id != self.author.id or payload.message_id != self.bot_message.id:
                return False
            to_check = str(payload.emoji)
            for (_emoji, _ans) in emoji_list:
                if to_check == _emoji:
                    answer = _ans
                    return True
            return False

        def message_check(m):
            if m.author.id == self.author.id and m.channel.id == self.channel.id and m.clean_content.lower() == 'exit':
                raise SessionTimeout
            return False

        tasks = [
            self.bot.wait_for('raw_reaction_add', check=reaction_check, timeout=timeout),
            self.bot.wait_for('message', check=message_check, timeout=timeout)
        ]

        done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

        try:
            done.pop().result()
        except (asyncio.TimeoutError, SessionTimeout) as e:
            self.bot.loop.create_task(embed_timeout_handler(self, emoji_list, message=self.bot_message))
            raise e
        finally:
            for future in pending:
                future.cancel()

        return answer

    async def prompt_with_list(self, entries, *, timeout=60.0, per_page=10, title='', footer=''):
        pages = Pages(self, entries, per_page=per_page, embed_footer=footer)
        paginating = pages.paginating
        pages.embed.title = title
        pages_task = self.bot.loop.create_task(pages.paginate())

        def check(m):
            if m.author.id == self.author.id and m.channel.id == self.channel.id:
                if m.clean_content.lower() == 'exit':
                    raise SessionTimeout
                if m.clean_content.isdigit():
                    return True
            return False

        valid_index = [i + 1 for i, _ in enumerate(entries)]

        if paginating:
            tasks = [self.bot.wait_for('message', check=check, timeout=timeout), pages_task]
        else:
            tasks = [self.bot.wait_for('message', check=check, timeout=timeout)]

        while True:
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            try:
                stuff = done.pop().result()
                if isinstance(stuff, discord.Message):
                    if int(stuff.clean_content) in valid_index:
                        for future in pending:
                            future.cancel()
                        return int(stuff.clean_content)
                    else:
                        tasks = [self.bot.wait_for('message', check=check, timeout=timeout)]
                        for future in pending:
                            tasks.append(future)
                        await self.send(f'{self.author.mention}, Invalid number! Did you make a typo?')
            except (asyncio.TimeoutError, SessionTimeout) as e:
                for future in pending:
                    future.cancel()
                if paginating:
                    self.bot.loop.create_task(embed_timeout_handler(self, pages.reaction_emojis, message=pages.message))
                raise e from None

    async def ask(self, *, message=None, timeout=60.0, message_check=None):
        if message:
            await self.send(message)

        if not message_check:
            def check(m):
                if m.author.id == self.author.id and m.channel.id == self.channel.id:
                    if m.clean_content.lower() == 'exit':
                        raise SessionTimeout
                    return True
                return False

            message_check = check

        ans = await self.bot.wait_for('message', timeout=timeout, check=message_check)
        return ans.clean_content

    async def send_in_task(self, message, emoji_list, *, embed):
        try:
            if embed:
                self.bot_message = await embed.send()
            else:
                self.bot_message = await self.send(message)
            current_message = self.bot_message

            for (emoji, _) in emoji_list:
                await current_message.add_reaction(emoji)
        except discord.errors.Forbidden:
            try:
                await self.send(
                    f'{self.author.mention}, Sorry, it looks like I don\'t have the permissions or roles to do that.\n'
                    f'Try enabling your DMS or contract the server owner to give me more permissions.')
            except:
                pass
