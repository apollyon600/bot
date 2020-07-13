import discord

class Embed(discord.Embed):
    nbst = '\u200b'

    def __init__(self, channel, *, user=None, **kwargs):
        self.channel = channel
        self.user = user

        super().__init__(
            color=self.color(channel),
            **kwargs
        )

    @staticmethod
    def color(channel):
        default = 0xbf2158

        if hasattr(channel, 'guild'):
            color = channel.guild.me.color
            return discord.Color(default) if color == 0x000000 else color
        else:
            return discord.Color(default)

    def add_field(self, *, name, value, inline=True):
        return super().add_field(name=f'**{name}**' if name else self.nbst, value=value or self.nbst, inline=inline)

    def set_image(self, url):
        return super().set_image(url=url)

    async def send(self):
        return await self.channel.send(self.user.mention if self.user else None, embed=self)