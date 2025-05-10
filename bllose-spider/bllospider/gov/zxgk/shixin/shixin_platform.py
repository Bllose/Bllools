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


# 爬取数据暂存列表
processed_data = []

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

LONG_WAITING_TIME = 10
# 正常等待时间
NORMAL_WAITING_TIME = 5
# 短等待时间
SHORT_WAITING_TIME = 2
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

def rename(abs_path: str):
    # 获取当前时间戳
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # 拆分路径和文件名
    directory, filename = os.path.split(abs_path)
    name, extension = os.path.splitext(filename)

    # 构建新的文件名
    new_filename = f"{name}_{timestamp}.{extension}"

    # 构建新的保存路径
    return os.path.join(directory, new_filename)

# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ 任务主入口 ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
def task_process(cralwer: ShixinCralwer, name: str, identify: str = None, auto = True):

    cur_retry_times = RETRY_TIMES
    while cur_retry_times > 0:
        try:
            return go(cralwer, name, identify, auto)
        except (NeedRestartError, ElementClickInterceptedException):
            # 需要完全重启浏览器，重新进入页面
            cralwer.refresh_environment()
            cralwer.init_root_url()
            cur_retry_times -= 1
            continue
        except:
            traceback.print_exc()
            cur_retry_times -= 1
            continue
    
    information_recorder(name, '查询尝试达到上限', identify)

