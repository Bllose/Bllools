from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import traceback

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

def task_process(processed_data, name, id_num = None):

    name_input = driver.find_element(By.XPATH, '//*[@id="pName"]')
    name_input.clear()
    name_input.send_keys(name)

    id_input = driver.find_element(By.XPATH, '//*[@id="pCardNum"]')
    id_input.clear()
    if id_num and len(id_num) > 0:
        id_input.send_keys(id_num)

    # //*[@id="yzm"] 选取这个input框，使得聚焦在这个输入框上，等待用户输入验证码
    driver.find_element(By.XPATH, '//*[@id="yzm"]').click()

    input('请手动填写验证码并查询，然后回车继续')
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[3]/form/div[4]/div[6]/button').click()
    time.sleep(1)


    elements = driver.find_elements(By.XPATH, '/html/body/div[2]/div/div[2]/div[4]/div[1]/div/table/tbody/p')
    if len(elements) > 0:
        element = elements[0]
        text_content = element.text
        if text_content is not None and len(text_content) > 0:
            print(text_content)
            if '验证码错误或验证码已过期。' in text_content:
                return False
            return True


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

        if driver.find_element(By.XPATH, xpath):
            # 聚焦选中的元素
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.XPATH, xpath))
            driver.find_element(By.XPATH, xpath).click()
            try:
                time.sleep(1)
                table_element = driver.find_element(By.XPATH, table_xpath)
            except:
                time.sleep(1)
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(1)
                table_element = driver.find_element(By.XPATH, table_xpath)
            
            curInfoDetail = extract_table_data(table_element)

            if len(curInfoDetail) == 0:
                driver.find_element(By.XPATH, xpath).click()
                time.sleep(1)
                table_element = driver.find_element(By.XPATH, table_xpath)
                curInfoDetail = extract_table_data(table_element)
            if len(curInfoDetail) == 0:
                print('不存在')
                continue

            processed_data.append(curInfoDetail)

            # 关闭弹窗
            driver.find_element(By.XPATH, r'/html/body/div[5]/div/div[2]/button').click()
            time.sleep(1)
        else:
            print('不存在')

    return True

if __name__ == '__main__':
    target_list = read_excel(TARGET_EXCEL_PATH)
    processed_data = []
    driver = init_browser()
    try:
        for target in target_list:
            ok = False
            while not ok:
                ok = task_process(processed_data, target['name'], target['id'])
            # task_process(processed_data, target['name'], target['id'])
    except Exception as e:
        print(f"发生异常: {e}")
        traceback.print_exc()
    finally:
        # 保存为excel
        df = pd.DataFrame(processed_data)
        df.to_excel(SAVED_EXCEL_PATH, index=False)

        # 打印页面标题
        print(driver.title)

        # 关闭浏览器
        driver.quit()

    