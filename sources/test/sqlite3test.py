# import sqlite3
# import logging

# logging.basicConfig(level=logging.DEBUG,
#                         format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
#                         datefmt='%H:%M:%S')

# # 创建与数据库的连接
# conn = sqlite3.connect('test.db')
# #创建一个游标 cursor
# cur = conn.cursor()
# # 建表的sql语句
# sql_text_1 = '''CREATE TABLE scores
#            (姓名 TEXT,
#             班级 TEXT,
#             性别 TEXT,
#             语文 NUMBER,
#             数学 NUMBER,
#             英语 NUMBER);'''
# # 执行sql语句
# # cur.execute(sql_text_1)
# # 插入单条数据
# sql_text_2 = "INSERT INTO scores VALUES('A', '一班', '男', 96, 94, 98)"
# cur.execute(sql_text_2)
# data = [('B', '一班', '女', 78, 87, 85),
#     ('C', '一班', '男', 98, 84, 90),
#     ]
# cur.executemany('INSERT INTO scores VALUES (?,?,?,?,?,?)', data)
# # 连接完数据库并不会自动提交，所以需要手动 commit 你的改动conn.commit()
# # 查询数学成绩大于90分的学生
# sql_text_3 = "SELECT * FROM scores WHERE 数学>90"
# cur.execute(sql_text_3)
# # 获取查询结果
# logging.warning(cur.fetchall())

a = input(': ')
print(a, end='\r\n')
# print(b, end='\r\n')
print('DONE')
