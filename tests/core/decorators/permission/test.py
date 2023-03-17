import pytest

from c3d3.core.decorators.permission.decorator import permission


class PermissionExampleOne:

    def __init__(self):
        self.api_key = 'api_key'
        self.secret_key = 'secret_key'

    @permission
    def example_one(self):
        return __class__.__name__


class PermissionExampleTwo:

    def __init__(self):
        self.api_key = None
        self.secret_key = None

    @permission
    def example_two(self):
        return __class__.__name__


class TestPermissionDecorator:

    def test_one(self):
        assert 'PermissionExampleOne' == PermissionExampleOne().example_one()

    def test_two(self):
        try:
            PermissionExampleTwo().example_two()
        except PermissionError:
            assert True
