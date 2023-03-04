from functools import wraps


def permission(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        if not isinstance(self.api_key, str) or not isinstance(self.secret_key, str):
            raise PermissionError('Set API or Secret key.')
        return fn(self, *args, **kwargs)
    return wrapper
