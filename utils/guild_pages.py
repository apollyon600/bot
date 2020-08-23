import asyncio

from lib import SessionTimeout
from . import Pages
from constants.discord import SKILL_EMOJIS


class GuildPages(Pages):
    def __init__(self, ctx, guild, entries, header_entries, *, timeout=120.0):
        super().__init__(ctx, entries, per_page=1, timeout=timeout)
        self.reaction_emojis.append(('\N{WHITE QUESTION MARK ORNAMENT}', self.show_guild_pages_help))
        self.reaction_emojis.append(('\N{INPUT SYMBOL FOR NUMBERS}', self.numbered_page))
        self.guild = guild
        self.header_entries = header_entries

    def prepare_embed(self, entries, page):
        self.embed.clear_fields()
        guild = self.guild

        page_number = f'\nPage {page} / {self.maximum_pages}.' if self.maximum_pages > 1 else ''
        footer = f'{self.embed_footer}{page_number}'
        self.embed.add_footer(text=footer)

        if page != 1:
            # Load leaderboard page
            self.embed.title = f'{guild.name} {self.header_entries[page - 1]}'
            self.embed.description = ''

            entries = entries[0]
            top3 = '\n'.join(entries[:3])
            if top3:
                self.embed.add_field(
                    name='**Top 3**',
                    value=f'```css\n{top3}```',
                    inline=False
                )

            top10 = '\n'.join(entries[3:10])
            if top10:
                self.embed.add_field(
                    name='**Top 10**',
                    value=f'```css\n{top10}```',
                    inline=False
                )

            for i in range(1, (len(entries) // 10) + (1 if (len(entries) % 10) else 0)):
                top = '\n'.join(entries[i * 10:(i + 1) * 10])
                if not top:
                    break
                self.embed.add_field(
                    name=f'**Top {(i + 1) * 10}**',
                    value=f'```css\n{top}```',
                    inline=False
                )
        else:
            # Load first page
            self.embed.title = f'{guild.name} | {guild.tag}' if guild.tag else guild.name

            description = f'```{guild.description}```' if guild.description else ''
            self.embed.description = f'{description}```Level > {guild.level}\n' \
                                     f'Members > {guild.member_amount}\n' \
                                     f'Online members > {guild.current_online}\n' \
                                     f'Owner > {guild.owner.player.uname if guild.owner else None}\n' \
                                     f'Created at > {guild.created_at.replace(microsecond=0)}``````' \
                                     f'Average deaths > {guild.average_deaths:,}\n' \
                                     f'Average money > {guild.average_money:,.2f}\n' \
                                     f'Average skills > {guild.average_skills:.2f}\n' \
                                     f'Average minion slots > {guild.minion_slot} ' \
                                     f'({guild.unique_minions} average crafted)```'

            for skill, level in guild.skills.items():
                self.embed.add_field(
                    name=f'{SKILL_EMOJIS[skill]}\t{skill.capitalize()}',
                    value=f'```Level > {level}\n'
                          f'XP > {guild.skills_xp.get(skill, 0):,.0f}```'
                )
            # So every skill embed field is same size
            left_over_field = 3 - (len(guild.skills) % 3)
            if left_over_field < 3:
                for i in range(0, left_over_field):
                    self.embed.add_field()

            for slayer, level in guild.slayers.items():
                self.embed.add_field(
                    name=f'{SKILL_EMOJIS[slayer]}\t{slayer.capitalize()}',
                    value=f'```Level > {level}\n'
                          f'XP > {guild.slayers_xp.get(slayer, 0):,.0f}```'
                )

            self.embed.add_field(
                name=f'{SKILL_EMOJIS["dungeons"]}\tDungeon Catacombs',
                value=f'```Average Level > {guild.average_dungeon_level:.2f}```'
            )

    async def show_guild_pages_help(self):
        """
        Shows how which page is what leaderboard.
        """
        self.embed.clear_fields()

        self.embed.title = 'Welcome to the help page.'
        self.embed.add_footer(text=f'We were on page {self.current_page} before this message.')

        description = '\n'.join(
            [f'Page {i + 1} > {name}' for i, name in enumerate(self.header_entries)])
        self.embed.description = f'What are these pages for?```{description}```'

        self.embed.add_field(
            name='\n\N{INPUT SYMBOL FOR NUMBERS}\tGo to page number',
            value='```React to this lets you type a page number to go to.```'
        )

        await self.message.edit(embed=self.embed)

        async def go_back_to_current_page():
            await asyncio.sleep(30.0)
            await self.show_current_page()

        self.bot.loop.create_task(go_back_to_current_page())

    async def show_current_page(self):
        if self.paginating:
            await self.show_page(self.current_page)

    async def numbered_page(self):
        """
        Lets you type a page number to go to.
        """
        to_delete = [await self.ctx.send(f'{self.author.mention}, What page do you want to go to?')]

        def message_check(m):
            if m.author.id == self.author.id and m.channel.id == self.channel.id:
                if m.clean_content.lower() == 'exit':
                    raise SessionTimeout
                if m.clean_content.isdigit():
                    return True
            return False

        try:
            msg = await self.bot.wait_for('message', check=message_check, timeout=30.0)
        except (asyncio.TimeoutError, SessionTimeout):
            to_delete.append(await self.ctx.send(f'{self.author.mention}, Input session closed.'))
            await asyncio.sleep(4)
        else:
            page = int(msg.clean_content)
            to_delete.append(msg)
            if page != 0 and page <= self.maximum_pages:
                await self.show_page(page)
            else:
                to_delete.append(
                    await self.ctx.send(f'{self.author.mention}, Invalid page given. ({page}/{self.maximum_pages})'))
                await asyncio.sleep(4)

        try:
            await self.channel.delete_messages(to_delete)
        except Exception:
            pass
