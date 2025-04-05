from concurrent.futures import ThreadPoolExecutor

def square(n):
    return n * n

with ThreadPoolExecutor(max_workers=3) as executor:
    # 提交任务
    futures = [executor.submit(square, i) for i in range(5)]
    # 获取结果
    for future in futures:
        print(future.result())  # 输出 0, 1, 4, 9, 16