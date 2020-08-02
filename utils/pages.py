import discord
import asyncio

from . import Embed, embed_timeout_handler


class Pages:
    def __init__(self, ctx, entries, *, per_page=10, embed_footer='', timeout=120.0):
        self.bot = ctx.bot
        self.ctx = ctx
        self.message = None
        self.channel = ctx.channel
        self.author = ctx.author
        self.entries = entries
        self.per_page = per_page
        self.embed_footer = embed_footer
        self.timeout = timeout
        self.embed = Embed(ctx=ctx)
        self.paginating = len(entries) > per_page
        pages, left_over = divmod(len(self.entries), self.per_page)
        if left_over:
            pages += 1
        self.maximum_pages = pages
        self.match = None
        self.current_page = None
        self.reaction_emojis = [
            ('\N{BLACK LEFT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}', self.first_page),
            ('\N{BLACK LEFT-POINTING TRIANGLE}', self.previous_page),
            ('\N{BLACK RIGHT-POINTING TRIANGLE}', self.next_page),
            ('\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE WITH VERTICAL BAR}', self.last_page)
        ]

    async def checked_show_page(self, page):
        if page != 0 and page <= self.maximum_pages:
            await self.show_page(page)

    async def first_page(self):
        """goes to the first page"""
        await self.show_page(1)

    async def last_page(self):
        """goes to the last page"""
        await self.show_page(self.maximum_pages)

    async def next_page(self):
        """goes to the next page"""
        await self.checked_show_page(self.current_page + 1)

    async def previous_page(self):
        """goes to the previous page"""
        await self.checked_show_page(self.current_page - 1)

    def get_page(self, page):
        base = (page - 1) * self.per_page
        return self.entries[base:base + self.per_page]

    def get_embed(self, entries, page):
        self.prepare_embed(entries, page)
        return self.embed

    def prepare_embed(self, entries, page):
        p = []
        for index, entry in enumerate(entries, 1 + ((page - 1) * self.per_page)):
            p.append(f'```{index} > {entry}```')

        page_number = f'\nPage {page} / {self.maximum_pages}.' if self.maximum_pages > 1 else ''
        footer = f'{self.embed_footer}{page_number}'
        self.embed.set_footer(text=footer)

        self.embed.description = ''.join(p)

    async def show_page(self, page, *, first=False):
        try:
            self.current_page = page
            entries = self.get_page(page)
            embed = self.get_embed(entries, page)

            if not self.paginating:
                return await self.embed.send()

            if not first:
                return await self.message.edit(embed=embed)

            self.message = await self.embed.send()
            for (reaction, _) in self.reaction_emojis:
                if self.maximum_pages == 2 and reaction in ('\u23ed', '\u23ee'):
                    continue

                await self.message.add_reaction(reaction)
        except discord.errors.Forbidden:
            self.paginating = False
            try:
                await self.ctx.send(
                    f'{self.ctx.author.mention}, Sorry, it looks like I don\'t have the permissions or roles to do that.\n'
                    f'Try enabling your DM or contract the server owner to give me more permissions.')
            except:
                pass

    def react_check(self, payload):
        if payload.user_id != self.author.id:
            return False

        if payload.message_id != self.message.id:
            return False

        to_check = str(payload.emoji)
        for (emoji, func) in self.reaction_emojis:
            if to_check == emoji:
                self.match = func
                return True
        return False

    async def paginate(self):
        """Actually paginate the entries and run the interactive loop if necessary."""
        first_page = self.show_page(1, first=True)
        if not self.paginating:
            await first_page
        else:
            # allow us to react to reactions right away if we're paginating
            self.bot.loop.create_task(first_page)

        while self.paginating:
            try:
                payload = await self.bot.wait_for('raw_reaction_add', check=self.react_check, timeout=self.timeout)
            except asyncio.TimeoutError as e:
                if not self.paginating:
                    pass
                self.paginating = False
                self.bot.loop.create_task(embed_timeout_handler(self.ctx, self.reaction_emojis, message=self.message))
                raise e from None

            try:
                await self.message.remove_reaction(payload.emoji, discord.Object(id=payload.user_id))
            except:
                pass  # can't remove it so don't bother doing so

            await self.match()
