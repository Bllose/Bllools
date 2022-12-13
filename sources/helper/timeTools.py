import datetime, calendar
from typing import List, Tuple


def now_week_of_month() -> int:
    return get_week_of_month(int(time.strftime("%Y")), int(time.strftime("%m")), int(time.strftime("%d")))


def get_week_of_month(year, month, day) -> int:
    begin = int(datetime.date(year, month, 1).strftime("%W"))
    end = int(datetime.date(year, month, day).strftime("%W"))

    return end - begin + 1


# 根据当前时间，返回上个月的最后一天
def lastMonth(now:datetime.datetime) -> datetime.datetime:
    firstDayOfThisMonth = now.replace(day = 1)
    lastDayOfLastMonth = firstDayOfThisMonth - datetime.timedelta(days=1)
    return lastDayOfLastMonth


# 获取当前时间和上个月最后一天的时间
def getThisMonthWithLast() -> List[datetime.datetime]:
    resultList = [datetime.datetime.now()]
    firstDayOfThisMonth = datetime.datetime.now().replace(day=1)
    lastDayOfLastMonth = firstDayOfThisMonth - datetime.timedelta(days=1)
    resultList.append(lastDayOfLastMonth)
    return resultList


def getTheWeekOfThisMonth(target: datetime.datetime, curMonth: datetime.datetime) -> int:
    # 判断输入的时间属于当月的第几周
    # param: target 被判断的时间
    # param: curMonth 用以判断的所属月份
    # return: 目标日期属于指定月份的第几周，当未匹配上时，返回 -1
    # PS: getTheWeekOfThisMonth(datetime.datetime.strptime('2022-5-1', '%Y-%m-%d'), datetime.datetime.strptime('2022-4-1', '%Y-%m-%d'))
    #     5
    #
    #     getTheWeekOfThisMonth(datetime.datetime.strptime('2022-3-28', '%Y-%m-%d'), datetime.datetime.strptime('2022-4-1', '%Y-%m-%d'))
    #     1
    #
    #     getTheWeekOfThisMonth(datetime.datetime.strptime('2022-3-27', '%Y-%m-%d'), datetime.datetime.strptime('2022-4-1', '%Y-%m-%d'))
    #     -1

    targetDay = target.strftime('%Y-%m-%d')
    cal = calendar.Calendar()
    weekCounter = 1
    for theWeek in cal.monthdatescalendar(curMonth.year, curMonth.month):
        for theDay in theWeek:
            if theDay.strftime('%Y-%m-%d') == targetDay:
                # print('判断目标时间{}, 为第{}周'.format(target, str(weekCounter)))
                return weekCounter
        weekCounter += 1
    return -1


def getBeginAndEnd(target:datetime.datetime) -> Tuple[datetime.datetime, datetime.datetime, datetime.datetime]:
    # 针对当前时间，获取完整周所对应的第一天，当前时间和最后一天
    # 完整周统计
    # @return 完整周第一天；输入时间点； 完整周最后一天
    # PS: 输入时间点 2022-4-12
    # 输出: (2022-3-28, 2022-4-12, 2022-5-1)
    # cal = calendar.Calendar()
    total = calendar.Calendar().monthdatescalendar(year=target.year,month=target.month)
    firstWeek = total.pop(0)
    firstDay = firstWeek.pop(0)

    lastWeek = total.pop()
    lastDay = lastWeek.pop()

    return firstDay, target, lastDay


def getEveryDayThisMonth() -> []:
    """
    获取到目前为止本月的每一天
    每一天的格式通过yyyy-MM-dd进行展示
    """
    result = []

    now = datetime.datetime.now()

    for day in range(1,now.day):
        this_month_start = datetime.datetime(now.year, now.month, day)
        result.append(this_month_start.strftime('%Y-%m-%d'))

    return result


def getEveryDayOfTheMonth(year: int, month: int) -> []:
    """
    返回指定月份的每一天
    """
    result = []
    try:
        for day in range(1, 32):
            this_month_start = datetime.datetime(year, month, day)
            result.append(this_month_start.strftime('%Y-%m-%d'))
    except (ValueError, TypeError):
        result.count(0) # DO NOTHING
    return result



# 判断当前日期是星期几 yyyy-MM-dd
def getTheDayOfTheWeek(target: str) -> int:
    return datetime.datetime.strptime(target, '%Y-%m-%d').weekday()


def getTimeStamp14() -> int:
    # 获取长度为14的时间戳
    return round(time.time() * 1000)


if __name__ == '__main__':
    import time
    # print(get_week_of_month(int(time.strftime("%Y")), int(time.strftime("%m")), int(time.strftime("%d"))))
    # print(getThisMonthWithLast())
    # print(getTheWeekOfThisMonth(datetime.datetime.strptime('2022-3-27', '%Y-%m-%d'), datetime.datetime.strptime('2022-4-1', '%Y-%m-%d')))
    # print(getBeginAndEnd(datetime.datetime.now()))
    # print(getEveryDayThisMonth())
    # print(getTheDayOfTheWeek('2022-07-04'))
    print(getEveryDayOfTheMonth(2022, 9))
