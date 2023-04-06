from functools import wraps
import pandas as pd


def to_dataframe(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        return pd.DataFrame(func(self, *args, **kwargs))
    return wrapper
