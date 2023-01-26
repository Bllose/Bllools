import logging
import os, random


class Individual:
    def __repr__(self):
        return '{}-{}:{}'.format(self._key, self._name, self.getGenderCN())

    def __init__(self):
        """
        独立的个体
        key: id
        """
        self._key = None
        self._gender = None
        self._name = None

        """
        历史记录
        """
        self._history = None

    def set_key(self, key):
        self._key = key
        return self

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        self.set_gender(gender)

    @gender.getter
    def gender(self):
        return self._gender

    def set_gender(self, gender):
        if gender == '男' or gender == 'male' or gender == 'man':
            self._gender = 1
        else:
            self._gender = 0
        return self

    def getGenderCN(self):
        return '男' if self._gender == 1 else '女'

    def set_name(self, name):
        self._name = name
        return self

    @property
    def history(self):
        return self._history

    @history.getter
    def history(self):
        return self._history

    @history.setter
    def history(self, historyList):
        self.set_history(historyList)

    def set_history(self, history):
        self._history = history
        return self


class Group:
    def __repr__(self):
        return '[{} : {}]'.format(self.male, self.female)

    def __init__(self):
        """
        队伍
        """
        self._individuals = []
        self.male = 0
        self.female = 0
        self.group_history = []

    @property
    def individuals(self):
        return self._individuals

    @individuals.setter
    def individuals(self, target):
        """
        向队伍中添加成员， 需要同步更新：
        1、性别数量
        2、总历史记录更新
        """
        if isinstance(target, list):
            if len(target) > 0:
                self._individuals.extend(target)
                for cur in target:
                    self.recordGender(cur.gender)
                    self.recordHistory(cur.history)
        else:
            self._individuals.append(target)
            self.recordGender(target.gender)
            self.recordHistory(target.history)

    def recordHistory(self, history: list):
        if len(self.group_history) < 1:
            for cur in history:
                self.group_history.extend([cur])
        else:
            for index in range(self.group_history):
                self.group_history[index].append(history[index])

    def recordGender(self, gender: int):
        if gender == 1:
            self.male += 1
        else:
            self.female += 1

    @individuals.getter
    def individuals(self):
        return self._individuals


class OriginData:
    def __init__(self):
        """
        数据源对象
        本类的任务就是将数据源加载为 group对象; individual 对象。
        最终以列表的形式进行返回
        """
        self._path = None
        self._type = None
        self._file_name = None
        self._sheet = None
        self._config = None

    def set_path(self, path):
        self._path = path
        return self

    def set_type(self, type):
        self._type = type
        return self

    def set_file_name(self, name):
        self._file_name = name
        return self

    def set_sheet_name(self, sheet):
        self._sheet = sheet
        return self

    def load(self) -> list:
        """
        加载 excel, 将数据装载到 individual, group 对象中
        """
        if self._path is None or self._file_name is None or self._config is None:
            logging.error()

        from openpyxl import load_workbook
        # 加载工作簿
        wb = load_workbook(self._path + os.sep + self._file_name)
        # 获取sheet页
        ws = wb[self._sheet]

        '''
        从文件中将数据提取出来
        '''
        maxRow = ws.max_row
        # maxColumn = ws.max_column

        keyColumn = ws[self._config.key]
        nameColumn = ws[self._config.name]
        genderColumn = ws[self._config.gender]
        col_list = self._config.datas
        datasList = []
        for cur in col_list:
            curColumn = ws[cur]
            datasList.append(curColumn)

        groups = []
        for i in range(1, maxRow):
            dataList = []
            for datas in datasList:
                dataList.append(datas[i].value)

            individual = Individual()
            individual.set_key(keyColumn[i].value).set_name(nameColumn[i].value).set_gender(genderColumn[i].value).set_history(dataList)

            group = Group()
            group.individuals = individual
            groups.append(group)

        return groups

    def config(self):
        if self._config is None:
            self._config = self.Configure()
        return self._config

    class Configure:
        def __init__(self):
            """
            定义excel表格中的结构
            key所在列通过 key(column) 指定
            名字 name(column)
            性别 gender(column)
            数据 data(columns) 支持范围输出 -, ~ 作为分隔符

            默认第一行为表头
            如果没有表头，则使用 withOutHeader 指定
            """
            self._key = None
            self._name = None
            self._gender = None
            self._datas = []
            self._header = True

        @property
        def key(self):
            return self._key

        @key.setter
        def key(self, column):
            self._key = column

        @key.getter
        def key(self):
            return self._key

        def set_key(self, column):
            self._key = column
            return self

        @property
        def name(self):
            return self._name

        @name.setter
        def name(self, column):
            self._name = column

        @name.getter
        def name(self):
            return self._name

        def set_name(self, column):
            self._name = column
            return self

        @property
        def gender(self):
            return self._gender

        @gender.setter
        def gender(self, column):
            self._gender = column

        @gender.getter
        def gender(self):
            return self._gender

        def set_gender(self, column):
            self._gender = column
            return self

        @property
        def datas(self):
            return self._datas

        @datas.getter
        def datas(self):
            return self._datas

        @datas.setter
        def datas(self, columns):
            self.set_datas(columns)

        def set_datas(self, columns: str):
            """
            定义数据所属列
            支持范围输入，通过 - 或者 ~ 进行连接
            """
            if columns is None or len(columns) < 1:
                return self

            temp = []
            if '-' in columns:
                temp = columns.split('-')
            elif '~' in columns:
                temp = columns.split('~')

            if len(temp) == 0:
                self._datas.append(columns)
            elif len(temp) > 0:
                from helper.common import get_column_list
                self._datas.extend(get_column_list(temp[0], temp[1]))

        def withOutHeader(self):
            self._header = False
            return self


