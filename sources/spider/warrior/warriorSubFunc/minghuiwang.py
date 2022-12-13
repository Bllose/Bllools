from bllools.spider.warrior.Warrior import Warrior
from selenium.webdriver.common.by import By

class minghuiwang(Warrior):
    def __init__(self,
                 root: str,
                 save_path: str,
                 begin: int,
                 max=2) -> None:
        super(minghuiwang, self).__init__(root, save_path, begin, max)

    def start(self):
        Warrior.start(self)

    """
    TODO - 具体实现
    """
    def getPages(self) -> list:
        # 大陆简讯 http://d28ob7jg26af9l.cloudfront.net/?coo0i4CMc=6Io&VLAS=0WfgIi3FdjF&BLXRX-=bB1eu&VEu=y8XdjtWk&TqAqBfjJ=ERF4EI0&tko9M?pageno=2
        # 问候李洪志师傅 http://d28ob7jg26af9l.cloudfront.net/?UNOoeuBwEgJ=mgE6-8tdqWg&nCHKJ2cYn=Z9HwUJnhx10&cN6W8=j
        self.driver.get(r'https://d28ob7jg26af9l.cloudfront.net/?coo0i4CMc=6Io&VLAS=0WfgIi3FdjF&BLXRX-=bB1eu&VEu=y8XdjtWk&TqAqBfjJ=ERF4EI0&tko9M')

        next = self.driver.find_element(by=By.XPATH, value='//*[@id="cp_category_listing_new"]/div[5]/table/tbody/tr/td[3]/a[2]')

        next.click()

        return super().getPages()


    """
    TODO - 具体实现
    """
    def getSubUrlList(self, curPageUrl: str) -> list:
        return super().getSubUrlList()


    """
    TODO - 具体实现
    """
    def recorder(self, subUrl: str) -> None:
        return super().recorder()


if __name__ == '__main__':
    mhw = minghuiwang(root=r'', save_path=r'', begin=0, max= 2)
    mhw.getPages()