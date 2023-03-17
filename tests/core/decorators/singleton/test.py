import pytest

from c3d3.core.decorators.singleton.decorator import singleton


@singleton
class SingleToneExampleOne:
    pass


class TestSingleToneDecorator:

    def test_one(self):
        first, second = SingleToneExampleOne(), SingleToneExampleOne()
        assert first is second
