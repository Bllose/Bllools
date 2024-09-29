import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

def ageRangeCalculate(minimalAge: int, maxmalAge: int):
    now = datetime.now()
    date_mini_years_ago = now - relativedelta(years=minimalAge)  
    date_max_years_age = now - relativedelta(years=maxmalAge)

    print("当前日期:", now.strftime("%Y-%m-%d"))  
    print("mini年前的日期:", date_mini_years_ago.strftime("%Y-%m-%d"))
    print("max年前的日期:", date_max_years_age.strftime("%Y-%m-%d"))

if __name__ == '__main__':
    ageRangeCalculate(65, 70)