def input_clean_set(cralwer: ShixinCralwer, xpath: str, value: str = None):
    """
    输入框清理并设置值
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

def getApiKey():
    global DOUBAO_API_KEY
    if DOUBAO_API_KEY == None or len(DOUBAO_API_KEY) == 0:
        DOUBAO_API_KEY = getApiKeyFromConfig()
    return DOUBAO_API_KEY

@bConfig()
def getApiKeyFromConfig(config):
    return config['doubao']['token']

def auto_set_captcha(driver, YZM_INPUT) -> str:
    """
    自动识别验证码
    """
    captcha_recogonized = None
    times = 0
    captchaFailedTimes = 0

    while not captcha_recogonized and times < TRY_TIMES_CLICK_CAPTCHAIMG:
        times += 1
        time.sleep(LONG_WAITING_TIME)
        captcha_request = get_captcha_request(driver)

        if captcha_request and captcha_request.response:
            if 'Please enable JavaScript and refresh the page.'.encode() in captcha_request.response.body:
                captchaFailedTimes += 1
                if captchaFailedTimes > 3:
                    raise NeedRestartError('需要开启JavaScript并刷新页面')

            logging.warning(LOGGING_INDENT + LOGGING_INDENT + f"拦截到验证码请求，开始识别验证码")
            # 将验证码图片数据转换为base64字符串
            base64_data = base64.b64encode(captcha_request.response.body).decode('utf-8')
            base64_data = 'data:image/png;base64,' + base64_data
            # print("验证码base64字符串：", base64_data)
            captcha_recogonized = identify_verification_code(original_image=base64_data,
                                                             text = TEXT,
                                                             apiKey = getApiKey()).replace(' ', '')
            
            if captcha_recogonized:
                logging.warning(LOGGING_INDENT + LOGGING_INDENT + f"填入验证码: {captcha_recogonized}")
                time.sleep(SHORT_WAITING_TIME)
                YZM_INPUT.send_keys(captcha_recogonized)
                time.sleep(SHORT_WAITING_TIME)
                break
            else:
                logging.warning(LOGGING_INDENT + LOGGING_INDENT + "验证码识别失败，刷新验证码等待重新识别")
                click_captchaImg(driver)
                time.sleep(1)
        else:
            logging.warning(LOGGING_INDENT + LOGGING_INDENT + "未找到验证码图片元素，刷新验证码等待重新识别")
            click_captchaImg(driver)
            time.sleep(1)

    return captcha_recogonized

def get_captcha_request(driver):
    """
    获取验证码请求
    """
    failed_list = []
    request = fetch_success_request(driver, failed_list)
    while not request:
        time.sleep(SHORT_WAITING_TIME)
        request = fetch_success_request(driver, failed_list)

    return request

def fetch_success_request(driver, failed_list):
    """
    获取成功的请求
    """
    for request in driver.requests[::-1]:
        if request.response and 'captchaNew.do' in request.url:
            if request.response.status_code == 200:
                return request
            else:
                failed_list.append(str(request.response.status_code) + ':' + request.response.reason)
                if len(failed_list) > TRY_TIMES_CLICK_CAPTCHAIMG:
                    failed_list.clear()
                    raise NeedRestartError("验证码无法刷新，需要重启浏览器")
    return None

def click_captchaImg(driver) -> None:
    # 点击验证码图片
    captcha_img = driver.find_element(By.XPATH, XPATH_CAPTCHA_IMG)
    tryAgain = True
    times = 0
    while tryAgain:
        try:
            captcha_img.click()
            return
        except ElementClickInterceptedException:
            time.sleep(10)
            times += 1
            if times > TRY_TIMES_CLICK_CAPTCHAIMG:
                logging.warning(LOGGING_INDENT + LOGGING_INDENT + f"点击验证码图片{times}次失败，跳过本次验证码刷新")
                return
    
def go(cralwer: ShixinCralwer, name: str, identify: str = None, auto = True) -> bool:
    # 名字输入框
    _ = input_clean_set(cralwer, XPATH_NAME_INPUT, name)
    # 身份证输入框
    _ = input_clean_set(cralwer, XPATH_ID_INPUT, identify)
    # 验证码输入框
    yzm_input = input_clean_set(cralwer, XPATH_CAPTCHA_INPUT)
    # 搜索按钮
    search_button = cralwer.driver.find_element(By.XPATH, XPATH_SEARCH_BUTTON)

    if auto:
        # 由于清除名字与身份证字段会触发验证码的刷新行为，需要等待验证码刷新完成
        time.sleep(NORMAL_WAITING_TIME)
        # 自动识别验证码，并填入验证码输入框
        _ = auto_set_captcha(cralwer.driver, yzm_input)
    else:
        input('请手动->填写验证码<-，然后回车继续')
    
    # 点击搜索按钮
    try:
        time.sleep(SHORT_WAITING_TIME)
        search_button.click()
        time.sleep(SHORT_WAITING_TIME)
    except ElementClickInterceptedException:
        time.sleep(NORMAL_WAITING_TIME)
        search_button.click()
    time.sleep(NORMAL_WAITING_TIME)

    # 尝试获取查询失败的结果，如果存在则处理失败场景
    elements = cralwer.driver.find_elements(By.XPATH, XPATH_SEARCH_FAILED)
    successed_elements = cralwer.driver.find_elements(By.XPATH, XPATH_SEARCH_SUCCED)
    if len(elements) < 1 and (
        len(successed_elements) < 1 or 'hide' in successed_elements[0].get_attribute('class')):
        raise NeedRestartError()

    if len(elements) > 0:
        logging.warning(LOGGING_INDENT + f"本次查询无结果，检查原因")
        element = elements[0]
        text_content = element.text
        if text_content is not None and len(text_content) > 0:
            if '验证码错误或验证码已过期。' in text_content:
                logging.warning(LOGGING_INDENT + f"本次查询验证码错误，自动重新查询")
                # 抛出异常，进行重试
                raise Exception("验证码错误或验证码已过期")
            information_recorder(name, text_content, identify)
            logging.warning(LOGGING_INDENT + f"本次查询无结果，保存原因并进入下一个查询")
            return True

    # 逐条查看并保存信息数据        
    return process_detail(cralwer.driver, name, auto)

def information_recorder(name: str, ex_content: str, identify: str = None):
    """
    特殊信息记录器（手动记录）
    """
    processed_data.append({
                "被执行人姓名/名称：": name,
                "性别：": ex_content,
                "身份证号码/组织机构代码：": '' if identify is None else identify,
                "执行法院：": "-",
                "省份：": "-",
                "执行依据文号：": "-",
                "立案时间：": "-",
                "案号：": "-",
                "做出执行依据单位：": "-",
                "生效法律文书确定的义务：": "-",
                "被执行人的履行情况：": "-",
                "失信被执行人行为具体情形：": "-",
                "发布时间：": "-"
            })

def process_detail(driver, name: str, auto: bool = True):
    # global processed_data
    logging.warning(LOGGING_INDENT + LOGGING_INDENT + f"针对查询到的列表信息，进行详细信息查询并记录")
    counter = 0

    # 遍历表格，点击每个表格的"查看"按钮，获取详细信息并保存
    for i in range(1, 100):
        xpath = f'/html/body/div[2]/div/div[2]/div[4]/div[1]/div/table/tbody/tr[{i}]/td[5]'
        # 使用find_elements来检查元素是否存在
        elements = driver.find_elements(By.XPATH, xpath)
        if not elements:
            if auto:
                # 抛出异常，进行重试
                raise Exception("识别不到“查看”按钮，可能是验证码错误或验证码已过期")
            else:
                input('请重新手动 ->填写验证码<- 并 ->查询<-，然后回车继续')
                elements = driver.find_elements(By.XPATH, xpath)
        
        if elements[0].text != '查看':
            logging.warning(LOGGING_INDENT + LOGGING_INDENT + f'识别第{i}个“查看”按钮失败，跳过')
            break

        curElement = driver.find_element(By.XPATH, xpath)
        if curElement:
            # 聚焦选中的元素
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", driver.find_element(By.XPATH, xpath))
            retry_click(curElement, driver)
            try:
                time.sleep(1)
                table_element = driver.find_element(By.XPATH, XPATH_TABLE_DETAIL_INFO)
            except:
                time.sleep(1)
                retry_click(curElement, driver)
                time.sleep(1)
                table_element = driver.find_element(By.XPATH, XPATH_TABLE_DETAIL_INFO)
            
            curInfoDetail = extract_table_data(table_element)
            if len(curInfoDetail) == 0:
                time.sleep(2)
                retry_click(curElement, driver)
                time.sleep(2)
                table_element = driver.find_element(By.XPATH, XPATH_TABLE_DETAIL_INFO)
                curInfoDetail = extract_table_data(table_element)

            if len(curInfoDetail) == 0:
                retry_click(driver.find_element(By.XPATH, xpath), driver)
                time.sleep(1)
                table_element = driver.find_element(By.XPATH, XPATH_TABLE_DETAIL_INFO)
                curInfoDetail = extract_table_data(table_element)
            if len(curInfoDetail) == 0:
                logging.warning(LOGGING_INDENT + LOGGING_INDENT + f'多次尝试后依然未能找到第{i}条数据，跳过')
                continue
            if name not in curInfoDetail.values():
                logging.warning(LOGGING_INDENT + LOGGING_INDENT + f'解析信息所属人与当前查询人{name}不一致，重新查询 -> {curInfoDetail}')
                raise Exception("解析信息所属人与当前查询人不一致")

            processed_data.append(curInfoDetail)
            counter += 1

            # 关闭弹窗
            # driver.find_element(By.XPATH, XPATH_DETAIL_TABLE_CLOSE_BUTTON).click()
            make_sure_click(XPATH_DETAIL_TABLE_CLOSE_BUTTON, driver)
            time.sleep(1)
        else:
            print('列表识别完成')
            break

    logging.warning(LOGGING_INDENT + LOGGING_INDENT + f"详情查询完毕, 共查询到{counter}条数据")
    return True

def make_sure_click(xpath: str, driver):
    # 直接关闭
    driver.find_element(By.XPATH, xpath).click()

    while 'block' in driver.find_element(By.XPATH,'//*[@id="show"]').get_attribute('style'):
        # 当检测到弹窗时，进行重试关闭
        time.sleep(SHORT_WAITING_TIME)
        driver.find_element(By.XPATH, xpath).click()
        time.sleep(SHORT_WAITING_TIME)
    
    # 当被关闭后，本质上只是将style由 block 变为 none
    # if 'none' in driver.find_element(By.XPATH,'//*[@id="show"]').get_attribute('style')
        
def retry_click(element, driver):
    try:
        element.click()
    except:
        make_sure_click(XPATH_DETAIL_TABLE_CLOSE_BUTTON, driver)
        time.sleep(NORMAL_WAITING_TIME)
        element.click()

def extract_table_data(table_element) -> dict:
    row_data = {}
    # 获取所有的 tbody 元素
    tbody_elements = table_element.find_elements(By.TAG_NAME, 'tbody')
    for tbody in tbody_elements:
        # 获取每个 tbody 中的所有行
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            # 获取每行中的所有单元格
            cells = row.find_elements(By.TAG_NAME, 'td')
            IS_KEY = True
            key = ''
            for cell in cells:
                # 获取单元格的文本内容
                if len(cell.text) > 1:
                    if IS_KEY:
                        key = cell.text
                        IS_KEY = False
                    else:
                        row_data[key] = cell.text
                        IS_KEY = True
    return row_data

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

if __name__ == "__main__":
    logging.basicConfig(filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s')
    # 带查询失信名单文件绝对路径
    TARGET_EXCEL_PATH = r'D:\temp\target.xlsx'
    # 爬取下来数据保存的文件绝对路径
    SAVED_EXCEL_PATH = r'D:\temp\processed_data.xlsx'
    # 读取目标excel文件
    target_list = read_excel(TARGET_EXCEL_PATH)
    # 初始化爬虫
    cralwer = ShixinCralwer()
    cralwer.init_root_url()

    try:
        # 遍历目标列表，进行查询
        for target in target_list:
            task_process(cralwer, target['name'], target['id'])
    except:
        traceback.print_exc()
    finally:
        if len(processed_data) > 0:
            # 保存为excel
            df = pd.DataFrame(processed_data)
            file4Saved = rename(SAVED_EXCEL_PATH)
            df.to_excel(file4Saved, index=False)
            logging.warning(f"已保存 {len(processed_data)} 条数据 -> 文件: {file4Saved}")
            processed_data.clear()
        else:
            logging.warning(f"本次查询无数据")
        # 关闭浏览器
        cralwer.cleanup()