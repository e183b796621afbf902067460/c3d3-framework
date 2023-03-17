import pytest

from c3d3.core.decorators.yieldmethod.decorator import yieldmethod


class TestOne:
    @yieldmethod
    def example_one(self, example: list = [1, 2, 3]):
        for i in example:
            yield i


class TestTwo:
    @yieldmethod
    def example_two(self, example: list = [None, 2, 3]):
        for i in example:
            yield i


class TestThree:
    @yieldmethod
    def example_three(self, example: list = [None, None, None]):
        for i in example:
            yield i


class TestYieldMethodDecorator:

    def test_one(self):
        assert 1 == TestOne().example_one()

    def test_two(self):
        assert 2 == TestTwo().example_two()

    def test_three(self):
        assert None == TestThree().example_three()

