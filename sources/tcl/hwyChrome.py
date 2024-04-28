import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import sys

chrome_driver_path = os.environ.get("CHROME_DRIVER")
if chrome_driver_path is None or not os.path.isfile(chrome_driver_path):
    print("请在系统总配置驱动路径 CHROME_DRIVER = /path/to/chromedriver")
    sys.exit(3)

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)  # Optional argument, if not specified will search path.
driver.get('https://auth.huaweicloud.com/authui/login.html?id=tcl_gf#/login')
time.sleep(1) # Let the user actually see something!

driver.implicitly_wait(5)

userNameColumn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[2]/div[3]/div[3]/form/input')
userNameColumn.send_keys('jg-dev-public')
passwordColumn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[2]/div[3]/div[4]/form/input')
passwordColumn.send_keys('!QAZ1qaz')

login_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[2]/div[4]/div/div/span')
login_button.click()


time.sleep(5)