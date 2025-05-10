
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException
import time
import os
import logging
from datetime import datetime
import pandas as pd
import traceback

from bllospider.exceptions.NeedRestartError import NeedRestartError

from bllospider.gov.zxgk.shixin.share.contents import *


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
    global MONITER_CAPTCHA_LOCKED
    # 名字输入框
    _ = input_clean_set(cralwer, XPATH_NAME_INPUT, name)
    # 身份证输入框
    _ = input_clean_set(cralwer, XPATH_ID_INPUT, identify)
    # 搜索按钮
    search_button = cralwer.driver.find_element(By.XPATH, XPATH_SEARCH_BUTTON)

    MONITER_CAPTCHA_LOCKED.wait()
    if auto:
        if MONITER_CAPTCHA_LOCKED.is_set():
            logging.warning(f'监视器锁: {MONITER_CAPTCHA_LOCKED}; 验证码填写标识符： {CAPTCHA_HAD_SETTED}; 继续操作')
            # time.sleep(NORMAL_WAITING_TIME)
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
                # raise Exception("解析信息所属人与当前查询人不一致")
                continue

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

# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ 任务主入口 ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
def mainTask(_cralwer: ShixinCralwer, _MONITER_CAPTCHA_LOCKED, _CAPTCHA_HAD_SETTED):
    import logging
    global cralwer
    global processed_data
    global CAPTCHA_HAD_SETTED
    global MONITER_CAPTCHA_LOCKED

    cralwer = _cralwer
    CAPTCHA_HAD_SETTED = _CAPTCHA_HAD_SETTED
    MONITER_CAPTCHA_LOCKED = _MONITER_CAPTCHA_LOCKED

    logging.basicConfig(filename='app.log', format='main - %(asctime)s - %(levelname)s - %(message)s')
    # 带查询失信名单文件绝对路径
    TARGET_EXCEL_PATH = r'D:\temp\target.xlsx'
    # 爬取下来数据保存的文件绝对路径
    SAVED_EXCEL_PATH = r'D:\temp\processed_data.xlsx'
    # 读取目标excel文件
    target_list = read_excel(TARGET_EXCEL_PATH)

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



if __name__ == "__main__":
    # 初始化爬虫
    # cralwer = ShixinCralwer()
    # cralwer.init_root_url()

    # mainTaskThread = threading.Thread(target=mainTask)
    # moniter_captchaThread = threading.Thread(target=moniter_captcha)

    # mainTaskThread.start()
    # moniter_captchaThread.start()

    # mainTaskThread.join()
    # moniter_captchaThread.join()

    print('done')