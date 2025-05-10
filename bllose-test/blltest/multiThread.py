import logging
import threading
import time


def worker():
    # 获取当前线程的名字
    thread_name = threading.current_thread().name
    logging.info(f'Thread {thread_name} is starting')
    time.sleep(2)
    logging.info(f'Thread {thread_name} is finishing')


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(threadName)s - %(levelname)s - %(message)s')
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, name=f'Thread-{i}')
        threads.append(t)
        t.start()

    for t in threads:
        t.join()