from enum import Enum

class OrgTypeEnum(Enum):
    USCC = ('CRED_ORG_USCC', '统一社会信用代码')
    REGCODE = ('CRED_ORG_REGCODE', '工商注册号')

    def __str__(self):
        return self.value[0]

    @property
    def msg(self):
        return self.value[1]

    @classmethod
    def of(cls, key):
        for curKey in cls:
            if curKey.value[0] == key:
                return curKey
        return cls.USCC

if __name__ == '__main__':
    print(type(OrgTypeEnum.of('test')))
    print(type(OrgTypeEnum.of('CRED_ORG_REGCODE').value[0]))
    print(OrgTypeEnum.of('CRED_ORG_REGCODE'))
    print(OrgTypeEnum.of('CRED_ORG_USCC').name)
    print(OrgTypeEnum.of('CRED_ORG_USCC').msg)