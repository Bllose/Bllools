import logging
import math
from grouping.relationship.Relation import UndirectRelation


class Student:
    def __init__(self,
                 name,
                 code,
                 number,
                 factor:float = 0.7,
                 times: int = 6):
        """
        :param name: 姓名
        :param code: 学号
        :param number: 班级编号, 该字段严格依次递增， 用于关系处理的关键字段， 从1开始编号
        :param factor: 关系因子，关系递减程度
        :param times: 有效关系记录， 原则上是向前递归几次关系才统计，太过久远的关系忽略
        """
        self.name = name
        self._gender = ''
        self.code = code
        self.number = number
        self.factor = factor
        self.times = times
        self._relation = []
        # 历史上已经被分配的团队记录
        self._history = []

    def __repr__(self):
        return self.name + ' - ' + str(self.number) + ' : ' + self.get_gender_cn()

    @property
    def relation(self):
        return self._relation

    @relation.setter
    def relation(self, value):
        if isinstance(value, list) and len(value) > 0 and isinstance(value[0], int):
            self._relation = value
        else:
            logging.error('illegal relation!')
            return

    @relation.getter
    def relation(self):
        return self._relation

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, value):
        """
        性别统一为: 0 - 女性；1 - 男性
        :param value: 目前接受 男女; man,woman; male,female
        :return:
        """
        if not isinstance(value, int):
            if 'man' == value or '男' == value or 'male' == value:
                self._gender = 1
            else:
                self._gender = 0
        else:
            if value != 0 and value != 1:
                logging.error('illega gender!')
                self._gender = 0
            else:
                self._gender = value

    @property
    def history(self):
        return self._history

    @history.setter
    def history(self, value):
        if isinstance(value, list):
            self._history.extend(value)
        else:
            self._history.append(value)

    @history.getter
    def history(self):
        return self._history

    def get_gender_cn(self) -> str:
        """
        获取性别的中文名
        :return:
        """
        if self._gender == 0 or self._gender == 'female' or self._gender == 'woman' or self._gender == '女':
            return '女'
        return '男'

    def correlation(self, target) -> float:
        """
        比较两个同学之间的关联关系
        越久之前同组的关系越稀薄
        假如关系递减因子为 0.5
        [8, 7] vs [8, 4] -> 0 + 1 * 0.5 = 0.5
        [4, 1] vs [4, 1] -> 1 + 1 * 0.5 = 1.5
        [1, 2, 3] vs [1, 2, 3] -> 1 + 1 * 0.5 + 1 * 0.25 = 1.75

        :param target: 被比较的Student
        :return: 关系关联性系数
        """
        result = float(0)
        total = len(self._history)
        if total == 0:
            return 0

        # 从最近的一次进行比较
        # 从第二次开始进行递减
        total = len(self._history)
        for index in range(total - 1, -1, -1):
            if total - 1 - index > self.times:
                break
            origin = self._history[index]
            compare = target.history[index]
            if origin == compare:
                result += float(1/total) * math.pow(self.factor, total - 1 - index)
            total -= 1
        return round(result, 5)

    def init_relation(self, len:int):
        self._relation = [0.00] * len

    def correlation_list(self, members:list, relation_recorder: list):
        if len(self._relation) != len(members):
            self.init_relation(len(members))

        for index in range(len(members)):
            compare_member = members[index]
            relation_rate = self.correlation(compare_member)
            if relation_rate not in relation_recorder:
                relation_recorder.append(relation_rate)
            self._relation[index] = relation_rate


