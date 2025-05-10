from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException,TimeoutException
import time
import os
from datetime import datetime
import pandas as pd
import traceback
import base64
import logging

from bllonfig.Config import bConfig
from bllospider.gov.zxgk.shixin.DoubaoImageRecognize import identify_verification_code
from bllospider.exceptions.NeedRestartError import NeedRestartError

# 带查询失信名单文件绝对路径
TARGET_EXCEL_PATH = r'D:\temp\target.xlsx'
# 爬取下来数据保存的文件绝对路径
SAVED_EXCEL_PATH = r'D:\temp\processed_data.xlsx'

# 验证码图片xpath路径
XPATH_CAPTCHA_IMG = '//*[@id="captchaImg"]'
# 验证码输入框xpath路径
XPATH_CAPTCHA_INPUT = '//*[@id="yzm"]'
# 姓名输入框xpath路径
XPATH_NAME_INPUT = '//*[@id="pName"]'
# 身份证输入框xpath路径
XPATH_ID_INPUT = '//*[@id="pCardNum"]'
# 搜索按钮xpath路径
XPATH_SEARCH_BUTTON = '/html/body/div[2]/div/div[2]/div[3]/form/div[4]/div[6]/button'
# 查询失败时，提示信息xpath路径
XPATH_SEARCH_FAILED = '/html/body/div[2]/div/div[2]/div[4]/div[1]/div/table/tbody/p'
# 查询成功时，表格所属的xpath路径
XPATH_SEARCH_SUCCED = '//*[@id="result-block"]'
# 点击查看后，详情弹出框xpath路径
XPATH_TABLE_DETAIL_INFO = '//*[@id="partyDetail"]'
# 详情弹框关闭按钮xpath路径
XPATH_DETAIL_TABLE_CLOSE_BUTTON = '/html/body/div[5]/div/div[2]/button'
# 悬浮窗口xpath路径
XPATH_SUBWINDOW = '//*[@id="frameImg"]'

# 失信平台请求地址
SHIXIN_URL = 'https://zxgk.court.gov.cn/shixin/'
# 发给大模型的提示语
TEXT = '提取图中文字，文字范围a-zA-Z0-9，只会出现四个字符，忽略所有空白字符'
# 豆包大模型apikey
DOUBAO_API_KEY = None

LONG_WAITING_TIME = 10
# 正常等待时间
NORMAL_WAITING_TIME = 5
# 短等待时间
SHORT_WAITING_TIME = 2
# 详情表格中人名的key
CHECK_NAME_KEY = '被执行人姓名/名称：'
# 爬取数据暂存列表
processed_data = []

