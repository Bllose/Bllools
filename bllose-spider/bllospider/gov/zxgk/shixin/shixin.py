from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import base64

from bllospider.gov.zxgk.shixin.AliBailianImageRecognize import recognize_text_from_image

# 设置火狐浏览器选项
firefox_options = Options()
# 若想在后台运行浏览器，可取消注释下面这行代码
# firefox_options.add_argument('-headless')
# 指定 Firefox 二进制文件的路径
firefox_options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'  # 根据实际安装路径修改

# 指定 geckodriver 的路径
geckodriver_path = r'D:\workplace\github\Bllools\geckodriver.exe'
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

# 查找验证码请求
captcha_request = None
for request in driver.requests:
    if request.response and 'captchaNew.do' in request.url:
        captcha_request = request
        break


driver.find_element(By.XPATH, '//*[@id="pName"]').send_keys('毕国军')

if captcha_request and captcha_request.response:
    # 将验证码图片数据转换为base64字符串
    base64_data = base64.b64encode(captcha_request.response.body).decode('utf-8')
    print("验证码base64字符串：", base64_data)
    captcha_recogonized = recognize_text_from_image(image_path=None, image_base64_string=base64_data)
    print(f"成功获取验证码图片数据: {captcha_recogonized}")
    # //*[@id="yzm"]
    driver.find_element(By.XPATH, '//*[@id="yzm"]').send_keys(captcha_recogonized)
    time.sleep(10)
    driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[3]/form/div[4]/div[6]/button').click()
else:
    print("未找到验证码图片请求")

# 打印页面标题
print(driver.title)

# 关闭浏览器
driver.quit()

    