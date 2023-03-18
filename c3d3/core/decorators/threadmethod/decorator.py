from threading import Thread
from functools import wraps
from concurrent.futures import Future


def _call(func, future, *args, **kwargs):
    ret = func(*args, **kwargs)
    future.set_result(ret)


def threadmethod(fn):
    @wraps(fn)
    def wrapper(self):
        future = Future()
        Thread(target=_call, args=(fn, future, self)).start()
        return future
    return wrapper
