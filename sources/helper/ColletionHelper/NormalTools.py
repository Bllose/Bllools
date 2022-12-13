import logging
import random


def random_divide(target: list, times: int) -> list:
    """
    随机的拆开一个列表，使其分裂成两部分。
    拆离部分将作为一个新列表返回， 剩下部分将以参数target保存
    :param target: 待拆列表
    :param times: 拆离的部分里面包含几个元素
    :return: 拆离部分的列表
    """
    result = []
    if len(target) <= times:
        logging.warning('队列无法拆分,待拆数量大于元素总量!')
        result.extend(target.copy())
        target.clear()

    while times > 0 and len(target) > 0:
        index = random.randint(0, len(target) - 1)
        result.append(target.pop(index))
        times -= 1

    return result
