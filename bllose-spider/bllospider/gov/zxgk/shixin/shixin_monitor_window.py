from bllospider.gov.zxgk.shixin.share.contents import *
import time
import threading
import logging

XPATH_NOTICE_CAPATCHA_ERROR = '//*[@id="layui-layer1"]'
SAFE_COUNTER_MAX = 4

def window_monitor(cralwer: ShixinCralwer, _MONITOR_WIN_LOCKED):
    THREAD_NAME = threading.current_thread().name
    """
    悬浮窗口监控
    """
    save_counter = 0
    while True:
        try:
            # 悬浮窗口
            subwindows = cralwer.driver.find_elements(By.XPATH, XPATH_NOTICE_CAPATCHA_ERROR)
            if subwindow:
                # 悬浮窗口出现
                logging.warning(THREAD_NAME + ' -> 悬浮窗口出现')
                # 关闭悬浮窗口
                save_counter = 0
                _MONITOR_WIN_LOCKED.clear()
            else:
                # 悬浮窗口未出现
                logging.warning(THREAD_NAME + ' -> 悬浮窗口未出现')
                save_counter += 1
            time.sleep(NORMAL_WAITING_TIME)
            if save_counter >= SAFE_COUNTER_MAX:
                _MONITOR_WIN_LOCKED.set()
        except:
            pass