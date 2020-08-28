from discord.ext import commands
import discord
from copy import deepcopy
import time

from utils import GroupWithCooldown, get_uuid_from_name, get_name_from_uuid, checks
from constants.db_schema import PLAYER_DATA


class Verify(commands.Cog, name='Skyblock'):
    def __init__(self, bot):
        self.bot = bot
        self.players_db = bot.db['players']

    @commands.group(cls=GroupWithCooldown, cooldown_after_parsing=True, invoke_without_command=True)
    @commands.cooldown(1, 10.0, commands.BucketType.user)
    async def verify(self, ctx, player: str = ''):
        """
        Verify your hypixel account to your discord.
        """
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

    @verify.command()
    @checks.is_sbs_admin()
    async def add(self, ctx, mojang_username, discord_user: discord.User = ''):
        """
        Force verify a discord id to mojang uuid.
        """
        if not discord_user:
            discord_user = ctx.author

        player_name, player_uuid = await get_uuid_from_name(mojang_username, session=self.bot.http_session)

        player_data = await self.players_db.find_one(
            {'$or': [{'discord_ids.discord_id': discord_user.id}, {'mojang_uuids.mojang_uuid': player_uuid}]})

        if player_data is None:
            player_data = deepcopy(PLAYER_DATA)

            player_data['discord_ids'].append({
                'discord_id': discord_user.id,
                'discord_usernames': [{
                    'discord_username': discord_user.name,
                    'updated_timestamp': int(time.time())
                }]
            })

            player_data['mojang_uuids'].append({
                'mojang_uuid': player_uuid,
                'mojang_usernames': []
            })

            mojang_names = await get_name_from_uuid(player_uuid, session=self.bot.http_session)
            for mojang_name in mojang_names[-5:]:
                timestamp = mojang_name.get('changedToAt', None)
                player_data['mojang_uuids'][0]['mojang_usernames'].append({
                    'mojang_username': mojang_name['name'],
                    'updated_timestamp': int(timestamp / 1000.0) if timestamp else None
                })

            await self.players_db.insert_one(player_data)

            await ctx.send(
                f'{ctx.author.mention}\nSuccesfully verified new hypixel player {player_name} to new discord user {discord_user.name}.')
        elif any(discord_user.id == discord_id['discord_id'] for discord_id in player_data['discord_ids']) and not any(
                player_uuid == mojang_uuid['mojang_uuid'] for mojang_uuid in player_data['mojang_uuids']):
            # Multiple mojang uuids
            mojang_uuid = {
                'mojang_uuid': player_uuid,
                'mojang_usernames': []
            }

            mojang_names = await get_name_from_uuid(player_uuid, session=self.bot.http_session)
            for mojang_name in mojang_names[-5:]:
                timestamp = mojang_name.get('changedToAt', None)
                mojang_uuid['mojang_usernames'].append({
                    'mojang_username': mojang_name['name'],
                    'updated_timestamp': int(timestamp / 1000.0) if timestamp else None
                })

            await self.players_db.update_one({'discord_ids.discord_id': discord_user.id},
                                             {'$push': {'mojang_uuids': mojang_uuid}})

            await ctx.send(
                f'{ctx.author.mention}\nSuccesfully verified new hypixel player {player_name} to discord user {discord_user.name}.')
        elif any(player_uuid == mojang_uuid['mojang_uuid'] for mojang_uuid in player_data['mojang_uuids']) and not any(
                discord_user.id == discord_id['discord_id'] for discord_id in player_data['discord_ids']):
            # Multiple discord ids
            discord_id = {
                'discord_id': discord_user.id,
                'discord_usernames': [{
                    'discord_username': discord_user.name,
                    'updated_timestamp': int(time.time())
                }]
            }

            await self.players_db.update_one({'mojang_uuids.mojang_uuid': player_uuid},
                                             {'$push': {'discord_ids': discord_id}})

            await ctx.send(
                f'{ctx.author.mention}\nSuccesfully verified new discord user {discord_user.name} to hypixel player {player_name}.')
        else:
            await ctx.send(f'{ctx.author.mention}\nThis discord user is already verified the hypixel account.')

    @verify.group(invoke_without_command=True)
    @checks.is_sbs_admin()
    async def remove(self, ctx):
        """
        Force remove discord id or mojang uuid from a verified user.
        """
        await ctx.send_help(ctx.command)

    @remove.command(name='discord')
    @checks.is_sbs_admin()
    async def discord_id(self, ctx, mojang_username, discord_user: discord.User = ''):
        """
        Force remove a verified discord id by mojang uuid.

        If discord user is empty it will take the message author discord id.
        """
        if not discord_user:
            discord_user = ctx.author

        player_name, player_uuid = await get_uuid_from_name(mojang_username, session=self.bot.http_session)

        player_data = await self.players_db.find_one({'mojang_uuids.mojang_uuid': player_uuid})

        if player_data is None:
            await ctx.send(f'{ctx.author.mention}\nThis hypixel player has never verified any discord account!')
        elif any(discord_user.id == discord_id['discord_id'] for discord_id in player_data['discord_ids']):
            await self.players_db.update_one({'mojang_uuids.mojang_uuid': player_uuid},
                                             {'$pull': {'discord_ids': {'discord_id': discord_user.id}}})

            await ctx.send(
                f'{ctx.author.mention}\nSuccessfully remove discord user {discord_user.name} from hypixel player {mojang_username}.')
        else:
            await ctx.send(
                f'{ctx.author.mention}\nThis hypixel player is not verified with discord user {discord_user.name}.')

    @remove.command(name='mojang')
    @checks.is_sbs_admin()
    async def mojang_name(self, ctx, mojang_username, discord_user: discord.User = ''):
        """
        Force remove a verified mojang uuid by discord id.

        If discord user is empty it will take the message author discord id.
        """
        if not discord_user:
            discord_user = ctx.author

        player_name, player_uuid = await get_uuid_from_name(mojang_username, session=self.bot.http_session)

        player_data = await self.players_db.find_one({'discord_ids.discord_id': discord_user.id})

        if player_data is None:
            await ctx.send(f'{ctx.author.mention}\nThis discord user has never verified any hypixel account!')
        elif any(player_uuid == mojang_uuid['mojang_uuid'] for mojang_uuid in player_data['mojang_uuids']):
            await self.players_db.update_one({'discord_ids.discord_id': discord_user.id},
                                             {'$pull': {'mojang_uuids': {'mojang_uuid': player_uuid}}})

            await ctx.send(
                f'{ctx.author.mention}\nSuccessfully remove hypixel player {mojang_username} from discord user {discord_user.name}.')
        else:
            await ctx.send(
                f'{ctx.author.mention}\nThis discord user is not verified with hypixel player {mojang_username}.')


def setup(bot):
    bot.add_cog(Verify(bot))
