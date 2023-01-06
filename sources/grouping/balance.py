import logging


class Individual:
    def __init__(self):
        """
        独立的个体
        key: id
        """
        self.key = None
        self.gender = None
        self.name = None

        """
        历史记录
        """
        self.history = None

    def set_key(self, key):
        self.key = key
        return self

    def set_gender(self, gender):
        self.gender = gender
        return self

    def set_name(self, name):
        self.name = name
        return self

    def set_history(self, history):
        self.history = history
        return self


class Group:
    def __init__(self):
        """
        队伍
        """
        self.individuals = []

    @property
    def individuals(self):
        return self.individuals

    @individuals.setter
    def individuals(self, target):
        if isinstance(target, list):
            self.individuals.extend(target)
        else:
            self.individuals.append(target)

    @individuals.getter
    def individuals(self):
        return self.individuals


class OriginData:
    def __init__(self):
        self._path = None
        self._type = None
        self._file_name = None
        self._sheet = None
        self._config = None

    def path(self, path):
        self._path = path
        return self

    def type(self, type):
        self._type = type
        return self

    def file_name(self, name):
        self._file_name = name
        return self

    def sheet_name(self, sheet):
        self._sheet = sheet
        return self

    def load(self):
        if self._path is None or self._file_name is None or self._config is None:
            logging.error()

        from openpyxl import load_workbook
        import os
        # 加载工作簿
        wb = load_workbook(self._path + os.sep + self._file_name)
        # 获取sheet页
        ws = wb[self._sheet]

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

        def key(self, column):
            self._key = column
            return self

        def name(self, column):
            self._name = column
            return self

        def gender(self, column):
            self._gender = column
            return self

        def datas(self, columns: str):
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


if __name__ == '__main__':
    od = OriginData()
    od.path(r'D:\workplace\temp\bllools\resources')\
        .file_name(r'HIT22VCteam.xlsx')\
        .sheet_name(r'Sheet1')
    od.config().key(r'B').name(r'C').gender(r'D').datas(r'E-J')
    od.load()

    student = Individual()

    team = Group()

    team.add(student)


