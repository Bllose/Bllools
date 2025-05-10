from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# 创建 ChromeOptions 对象
chrome_options = Options()
chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"  # 替换为实际路径

# 创建 Service 对象
service = Service(r"D:\etc\drivers\chromeDriver\136.0.7103.49\chromedriver.exe")

# 添加调试参数
chrome_options.add_argument("--verbose")
chrome_options.add_argument("--log-path=D:\chromedriver.log")

# 创建 WebDriver 实例
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://www.google.com")