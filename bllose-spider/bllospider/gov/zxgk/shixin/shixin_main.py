from bllospider.gov.zxgk.shixin.shixin_tasks import mainTask
from bllospider.gov.zxgk.shixin.shixin_monitor_capatch import moniter_captcha
from bllospider.gov.zxgk.shixin.shixin_monitor_window import window_monitor
from bllospider.gov.zxgk.shixin.share.contents import ShixinCralwer, cralwer
import threading
from threading import Event
import urllib3
urllib3.util.connection.DEFAULT_MAX_POOL_SIZE = 50


# 验证器锁
MONITER_CAPTCHA_LOCKED = Event()
# 页面弹窗监控器锁
MONITOR_WIN_LOCKED = Event()


def do_main():
    global cralwer

    cralwer = ShixinCralwer()
    cralwer.init_root_url()

    mainTaskThread = threading.Thread(target=mainTask,name='MainTask', args=(cralwer, MONITER_CAPTCHA_LOCKED, MONITOR_WIN_LOCKED))
    moniter_captchaThread = threading.Thread(target=moniter_captcha,name='CaptchaMonitor', args=(cralwer, MONITER_CAPTCHA_LOCKED))
    # window_monitorThread = threading.Thread(target=window_monitor,name='WinMonitor', args=(cralwer, MONITOR_WIN_LOCKED))


    mainTaskThread.start()
    moniter_captchaThread.start()
    # window_monitorThread.start()

    mainTaskThread.join()
    moniter_captchaThread.join()
    # window_monitorThread.join()

    print('done')


if __name__ == '__main__':
    do_main()