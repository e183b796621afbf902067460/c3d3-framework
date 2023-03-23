from functools import wraps
import pandas as pd


def to_dataframe(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        return self.df.append(func(self, *args, **kwargs), ignore_index=True)
    return wrapper
