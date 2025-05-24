import tushare as ts
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('tushare_token')
ts.set_token(token)

pro = ts.pro_api()
# 多个股票
# 300059.SZ 东方财富
# 002303.SZ 美盈森
df = pro.daily(ts_code='300059.SZ,002303.SZ', start_date='20200522', end_date='20250522')
# 保存到excel
df.to_excel('data_market.xlsx', index=False) 
