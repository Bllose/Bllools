import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import sys
import cmd2
import logging


class UatMbyqHandler(cmd2.Cmd):

    def __init__(self):
        super().__init__()


    load_parser = cmd2.Cmd2ArgumentParser()
    load_parser.add_argument('-l', '--loglevel', type=int, default=40, help='设置日志等级DEBUG:10; INFO:20; WARNING:30; ERROR:40(DEFUALT)')
    load_parser.add_argument('-p', '--proxy', type=str, help='服务器代理')
    

    @cmd2.with_argparser(load_parser)
    def do_load(self, args):
        """
        通过加载配置文件， 直接登录生产数据查询页面
        """
        logging.basicConfig(level=args.loglevel)
        # 当前文件的绝对路径
        exe_path = sys.argv[0]
        # 当前文件所在目录
        exe_dir = os.path.dirname(exe_path)
        current_work_dir = exe_dir
        configYml = 'mbyq_config.yml'

        absYml = current_work_dir + os.sep + configYml
        logging.debug(f'加载配置文件: {absYml}')
        config = ''
        if os.path.isfile(absYml):
            with open(absYml, 'r', encoding='utf-8') as f:
                config = f.read()
                if config is not None and len(config) > 1:
                    import yaml
                    data = yaml.safe_load(config)
                    logging.info(f'通过文件 {configYml} 加载相关配置')
                    login_url = data['tcl']['uat']['mbyq']['url']
                    chrome_driver_path = data['driver']['browser']['chrome'].strip()

        if chrome_driver_path is None or len(chrome_driver_path) < 1:
            chrome_driver_path = os.environ.get("CHROME_DRIVER")
            if chrome_driver_path is None or not os.path.isfile(chrome_driver_path):
                print("请在系统总配置驱动路径 CHROME_DRIVER = /path/to/chromedriver")
                sys.exit(3)

        self.options = webdriver.ChromeOptions()
        # 执行完成后不要关闭浏览器
        self.options.add_experimental_option("detach", True)
        if args.proxy is not None and len(args.proxy) > 1:
            # 设置代理
            self.options.add_argument("--proxy-server=" + args.proxy)
        logging.debug(f'加载驱动{chrome_driver_path}')


        service = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=service, options=self.options)  # Optional argument, if not specified will search path.
        self.driver.get(login_url)
            
        time.sleep(1) # Let the user actually see something!
        # 隐式等待
        self.driver.implicitly_wait(5)

        userNameColumn = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/form/div[1]/input')
        # userNameColumn.send_keys(login_user)
        passwordColumn = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/form/div[2]/input')
        # passwordColumn.send_keys(login_password)

        login_button = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/form/div[3]/button')
        login_button.click()

        # 显性等待 好像不起作用，还是会找不到组件
        # WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/nav/div[2]/div/ul/li[2]/a')))
        self.driver.implicitly_wait(5)
        # 选择SQL查询栏位
        self.driver.find_element(By.XPATH, '/html/body/div[1]/nav/div[2]/div/ul/li[2]/a').click()
        self.driver.implicitly_wait(5)
        # 跳入 在线查询子页面
        self.driver.find_element(By.XPATH, '/html/body/div[1]/nav/div[2]/div/ul/li[2]/ul/li[1]/a').click()

        self.driver.implicitly_wait(5)
        # WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[1]/div/div[2]/form/div[2]/div[1]/div/button/div/div/div')))
        # 选择 实例
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[1]/div/div[2]/form/div[2]/div[1]/div/button/div/div/div').click()
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[1]/div/div[2]/form/div[2]/div[1]/div/div/div[1]/input').send_keys('极光生产只读实例')
        # 选择生产实例
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[1]/div/div[2]/form/div[2]/div[1]/div/div/div[2]/ul/li[2]/a').click()
        # 选择数据库
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[1]/div/div[2]/form/div[2]/div[2]/div/button/div/div/div').click()
        # 选择order数据库
        self.driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[1]/div/div[2]/form/div[2]/div[2]/div/div/div[2]/ul/li[22]/a').click()
        # 获取SQL 输入框
        self.line_group = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[1]/div/div[2]/form/div[1]/pre/div[2]/div/div[3]')
        # self.line_group.text 将会展示面板上所有SQL
        


    speak_parser = cmd2.Cmd2ArgumentParser()
    speak_parser.add_argument('-p', '--piglatin', action='store_true', help='atinLay')
    speak_parser.add_argument('-s', '--shout', action='store_true', help='N00B EMULATION MODE')
    speak_parser.add_argument('-r', '--repeat', type=int, help='output [n] times')
    speak_parser.add_argument('words', nargs='+', help='words to say')

    @cmd2.with_argparser(speak_parser)
    def do_speak(self, args):
        """Repeats what you tell me to."""
        words = []
        for word in args.words:
            if args.piglatin:
                word = '%s%say' % (word[1:], word[0])
            if args.shout:
                word = word.upper()
            words.append(word)
        repetitions = args.repeat or 1
        for _ in range(min(repetitions, self.maxrepeats)):
            # .poutput handles newlines, and accommodates output redirection too
            self.poutput(' '.join(words))


if __name__ == '__main__':
    c = UatMbyqHandler()
    sys.exit(c.cmdloop())