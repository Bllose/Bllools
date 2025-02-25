

def function(config: dict = {}):
    """
    locals 函数返回当前作用域的局部变量字典
    """
    a = 10
    b = 'hello'
    return locals()


if __name__ == '__main__':
    print(function())