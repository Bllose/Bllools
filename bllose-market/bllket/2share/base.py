import tushare as ts
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv('tushare_token')
ts.set_token(token)

pro = ts.pro_api()

#查询当前所有正常上市交易的股票列表
# data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
# 导出excel文件
# data.to_excel('data.xlsx', index=False) 

