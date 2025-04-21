import sys
import os
import logging
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By


class SeleniumClient():
    def __init__(self, path:str = None):
        self.path = path
        self.driver = None
        self.service = None

    def getDriver(self):
        if self.driver is None:
            self.initDriver()
        return self.driver
    
    def initDriver(self):
        # 尝试多个可能的路径
        possible_paths = [
            # 1. 如果是exe运行，获取exe所在目录
            os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else None,
            # 2. 当前脚本所在目录
            os.path.dirname(os.path.abspath(__file__)),
            # 3. 当前工作目录
            os.getcwd()
        ]

        # 移除None值
        possible_paths = [p for p in possible_paths if p]
        
        # 遍历所有可能的路径查找chromedriver.exe
        chrome_driver_path = None
        for path in possible_paths:
            # temp_path = os.path.join(path, 'chromedriver.exe')
            temp_path = os.path.join(path, 'geckodriver.exe')
            if os.path.isfile(temp_path):
                chrome_driver_path = temp_path
                break
        
        if chrome_driver_path is None:
            raise FileNotFoundError('无法找到chromedriver.exe，请确保它在正确的位置')

        logging.info(f"chromedriver path: {chrome_driver_path}")
        self.load_path = chrome_driver_path
        # 创建 ChromeDriver 服务对象
        self.service = Service(chrome_driver_path)
        # 添加Chrome选项
        chrome_options = Options()
        # 禁用开发者工具日志输出
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('Sec-Fetch-Site=same-origin')
        # self.driver = webdriver.Chrome(service=self.service, options=chrome_options)
        self.driver = webdriver.Firefox(service=self.service, options=chrome_options)
        return self.driver

    def closeDriver(self):
        if self.service is not None and self.driver is not None:
            self.driver.quit()
            self.service.stop()
