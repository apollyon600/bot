import discord
from datetime import datetime


class Embed(discord.Embed):
    nbst = '\u200b'

    def __init__(self, *, ctx=None, channel=None, user=None, **kwargs):
        if ctx and not channel:
            self.channel = ctx.channel
            self.user = ctx.author or None
        elif channel and not ctx:
            self.channel = channel
            self.user = user

        super().__init__(color=self.color(channel), **kwargs)

    @staticmethod
    def color(channel):
        default = 0xbf2158

        if hasattr(channel, 'guild'):
            color = channel.guild.me.color
            return discord.Color(default) if color == 0x000000 else color
        else:
            return discord.Color(default)

    def add_field(self, *, name=None, value=nbst, inline=True):
        return super().add_field(name=f'**{name}**' if name else self.nbst, value=value, inline=inline)

    def add_footer(self, text):
        super().set_footer(
            text=f'{text}\nSkyblock Simplified',
            icon_url='https://i.imgur.com/V7ENVHr.png'
        )
        return self

    async def send(self, *, dm=False, dm_extra=False):
        self.timestamp = datetime.now()

        if not self.footer:
            super().set_footer(
                text='Skyblock Simplified',
                icon_url='https://i.imgur.com/V7ENVHr.png'
            )

        if dm and not isinstance(self.channel, discord.DMChannel):
            msg = await self.user.send(self.user.mention, embed=self)
            if dm_extra:
                await self.channel.send(f'{self.user.mention}, I have sent you a DM with the information!')
            return msg
        return await self.channel.send(self.user.mention if self.user else None, embed=self)
