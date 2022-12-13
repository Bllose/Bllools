from bllools.spider.warrior.Warrior import Warrior
import logging
import os
import time
import random
import requests
from openpyxl import drawing
from PIL import Image
from PIL import ImageDraw
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

class dajiyuan(Warrior):
    def __init__(self,
                 root: str,
                 save_path: str,
                 begin: int,
                 max=2) -> None:
        super(dajiyuan, self).__init__(root, save_path, begin, max)

    def start(self):
        Warrior.start(self)

    # 获取主页面逻辑入口
    def getPages(self) -> list:
        rsp = self.myGetFunc(self.root)
        while rsp is None:
            logging.info('重试一次获取主页逻辑入口 ...')
            rsp = self.myGetFunc(self.root)
        self.getPageList(rsp.text)

    def getPageList(self, htmlStr: str) -> list:
        from lxml import etree
        html = etree.HTML(htmlStr)
        html_data = html.xpath('//*[@id="readme"]/article/table/tbody/tr[34]/td/h3/a')

        self.pagesUrlList = []
        for curPageLink in html_data:
            self.pagesUrlList.append(curPageLink.attrib['href'])
        del (self.pagesUrlList[0])  # 第一页无用， 直接丢掉

    def recorder(self, subUrl: str) -> None:
        counter = 1
        while self.tryBestForUrl(subUrl):
            logging.debug('重试 %d 次...', counter)
            counter += 1
            if counter > 10:
                logging.warning('地址重试多次后依然无法联通，跳过该地址：%s', subUrl)
                return
        self.driver.implicitly_wait(3)

        try:
            title = self.driver.find_element(by=By.XPATH, value='//*[@id="readme"]/article/table/tbody/tr[3]/td[1]/h2[1]')
            print(subUrl, title.text)
        except:
            print('当前网页没有主题，无法记录信息，跳过该页。 网址: %s', subUrl)
            second = random.randint(5, 15)
            logging.debug('休眠%d秒...', second)
            time.sleep(second)
            return

        '''
        选择一个子主题
        然后向下选择三段正文
        如果没有子主题， 则直接选择三段正文
        '''
        try:
            title2 = self.driver.find_element(by=By.XPATH,
                                              value='//*[@id="readme"]/article/table/tbody/tr[3]/td[1]/h2[2]')
        except NoSuchElementException:
            # 如果没有子主题则从第二个段落开始记录
            title2 = self.driver.find_element(by=By.XPATH,
                                              value='//*[@id="readme"]/article/table/tbody/tr[3]/td[1]/p[1]')

        location = title2.location
        size = title2.size
        # 滑轮滚动到第二主题位置
        self.driver.execute_script("window.scrollTo(0, " + str(title2.location['y']) + ")")
        # 截取当前网页作为临时存储
        self.driver.save_screenshot('tempImage.png')

        minY = location['y']  # 有效段落上沿
        maxY = minY

        redLine = Image.open("tempImage.png")
        redDraw = ImageDraw.ImageDraw(redLine)
        top_left_corner = (57, 50)
        # 获取正文对象
        contentList = []
        counter = 1
        for i in range(1, 999):
            curContent = self.driver.find_element(by=By.XPATH,
                                                  value='//*[@id="readme"]/article/table/tbody/tr[3]/td[1]/p[' + str(
                                                      i) + ']')
            curY = curContent.location['y']
            if curY > minY and counter < 4:
                contentList.append(curContent)
                curSize = curContent.size
                lower_right_corner = (top_left_corner[0] + curSize['width'], top_left_corner[1] + curSize['height'])
                redDraw.rectangle((top_left_corner, lower_right_corner), fill=None, outline='red', width=5)
                top_left_corner = (57, top_left_corner[1] + curSize['height'] + 15)
                maxY = curY + curSize['height']
                counter += 1
            if counter >= 4:
                break

        redLine.save("pageImageWithRedLine.png")

        im = Image.open('pageImageWithRedLine.png')
        # 根据第一个主题和第二个主题的位置差， 截取当中内容
        theWidth = size['width'] + 55
        theHeight = maxY - minY
        im = im.crop((55, 48, theWidth, theHeight))
        if theHeight > 100:
            im = im.resize((350, 250), resample=Image.NEAREST)
        pic = os.path.join(self.savePath, title.text + '.png')
        im.save(pic)

        Warrior.excelRecorder(self, subUrl, title.text, 'github.com', '境外', pic)
        second = random.randint(5, 15)
        logging.debug('休眠%d秒...', second)
        time.sleep(second)


    def getSubUrlList(self, curPageUrl: str) -> list:
        rsp = self.myGetFunc(curPageUrl)
        while rsp is None:
            logging.info('再次尝试获取当前页主题列表 ...')
            rsp = self.myGetFunc(curPageUrl)
        return self.getSubUrlProcesser(rsp.text)

    def getSubUrlProcesser(self, htmlStr: str) -> list:
        from lxml import etree
        html = etree.HTML(htmlStr)
        html_data = html.xpath('//*[@id="readme"]/article/table/tbody/tr')

        subList = []
        for num in range(4, len(html_data)):
            sub_html_data = html.xpath('//*[@id="readme"]/article/table/tbody/tr[' + str(num) + ']/td/a')
            if len(sub_html_data) < 1:
                continue
            subList.append(sub_html_data[0].attrib['href'])
        return subList


    def myGetFunc(self, url):
        try:
            return requests.get(url)
        except:
            return None
        


if __name__ == '__main__':
    djy = dajiyuan(root='https://github.com/qxaeoq3717/djy/blob/master/gb/nf1176106.md',
                    save_path= '.',
                    begin= 0,
                    max=2 )
    djy.start()