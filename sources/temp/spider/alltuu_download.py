import time
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException


# 针对闪传平台进行批量下载操作
# 官网: https://www.alltuu.com/
# 见面会 HIT 22VC https://as.alltuu.com/album/1232551006/?from=qrCode

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
driver = webdriver.Chrome(executable_path=r'D:\etc\drivers\chromedriver_106.0.5249.61.exe', chrome_options=options)
driver.get(r'https://as.alltuu.com/album/1404012759/?from=link')
time.sleep(3)

# 打开查看页面
driver.find_element(by=By.XPATH, value = r'//*[@id="root"]/body/div[1]/div/div/div/div[1]/section/section[2]/section[1]').click()

for index in range(210):
    driver.find_element(by=By.XPATH, value=r'//*[@id="root"]/body/div[1]/div/div/div/div[4]/button[3]').click()
    driver.find_element(by=By.XPATH, value=r'//*[@id="root"]/body/div[1]/div/div/div/div[4]/div[1]/button[3]').click()
    time.sleep(3)


driver.close()
logging.info('DONE')