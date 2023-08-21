from bs4 import BeautifulSoup
import requests
import logging
import time

logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')
requests.packages.urllib3.disable_warnings()

BASE_URL = r'https://www.xincanshu.com'
CPU_ROOT = BASE_URL + '/cpu'
XJB_ROOT = CPU_ROOT + '/tiantipaihang-xingjiabi.html'
DH_ROOT = CPU_ROOT + '/tiantipaihang-duohe.html'
DAH_ROOT = CPU_ROOT + '/tiantipaihang-danhe.html'
HX_ROOT = CPU_ROOT + '/tiantipaihang-hexian.html'
NEWEST_ROOT = CPU_ROOT + '/tiantipaihang-zuixin.html'
URL_LIST = [CPU_ROOT, XJB_ROOT, DH_ROOT, DAH_ROOT, HX_ROOT, NEWEST_ROOT]

# proxies = {
#     'http': '127.0.0.1:7078',
#     'https': '127.0.0.1:7078'
# }
#
# response = requests.get(CPU_ROOT, proxies=proxies, verify=False)
# # logging.debug(response)
# if response.status_code == 200:
#     html_doc = response.text
#
# soup = BeautifulSoup(html_doc, 'html.parser')
# externals = soup.find_all('a', 'external')
#
# for external in externals:
#     name = external.attrs['title']
#     cur_url = BASE_URL + external.attrs['href'] + r'canshu.html'
#     response = requests.get(cur_url, proxies=proxies, verify=False)
#     soup2 = BeautifulSoup(response.text, 'html.parser')
#     targets = soup2.find_all(attrs={'data-text': '支持最大内存'})
#     for target in targets:
#         capacity = target.find('td', 'hover_edit_param').span.text.strip()
#         logging.info(f'{name}\t{capacity}')


def getCapability(root_url) -> int:
    proxies = {
        'http': '127.0.0.1:7078',
        'https': '127.0.0.1:7078'
    }

    response = requests.get(root_url, proxies=proxies, verify=False)
    if response.status_code == 200:
        html_doc = response.content.decode('utf-8')
    else:
        return response.status_code

    soup = BeautifulSoup(html_doc, 'html.parser')
    externals = soup.find_all('a', 'external')

    for external in externals:
        if 'title' not in external.attrs:
            continue
        name = external.attrs['title']
        cur_url = BASE_URL + external.attrs['href'] + r'canshu.html'
        response = requests.get(cur_url, proxies=proxies, verify=False)
        soup2 = BeautifulSoup(response.text, 'html.parser')
        targets = soup2.find_all(attrs={'data-text': '支持最大内存'})
        for target in targets:
            capacity = target.find('td', 'hover_edit_param').span.text.strip()
            logging.info(f'{name}\t{capacity}')

    return 200


for cur_url in URL_LIST:
    logging.info("#####################################")
    logging.info("#####################################")
    count = 0
    if getCapability(cur_url) != 200 and count < 5:
        count += 1
        logging.warning(f'第{count}次失败，休眠5秒')
        time.sleep(5)
    logging.info("#####################################")
    logging.info("#####################################")