class Grouping:
    def __init__(self, groupList: list, decay: float = 0.7):
        """
        分组方法
        @param groupList: 待分组的原始数据，由 group 对象构成的列表
        @param decay: 衰减因子，配对时历史记录的衰减速度
        """
        self.originalDatas = groupList
        self.decayFactor = decay
        self.manList = []
        self.womanList = []
        for group in groupList:
            if group.individuals[0].gender == 1:
                self.manList.append(group)
            else:
                self.womanList.append(group)

    def process(self, order: int):
        """
        @param order: 分组数量

        分组的执行逻辑
        """
        manList, restManList = self.randomDrawing(self.manList, order)
        womenList, restWomenList = self.randomDrawing(self.womanList, order)

        # 合并 manList and womanList
        self.straightMerge(manList, order)
        self.straightMerge(womenList, order)
        # manList.extend(womenList)
        # self.straightMerge(manList, order)

        # rest 合入主列表

    def straightMerge(self, target: list, order: int):
        """
        目标队列按照衰减因子进行配对
        相似程度最低的一对相互匹配
        """
        if target is None or len(target) < 1:
            return

        # 首先选取随机元素作为队伍选择基础
        tempList = []
        tempLen = 0
        while tempLen < order:
            chose_index = random.randint(0, len(target) - 1)
            tempList.append(target.pop(chose_index))
            tempLen = len(tempList)

        # 根据队伍基础元素，计算关联关系， 选择最低关系系数组队
        for index in range(len(target)):
            cur = order % index


    def randomDrawing(self, target: list, order: int) -> tuple:
        """
        随机从列表 #target 中抽取元素， 最终生成一个初步合并的队列和一个剩余队列
        @param target: 待处理列表
        @param order: 每组人数量
        """
        orderLen = len(target)
        restLen = orderLen % order
        if restLen > 0:
            # 当需要将多余列表单独分出来时
            # 通过随机数确定去除元素
            # 将随机取出人员单独保存
            restList = []
            targetLen = orderLen - restLen

            while orderLen > targetLen:
                chose_index = random.randint(0, orderLen - 1)
                restList.append(target.pop(chose_index))
                orderLen = len(target)
            return target, restList
        if orderLen >= order:
            # 如果人员数量不需要额外保存， 则直接返回对象列表， 剩余列表则为空列表
            return target, []
        else:
            # 如果总数量还不够一次完整分组， 则将所有人作为剩余部分进行返回
            return [], target


if __name__ == '__main__':
    od = OriginData()
    od.set_path(os.path.abspath('../../resources'))\
        .set_file_name(r'HIT22VCteam.xlsx')\
        .set_sheet_name(r'Sheet1')
    od.config().set_key(r'B').set_name(r'C').set_gender(r'D').set_datas(r'E-J')
    originalDatasList = od.load()
    grouping = Grouping(originalDatasList)
    finalList = grouping.process()




