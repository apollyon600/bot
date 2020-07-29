import aiohttp
import asyncio
from typing import Optional
from urllib.parse import quote


class ResponseCodeError(ValueError):
    """
    Exception raised when a non-OK HTTP response is received.
    """

    def __init__(
            self,
            response: aiohttp.ClientResponse,
            response_json: Optional[dict] = None,
            response_text: str = ""
    ):
        self.status = response.status
        self.response_json = response_json or {}
        self.response_text = response_text
        self.response = response

    def __str__(self):
        response = self.response_json if self.response_json else self.response_text
        return f"Status: {self.status} Response: {response}"


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
        if should_raise and response.status >= 400:
            try:
                response_json = await response.json()
                raise ResponseCodeError(response=response, response_json=response_json)
            except aiohttp.ContentTypeError:
                response_text = await response.text()
                raise ResponseCodeError(response=response, response_text=response_text)

    async def request(self, method: str, endpoint: str, *, raise_for_status: bool = True, **kwargs):
        """
         A HTTP request to the Hypixel API and return the JSON response.
         """
        await self._ready.wait()

        kwargs['params']['key'] = self.key
        async with self.session.request(method.upper(), self._url_for(endpoint), **kwargs) as resp:
            await self.maybe_raise_for_status(resp, raise_for_status)
            return await resp.json()

    async def get(self, endpoint: str, *, raise_for_status: bool = True, **kwargs):
        """
        Hypixel API Get.
        """
        return await self.request("GET", endpoint, raise_for_status=raise_for_status, **kwargs)
