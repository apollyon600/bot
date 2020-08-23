from discord.ext import commands
from copy import deepcopy
import time

from utils import CommandWithCooldown, get_uuid_from_name, get_name_from_uuid
from constants.db_schema import PLAYER_DATA


# TODO: add force verify for admin
class Verify(commands.Cog, name='Skyblock'):
    def __init__(self, bot):
        self.bot = bot
        self.players_db = bot.db['players']

    @commands.command(cls=CommandWithCooldown, cooldown_after_parsing=True)
    @commands.cooldown(1, 10.0, commands.BucketType.user)
    async def verify(self, ctx, player: str = ''):
        if not player:
            player = await ctx.ask(message=f'{ctx.author.mention}\nWhat is your minecraft username?')

        player_name, player_uuid = await get_uuid_from_name(player, session=self.bot.http_session)
        player = await self.bot.hypixel_api_client.get_player(player_uuid, uname=player_name)

        if str(ctx.author) != player.discord_tag:
            return await ctx.send(f'{ctx.author.mention}\nYour haven\'t linked your discord to your hypixel account!')

        player_data = await self.players_db.find_one(
            {'$or': [{'discord_ids.discord_id': ctx.author.id}, {'mojang_uuids.mojang_uuid': player.uuid}]})

        if player_data is None:
            player_data = deepcopy(PLAYER_DATA)

            player_data['discord_ids'].append({
                'discord_id': ctx.author.id,
                'discord_usernames': [{
                    'discord_username': ctx.author.name,
                    'updated_timestamp': int(time.time())
                }]
            })

            player_data['mojang_uuids'].append({
                'mojang_uuid': player.uuid,
                'mojang_usernames': []
            })

            mojang_names = await get_name_from_uuid(player.uuid, session=self.bot.http_session)
            for mojang_name in mojang_names[-5:]:
                timestamp = mojang_name.get('changedToAt', None)
                player_data['mojang_uuids'][0]['mojang_usernames'].append({
                    'mojang_username': mojang_name['name'],
                    'updated_timestamp': int(timestamp / 1000.0) if timestamp else None
                })

            await self.players_db.insert_one(player_data)

            await ctx.send(f'{ctx.author.mention}\nSuccesfully verified your hypixel account with your discord.')
        elif any(ctx.author.id == discord_id['discord_id'] for discord_id in player_data['discord_ids']) and not any(
                player.uuid == mojang_uuid['mojang_uuid'] for mojang_uuid in player_data['mojang_uuids']):
            # Multiple mojang uuids
            mojang_uuid = {
                'mojang_uuid': player.uuid,
                'mojang_usernames': []
            }

            mojang_names = await get_name_from_uuid(player.uuid, session=self.bot.http_session)
            for mojang_name in mojang_names[-5:]:
                timestamp = mojang_name.get('changedToAt', None)
                mojang_uuid['mojang_usernames'].append({
                    'mojang_username': mojang_name['name'],
                    'updated_timestamp': int(timestamp / 1000.0) if timestamp else None
                })

            await self.players_db.update_one({'discord_ids.discord_id': ctx.author.id},
                                             {'$push': {'mojang_uuids': mojang_uuid}})

            await ctx.send(f'{ctx.author.mention}\nSuccessfully verified your new hypixel account!')
        elif any(player.uuid == mojang_uuid['mojang_uuid'] for mojang_uuid in player_data['mojang_uuids']) and not any(
                ctx.author.id == discord_id['discord_id'] for discord_id in player_data['discord_ids']):
            # Multiple discord ids
            discord_id = {
                'discord_id': ctx.author.id,
                'discord_usernames': [{
                    'discord_username': ctx.author.name,
                    'updated_timestamp': int(time.time())
                }]
            }

            await self.players_db.update_one({'mojang_uuids.mojang_uuid': player.uuid},
                                             {'$push': {'discord_ids': discord_id}})

            await ctx.send(f'{ctx.author.mention}\nSuccessfully verified your new discord!')
        else:
            await ctx.send(f'{ctx.author.mention}\nYou\'re already verified.')


def setup(bot):
    bot.add_cog(Verify(bot))
