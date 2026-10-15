import requests
import logging
import time

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

TOTAL_NUMBER = 20
URL = 'https://www.httpbin.org/delay/5'

start_time = time.time()
for _ in range(TOTAL_NUMBER):
    logging.info('scraping url %s',URL)
    response = requests.get(URL)

end_time = time.time()

logging.info('total time %s seconds',end_time-start_time)