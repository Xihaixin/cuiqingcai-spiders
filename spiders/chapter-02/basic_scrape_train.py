import re
import requests
from urllib.parse import urljoin
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGE = 10
def scrape_page(url):
    logging.info('scraping%s...',url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        logging.error('get invalid status code %s while scraping %s',response.status_code,url)
    except requests.RequestException:
        logging.error('error occurred while scraping %s',url,exc_info=True)

def scrape_index(page):
    index_url = f'{BASE_URL}/page/{page}'
    return scrape_page(index_url)

def parse_index(html):
    pattern = re.compile('<a .*href="(.*?)".*? class="name">')
    items = re.findall(pattern,html)
    if not items:
        return []
    for item in items:
        detail_url = urljoin(BASE_URL,item)
        logging.info('get detail url %s',detail_url)
        yield detail_url
# def main():
#     for page in range(1,TOTAL_PAGE+1):
#         index_html = scrape_index(page)
#         detail_urls = parse_index(index_html)
#         for detail_url in detail_urls:
#             detail_html = scrape_detail(detail_url)
#             data = parse_detail(detail_html)
#             logging.info('get detail data %s',data)
#             logging.info('saving data to json file')
#             save_data(data)
#             logging.info('data saved successfully')


## 改写main()方法，进行多进程加速
def main(page):
    index_html = scrape_index(page)
    detail_urls = parse_index(index_html)
    for detail_url in detail_urls:
        detail_html = scrape_detail(detail_url)
        data = parse_detail(detail_html)
        logging.info('get detail data %s',data)
        logging.info('saving data to json file')
        save_data(data)
        logging.info('data saved successfully')

     
        
def scrape_detail(url):
    return scrape_page(url)

def parse_detail(html):
    cover_pattern = re.compile('class="item.*?<img.*?src="(.*?)".*?class="cover">',re.S)
    name_pattern = re.compile('<h2.*?>(.*?)</h2>')
    categories_pattern = re.compile('<button.*?category.*?<span>(.*?)</span>.*?</button>',re.S)
    published_at_pattern = re.compile('(\d{4}-\d{2}-\d{2}\s?上映)') # type: ignore
    drama_pattern = re.compile('<div.*?drama.*?>.*?<p.*?>(.*?)</p>',re.S)
    score_pattern = re.compile('<p.*?score.*?>(.*?)</p>',re.S)

    cover = re.search(cover_pattern,html).group(1).strip() if re.search(cover_pattern,html) else None # type: ignore
    name = re.search(name_pattern,html).group(1).strip() if re.search(name_pattern,html) else None # type: ignore
    categories = re.findall(categories_pattern,html) if re.search(categories_pattern,html) else None 
    published_at = re.search(published_at_pattern,html).group(1).strip() if re.search(published_at_pattern,html) else None # type: ignore
    drama = re.search(drama_pattern,html).group(1).strip() if re.search(drama_pattern,html) else None # type: ignore
    score = float(re.search(score_pattern,html).group(1).strip()) if re.search(score_pattern,html) else None # type: ignore

    return {
        'cover':cover,
        'name':name,
        'categories':categories,
        'pubilshed_at':published_at,
        'drama':drama,
        'score':score
    }

# import json
# from os import makedirs
# from os.path import exists

# RESULTS_DIR = 'results'
# exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

# def save_data(data):
#     name = data.get('name')
#     data_path = f'{RESULTS_DIR}/{name}.json'
#     json.dump(data,open(data_path,'w',encoding='utf-8'),ensure_ascii=False,indent=2)

import json
import re
from os import makedirs
from os.path import exists

RESULTS_DIR = 'results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

def clean_filename(name):
    # 移除或替换文件名中的特殊字符
    return re.sub(r'[<>:"/\\|?*]', '_', name).strip()

def save_data(data):
    try:
        name = data.get('name')
        if not name:  # 确保名称不为空
            logging.error("Data missing 'name' field, cannot save.")
            return
        cleaned_name = clean_filename(name)
        if not cleaned_name:
            logging.error("Filename is invalid or too long after cleaning.")
            return
        data_path = f'{RESULTS_DIR}/{cleaned_name}.json'
        with open(data_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
        logging.info(f'Data saved successfully to {data_path}')
    except IOError as e:
        logging.error(f"Failed to write data to {data_path}: {e}")
    except TypeError as e:
        logging.error(f"Failed to serialize data to JSON: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

import multiprocessing

if __name__ == '__main__':
    pool = multiprocessing.Pool()
    pages = range(1,TOTAL_PAGE+1)
    pool.map(main,pages)
    pool.close()
    pool.join()
