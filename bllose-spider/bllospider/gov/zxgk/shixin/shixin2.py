from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from openai import BadRequestError, OpenAI
import time
import pandas as pd
import traceback
import base64
import logging

"""
以下三个路径替换为自己具体的文件路径
"""
# 带查询失信名单文件绝对路径
TARGET_EXCEL_PATH = r'D:\temp\target.xlsx'

# 爬取下来数据保存的文件绝对路径
SAVED_EXCEL_PATH = r'D:\temp\processed_data.xlsx'

# 火狐浏览器exe启动文件绝对路径
FIREFOX_BINARY_PATH = r'C:\Program Files\Mozilla Firefox\firefox.exe'

# 火狐浏览器驱动文件绝对路径
FIREFOX_GECKODRIVER_PATH = r'D:\workplace\github\Bllools\geckodriver.exe'

# 自动填写验证码时需要填写API KEY
DOUBAO_API_KEY = ''

# 以下部分不用修改
# 日志打印缩进
LOGGING_INDENT = '————>'
# 验证码刷新失败重试次数上限
TRY_TIMES_CLICK_CAPTCHAIMG = 10


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
            print(f"姓名: {name}, 身份证: {id_num}")
            result_list.append(curLine)

    except FileNotFoundError:
        print(f"错误: 未找到文件 {file_path}。")
    except Exception as e:
        print(f"发生未知错误: {e}")
    finally:
        return result_list
        
def init_browser():
    # 设置火狐浏览器选项
    firefox_options = Options()
    # 若想在后台运行浏览器，可取消注释下面这行代码
    # firefox_options.add_argument('-headless')
    # 指定 Firefox 二进制文件的路径
    firefox_options.binary_location = FIREFOX_BINARY_PATH  # 根据实际安装路径修改

    # 指定 geckodriver 的路径
    geckodriver_path = FIREFOX_GECKODRIVER_PATH
    service = Service(geckodriver_path)

    # 创建火狐浏览器驱动实例
    driver = webdriver.Firefox(service=service, options=firefox_options)

    # 打开指定的网站
    driver.get('https://zxgk.court.gov.cn/shixin/')

    # 等待验证码图片元素加载完成
    WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="captchaImg"]'))
    )

    # 等待一段时间确保网络请求完成
    time.sleep(2)
    return driver

def auto_set_captcha(driver, YZM_INPUT) -> str:
    captcha_recogonized = None
    times = 0

    while not captcha_recogonized:
        times += 1
        captcha_request = None
        logging.warning(LOGGING_INDENT + LOGGING_INDENT + f"开始第{times}次尝试识别验证码")
        for request in driver.requests[::-1]:
            if request.response and 'captchaNew.do' in request.url:
                captcha_request = request
                break

        if captcha_request and captcha_request.response:
            logging.warning(LOGGING_INDENT + LOGGING_INDENT + f"拦截到验证码请求，开始识别验证码")
            # 将验证码图片数据转换为base64字符串
            base64_data = base64.b64encode(captcha_request.response.body).decode('utf-8')
            base64_data = 'data:image/png;base64,' + base64_data
            # print("验证码base64字符串：", base64_data)
            captcha_recogonized = identify_verification_code(original_image=base64_data).replace(' ', '')
            
            if captcha_recogonized:
                logging.warning(LOGGING_INDENT + LOGGING_INDENT + f"填入验证码: {captcha_recogonized}")
                YZM_INPUT.send_keys(captcha_recogonized)
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

def click_captchaImg(driver):
    # 点击验证码图片
    captcha_img = driver.find_element(By.XPATH, '//*[@id="captchaImg"]')
    tryAgain = True
    times = 0
    while tryAgain:
        try:
            captcha_img.click()
            tryAgain = False
        except ElementClickInterceptedException:
            time.sleep(10)
            times += 1
            if times > TRY_TIMES_CLICK_CAPTCHAIMG:
                logging.warning(LOGGING_INDENT + LOGGING_INDENT + f"点击验证码图片{times}次失败，跳过本次验证码刷新")
                tryAgain = False

