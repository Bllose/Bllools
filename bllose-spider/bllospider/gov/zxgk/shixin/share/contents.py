from seleniumwire import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from bllonfig.Config import bConfig

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
# 验证码错误或已过期的提示框xpath路径
XPATH_CAPTCHA_ERROR = '//*[@id="layui-layer1"]'
# 验证码错误或已过期的提示框关闭按钮xpath路径
XPATH_CAPTCHA_ERROR_BUTTON = '/html/body/div[9]/div[3]/a'

# 验证器锁
MONITER_CAPTCHA_LOCKED = True
# 验证码是否已设置
CAPTCHA_HAD_SETTED = False

LONG_WAITING_TIME = 10
# 正常等待时间
NORMAL_WAITING_TIME = 5
# 短等待时间
SHORT_WAITING_TIME = 1

# 爬取数据暂存列表
processed_data = []
# 全局的爬虫实例
cralwer = None

# 重试次数
RETRY_TIMES = 5
# 验证码刷新失败重试次数上限
TRY_TIMES_CLICK_CAPTCHAIMG = 10
# 日志打印缩进
LOGGING_INDENT = '————>'

# 失信平台请求地址
SHIXIN_URL = 'https://zxgk.court.gov.cn/shixin/'
# 保存数据的excel路径
SAVED_EXCEL_PATH = 'shixin.xlsx'
# 发给大模型的提示语
TEXT = '提取图中文字，文字范围a-zA-Z0-9，只会出现四个字符，忽略所有空白字符'
# 豆包大模型apikey
DOUBAO_API_KEY = None

# 详情表格中人名的key
CHECK_NAME_KEY = '被执行人姓名/名称：'

class ShixinCralwer:
    def __init__(self):
        self.firefox_options = None
        self.service = None
        self.driver = None
        self.refresh_environment()

    @bConfig()
    def refresh_environment(self, config):
        self.cleanup()
        
        # 设置火狐浏览器选项
        self.firefox_options = Options()
        # 若想在后台运行浏览器，可取消注释下面这行代码
        # firefox_options.add_argument('-headless')
        # 指定 Firefox 二进制文件的路径
        self.firefox_options.binary_location = config['cralwer']['firefox']['binary'] 
        # self.firefox_options.set_capability('loggingPrefs', {'browser': 'ALL'}) # 启用所有日志级别的日志
        self.firefox_options.set_preference('devtools.console.stdout.content', True)

        # 指定 geckodriver 的路径
        self.service = Service(config['cralwer']['firefox']['geckodriver'])

        # 创建火狐浏览器驱动实例
        self.driver = webdriver.Firefox(service=self.service, options=self.firefox_options)
    
    def init_root_url(self):
        self.driver.get(SHIXIN_URL)
        # 等待验证码图片元素加载完成
        while not self._waiting_web_load():
            self.driver.refresh()
        time.sleep(NORMAL_WAITING_TIME)
        # 隐藏悬浮窗口
        floatingWindow = self.driver.find_element(By.XPATH, XPATH_SUBWINDOW)
        self.driver.execute_script("arguments[0].classList.add('hide');", floatingWindow)
        time.sleep(SHORT_WAITING_TIME)
    
    def _waiting_web_load(self) -> bool:
        # 等待页面加载完成
        try:
            WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((By.XPATH, XPATH_CAPTCHA_IMG))
            )
            return True
        except:
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