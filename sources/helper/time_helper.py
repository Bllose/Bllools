import time
import datetime

t = time.time()
#
# print(t)  # 原始时间数据
# print(int(t))  # 秒级时间戳
# print(int(round(t * 1000)))  # 毫秒级时间戳
print(int(round(t * 1000000)))  # 微秒级时间戳

dt = '2024-04-07 11:03:54'
ts = int(time.mktime(time.strptime(dt, "%Y-%m-%d %H:%M:%S")) * 1000000)
print(ts)