class Team:
    """
    组成的小组

    """
    def __init__(self):
        self._students = [] # 本小组成员
        self.boy_num = 0
        self.girl_num = 0
        self._history = [] # 小组成员总历史
        self._relation = [] # 小组与其他组的关系记录列表

    def __repr__(self):
        return '{} - {}:{}'.format(len(self._students), self.boy_num, self.girl_num)

    @property
    def students(self):
        return self._students

    @students.setter
    def students(self, value):
        if isinstance(value, list):
            self._students.extend(value)
            for student in value:
                self.add_history(student.history)
                if student.gender == 0:
                    self.girl_num += 1
                else:
                    self.boy_num += 1
        else:
            self._students.append(value)
            self.add_history(value.history)
            if value.gender == 0:
                self.girl_num += 1
            else:
                self.boy_num += 1

    @students.getter
    def students(self):
        return self._students

    @property
    def history(self):
        return self._history

    @history.getter
    def history(self):
        return self._history

    def add_history(self, history: list):
        if len(self._history) == 0:
            self._history = [(x,) for x in history]
        else:
            for index in range(len(history)):
                self._history[index] += (history[index],)

    def correlation_list(self, groups: list, factor, times) -> None:
        if len(self._relation) != len(groups):
            self._relation = [0.00] * len(groups)
        for index in range(len(groups)):
            another = groups[index]
            relation = self.correlation(another, factor, times)
            self._relation[index] = round(relation, 5)

    def correlation(self, another, factor: float, times: int) -> float:
        """
        计算当前小组与对比小组的关联关系
        PS: [(1,2,), (3,4,)] vs [(1,4,),(2,3,)]
        :param times: 关系最大统计伦次
        :param factor: 关系递减因子
        :param another: 进行比较的另外一个小组
        :return: 关系值
        """
        total_relation = 0.00
        denominator = len(self._history)
        if len(another.history) != denominator:
            logging.error('[{}] : [{}] 两个队伍的历史记录次数不一致，无法进行关系匹配!'.format(self, another))
            return -1
        for index in range(denominator-1, -1, -1):
            oneHander = self._history[index]
            anotherHander = another.history[index]
            repeat_time = self.getDuplicationTimes(oneHander, anotherHander)
            total_relation += (repeat_time / denominator) * math.pow(factor, denominator - 1 - index)
        return total_relation

    def getDuplicationTimes(self, one_hander:tuple, another_hander:tuple) -> int:
        result = 0
        temp_list = []
        for cur in one_hander + another_hander:
            if cur in temp_list:
                result += 1
            else:
                temp_list.append(cur)
        return result


