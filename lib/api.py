import aiohttp
import asyncio
from urllib.parse import quote

from . import Player
from . import HypixelResponseCodeError, HypixelAPITimeout, HypixelAPINoSuccess, HypixelAPIRateLimitError


class HypixelAPIClient:
    """
    Hypixel API wrapper.
    """

    _url = 'https://api.hypixel.net'

    def __init__(self, api_key, loop: asyncio.AbstractEventLoop, **kwargs):
        self.key = api_key
        self.loop = loop
        self.session = None

        self._ready = asyncio.Event(loop=loop)
        self._creation_task = None
        self._default_session_kwargs = kwargs

        self.recreate()

    @classmethod
    def _url_for(cls, endpoint: str) -> str:
        return f"{cls._url}/{quote(endpoint)}"

    def recreate(self, force: bool = False, **session_kwargs):
        """
        Schedule the aiohttp session to be created with `session_kwargs` if it's been closed.

        If `force` is True, the session will be recreated even if an open one exists. If a task to
        create the session is pending, it will be cancelled.

        `session_kwargs` is merged with the kwargs given when the `APIClient` was created and
        overwrites those default kwargs.
        """
        if force or self.session is None or self.session.closed:
            if force and self._creation_task:
                self._creation_task.cancel()

            # Don't schedule a task if one is already in progress.
            if force or self._creation_task is None or self._creation_task.done():
                self._creation_task = self.loop.create_task(self._create_session(**session_kwargs))

    async def _create_session(self, **session_kwargs):
        """
        Create the aiohttp session with `session_kwargs` and set the ready event.

        `session_kwargs` is merged with `_default_session_kwargs` and overwrites its values.
        If an open session already exists, it will first be closed.
        """
        await self.close()
        self.session = aiohttp.ClientSession(**{**self._default_session_kwargs, **session_kwargs})
        self._ready.set()

    async def close(self):
        """
        Close the aiohttp session and unset the ready event.
        """
        if self.session:
            await self.session.close()

        self._ready.clear()

    @staticmethod
    async def maybe_raise_for_status(response: aiohttp.ClientResponse, should_raise: bool):
        """
        Raise ResponseCodeError for non-OK response if an exception should be raised.
        """
        if should_raise and response.status == 429:
            raise HypixelAPIRateLimitError
        elif should_raise and response.status >= 400:
            try:
                response_json = await response.json()
                raise HypixelResponseCodeError(response=response, response_json=response_json)
            except aiohttp.ContentTypeError:
                response_text = await response.text()
                raise HypixelResponseCodeError(response=response, response_text=response_text)

    async def request(self, method: str, endpoint: str, *, raise_for_status: bool = True, **kwargs):
        """
        A HTTP request to the Hypixel API and return the JSON response.
        """
        await self._ready.wait()

        if 'params' not in kwargs:
            kwargs['params'] = {}
        kwargs['params']['key'] = self.key
        try:
            async with self.session.request(method.upper(), self._url_for(endpoint), **kwargs) as resp:
                await self.maybe_raise_for_status(resp, raise_for_status)
                resp = await resp.json()
                if resp is None or 'success' not in resp:
                    raise HypixelAPINoSuccess
                if not resp['success']:
                    raise HypixelAPINoSuccess
                return resp
        except asyncio.TimeoutError:
            raise HypixelAPITimeout

    async def get(self, endpoint: str, *, raise_for_status: bool = True, **kwargs):
        """
        Hypixel API Get.
        """
        return await self.request("GET", endpoint, raise_for_status=raise_for_status, **kwargs)

    async def get_player(self, uname, uuid, *, raise_for_status: bool = True, **kwargs):
        """
        Hypixel API get player, return player object.
        """
        data = await self.get('player', raise_for_status=raise_for_status, **{**{'params': {'uuid': uuid}}, **kwargs})
        return Player(
            uname=uname,
            uuid=uuid,
            player_data=data['player'],
            hypixel_api_client=self
        )

    async def get_skyblock_profiles(self, uuid, *, raise_for_status: bool = True, **kwargs):
        """
        Hypixel API get skyblock profiles.
        """
        data = await self.get('skyblock/profiles', raise_for_status=raise_for_status,
                              **{**{'params': {'uuid': uuid}}, **kwargs})
        return data['profiles']

    async def get_key_status(self, *, raise_for_status: bool = True, **kwargs):
        """
        Hypixel API get key status.
        """
        data = await self.get('key', raise_for_status=raise_for_status, **kwargs)
        return data['record']
