import aiohttp
import asyncio

from . import APIKeyError, HypixelAPIError, session


class HypixelApiInterface:
    def __next_key__(self):
        self.__key_id__ += 1
        if self.__key_id__ == len(self._api_keys):
            self.__key_id__ = 0
        return self._api_keys[self.__key_id__]

    async def __call_api__(self, api, **kwargs):
        kwargs['key'] = self.__next_key__()
        url = f'https://api.hypixel.net{api}'

        try:
            async with (await session()).get(url, params=kwargs) as data:
                data = await data.json(content_type=None)

                if data['success']:
                    return data
                elif data['cause'] == 'Invalid API key!':
                    raise APIKeyError(kwargs["key"], f'Invalid API key')
                else:
                    raise HypixelAPIError(data['cause'])

        except asyncio.TimeoutError:
            return await self.__call_api__(api, **kwargs)

        except aiohttp.ClientResponseError as e:
            if e.status == 403:
                raise HypixelAPIError(f'Your request to {url} was not granted')
            elif e.status == 429:
                raise HypixelAPIError('You are being ratelimited')
            elif e.status == 500:
                raise HypixelAPIError('Hypixel\'s servers could not complete your request')
            elif e.status == 502:
                raise HypixelAPIError('Hypixel\'s API is currently not working. Please try again in a few minutes.')
            else:
                raise e from None

    # noinspection PyArgumentList
    async def __new__(cls, api_keys, *args, **kwargs):
        instance = super().__new__(cls)

        if isinstance(api_keys, str):
            instance._api_keys = [api_keys]
        else:
            instance._api_keys = api_keys

        instance.__key_id__ = 0

        await instance.__init__(api_keys, *args, **kwargs)
        return instance
