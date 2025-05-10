from bllospider.gov.zxgk.shixin.share.contents import *
from bllonfig.Config import bConfig
from bllospider.gov.zxgk.shixin.DoubaoImageRecognize import identify_verification_code
import time
import logging
import base64

from selenium.common.exceptions import ElementClickInterceptedException

SAFE_COUNTER_MAX = 10
HAD_SET_CAPTCHA = False

def moniter_captcha(_cralwer: ShixinCralwer, _MONITER_CAPTCHA_LOCKED):
    logging.basicConfig(filename='moniterCaptcha.log', format='captcha - %(asctime)s - %(levelname)s - %(message)s')
    global cralwer
    global MONITER_CAPTCHA_LOCKED
    global HAD_SET_CAPTCHA

    cralwer = _cralwer
    MONITER_CAPTCHA_LOCKED = _MONITER_CAPTCHA_LOCKED

    # 安全计数器
    safe_counter = 0
    # 等待页面首次加载
    time.sleep(10) 

    # 验证码输入框
    yzm_input = input_clean_set(cralwer, XPATH_CAPTCHA_INPUT)
    # 获取当前所有请求
    current_requests = cralwer.driver.requests

    theLatestCaptchaRequest = get_the_latest_captcha_request(current_requests)
    if theLatestCaptchaRequest:
        try_to_set_captcha(theLatestCaptchaRequest, yzm_input)

    requestCounter = len(current_requests)
    while True:
        current_requests = cralwer.driver.requests
        if requestCounter < len(current_requests):
            # 新的请求被添加
            new_requests = current_requests[requestCounter:]
            theLatestCaptchaRequest = get_the_latest_captcha_request(new_requests)
            if theLatestCaptchaRequest:
                logging.warning('发现新的验证码请求，重新设置验证码')
                MONITER_CAPTCHA_LOCKED.clear()
                HAD_SET_CAPTCHA = try_to_set_captcha(theLatestCaptchaRequest, yzm_input)
            else:
                logging.warning(f'没有验证码请求，safe_counter{safe_counter}')
                safe_counter += 1
            requestCounter = len(current_requests)
        else:
            logging.warning(f'没有新请求，safe_counter{safe_counter}')
            safe_counter += 1
        time.sleep(SHORT_WAITING_TIME)
        if safe_counter > SAFE_COUNTER_MAX and HAD_SET_CAPTCHA:
            logging.warning(f'safe_counter{safe_counter}')
            MONITER_CAPTCHA_LOCKED.set()
            safe_counter = 0
        if safe_counter > SAFE_COUNTER_MAX * 2:
            logging.warning(f'safe_counter{safe_counter}')
            safe_counter = 0
            logging.warning(f'重新加载页面')
            cralwer.driver.refresh()
            time.sleep(LONG_WAITING_TIME)

def try_to_set_captcha(request, yzm_input):
    yzm_input.clear()

    logging.warning(f'尝试自动识别验证码{request}')
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
                time.sleep(SHORT_WAITING_TIME)
                yzm_input.send_keys(captcha_recogonized)
                time.sleep(SHORT_WAITING_TIME)
                logging.warning(f'验证码识别成功，自动输入 -> {captcha_recogonized}')
                return True
    # 到这里说明未能正确赋值验证码，返回False
    logging.warning(f'验证码识别失败，刷新验证码')
    click_captchaImg(cralwer.driver)
    return False

def get_the_latest_captcha_request(requests):
    for request in requests[::-1]:
        if request.response and 'captchaNew.do' in request.url:
            return request
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