class ShixinCralwer:
    def __init__(self):
        self.firefox_options = None
        self.service = None
        self.driver = None
        self.refresh_environment()

    @bConfig()
    def refresh_environment(self, config, type: str = 'chrome'):
        self.cleanup()
        
        if type == 'firefox':
            self.init_firefox(config)
        elif type == 'chrome':
            self.init_chrome(config)
        else:
            raise Exception('type must be firefox or chrome')
        
    def init_chrome(self, config):
        # 设置 Chrome 浏览器选项
        self.chrome_options = Options()
        # 若想在后台运行浏览器，可取消注释下面这行代码
        # self.chrome_options.binary_location = config['cralwer']['chrome']['binary']
        # self.chrome_options.add_argument('--enable-logging')
        # self.chrome_options.add_argument('--v=1')
        # self.chrome_options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
        self.service = Service(config['cralwer']['chrome']['driver'])
        # self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.driver = webdriver.Chrome(service=self.service)
    
    def init_firefox(self, config):
        # 设置火狐浏览器选项
        self.firefox_options = Options()
        # 若想在后台运行浏览器，可取消注释下面这行代码
        # firefox_options.add_argument('-headless')
        # 指定 Firefox 二进制文件的路径
        self.firefox_options.binary_location = config['cralwer']['firefox']['binary'] 
        self.firefox_options.set_preference('devtools.console.stdout.content', True)
        # 旧版本
        # self.firefox_options.log.level = "trace"
        # self.firefox_options.set_capability('moz:loggingPrefs', {'browser': 'ALL'})

        # 指定 geckodriver 的路径
        self.service = Service(config['cralwer']['firefox']['geckodriver'])

        # 创建火狐浏览器驱动实例
        self.driver = webdriver.Firefox(service=self.service, options=self.firefox_options)

    def init_root_url(self):
        self.driver.get(SHIXIN_URL)
        # 等待验证码图片元素加载完成
        while not self.waiting_web_load():
            self.driver.refresh()
        time.sleep(NORMAL_WAITING_TIME)
        # 隐藏悬浮窗口
        floatingWindow = self.driver.find_element(By.XPATH, XPATH_SUBWINDOW)
        self.driver.execute_script("arguments[0].classList.add('hide');", floatingWindow)
        time.sleep(SHORT_WAITING_TIME)
    
    def waiting_web_load(self) -> bool:
        # 等待页面加载完成
        try:
            WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, XPATH_CAPTCHA_IMG))
            )
            return True
        except TimeoutException:
            return False
    
    def cleanup(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
        if self.service:
            self.service.stop()
            self.service = None
        if self.firefox_options:
            self.firefox_options = None

def read_excel(file_path) -> list:
    """
    读取目标excel文件  
    目标文件格式:
    第一列：姓名
    第二列：身份证
    目标文件数据必须隶属于Sheet1页签
    """
    result_list = []
    try:
        # 读取 Excel 文件，将第二列（身份证）强制转换为字符串类型
        df = pd.read_excel(file_path, sheet_name='Sheet1')

        # 获取第一列（姓名）和第二列（身份证）
        names = df.iloc[:, 0]
        ids = df.iloc[:, 1]

        # 输出结果
        for name, id_num in zip(names, ids):
            id_num = str(id_num)
            id_num = '' if id_num == 'nan' else id_num
            curLine = {
                'name': name.strip(),
                'id': id_num.strip()
            }
            # print(f"姓名: {name}, 身份证: {id_num}")
            result_list.append(curLine)

    except FileNotFoundError:
        print(f"错误: 未找到文件 {file_path}。")
    except Exception as e:
        print(f"发生未知错误: {e}")
    finally:
        return result_list

def input_clean_set(cralwer: ShixinCralwer, xpath: str, value: str = None):
    """
    输入框清理并设置值, 并返回当前元素
    """
    current_element = cralwer.driver.find_element(By.XPATH, xpath)

    try:
        current_element.clear()
        if value and len(value) > 0:
            current_element.send_keys(value)
    except:
        time.sleep(5)
        current_element.clear()
        if value and len(value) > 0:
            current_element.send_keys(value)
    
    return current_element

def get_the_latest_captcha_request(requests):
    """
    从浏览器的请求记录列表中获取最新的验证码请求
    """
    for request in requests[::-1]:
        if request.response and 'captchaNew.do' in request.url:
            return request
    return None

def get_captcha(request) -> str:
    """
    从验证码请求中获取验证图片，然后通过大模型识别验证码，如果成功则返回验证码
    """
    try:
        if request and request.response and request.response.status_code == 200:
            if request.response.status_code == 200:
                # 将验证码图片数据转换为base64字符串
                base64_data = base64.b64encode(request.response.body).decode('utf-8')
                base64_data = 'data:image/png;base64,' + base64_data
                # print("验证码base64字符串：", base64_data)
                captcha_recogonized = identify_verification_code(original_image=base64_data,
                                                                text = TEXT,
                                                                apiKey = getApiKey()).replace(' ', '')
                if captcha_recogonized:
                    logging.warning(f'验证码识别成功，自动输入 -> {captcha_recogonized}')
                    return captcha_recogonized
    except Exception as e:
        logging.error(f'验证码识别失败 -> {e}')
    return None

def getApiKey():
    global DOUBAO_API_KEY
    if DOUBAO_API_KEY == None or len(DOUBAO_API_KEY) == 0:
        DOUBAO_API_KEY = getApiKeyFromConfig()
    return DOUBAO_API_KEY

@bConfig()
def getApiKeyFromConfig(config):
    return config['doubao']['token']

if __name__ == '__main__':
    logging.basicConfig(filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s')
    # 1. excel 获取查询目标数据
    target_list = read_excel(TARGET_EXCEL_PATH)
    # 2. 初始化浏览器
    cralwer = ShixinCralwer()
    cralwer.init_root_url()

    # 3. 循环处理查询目标任务
    for target in target_list:
        name = target['name']
        identify = target['id']
        # 3.1 查询目标填入查询框
        # 名字输入框
        _ = input_clean_set(cralwer, XPATH_NAME_INPUT, name)
        # 身份证输入框
        _ = input_clean_set(cralwer, XPATH_ID_INPUT, identify)
        # 验证码输入框
        yzm_input = input_clean_set(cralwer, XPATH_CAPTCHA_INPUT)
        # 搜索按钮
        search_button = cralwer.driver.find_element(By.XPATH, XPATH_SEARCH_BUTTON)
        
        # 3.2 循环确认验证码并保障查询按钮成功执行
        safe_counter = 0
        requestCounter = 0
        # 获取当前所有请求记录
        while True:
            current_requests = cralwer.driver.requests
            if requestCounter < len(current_requests):
                new_requests = current_requests[requestCounter:]
                theLatestCaptchaRequest = get_the_latest_captcha_request(new_requests)
                if theLatestCaptchaRequest:
                    theLatestCaptcha = get_captcha(theLatestCaptchaRequest)
                    if theLatestCaptcha:
                        yzm_input.clear()
                        yzm_input.send_keys(theLatestCaptcha)
                        logging.warning(f'验证码输入成功，{theLatestCaptcha}') 
                    else:
                        # 验证码识别失败，点击验证码图片，刷新验证码
                        captcha_img = cralwer.driver.find_element(By.XPATH, XPATH_CAPTCHA_IMG)
                        captcha_img.click()
                        time.sleep(NORMAL_WAITING_TIME)
                else:
                    # 有新的请求，但是没有验证码请求
                    safe_counter += 1
                requestCounter = len(current_requests)
            else:
                # 没有新请求
                safe_counter += 1
            time.sleep(SHORT_WAITING_TIME)
            if safe_counter > 10:
                break
        # 点击搜索按钮
        search_button.click()
        time.sleep(NORMAL_WAITING_TIME)

        print('DONE!')                    
    
    
    # 3.2.1 
    # 3.3 循环获取查询结果并确保验证码刷新后及时更新验证码