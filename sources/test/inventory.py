import os
import datetime
import logging

logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
                        datefmt='%H:%M:%S')

class ContextInfo():
    def __init__(self):
        self.ContextInfo = 0.0
        self.sector_code_list = []


class mockTest():
    def __init__(self):
        self.ContextInfo = ContextInfo()
        self.ContextInfo.bigAttack = 300000 # 三十万算主力进攻资金

        self.ContextInfo.sector_code_list = ['002292.SZ', '000651.SZ', '002712.SZ', '600030.SH', '002558.SZ', '603169.SH',
                                        '002197.SZ', '601377.SH', '002343.SZ', '002280.SZ', '000725.SZ', '001330.SZ',
                                        '601928.SH', '601136.SH', '600977.SH', '002739.SZ', '002425.SZ', '600732.SH',
                                        '600435.SH', '002315.SZ', '000688.SZ', '002864.SZ', '603163.SH', '002291.SZ',
                                        '601702.SH', '000978.SZ', '601007.SH', '603199.SH', '600138.SH', '002429.SZ',
                                        '605081.SH', '000430.SZ', '002306.SZ', '600750.SH', '600358.SH', '600771.SH',
                                        '603063.SH', '601058.SH', '000963.SZ', '600038.SH', '002970.SZ', '603170.SH',
                                        '000686.SZ', '600511.SH', '002773.SZ', '605186.SH', '002299.SZ', '600610.SH',
                                        '603235.SH', '600998.SH', '002262.SZ', '603733.SH', '600774.SH']

        self.ContextInfo.workSpace = r'D:\QuantitativeDatas'
        self.ContextInfo.stocksPath = self.ContextInfo.workSpace + os.sep + r'Stocks' + os.sep + datetime.datetime.now().strftime(
            '%Y%m%d')
        if not os.path.exists(self.ContextInfo.stocksPath):
            os.mkdir(self.ContextInfo.stocksPath)
        # 初始化一些必要参数
        init_inventory(self.ContextInfo)


def init_inventory(ContextInfo):
    # 读取已经保存本地的文件， 将数据加载到内存
    recorderMap = {}

    files = os.listdir(ContextInfo.stocksPath)
    for file in files:
        if not file.endswith('csv'):
            logging.debug(f'非法文件，跳过：{file}')
            continue
        code = file[:-4]  # '剔除掉尾缀：.csv'
        loadedFile = open(ContextInfo.stocksPath + os.sep + file, 'r')
        _ = loadedFile.readline()  # 表头跳过
        curLine = loadedFile.readline().split(',')
        while curLine and len(curLine) > 1:
            curMap = {}
            if code not in recorderMap:
                # 第一次加载，初始化第一行数据
                curMap['offensive'] = 0.0
                curMap['offentotal'] = 0.0
                # 例行更新
                normalDatas(curMap, curLine)
                recorderMap[code] = curMap
            else:
                curMap = recorderMap[code]
                amountNew = float(curLine[6])
                amountOld = float(curMap['amount'])
                amountChange = amountNew - amountOld # 成交额总量变化，计算出当前tick所产生的交易额
                if curMap['lastPrice'] >= curLine[1]:
                    if curMap['lastPrice'] == curLine[1]:
                        # 当价格没有变动时，判断金额是否足够大
                        if amountChange >= ContextInfo.bigAttack:
                            logging.debug(
                                f"time:{curLine[0]}, upAmount:{amountChange}, curAmount:{curMap['offentotal'] + amountChange}")
                            curMap['offensive'] = amountChange  # 记录本次进攻资金
                            curMap['offentotal'] += amountChange # 将本次进攻资金纳入总量
                else:
                    logging.debug(f"time:{curLine[0]}, upAmount:{amountChange}, curAmount:{curMap['offentotal'] + amountChange}")
                    # 当前tick价格已经高于前一次价格，股价上涨，记录本次进攻资金
                    curMap['offensive'] = amountChange  # 记录本次进攻资金
                    curMap['offentotal'] += amountChange  # 将本次进攻资金纳入总量
                # 例行更新
                normalDatas(curMap, curLine)
            # 下一行
            curLine = loadedFile.readline().split(',')


def normalDatas(curMap, curLine):
    curMap['timetag'] = curLine[0]
    curMap['lastPrice'] =  curLine[1]
    curMap['open'] = curLine[2]
    curMap['high'] = curLine[3]
    curMap['low'] = curLine[4]
    curMap['lastClose'] = curLine[5]
    curMap['amount'] = curLine[6]
    curMap['volume'] = curLine[7]
    curMap['pvolume'] = curLine[8]


if __name__ == '__main__':
    mockTest()