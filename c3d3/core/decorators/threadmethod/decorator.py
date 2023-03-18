from threading import Thread
from functools import wraps
from concurrent.futures import Future


def _call(func, future, *args, **kwargs):
    ret = func(*args, **kwargs)
    future.set_result(ret)


def threadmethod(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        future = Future()
        Thread(target=_call, args=(fn, future, *args, kwargs)).start()
        return future
    return wrapper
