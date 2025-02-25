from enum import Enum

class EqbEnum(Enum):
    """
    e签宝环境选择
    默认返回 'test'环境
    当且仅当选择 'pro' 时才返回生产环境
    """
    TEST = ('test', '测试环境')
    PRO = ('pro', '生产环境')

    def __str__(self):
        return self.value[0]

    @property
    def msg(self):
        return self.value[1]

    @classmethod
    def of(cls, env):
        for curEnv in cls:
            if curEnv.value[0] == env.lower():
                return curEnv
        return cls.TEST
    
    @classmethod
    def theCodeOf(cls, env):
        return cls.of(env).name.lower()


if __name__ == '__main__':
    print(type(EqbEnum.of('test')))
    print(type(EqbEnum.of('test').value[0]))
    print(EqbEnum.of('test').value[0])
    print(EqbEnum.of('pro'))
    print(EqbEnum.of('pro1').name)
    print(EqbEnum.of('pro1').msg)