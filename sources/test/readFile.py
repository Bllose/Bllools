import mmap
from collections import deque

# with open(r'D:\QuantitativeDatas\Stocks\600000.SH.csv') as f:
#     s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
#     print(s.find(bytes('20230420 11:40:20.880', 'utf-8')))


def buff_count(file_name) -> tuple:
    with open(file_name, 'rb') as f:

        count = 0
        buf_size = 1024 * 1024
        buf = f.read(buf_size)
        length = 0
        while buf:
            length += buf_size

            positions = [i for (i, j) in enumerate(buf.decode()) if j == '\n']
            count += len(positions)

            lastPosition = positions[-1]
            if lastPosition < buf_size:
                length -= buf_size
                length += positions[-3] + 1

            buf = f.read(buf_size)
        count -= 1

        return count, length


total, postion = buff_count(r'D:\QuantitativeDatas\Stocks\600000.SH.csv')
fo = open(r'D:\QuantitativeDatas\Stocks\600000.SH.csv', 'r')
fo.seek(postion, 0)


print(fo.readline(), end='')
print('##################################################')
print(fo.readline(), end='')

