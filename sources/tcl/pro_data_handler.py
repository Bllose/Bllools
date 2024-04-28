import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
import sys
import cmd2


class ProDataHandler(cmd2.Cmd):

    def do_load(self, _: cmd2.Statement):
        """
        通过加载配置文件， 直接登录生产数据查询页面
        """
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
                    login_url = data['tcl']['pro']['data']['url']
                    login_user = data['tcl']['pro']['data']['user']
                    login_password = data['tcl']['pro']['data']['password']
                    chrome_driver_path = data['driver']['browser']['chrome']

        if chrome_driver_path is None or len(chrome_driver_path) < 1:
            chrome_driver_path = os.environ.get("CHROME_DRIVER")
            if chrome_driver_path is None or not os.path.isfile(chrome_driver_path):
                print("请在系统总配置驱动路径 CHROME_DRIVER = /path/to/chromedriver")
                sys.exit(3)

        options = webdriver.ChromeOptions()
        # 执行完成后不要关闭浏览器
        options.add_experimental_option("detach", True)
        service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)  # Optional argument, if not specified will search path.
        self.driver.get(login_url)
        time.sleep(1) # Let the user actually see something!

        self.driver.implicitly_wait(5)

        userNameColumn = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/form/div[1]/input')
        userNameColumn.send_keys(login_user)
        passwordColumn = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/form/div[2]/input')
        passwordColumn.send_keys(login_password)

        login_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/form/div[3]/button')
        login_button.click()


if __name__ == '__main__':
    c = ProDataHandler()
    sys.exit(c.cmdloop())