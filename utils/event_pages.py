import discord
import asyncio
import aiohttp
from discord import TextChannel, Webhook, AsyncWebhookAdapter

from lib import SessionTimeout
from . import Embed, embed_timeout_handler, send_no_permission_embed
from constants.discord import SKYBLOCK_EVENTS


class EventPages:
    def __init__(self, ctx, guild_config, guilds_db):
        self.ctx = ctx
        self.bot = ctx.bot
        self.guilds_db = guilds_db
        self.message = ctx.message
        self.channel = ctx.channel
        self.guild = ctx.guild
        self.author = ctx.author
        self.guild_config = guild_config
        self.manage_messages = self.channel.permissions_for(self.guild.me).manage_messages

        self.embed = Embed(ctx=ctx)
        self.current_page = None
        self.previous_page = None
        self.paginating = True
        self.match = None

        self.main_page_emojis = [
            ('📄', self.set_default_channel, ''),
            ('📣', self.set_default_mention, ''),
            ('⚙️', self.toggle_event_system, ''),
        ]

        for event in SKYBLOCK_EVENTS.keys():
            self.main_page_emojis.append((SKYBLOCK_EVENTS[event]['emoji'], self.show_event_page, event))
        self.main_page_emojis.append(('✅', self.enable_all_events, ''))
        self.main_page_emojis.append(('❎', self.disable_all_events, ''))

        self.event_page_emojis = [
            ('📄', self.set_event_channel, ''),
            ('📣', self.set_event_mention, ''),
            ('✅', self.enable_event, ''),
            ('❎', self.disable_event, ''),
            ('⬅️', self.default_page, 'default')
        ]

    async def default_page(self, *, first=False, with_emoji=True):
        self.embed.clear_fields()
        self.embed.title = 'Skyblock Events Configuration'
        self.embed.description = 'Welcome to skyblock events configuration page for your discord server.'

        role_id = self.guild_config['events']['default_mention_id']
        mention_text = f'<@&{role_id}>' if role_id is not None else None
        webhook_data = self.guild_config['events']['default_webhook_data']
        channel_text = f'<#{webhook_data.split("/")[2]}>' if webhook_data is not None else None

        self.embed.add_field(
            name='⚙️\tSystem Status',
            value=f'{"Enabled" if self.guild_config["events"]["default_enabled"] else "Disabled"}'
        ).add_field(
            name='📣\tDefault Mention',
            value=f'{mention_text}'
        ).add_field(
            name='📄\tDefault Channel',
            value=f'{channel_text}'
        )

        for event in SKYBLOCK_EVENTS:
            self.embed.add_field(
                name=f'{SKYBLOCK_EVENTS[event]["emoji"]}\t{SKYBLOCK_EVENTS[event]["name"]}',
                value=f'{"Enabled" if self.guild_config["events"][event]["enabled"] else "Disabled"}'
            )

        self.embed.add_field().add_field(
            name='✅/❎\tEnable/Disable all',
            value='React to enable/disable all events at once.'
        )

        try:
            if first:
                self.message = await self.embed.send()
                self.current_page = 'default'

                for (emoji, _, page) in self.main_page_emojis:
                    await self.message.add_reaction(emoji)
            else:
                await self.message.edit(embed=self.embed)

                # Remove old emojis and add new emojis if previous page was event page
                if self.previous_page != 'default' and with_emoji:
                    if self.manage_messages:
                        await self.message.clear_reactions()
                    else:
                        try:
                            for (emoji, _, __) in self.event_page_emojis:
                                await self.message.remove_reaction(emoji, self.bot.user)
                        except Exception:
                            pass

                    for (emoji, _, page) in self.main_page_emojis:
                        await self.message.add_reaction(emoji)
        except discord.errors.Forbidden:
            self.paginating = False
            try:
                await send_no_permission_embed(self.ctx)
            except Exception:
                pass

    async def show_event_page(self, *, with_emoji=True):
        self.embed.clear_fields()
        self.embed.title = f'{SKYBLOCK_EVENTS[self.current_page]["name"]} Configuration'
        self.embed.description = ''

        role_id = self.guild_config["events"][self.current_page]["mention_id"]
        mention_text = f'<@&{role_id}>' if role_id is not None else None
        webhook_data = self.guild_config["events"][self.current_page]["webhook_data"]
        channel_text = f'<#{webhook_data.split("/")[2]}>' if webhook_data is not None else None

        self.embed.add_field(
            name='✅/❎\tStatus',
            value=f'{"Enabled" if self.guild_config["events"][self.current_page]["enabled"] else "Disabled"}'
        ).add_field(
            name='📣\tMention',
            value=f'{mention_text}'
        ).add_field(
            name='📄\tChannel',
            value=f'{channel_text}'
        )
        await self.message.edit(embed=self.embed)

        # Remove old emojis and add new emojis if previous page was default page
        if self.previous_page == 'default' and with_emoji:
            if self.manage_messages:
                await self.message.clear_reactions()
            else:
                try:
                    for (emoji, _, __) in self.main_page_emojis:
                        await self.message.remove_reaction(emoji, self.bot.user)
                except Exception:
                    pass

            for (emoji, _, page) in self.event_page_emojis:
                await self.message.add_reaction(emoji)

    async def enable_event(self):
        # Check if event is not already enabled and event webhook or default webhook is not empty
        if not self.guild_config['events'][self.current_page]['enabled'] and (
                self.guild_config['events'][self.current_page]['webhook_data'] is not None or
                self.guild_config['events']['default_webhook_data'] is not None):
            self.guild_config['events'][self.current_page]['enabled'] = True
            await self.guilds_db.update_one({'_id': self.guild_config['_id']},
                                            {'$set': {f'events.{self.current_page}.enabled': True}})

            await self.show_event_page(with_emoji=False)

    async def enable_all_events(self):
        # Check if all events are not already enabled
        to_update = {}
        for event in SKYBLOCK_EVENTS.keys():
            if not self.guild_config['events'][event]['enabled'] and (
                    self.guild_config['events'][event]['webhook_data'] is not None or
                    self.guild_config['events']['default_webhook_data'] is not None):
                self.guild_config['events'][event]['enabled'] = True
                to_update.update({f'events.{event}.enabled': True})

        if to_update:
            await self.guilds_db.update_one({'_id': self.guild_config['_id']}, {'$set': to_update})

            await self.default_page(with_emoji=False)

    async def disable_event(self):
        # Check if event is not already disabled
        if self.guild_config['events'][self.current_page]['enabled']:
            self.guild_config['events'][self.current_page]['enabled'] = False
            await self.guilds_db.update_one({'_id': self.guild_config['_id']},
                                            {'$set': {f'events.{self.current_page}.enabled': False}})

            await self.show_event_page(with_emoji=False)

    async def disable_all_events(self):
        # Check if all events are not already disabled
        to_update = {}
        for event in SKYBLOCK_EVENTS.keys():
            if self.guild_config['events'][event]['enabled']:
                self.guild_config['events'][event]['enabled'] = False
                to_update.update({f'events.{event}.enabled': False})

        if to_update:
            await self.guilds_db.update_one({'_id': self.guild_config['_id']}, {'$set': to_update})

            await self.default_page(with_emoji=False)

    async def toggle_event_system(self):
        if self.guild_config['events']['default_enabled']:
            self.guild_config['events']['default_enabled'] = False
            await self.guilds_db.update_one({'_id': self.guild_config['_id']},
                                            {'$set': {'events.default_enabled': False}})

            await self.default_page(with_emoji=False)
        else:
            self.guild_config['events']['default_enabled'] = True
            await self.guilds_db.update_one({'_id': self.guild_config['_id']},
                                            {'$set': {'events.default_enabled': True}})

            await self.default_page(with_emoji=False)

    async def set_event_channel(self):
        to_delete = [await self.ctx.send(
            f'{self.author.mention}\nWhich channel would you want this event alert?\n'
            f'Please mention/enter channel or None to unset channel.\n'
            f'The bot will automatically create webhook for you.')]

        def message_check(m):
            if m.author.id == self.author.id and m.channel.id == self.channel.id:
                if m.clean_content.lower() == 'exit':
                    raise SessionTimeout
                if m.clean_content.isdigit() or len(m.channel_mentions) == 1 or m.clean_content.lower() == 'none':
                    return True
            return False

        try:
            msg = await self.bot.wait_for('message', check=message_check, timeout=30.0)
        except (asyncio.TimeoutError, SessionTimeout):
            to_delete.append(await self.ctx.send(f'{self.author.mention}, Input session closed.'))
            await asyncio.sleep(5)
        else:
            to_delete.append(msg)

            if msg.clean_content.lower() == 'none' or (msg.clean_content.isdigit() and int(msg.clean_content) == 0):
                # Check if it's not already empty
                if self.guild_config['events'][self.current_page]['webhook_data'] is not None:
                    # Try delete old webhook
                    try:
                        splitted_webhook_data = self.guild_config['events'][self.current_page]['webhook_data'].split(
                            '/')
                        old_webhook = Webhook.partial(splitted_webhook_data[0], splitted_webhook_data[1],
                                                      adapter=AsyncWebhookAdapter(self.bot.http_session))

                        await old_webhook.delete(
                            reason=f'Member: {self.author.id} deleted channel for {SKYBLOCK_EVENTS[self.current_page]["name"]} alert.')
                    except Exception:
                        pass

                    # Try disble event if there is no default webhook
                    to_update = {}
                    if self.guild_config['events']['default_webhook_data'] is None:
                        self.guild_config['events'][self.current_page]['enabled'] = False
                        to_update.update({f'events.{self.current_page}.enabled': False})

                    to_update.update({f'events.{self.current_page}.webhook_data': None})
                    self.guild_config['events'][self.current_page]['webhook_data'] = None
                    await self.guilds_db.update_one({'_id': self.guild_config['_id']}, {'$set': to_update})

                    await self.show_event_page(with_emoji=False)
            else:
                if msg.clean_content.isdigit():
                    channel = self.guild.get_channel(int(msg.clean_content))
                else:
                    channel = self.guild.get_channel(msg.raw_channel_mentions[0])

                if isinstance(channel, TextChannel):
                    webhook_data = self.guild_config['events'][self.current_page]['webhook_data']

                    # Check if it's not already the same channel
                    if webhook_data is None or webhook_data.split('/')[2] != channel.id:
                        # Try delete old webhook if not the same
                        if webhook_data is not None:
                            try:
                                splitted_webhook_data = webhook_data.split('/')
                                old_webhook = Webhook.partial(splitted_webhook_data[0], splitted_webhook_data[1],
                                                              adapter=AsyncWebhookAdapter(self.bot.http_session))

                                await old_webhook.delete(
                                    reason=f'Member: {self.author.id} deleted channel for {SKYBLOCK_EVENTS[self.current_page]["name"]} alert.')
                            except Exception:
                                pass

                        # Check webhook permission
                        if not channel.permissions_for(self.guild.me).manage_webhooks:
                            to_delete.append(await send_no_permission_embed(self.ctx))
                            await asyncio.sleep(4)
                            return

                        # Create webhook for event
                        webhook = await channel.create_webhook(
                            name=f'{SKYBLOCK_EVENTS[self.current_page]["name"]} Alert',
                            reason=f'Member: {self.author.id} created webhook for {SKYBLOCK_EVENTS[self.current_page]["name"]} alert.')

                        self.guild_config['events'][self.current_page][
                            'webhook_data'] = f'{webhook.id}/{webhook.token}/{channel.id}'
                        await self.guilds_db.update_one({'_id': self.guild_config['_id']}, {'$set': {
                            f'events.{self.current_page}.webhook_data': f'{webhook.id}/{webhook.token}/{channel.id}'}})

                        await self.show_event_page(with_emoji=False)
                else:
                    to_delete.append(
                        await self.ctx.send(f'{self.author.mention}, Invalid channel.'))
                    await asyncio.sleep(5)

        try:
            await self.channel.delete_messages(to_delete)
        except Exception:
            pass

    async def set_default_channel(self):
        to_delete = [await self.ctx.send(
            f'{self.author.mention}\nWhich channel would you want to set the default event alert?\n'
            f'Please mention/enter channel or None to unset channel.\n'
            f'The bot will automatically create webhook for you.')]

        def message_check(m):
            if m.author.id == self.author.id and m.channel.id == self.channel.id:
                if m.clean_content.lower() == 'exit':
                    raise SessionTimeout
                if m.clean_content.isdigit() or len(m.channel_mentions) == 1 or m.clean_content.lower() == 'none':
                    return True
            return False

        try:
            msg = await self.bot.wait_for('message', check=message_check, timeout=30.0)
        except (discord.NotFound, discord.Forbidden, aiohttp.ClientResponseError):
            to_delete.append(await self.ctx.send(f'{self.author.mention}, Input session closed.'))
            await asyncio.sleep(4)
        else:
            to_delete.append(msg)

            if msg.clean_content.lower() == 'none' or (msg.clean_content.isdigit() and int(msg.clean_content) == 0):
                # Check if it's not already empty
                if self.guild_config['events']['default_webhook_data'] is not None:
                    # Try delete old webhook
                    try:
                        splitted_webhook_data = self.guild_config['events']['default_webhook_data'].split('/')
                        old_webhook = Webhook.partial(splitted_webhook_data[0], splitted_webhook_data[1],
                                                      adapter=AsyncWebhookAdapter(self.bot.http_session))
                        await old_webhook.delete(
                            reason=f'Member: {self.author.id} deleted channel for default alert.')
                    except Exception:
                        pass

                    to_update = {}
                    for event in SKYBLOCK_EVENTS.keys():
                        # Try disable event if event webhook url is empty
                        if self.guild_config['events'][event]['webhook_data'] is None:
                            self.guild_config['events'][event]['enabled'] = False
                            to_update.update({f'events.{event}.enabled': False})

                    to_update.update({'events.default_webhook_data': None})
                    self.guild_config['events']['default_webhook_data'] = None
                    await self.guilds_db.update_one({'_id': self.guild_config['_id']}, {'$set': to_update})

                    await self.default_page(with_emoji=False)
            else:
                if msg.clean_content.isdigit():
                    channel = self.guild.get_channel(int(msg.clean_content))
                else:
                    channel = self.guild.get_channel(msg.raw_channel_mentions[0])

                if isinstance(channel, TextChannel):
                    webhook_data = self.guild_config['events']['default_webhook_data']

                    # Check if it's not already the same channel
                    if webhook_data is None or webhook_data.split('/')[2] != channel.id:
                        # Try delete old webhook if not the same
                        if webhook_data is not None:
                            try:
                                splitted_webhook_data = webhook_data.split('/')
                                old_webhook = Webhook.partial(splitted_webhook_data[0], splitted_webhook_data[1],
                                                              adapter=AsyncWebhookAdapter(self.bot.http_session))

                                await old_webhook.delete(
                                    reason=f'Member: {self.author.id} deleted channel for default alert.')
                            except Exception:
                                pass

                        # Check webhook permission
                        if not channel.permissions_for(self.guild.me).manage_webhooks:
                            to_delete.append(await send_no_permission_embed(self.ctx))
                            await asyncio.sleep(4)
                            return

                        # Create and update default webhook
                        webhook = await channel.create_webhook(
                            name='Default Skyblock Events Alert',
                            reason=f'Member: {self.author.id} created default webhook for skyblock events alert.')

                        self.guild_config['events'][
                            'default_webhook_data'] = f'{webhook.id}/{webhook.token}/{channel.id}'
                        await self.guilds_db.update_one({'_id': self.guild_config['_id']}, {
                            '$set': {'events.default_webhook_data': f'{webhook.id}/{webhook.token}/{channel.id}'}})

                        await self.default_page(with_emoji=False)
                else:
                    to_delete.append(
                        await self.ctx.send(f'{self.author.mention}, Invalid channel.'))
                    await asyncio.sleep(4)

        try:
            await self.channel.delete_messages(to_delete)
        except Exception:
            pass

    async def set_event_mention(self):
        to_delete = [await self.ctx.send(
            f'{self.author.mention}\nWhich role would you want to set this event mention?\n'
            f'Please mention/enter role or None to unset mention for this event.')]

        def message_check(m):
            if m.author.id == self.author.id and m.channel.id == self.channel.id:
                if m.clean_content.lower() == 'exit':
                    raise SessionTimeout
                if m.clean_content.isdigit() or len(m.role_mentions) == 1 or m.clean_content.lower() == 'none':
                    return True
            return False

        try:
            msg = await self.bot.wait_for('message', check=message_check, timeout=30.0)
        except (asyncio.TimeoutError, SessionTimeout):
            to_delete.append(await self.ctx.send(f'{self.author.mention}, Input session closed.'))
            await asyncio.sleep(5)
        else:
            to_delete.append(msg)

            if msg.clean_content.lower() == 'none' or (msg.clean_content.isdigit() and int(msg.clean_content) == 0):
                # If it's not none already
                if self.guild_config['events'][self.current_page]['mention_id'] is not None:
                    self.guild_config['events'][self.current_page]['mention_id'] = None
                    await self.guilds_db.update_one({'_id': self.guild_config['_id']},
                                                    {'$set': {f'events.{self.current_page}.mention_id': None}})

                    await self.show_event_page(with_emoji=False)
            else:
                if msg.clean_content.isdigit():
                    role = self.guild.get_role(int(msg.clean_content))
                else:
                    role = self.guild.get_role(msg.raw_role_mentions[0])

                if role is not None:
                    # If it's not the same already, set and save it
                    if self.guild_config['events'][self.current_page]['mention_id'] != role.id:
                        self.guild_config['events'][self.current_page]['mention_id'] = role.id
                        await self.guilds_db.update_one({'_id': self.guild_config['_id']},
                                                        {'$set': {f'events.{self.current_page}.mention_id': role.id}})

                        await self.show_event_page(with_emoji=False)
                else:
                    to_delete.append(await self.ctx.send(f'{self.author.mention}, Invalid role.'))
                    await asyncio.sleep(4)

        try:
            await self.channel.delete_messages(to_delete)
        except Exception:
            pass

    async def set_default_mention(self):
        to_delete = [await self.ctx.send(
            f'{self.author.mention}\nWhich role would you want to set default mention?\n'
            f'Please mention/enter role or None to unset default mention.')]

        def message_check(m):
            if m.author.id == self.author.id and m.channel.id == self.channel.id:
                if m.clean_content.lower() == 'exit':
                    raise SessionTimeout
                if m.clean_content.isdigit() or len(m.role_mentions) == 1 or m.clean_content.lower() == 'none':
                    return True
            return False

        try:
            msg = await self.bot.wait_for('message', check=message_check, timeout=30.0)
        except (asyncio.TimeoutError, SessionTimeout):
            to_delete.append(await self.ctx.send(f'{self.author.mention}, Input session closed.'))
            await asyncio.sleep(4)
        else:
            to_delete.append(msg)

            if msg.clean_content.lower() == 'none' or (msg.clean_content.isdigit() and int(msg.clean_content) == 0):
                # If it's not already none
                if self.guild_config['events']['default_mention_id'] is not None:
                    self.guild_config['events']['default_mention_id'] = None
                    await self.guilds_db.update_one({'_id': self.guild_config['_id']},
                                                    {'$set': {'events.default_mention_id': None}})

                    await self.default_page(with_emoji=False)
            else:
                if msg.clean_content.isdigit():
                    role = self.guild.get_role(int(msg.clean_content))
                else:
                    role = self.guild.get_role(msg.raw_role_mentions[0])

                if role is not None:
                    # Check if it's not already the same role
                    if self.guild_config['events']['default_mention_id'] != role.id:
                        self.guild_config['events']['default_mention_id'] = role.id
                        await self.guilds_db.update_one({'_id': self.guild_config['_id']},
                                                        {'$set': {'events.default_mention_id': role.id}})

                        await self.default_page(with_emoji=False)
                else:
                    to_delete.append(await self.ctx.send(f'{self.author.mention}, Invalid role.'))
                    await asyncio.sleep(4)

        try:
            await self.channel.delete_messages(to_delete)
        except Exception:
            pass

    def react_check(self, payload):
        if payload.user_id == self.author.id and payload.message_id == self.message.id:
            to_check = str(payload.emoji)
            emoji_list = self.main_page_emojis if self.current_page == 'default' else self.event_page_emojis

            for (emoji, func, page) in emoji_list:
                if to_check == emoji:
                    self.match = func
                    if page:
                        self.previous_page = self.current_page
                        self.current_page = page
                    return True

        return False

    async def paginate(self):
        """
        Actually paginate the entries and run the interactive loop if necessary.
        """
        self.bot.loop.create_task(self.default_page(first=True))

        while self.paginating:
            try:
                payload = await self.bot.wait_for('raw_reaction_add', check=self.react_check, timeout=120.0)
            except asyncio.TimeoutError:
                if not self.paginating:
                    pass
                self.paginating = False

                emoji_list = [(emoji, None) for (emoji, _, __) in self.main_page_emojis] \
                    if self.current_page == 'default' else [(emoji, None) for (emoji, _, __) in self.event_page_emojis]
                self.bot.loop.create_task(embed_timeout_handler(self.ctx, emoji_list, message=self.message))
                break

            try:
                await self.message.remove_reaction(payload.emoji, discord.Object(id=payload.user_id))
            except Exception:
                pass  # can't remove it so don't bother doing so

            try:
                await self.match()
            except discord.errors.Forbidden as e:
                self.paginating = False
                raise e
