import aiohttp
import pymongo
import motor
import logging
import asyncio
import json

LIMIT = 18
SCRAPE_PAGE = 50
CONCURRENCY = 5 #定义最大并发量
INDEX_URL = 'https://spa5.scrape.center/api/book/?limit=18&offset={offset}'
DETAIL_URL = 'https://spa5.scrape.center/api/book/{id}'


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

semaphore = asyncio.Semaphore(CONCURRENCY)
session = None

async def scrape_api(url):
    async with semaphore:
        try:
            logging.info('Scraping %s ...', url)
            async with session.get(url) as response:    # type: ignore
                response.raise_for_status()  # 将抛出HTTP错误异常
                data = await response.json()
                return data
        except aiohttp.ClientError as e:
            logging.error('Client error occurred while scraping %s: %s', url, e)
        except json.JSONDecodeError as e:
            logging.error('JSON decode error occurred: %s', e)
        except Exception as e:
            logging.error('An unexpected error occurred: %s', e)
        return None

async def scrape_index(page):
    url = INDEX_URL.format(offset=LIMIT*(page-1))
    return await scrape_api(url)

from motor.motor_asyncio import AsyncIOMotorClient
MONGO_CONNECTION_STRING = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'books'
MONGO_COLLECTION_NAME = 'books'
client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

async def save_data(data):
    if data is not None:
        logging.info('saving data %s', data)
        return await collection.update_one({
            'id': data.get('id')
        }, {
            '$set': data
        }, upsert=True)
    else:
        logging.error('No data to save')
        return None

async def scrape_detail(id):
    url = DETAIL_URL.format(id=id)
    data = await scrape_api(url)
    await save_data(data)


async def main():
    global session
    try:
        session = aiohttp.ClientSession()
        scrape_index_tasks = [asyncio.ensure_future(scrape_index(page)) for page in range(1, SCRAPE_PAGE + 1)]
        results = await asyncio.gather(*scrape_index_tasks, return_exceptions=True)
        logging.info('result %s', json.dumps(results, ensure_ascii=False, indent=2))
        ids = []
        for index_data in results:
            if isinstance(index_data, Exception):
                logging.error('Error during index scrape: %s', index_data)
                continue
            if not index_data:
                continue
            for item in index_data.get('results'): # type: ignore
                ids.append(item.get('id'))
        scrape_detail_tasks = [asyncio.ensure_future(scrape_detail(id)) for id in ids]
        await asyncio.wait(scrape_detail_tasks)
    finally:
        await session.close() # type: ignore
   

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
