from functools import wraps


def yieldmethod(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        for elem in func(self, *args, **kwargs):
            if elem:
                return elem
    return wrapper
