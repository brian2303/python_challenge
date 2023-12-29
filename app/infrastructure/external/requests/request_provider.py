import aiohttp


class RequestsProvider:

    @classmethod
    async def fetch(cls, session, params, url):
        async with session.get(url, params=params) as response:
            if response.status == 200:
                return await response.json()

    async def get_request(self, params, url):
        async with aiohttp.ClientSession() as session:
            response = await self.fetch(session, params, url)
            return response
