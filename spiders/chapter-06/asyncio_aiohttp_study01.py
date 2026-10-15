import time
import requests
import aiohttp
import asyncio

start_time = time.time()
async def get(url):
    session = aiohttp.ClientSession()
    response = await session.get(url)
    await response.text()   # 这里是什么？
    await session.close()
    return response

async def request():
    url = 'https://www.httpbin.org/delay/5'
    print('Waiting for ',url)
    response = await get(url)
    print('Get response from ',url,'response->',response)

tasks = [asyncio.ensure_future(request()) for _ in range(10)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

end_time = time.time()
print('Total time :',end_time-start_time)