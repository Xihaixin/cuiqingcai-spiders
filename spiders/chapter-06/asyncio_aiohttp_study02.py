import aiohttp
import asyncio

async def fetch(session,url):
    async with session.get(url) as response:
        return await response.text(),response.status


async def main():
    async with aiohttp.ClientSession() as Session:
        html,status = await fetch(Session,'https://cuiqingcai.com')
        print(f'html:{html}...')
        print(f'status:{status}')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())