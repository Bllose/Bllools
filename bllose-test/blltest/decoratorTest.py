import time
import requests


def request_retry_wrapper(retry_num=50, retry_delay=0.1):
    """
    请求重试装饰器
    :param retry_num: 重试次数
    :param retry_delay: 重试间隔
    :return:
    """
    def wrapper1(func):
        def wrapper2(*args, **kwargs):
            for i in range(retry_num - 1):
                print('retry:', i)
                try:
                    result = func(*args, **kwargs)
                    # 50001 服务暂时不可用，请稍后重试
                    # 50004 接口请求超时（不代表请求成功或者失败，请检查请求结果）
                    # 50011 用户请求频率过快，超过该接口允许的限额。请参考 API 文档并限制请求
                    # 50013 当前系统繁忙，请稍后重试
                    # 50026 系统错误，请稍后重试
                    if result['code'] in ['50001', '50004', '50011', '50013', '50026']:
                        time.sleep(retry_delay)
                        continue
                    else:
                        return result
                except requests.exceptions.ConnectionError:
                    time.sleep(retry_delay)
            result = func(*args, **kwargs)
            return result
        return wrapper2
    return wrapper1


def my_retry_test():
    @request_retry_wrapper()
    def test():
        print('test')
        return {'code': '50001'}

    print(test())

if __name__ == '__main__':
    my_retry_test()