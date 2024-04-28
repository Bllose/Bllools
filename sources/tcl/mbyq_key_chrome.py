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


current_work_dir = os.path.dirname(__file__)
configYml = 'mbyq_config.yml'

absYml = current_work_dir + os.sep + configYml
config = ''
if os.path.isfile(absYml):
    with open(absYml, 'r', encoding='utf-8') as f:
        config = f.read()
        if config is not None and len(config) > 1:
            import yaml
            data = yaml.safe_load(config)
            print(f'通过文件 {configYml} 加载相关配置')
            login_url = data['huawei']['cloud']['login']['url']
            login_user = data['huawei']['cloud']['login']['user']
            login_password = data['huawei']['cloud']['login']['password']


options = webdriver.ChromeOptions()
# 执行完成后不要关闭浏览器
options.add_experimental_option("detach", True)
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)  # Optional argument, if not specified will search path.
driver.get(login_url)
time.sleep(1) # Let the user actually see something!

driver.implicitly_wait(5)

userNameColumn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[2]/div[3]/div[3]/form/input')
userNameColumn.send_keys(login_user)
passwordColumn = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[2]/div[3]/div[4]/form/input')
passwordColumn.send_keys(login_password)

login_button = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[2]/div[4]/div/div/span')
login_button.click()


time.sleep(5)