class Class:
    def __init__(self):
        """
        本班级分组基于无相同
        通过计算同学之间的关系度，寻找最优解
        """
        self.total = 0
        self._students = []
        self._teams = []
        self.man = []
        self.woman = []
        self.re_matrix = []
        self.te_matrix = []
        self.relation_recorder = []

    @property
    def students(self):
        return self._students

    @students.getter
    def students(self):
        return self._students

    @students.setter
    def students(self, value):
        """
        欢迎新同学加入
        :param value: 同学，或者同学们
        :return:
        """
        if isinstance(value, list):
            for student in value:
                self.absorb_student(student)
            self.total += len(value)
        else:
            self.absorb_student(value)
            self.total += 1

    @property
    def teams(self):
        return self._teams

    @teams.setter
    def teams(self, value):
        if isinstance(value, list):
            self._teams.extend(value)
        else:
            self._teams.append(value)

    @teams.getter
    def teams(self):
        return self._teams

    def absorb_student(self, student) -> None:
        """
        吸纳同学信息
        初始化同学的关联关系数组
        并记录男女分组
        :param student: 入组同学
        """
        if student.gender == 0:
            self.woman.append(student.number)
        else:
            self.man.append(student.number)
        self._students.append(student)

    def establish_next_grouping(self, times: int) -> dict:
        """
        计算下一次分组
        :return: 返回一个分组结果
        """
        boy_list = self.man
        girl_list = self.woman
        least_each_team = int(self.total/times) # 每组至少人数
        least_each_boy = int(len(boy_list)/times) # 每组至少男生数
        least_each_girl = int(len(girl_list)/times) # 每组至少女生数

        # 通过关系度进行匹配
        # 尽可能将关系淡的同学组成一队
        for relation in self.relation_recorder:
            for row in range(len(self.re_matrix)):
                cur_line = self.re_matrix[row]
                if self.allOfNegative(cur_line):
                    logging.debug('{} 已经配对，跳过匹配'.format(self._students[row]))
                    continue
                for column in range(len(cur_line)):
                    if relation >= cur_line[column] > -1:
                        logging.debug('{} 与 {} 配对成功, 他们的关系度为: {}'.format(row, column, cur_line[column]))
                        new_team = Team()
                        new_team.students = self._students[row]
                        new_team.students = self._students[column]
                        self._teams.append(new_team)
                        self.negative_matirx(row, column)
                        break

        for index in range(len(self._teams)):
            curTeam = self._teams[index]
            curTeam.correlation_list(groups = self._teams, factor=0.7, times=6)

        self.establish_relation_matrix()

        while len(self._teams) >= (times * 2 - 1):
            self.merge_team()

        if len(self._teams) > times:
            self.merge_team()
        logging.debug('初步组队完成 ...')

    def merge_team(self):
        target_index = -1
        new_team = []
        for curTeamRelationList in self.te_matrix:
            target_index += 1
            if self.allOfNegative(curTeamRelationList):
                continue
            sorted_relation = sorted(curTeamRelationList, reverse=True)
            min_relation = sorted_relation.pop()
            while min_relation == -1:
                min_relation = sorted_relation.pop()
            part_index = curTeamRelationList.index(min_relation)
            part = self._teams[part_index]
            target = self._teams[target_index]
            target.students = part.students
            new_team.append(target)
            self.negative(self.te_matrix, target_index, part_index)
        self._teams = new_team

    def negative(self, matrix, row, column):
        matrix[row] = [-1 for x in matrix[row]]
        matrix[column] = [-1 for x in matrix[row]]
        for curRow in range(len(matrix)):
            matrix[curRow][column] = -1
            matrix[curRow][row] = -1

    def negative_matirx(self, row, column):
        """
        将关系矩阵中的第 row 行和第 column 列全部置为 -1， 表示不再接受组队
        :param row:
        :param column:
        :return:
        """
        self.re_matrix[row] = [-1 for x in self.re_matrix[row]]
        self.re_matrix[column] = [-1 for x in self.re_matrix[row]]
        for curRow in range(len(self.re_matrix)):
            self.re_matrix[curRow][column] = -1
            self.re_matrix[curRow][row] = -1

    def establish_relation_matrix(self):
        self.re_matrix = []
        self.te_matrix = []
        """
        将已经计算好的组员关系表组装成关系矩阵
        :return:
        """
        for student in self._students:
            self.re_matrix.append(student.relation)

        for team in self._teams:
            self.te_matrix.append(team._relation)


    def add_relation(self, relation:dict ):
        """
        添加已经存在的关系
        这是关系统计的第一步
        先将每位同学每次所在组记录到自己的历史记录中
        每次组队信息要严格按照先后顺序加入， 否则就不准了
        :param relation: {1: [19, 25, 30, 33, 38, 51], 2: [4, 11, 23, 37, 43, 45], 3: [5, 8, 10, 22, 26, 54], 4: [3, 20, 24, 34, 36, 47, 55], 5: [16, 17, 27, 49, 52, 53], 6: [7, 9, 15, 29, 40, 42], 7: [13, 18, 21, 28, 44, 46, 56], 8: [1, 31, 32, 39, 41, 50], 9: [2, 6, 12, 14, 35, 48]}
        """
        for groupNo, memberList in relation.items():
            for member in memberList:
                self._students[member - 1].history = groupNo

    def caculate_relation(self):
        """
        当该方法调用时，我们认为历史记录已经完成统计
        我们通过历史记录的比对，算出每一位同学对所有其他同学的关系值，并保存到同学的关系数组上
        这个数组最终会组成班级的关系矩阵
        :return:
        """
        student_list = self._students
        for index in range(len(student_list)):
            student_list[index].correlation_list(student_list, self.relation_recorder)
        self.relation_recorder = sorted(self.relation_recorder)

    def allOfNegative(self, cur_line):
        for cur in cur_line:
            if cur != -1:
                return False
        return True


def splitList(target: list, index: int) -> tuple:
    """
    分割列表，将返回一个关键元素， 和剔除该关键元素的子列表
    :param target: 将要处理的列表
    :param index: 关键元素所在位置
    :return: 关键元素值, 剔除掉关键元素的子列表
    """
    num = 0
    result = []
    for ind in range(len(target)):
        if ind == index:
            num = target[ind]
        else:
            result.append(target[ind])
    return num, result


def relationAdd(class_room: Class, relationship: dict) -> None:
    """
    给当前班级添加已经存在的一次关系
    :param class_room: 等待添加本次关系的班级
    :param relationship: 小组编号:[班级编号1,...] PS： {1: [19, 25, 30, 33, 38, 51], 2: [4, 11, 23, 37, 43, 45], 3: [5, 8, 10, 22, 26, 54], 4: [3, 20, 24, 34, 36, 47, 55], 5: [16, 17, 27, 49, 52, 53], 6: [7, 9, 15, 29, 40, 42], 7: [13, 18, 21, 28, 44, 46, 56], 8: [1, 31, 32, 39, 41, 50], 9: [2, 6, 12, 14, 35, 48]}
    :return:
    """
    # 对总体关系的记录
    for num, group in relationship.items():
        for index in range(len(group)):
            key, members = splitList(group, index)
            


if __name__ == '__main__':
    print(splitList([1,2,3,4,5], 2))
