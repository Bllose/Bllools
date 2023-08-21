from bs4 import BeautifulSoup
import requests
import logging
import time

"""
英特尔官网针对CPU的信息列表
用来爬取指定信息进行输出比较
"""

logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')
requests.packages.urllib3.disable_warnings()

BASE_URL = r'https://www.intel.cn'
ROOT_URL = BASE_URL + r'/content/www/cn/zh/products/details/processors/celeron/products.html'

response = requests.get(ROOT_URL, verify=False)
if response.status_code == 200:
    html_doc = response.content.decode('utf-8')
else:
    logging.warning()

soup = BeautifulSoup(html_doc, 'html.parser')
tables = soup.find_all('tbody')

for table in tables:
    links = table.find_all('a')
    for link in links:
        name = link.text
        curr_url = BASE_URL + link.attrs['href']
        response1 = requests.get(curr_url, verify=False)
        if response1.status_code == 200:
            html_doc_1 = response1.content.decode('utf-8')
        else:
            logging.warning()
        cur_soup = BeautifulSoup(html_doc_1, 'html.parser')
        kuozhan = cur_soup.find_all('div', id='specs-1-0-5')
        if kuozhan:
            context = kuozhan[0].text.strip().replace('\n\n\n\n\n', ' ').replace('\n', '')
            print(f'{name}\t{context}')
        else:
            print(f'{name}\tno info')