def retry_click(element):
    try:
        element.click()
    except ElementClickInterceptedException:
        time.sleep(10)
        element.click()

def task_process(driver, processed_data, name, id_num = None, auto = False):
    """
    处理单个查询任务
    :param driver: 浏览器驱动
    :param processed_data: 已处理的数据
    :param name: 姓名
    :param id_num: 身份证
    :param auto: 是否自动填写验证码
    :return: 是否成功
    """
    
    name_input = driver.find_element(By.XPATH, '//*[@id="pName"]')
    name_input.clear()
    logging.warning(LOGGING_INDENT + f"填写查询人名称：{name}")
    name_input.send_keys(name)

    id_input = driver.find_element(By.XPATH, '//*[@id="pCardNum"]')
    id_input.clear()
    if id_num and len(id_num) > 0:
        logging.warning(LOGGING_INDENT + f"填写查询人身份证：{id_num}")
        id_input.send_keys(id_num)

    # //*[@id="yzm"] 选取这个input框，使得聚焦在这个输入框上，等待用户输入验证码
    YZM_INPUT = driver.find_element(By.XPATH, '//*[@id="yzm"]')
    try:
        YZM_INPUT.clear()
        YZM_INPUT.click()
    except ElementClickInterceptedException:
        time.sleep(10)
        YZM_INPUT.clear()
        YZM_INPUT.click()
    # 先定位到查询按钮，因为后续再定位按钮容易触发验证码刷新
    search_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[3]/form/div[4]/div[6]/button')

    if auto:
        logging.warning(LOGGING_INDENT + f"本次自动填写验证码逻辑开始")
        time.sleep(5)
        auto_set_captcha(driver, YZM_INPUT)
        logging.warning(LOGGING_INDENT + f"本次自动填写验证码逻辑结束")
    else:
        input('请手动填写验证码并查询，然后回车继续')

    try:
        logging.warning(LOGGING_INDENT + f"点击查询按钮,尝试查询")
        search_button.click()
    except ElementClickInterceptedException:
        logging.warning(LOGGING_INDENT + f"查询按钮被遮挡，等待10s后重新点击查询按钮")
        time.sleep(10)
        search_button.click()
    time.sleep(10)


    elements = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div[2]/div[4]/div[1]/div/table/tbody/p')
    if len(elements) > 0:
        logging.warning(LOGGING_INDENT + f"本次查询无结果，检查原因")
        element = elements[0]
        text_content = element.text
        if text_content is not None and len(text_content) > 0:
            if '验证码错误或验证码已过期。' in text_content:
                logging.warning(LOGGING_INDENT + f"本次查询验证码错误，自动重新查询")
                return False
            processed_data.append({
                "被执行人姓名/名称：": name,
                "性别：": text_content,
                "身份证号码/组织机构代码：": '' if id_num is None else id_num,
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
            logging.warning(LOGGING_INDENT + f"本次查询无结果，保存原因并进入下一个查询")
            return True
    return process_detail(driver, processed_data, name)

def process_detail(driver, processed_data, name):
    logging.warning(LOGGING_INDENT + LOGGING_INDENT + f"针对查询到的列表信息，进行详细信息查询并记录")
    counter = 0
    # 判断xpath是否存在
    for i in range(1, 100):
        xpath = f'/html/body/div[2]/div/div[2]/div[4]/div[1]/div/table/tbody/tr[{i}]/td[5]'
        # 使用find_elements来检查元素是否存在
        elements = driver.find_elements(By.XPATH, xpath)
        if not elements:
            input('请重新手动填写验证码并查询，然后回车继续')
            elements = driver.find_elements(By.XPATH, xpath)
        
        if elements[0].text != '查看':
            break

        table_xpath = r'//*[@id="partyDetail"]'

        curElement = driver.find_element(By.XPATH, xpath)
        if curElement:
            # 聚焦选中的元素
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH, xpath))
            retry_click(curElement)
            try:
                time.sleep(1)
                table_element = driver.find_element(By.XPATH, table_xpath)
            except:
                time.sleep(1)
                retry_click(curElement)
                time.sleep(1)
                table_element = driver.find_element(By.XPATH, table_xpath)
            
            curInfoDetail = extract_table_data(table_element)
            if len(curInfoDetail) == 0:
                time.sleep(2)
                retry_click(curElement)
                time.sleep(2)
                table_element = driver.find_element(By.XPATH, table_xpath)
                curInfoDetail = extract_table_data(table_element)

            if len(curInfoDetail) == 0:
                retry_click(driver.find_element(By.XPATH, xpath))
                time.sleep(1)
                table_element = driver.find_element(By.XPATH, table_xpath)
                curInfoDetail = extract_table_data(table_element)
            if len(curInfoDetail) == 0:
                logging.warning(LOGGING_INDENT + LOGGING_INDENT + f'多次尝试后依然未能找到第{i}条数据，跳过')
                continue

            processed_data.append(curInfoDetail)
            counter += 1

            # 关闭弹窗
            driver.find_element(By.XPATH, r'/html/body/div[5]/div/div[2]/button').click()
            time.sleep(1)
        else:
            print('列表识别完成')

    logging.warning(LOGGING_INDENT + LOGGING_INDENT + f"详情查询完毕, 共查询到{counter}条数据")
    return True

