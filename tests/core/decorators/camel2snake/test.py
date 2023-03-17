import pytest

from c3d3.core.decorators.camel2snake.decorator import camel2snake


@camel2snake
def example_one(example: str = 'ABC'):
    return example


@camel2snake
def example_two(example: str = 'ExampleClassName'):
    return example


@camel2snake
def example_three(example: str = 'already_snake_case'):
    return example


@camel2snake
def example_four(example: str = 'startsWithSmallCase'):
    return example


@camel2snake
def example_five(example: str = 'small'):
    return example


class TestCamel2SnakeDecorator:

    def test_one(self):
        assert 'a_b_c' == example_one()

    def test_two(self):
        assert 'example_class_name' == example_two()

    def test_three(self):
        assert 'already_snake_case' == example_three()

    def test_four(self):
        assert 'starts_with_small_case' == example_four()

    def test_five(self):
        assert 'small' == example_five()
