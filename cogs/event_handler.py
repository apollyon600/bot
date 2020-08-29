from discord.ext import commands
import time

from utils import get_guild_config
from constants.discord import SKYBLOCK_EVENTS


class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Start all skyblock event schedules
        cog = self.bot.get_cog('Skyblock')
        text = ''
        for event in SKYBLOCK_EVENTS.keys():
            text += await cog.schedule_event(event)
        print(text)

        print(f'Logged on as {self.bot.user}! (ID: {self.bot.user.id})')

    @commands.Cog.listener()
    async def on_command(self, ctx):
        filtered_args = ctx.message.clean_content.split()[2:] or []
        print(f'{ctx.author} used {ctx.command} {filtered_args} in {"a DM" if ctx.guild is None else ctx.guild.name} '
              f'at {ctx.message.created_at}.')

    @commands.Cog.listener()
    async def on_user_update(self, before, after):
        if before.name != after.name:
            discord_username = await self.bot.db['discord_usernames'].find_one({'_id': before.id})
            if discord_username is None:
                return

            discord_username['current_name'] = after.name
            if len(discord_username['name_history']) == 5:
                discord_username.pop(0)
            discord_username['name_history'].append({
                'name': before.name,
                'updated_timestamp': discord_username['updated_timestamp']
            })
            discord_username['updated_timestamp'] = int(time.time())

            await self.bot.db['discord_usernames'].replace_one({'_id': before.id}, discord_username)

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        """
        Executes when a guild updates.
        """
        # Skip blacklisted guilds
        if before.id in self.bot.blacklisted_guild_ids:
            return

        to_update = {}
        if before.name != after.name:
            to_update.update({'name': after.name})
        if str(before.icon_url) != str(after.icon_url):
            to_update.update({'icon': str(after.icon_url)})
        if str(before.banner_url) != str(before.banner_url):
            to_update.update({'banner': str(after.icon_url)})

        if to_update:
            to_update.update({'last_update': int(time.time())})
            await self.bot.db['guilds'].update_one({'_id': before.id}, {'$set': to_update})

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        """
        Executes when bot joins a guild.
        """
        # Skip blacklisted guilds
        if guild.id in self.bot.blacklisted_guild_ids:
            return

        await get_guild_config(self.bot.db['guilds'], guild=guild)


def setup(bot):
    bot.add_cog(EventHandler(bot))
