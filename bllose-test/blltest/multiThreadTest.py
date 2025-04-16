from concurrent.futures import ThreadPoolExecutor

def square(n):
    return n * n

with ThreadPoolExecutor(max_workers=3) as executor:
    # 提交任务
    futures = [executor.submit(square, i) for i in range(5)]
    # 获取结果
    for future in futures:
        print(future.result())  # 输出 0, 1, 4, 9, 16


# Python线程受GIL限制
import threading
def cpu_task():
    while True: pass
t1 = threading.Thread(target=cpu_task)
t2 = threading.Thread(target=cpu_task)
t1.start()  # 两个线程无法同时占据CPU


shared_data = []  # 全局变量共享
lock = threading.Lock()

def unsafe_thread():
    global shared_data
    shared_data.append(1)  # 需要加锁保证原子性

def safe_thread():
    with lock:
        shared_data.append(1)