def identify_verification_code(original_image: str) -> str:
    """
    识别验证码
    :param original_image: 验证码图片的base64编码; 图片的网络地址
    :return: 识别结果
    base64编码格式:
    data:image/替换为图片的格式;base64,替换为具体图片的base64编码
    """

    # 请确保您已将 API Key 存储在环境变量 ARK_API_KEY 中
    # 初始化Ark客户端，从环境变量中读取您的API Key
    client = OpenAI(
        # 此为默认路径，您可根据业务所在地域进行配置
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        api_key=DOUBAO_API_KEY,
    )
 
    try:
        logging.warning(LOGGING_INDENT + LOGGING_INDENT + LOGGING_INDENT + "将验证码交给豆包大模型进行识别")
        response = client.chat.completions.create(
            # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
            model="doubao-1.5-vision-lite-250315",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": original_image
                            },
                        },
                        {"type": "text", "text": "提取图中文字,文字识别范围a~zA~Z0~9, 不要输出其他字符"},
                    ],
                }
            ],
        )

        logging.warning(LOGGING_INDENT + LOGGING_INDENT + LOGGING_INDENT + f"识别结果：{response.choices[0]}")
        return response.choices[0].message.content
    except BadRequestError as e:
        logging.warning(LOGGING_INDENT + LOGGING_INDENT + LOGGING_INDENT + e.message)
        return ""


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
    logging.warning("主流程第一步： 读取待查询名单, excel路径：" + TARGET_EXCEL_PATH)
    target_list = read_excel(TARGET_EXCEL_PATH)
    processed_data = []
    logging.warning("主流程第二步： 初始化浏览器")
    driver = init_browser()
    try:
        logging.warning("主流程第三步： 开始遍历列表，查询每一个名单")
        for target in target_list:
            ok = False
            while not ok:
                ok = task_process(driver, processed_data, target['name'], target['id'], auto=True)
            # task_process(processed_data, target['name'], target['id'])
    except Exception as e:
        print(f"发生异常: {e}")
        traceback.print_exc()
    finally:
        logging.warning("主流程第四步： 将查询结果保存为excel, excel路径：" + SAVED_EXCEL_PATH)
        # 保存为excel
        df = pd.DataFrame(processed_data)
        df.to_excel(SAVED_EXCEL_PATH, index=False)

        # 打印页面标题
        print(driver.title)

        logging.warning("主流程第五步： 关闭浏览器")
        # 关闭浏览器
        driver.quit()

    