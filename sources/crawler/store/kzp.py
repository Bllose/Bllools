from bs4 import BeautifulSoup
import requests
import logging
import time
import uuid

"""
针对快转铺进行数据爬取
https://sz.kuaizhuanpu.com/
"""

HOST_URL = r'https://sz.kuaizhuanpu.com'
PAGE_URL = r'/s?s_type=&s_isnull=&s=&s_consort={s_consort}&s_addresscode={s_addresscode}&s_minsize=&s_maxsize=&s_min_price_month=&s_max_price_month=&s_storetype=0&price_px=&size_px=&time_px=&s_hosttype=&pageno={pageno}'
header = {
'Authority': 'sz.kuaizhuanpu.com',
'Method': 'GET',
'Path': '/s?s_type=1&s_isnull=&s=&s_consort=001&s_addresscode=001007004010&s_minsize=&s_maxsize=&s_min_price_month=&s_max_price_month=&s_storetype=0&price_px=&size_px=&time_px=&s_hosttype=',
'Scheme': 'https',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9',
'Cookie': 'Hm_lvt_73e234ff52a5e233f00d95fb94bcc0e9=1686652547,1686747829; kaitou=sz; ASPSESSIONIDAAQTADDA=JIEPJMNAJIPMIHIDGPFFFMDB; ASPSESSIONIDACQSCBCA=MKCHDMNACDILGCIEHDFAAHDL; ASPSESSIONIDASSSRCRC=EHGLPMNAFNNHLFFIMDPMEPEP; ASPSESSIONIDAAQSCBCA=IPELKMNAPAALPLOHKNABEJCH; ASPSESSIONIDCQSSQASC=IJAIMLNANGDHDJEJIMHLEHCL; ASPSESSIONIDAARSDACA=BGKDINNAAIAIPOIIFMOFFKBF; ASPSESSIONIDCQQSSDQC=LIMFONNAAPFGGLLCFDPDNJFJ; ASPSESSIONIDCSQTQASD=NHPFGONAKALHNEKDGPKAMNDK; ASPSESSIONIDAAQRCBCB=AKHPNMNABAPFCOBFABCJCMKM; ASPSESSIONIDCQSSRASD=ANIPMPNAOPDCELJGJBLEKCHP; ASPSESSIONIDCCTQBADB=JDJHOBOAPDELEEHKHJPONJJM; Hm_lpvt_73e234ff52a5e233f00d95fb94bcc0e9=1686751350',
'Referer': 'https://sz.kuaizhuanpu.com/s?s_type=1&s_isnull=&s=&s_consort=001&s_addresscode=001007004009&s_minsize=&s_maxsize=&s_min_price_month=&s_max_price_month=&s_storetype=0&price_px=&size_px=&time_px=&s_hosttype=',
'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
'Sec-Ch-Ua-Mobile': '?0',
'Sec-Ch-Ua-Platform': '"Windows"',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

s_consort='001'         # 酒楼餐饮
BAO_AN = {
    # '001007004',        # 宝安(不限)
    '001007004000': '宝安周边',     # 宝安（宝安周边）
    '001007004001': '翻身路',     # 宝安(翻身路)
    '001007004002': '宝安中心区',     # 宝安(宝安中心区）
    '001007004003': '福永',     # 宝安(福永）
    '001007004004': '沙井',     # 宝安(沙井）
    '001007004005': '石岩',     # 石岩
    '001007004006': '松岗',     # 松岗
    '001007004007': '桃源居',     # 桃源居
    '001007004008': '新安',     # 新安
    '001007004009': '新中心区',     # 新中心区
    '001007004010': '西乡',     # 西乡
}

LONG_GANG = {
    '001007005000': '横岗',
    '001007005001': '坂田',
    '001007005002': '龙岗中心城',
    '001007005003': '平湖',
    '001007005004': '坪地',
    '001007005005': '大运新城',
    '001007005006': '万科城',
    '001007005007': '龙岗周边',
}

LONG_HUA = {
    '001007009000': '大浪',
    '001007009001': '观澜',
    '001007009002': '金地梅陇镇',
    '001007009003': '锦绣江南',
    '001007009004': '莱蒙水榭春天',
    '001007009005': '龙华',
    '001007009006': '龙华中心区',
    '001007009007': '龙华周边',
    '001007009008': '美丽365花园',
    '001007009009': '梅林关口',
    '001007009010': '民治',
    '001007009011': '深圳北站',
    '001007009012': '世纪春城',
}

BU_JI = {
    '001007006000': '百鸽笼',
    '001007006001': '布吉关',
    '001007006002': '布吉街',
    '001007006003': '布吉周边',
    '001007006004': '长龙',
    '001007006005': '大芬村',
    '001007006006': '丹竹头',
    '001007006007': '康桥',
    '001007006008': '丽湖',
    '001007006009': '木棉湾',
    '001007006010': '南岭',
    '001007006011': '下水径',
    '001007006012': '信义',
    '001007006013': '又一村',
    '001007006014': '中海怡翠',
}

def lastest_info(code):
    preUrl = PAGE_URL.replace('{s_consort}', s_consort)
    preUrl = preUrl.replace('{s_addresscode}', code)

    for index in range(1, 2):
        stopping = False
        currentUrl = preUrl.replace('{pageno}', str(index))
        response = requests.get(HOST_URL + currentUrl)
        if response.status_code == 200:
            html_doc = response.content.decode('utf-8')
            soup = BeautifulSoup(html_doc, 'html.parser')
            currentStoreList = soup.find_all('div', class_='search-list-box')[0].find_all('div', class_='list')[0].find_all('li')
            for currentStore in currentStoreList:
                title = currentStore.find('div', class_='demo').find('div', class_='title').text.strip()
                path = currentStore.find('div', class_='demo').find('div', class_='title').find('a').attrs['href']
                type = currentStore.find('div', class_='demo').find('div', class_='text f').text.strip()
                address = currentStore.find('div', class_='demo').find('div', class_='text d').text.strip()
                phone = currentStore.find('div', class_='demo').find('div', class_='phonebox').contents[1].replace('<div class="phone">', '').replace('</div>', '')
                redtime = currentStore.find('div', class_='demo').find('div', class_='phonebox').find('span', class_='redtime')
                if redtime:
                    redtime = redtime.text.replace('\n', '\t')
                else:
                    stopping = True
                    break
                square, zujin, prices, rate = price_analysis(currentStore.find('div', class_='price').text.split('\n'))


                print(f'最新\t{title}\t{type}\t{address}\t{phone}\t{square}\t{zujin}\t{rate}\t{prices}\t{redtime}\t{HOST_URL}{path}')
            if stopping:
                break
        else:
            print(f'{response.status_code}\t{response.content}\t{response.text}')
            break


def price_analysis(priceArray):
    square = priceArray[1].replace('面  积：', '')
    zujin = priceArray[2].replace('租  金：', '').replace('/月', '').replace(',', '').replace('元', '')
    square_number = float(square.replace('平方米', ''))
    if '万' in zujin:
        zujin = float(zujin.replace('万', '')) * 10000
    rate = int(zujin) / square_number / 30
    prices = priceArray[3]

    if '面议' in prices:
        prices = '面议'
    else:
        prices = prices.replace('转手费：', '').replace('元', '')
        if '万' in prices:
            prices = float(prices.replace('万', ''))
            prices = str(int(prices * 10000))
    return square_number, zujin, prices, '{:.2f}'.format(rate)


def more_info(area: str, name: str):
    preUrl = PAGE_URL.replace('{s_consort}', s_consort)
    preUrl = preUrl.replace('{s_addresscode}', area)

    for index in range(1, 50):
        currentUrl = preUrl.replace('{pageno}', str(index))
        response = requests.get(HOST_URL + currentUrl)
        if response.status_code == 200:
            html_doc = response.content.decode('utf-8')
            soup = BeautifulSoup(html_doc, 'html.parser')
            fanye = soup.find_all('div', class_='fanye')[0].find('a', class_='cur')
            if not fanye:
                return
            fanye = int(fanye.text)
            if index > fanye:
                break
            currentStoreList = soup.find_all('div', class_='search-list-box')[0].find_all('div', class_='list')[0].find_all('li')
            for currentStore in currentStoreList:
                title = currentStore.find('div',class_='demo').find('div', class_='title').text.strip()
                path = currentStore.find('div', class_='demo').find('div', class_='title').find('a').attrs['href']
                type = currentStore.find('div',class_='demo').find('div', class_='text f').text.strip()
                address = currentStore.find('div', class_='demo').find('div', class_='text d').text.strip()
                phone = currentStore.find('div', class_='demo').find('div', class_='phonebox').contents[1].replace('<div class="phone">', '').replace('</div>', '')
                square, zujin, prices, rate = price_analysis(currentStore.find('div', class_='price').text.split('\n'))
                print(f'{name}\t{title}\t{type}\t{address}\t{phone}\t{square}\t{zujin}\t{rate}\t{prices}\t{HOST_URL}{path}')
        else:
            print(f'{response.status_code}\t{response.content}\t{response.text}')
            break


if __name__ == '__main__':

    # lastest_info('001007004')
    # for key, value in BAO_AN.items():
    #     more_info(key, value)

    # lastest_info('001007005')
    # for key, value in LONG_GANG.items():
    #     more_info(key, value)

    # lastest_info('001007009')
    # for key, value in LONG_HUA.items():
    #     more_info(key, value)

    lastest_info('001007006')
    for key, value in BU_JI.items():
        more_info(key, value)