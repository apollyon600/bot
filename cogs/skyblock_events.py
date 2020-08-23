from discord import Webhook, AsyncWebhookAdapter
from discord.ext import commands
from datetime import datetime

from constants.discord import SKYBLOCK_EVENTS
from utils import Scheduler, EventPages, Embed, checks, current_milli_time, get_guild_config, get_event_estimate_time


# TODO: known issue: magma boss time is a little bit off atm.
class SkyblockEvents(commands.Cog, name='Skyblock'):
    """
    General commands for skyblock
    """

    emoji = '🏝️'

    def __init__(self, bot):
        self.bot = bot
        self.guilds_db = bot.db['guilds']

        self.scheduler = Scheduler(self.__class__.__name__)
        self.event_schedules = {}

    def cog_unload(self):
        """
        Cancel scheduled event tasks.
        """
        self.scheduler.cancel_all()

    @commands.group(invoke_without_command=True)
    async def events(self, ctx):
        """
        Commands for skyblock events.
        """
        await ctx.send_help(ctx.command)

    @events.command()
    @checks.is_guild_admin()
    @commands.max_concurrency(1, per=commands.BucketType.guild, wait=False)
    async def setup(self, ctx):
        """
        Config skyblock events alert for your server.
        """
        guild_config = await get_guild_config(self.guilds_db, ctx=ctx)

        page = EventPages(ctx, guild_config, self.guilds_db)
        await page.paginate()

    @events.group(invoke_without_command=True)
    @checks.is_sbs_admin()
    async def schedule(self, ctx):
        await ctx.send_help(ctx.command)

    @schedule.command()
    @checks.is_sbs_admin()
    async def start(self, ctx, *, event_name):
        """
        Enter <event name> to start that event schedule or `all` to start all.
        """
        _text = ''
        _found = False
        for event in SKYBLOCK_EVENTS.keys():
            if event_name.lower() in (SKYBLOCK_EVENTS[event]['name'].lower(), 'all', event.lower()):
                _found = True
                _text += await self.schedule_event(event)

        if not _found:
            await ctx.send(f'{ctx.author.mention}, Failed to start {event_name}.')
        else:
            await ctx.send(f'{ctx.author.mention}\n{_text}')

    @schedule.command()
    @checks.is_sbs_admin()
    async def stop(self, ctx, *, event_name):
        """ 
        Enter <event name> to stop that event schedule or `all` to stop all.
        """
        _text = ''
        _found = False
        for event in SKYBLOCK_EVENTS.keys():
            if event_name.lower() in (SKYBLOCK_EVENTS[event]['name'].lower(), 'all', event.lower()):
                _found = True
                _text += await self.delete_event_schedule(event)

        if not _found:
            await ctx.send(f'{ctx.author.mention}, Failed to start {event_name}.')
        else:
            await ctx.send(f'{ctx.author.mention}\n{_text}')

    @schedule.command()
    @checks.is_sbs_admin()
    async def status(self, ctx):
        """
        Check all the skyblock event schedules status.
        """
        embed = Embed(
            ctx=ctx,
            title='Current event schedules status',
            description=f'There is currently {len(self.event_schedules)} event schedules.'
        )

        for event in self.event_schedules.values():
            embed.add_field(
                name=f'{SKYBLOCK_EVENTS[event["name"]]["name"]} Status',
                value=f'Current estimate > {datetime.fromtimestamp(event["estimate"] / 1000.0).isoformat(" ", "seconds")}\n'
                      f'Next schedule > {event["time"].isoformat(" ", "seconds")}\n'
                      f'Next schedule type > {event["type"]}',
                inline=False
            )

        await embed.send()

    def _schedule_event_task(self, event_data):
        """
        Schedule an event.
        """
        event_task_id = event_data['task_id']
        event_datetime = event_data['time']

        self.event_schedules[event_task_id] = event_data

        coroutine = self.send_event_alert(event_data) if event_data['type'] == 'alert' else self.get_event_estimate(
            event_data)
        self.scheduler.schedule_at(event_datetime, event_task_id, coroutine)

    async def send_event_alert(self, event_data):
        """
        Send the event alert 5 mins before starting and schedule tasks to get new estimate time.
        """
        del self.event_schedules[event_data['task_id']]

        event = event_data['name']
        _howlong = ((event_data['estimate'] - current_milli_time()) / 1000.0) / 60.0
        _when = datetime.fromtimestamp(event_data["estimate"] / 1000.0).isoformat(" ", "seconds")
        embed = Embed(
            title=f'{SKYBLOCK_EVENTS[event]["name"]} Alert',
            description=f'The event is starting soon in {_howlong:.2f} minutes at {_when}.'
        )

        async for guild in self.guilds_db.find({'events.default_enabled': True, f'events.{event}.enabled': True}):
            self.bot.loop.create_task(self._event_alert(guild, event, embed))

        # Calculate time when to get new estimate time. (20 min after event happened)
        time = datetime.fromtimestamp((event_data['estimate'] / 1000.0) + 1200)

        # Schedule new task to get new estimate
        event_data['task_id'] = id(time)
        event_data['type'] = 'get_estimate'
        event_data['time'] = time

        self._schedule_event_task(event_data)

    async def get_event_estimate(self, event_data):
        """
        Get new event estimate time and schedule tasks to alert the event.
        """
        del self.event_schedules[event_data['task_id']]

        event = event_data['name']
        estimate = await get_event_estimate_time(SKYBLOCK_EVENTS[event]['endpoint'], session=self.bot.http_session)
        if estimate is None or estimate < (current_milli_time() + (300 * 1000)):
            time = (current_milli_time() / 1000.0) + 600
            time = datetime.fromtimestamp(time)

            # Reschedule in 10 mins to get new estimate
            event_data['task_id'] = id(time)
            event_data['time'] = time

            self._schedule_event_task(event_data)
        else:
            time = datetime.fromtimestamp((estimate / 1000.0) - 300.0)

            # Schedule new event alert
            event_data['task_id'] = id(time)
            event_data['type'] = 'alert'
            event_data['estimate'] = estimate
            event_data['time'] = time

            self._schedule_event_task(event_data)

    async def delete_event_schedule(self, event):
        """
        Delete an event schedule given its name and cancel the running task.
        """
        for event_schedule in self.event_schedules.values():
            if event_schedule['name'] == event:
                del self.event_schedules[event_schedule['task_id']]
                self.scheduler.cancel(event_schedule['task_id'])

                return f'{SKYBLOCK_EVENTS[event]["name"]} has been successfully stopped.\n'
        return f'{SKYBLOCK_EVENTS[event]["name"]} is already stopped.\n'

    async def schedule_event(self, event):
        """
        Schedule an event given its name.
        """
        # Check if event is already started
        if any(event == schedule['name'] for schedule in self.event_schedules.values()):
            return f'{SKYBLOCK_EVENTS[event]["name"]} is already running.\n'

        estimate = await get_event_estimate_time(SKYBLOCK_EVENTS[event]['endpoint'], session=self.bot.http_session)
        if estimate is None:
            return f'Failed to schedule {SKYBLOCK_EVENTS[event]["name"]}.\n'

        # Calculate when to alert event (5 mins before event starts)
        time = datetime.fromtimestamp((estimate / 1000.0) - 300.0)

        event_data = {
            'name': event,
            'task_id': id(time),
            'type': 'alert',
            'estimate': estimate,
            'time': time
        }
        self._schedule_event_task(event_data)

        return f'{SKYBLOCK_EVENTS[event]["name"]} has been successfully started.\n'

    async def _event_alert(self, guild_config, event, embed):
        if guild_config['events'][event]['webhook_data'] is not None:
            splitted_webhook_data = guild_config['events'][event]['webhook_data'].split('/')
        else:
            splitted_webhook_data = guild_config['events']['default_webhook_data'].split('/')

        # Get webhook to alert to
        webhook = Webhook.partial(splitted_webhook_data[0], splitted_webhook_data[1],
                                  adapter=AsyncWebhookAdapter(self.bot.http_session))

        embed.timestamp = datetime.now()
        embed.set_footer(
            text='Skyblock Simplified',
            icon_url='https://i.imgur.com/V7ENVHr.png'
        )

        mention_id = guild_config['events'][event]['mention_id']
        if mention_id is None:
            mention_id = guild_config['events']['default_mention_id']

        # Send webhook embed
        try:
            await webhook.send(content=f'<@&{mention_id}>' if mention_id else '', embed=embed,
                               username=f'{SKYBLOCK_EVENTS[event]["name"]} Alert',
                               avatar_url='https://i.imgur.com/Fhx03E7.png')
        except Exception:
            await self._handle_failed_webhook_send(guild_config, event, int(guild_config['_id']))

    async def _handle_failed_webhook_send(self, guild_config, event, guild_id):
        # Try to send message to owner that it's failed
        try:
            guild = self.bot.get_guild(guild_id)
            owner = guild.owner

            await owner.send(
                f'{owner.mention}\nFailed to send {SKYBLOCK_EVENTS[event]["name"]} to the configurated channel.\n'
                f'This may be due to not enough permission or someone deleted the webhook.\n'
                f'Please configure again with `sbs events setup`.')
        except Exception:
            pass

        # Set enabled to false, webhook/channel to none
        await self.guilds_db.update_one({'_id': guild_config['_id']},
                                        {'$set': {f'events.{event}.enabled': False,
                                                  f'events.{event}.webhook_data': None}})


def setup(bot):
    bot.add_cog(SkyblockEvents(bot))
