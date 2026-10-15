import requests
import logging
from bs4 import BeautifulSoup

TOTAL_PAGE = 50
BASIC_URL = 'https://q.elecfans.com/c/p{page}/'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')
def scrape_url(url):
    logging.info('Scraping url %s...',url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        logging.info('Scraping %s meet error while the status is %s',url,response.status_code)
    except requests.RequestException:
        logging.error('error occurred while scraping %s',url,exc_info=True)

def scrape_index(index):
    url = BASIC_URL.format(page=index)
    return scrape_url(url)

def scrape_detail(html):
    list_company = []
    soup = BeautifulSoup(html,'lxml')
    lis_data = soup.find('ul',attrs={'data-v-d575652c':True}).find_all(name='li') # type: ignore
    for li in lis_data:  # type: ignore
        a_herf = li.find('a').attrs['href']
        # 获取公司logo
        img = li.find('img').attrs['src']
        if img[:5]!='https':
            img_https = 'https'+img
        else:img_https = img
        # 获取公司简称和全称
        head_name = li.find('h5').string.strip()
        company_name = li.find(class_='companyName').string.strip()
        company={'aherf':a_herf,'img_https':img_https,
                 'head_name':head_name,'company_name':company_name
                 }
        # 为该公司添加标签
        # 检查 'tags' 键是否存在于字典中
        if 'tags' not in company:
            # 如果不存在，初始化一个空列表
            company['tags'] = []

        tags_div = li.find(class_='tags')

        if tags_div:
            span_tags = tags_div.find_all('span')
            for span in span_tags:
                company['tags'].append(span.text.strip())
        else:company['tags'] = ''

        list_company.append(company)
    logging.info('The company information:%s',list_company)

def main():
    for page in range(1,TOTAL_PAGE+1):
        res = scrape_index(page)
        scrape_detail(res)
        
    

if __name__ == '__main__':
    main()
   
    
