
class UndirectRelation:
    def __init__(self, total):
        self.total = total
        self.relation = []
        for index in range(total):
            self.relation.append([0] * total)

    def __repr__(self):
        showMsg = ''
        for curLine in self.relation:
            showMsg += (' '.join([str(x) for x in curLine]) + '\r\n')
        return showMsg

    def getArr(self):
        return self.relation


if __name__ == '__main__':
    diagram = UndirectRelation(1)
    print(diagram)
    diagram = UndirectRelation(2)
    print(diagram)
