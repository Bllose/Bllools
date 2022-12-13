import time
from functools import wraps

cache_map = {}


def mem_cache(last: int):
    """
    内存缓存
    :param last: 缓存持续时间，单位秒
    :return:
    """
    def _mem_cache(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            value = None
            name = func.__name__
            if name in cache_map:
                recorderTime = cache_map.get(name)
                if int(time.time()) - recorderTime > last:
                    value = func(*args, **kwargs)
                    cache_map[name] = int(time.time())
                    cache_map[name+'_value'] = value
                else:
                    value = cache_map[name+'_value']
            else:
                value = func(*args, **kwargs)
                cache_map[name] = int(time.time())
                cache_map[name + '_value'] = value
            return value
        return wrapper
    return _mem_cache
