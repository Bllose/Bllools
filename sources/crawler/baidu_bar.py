from bs4 import BeautifulSoup
import requests
import logging
import time
import uuid

"""
百度贴吧趴图
"""

logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')
requests.packages.urllib3.disable_warnings()

BASE_URL = r'https://tieba.baidu.com'
ROOT_URL = BASE_URL + r'/p/8415941629?pn=1'
DOWNLOAD_ROOT = r'C:\Users\bllos\Pictures\灯光画\temp'

response = requests.get(ROOT_URL, verify=False)
if response.status_code == 200:
    html_doc = response.content.decode('utf-8')
else:
    logging.warning()

soup = BeautifulSoup(html_doc, 'html.parser')
imgs = soup.find_all('img', class_= 'BDE_Image')

counter = 1
for img in imgs:
    download_url = img.attrs['src']
    download = requests.get(download_url)
    with open(DOWNLOAD_ROOT + r'\\' + str(uuid.uuid1()) + '.jpg', 'wb') as pic:
        pic.write(download.content)
        logging.info(f'完成第{counter}张图片下载')
        counter += 1