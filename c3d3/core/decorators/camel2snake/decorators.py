from functools import wraps
import re


def camel2snake(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', func(*args, **kwargs)).lower()
    return wrapper
