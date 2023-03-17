import pytest

from c3d3.core.decorators.classproperty.decorator import classproperty


class ClassPropertyExampleOne:

    @classproperty
    def example_one(self):
        return __class__.__name__


class TestClassPropertyDecorator:

    # without brackets
    def test_one(self):
        assert 'ClassPropertyExampleOne' == ClassPropertyExampleOne.example_one
