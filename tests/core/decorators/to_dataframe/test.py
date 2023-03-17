import pandas as pd
import pytest

from c3d3.core.decorators.to_dataframe.decorator import to_dataframe


class ToDataFrameExampleOne:

    def __init__(self):
        self.df = pd.DataFrame(columns=['column_one', 'column_two', 'column_three'])

    @to_dataframe
    def example_one(self):
        return [
            {
                'column_one': 1,
                'column_two': 2,
                'column_three': 3
            }
        ]


class TestToDataFrameDecorator:

    def test_one(self):
        assert type(ToDataFrameExampleOne().example_one()) == pd.DataFrame

    def test_two(self):
        assert list(ToDataFrameExampleOne().example_one().columns) == ['index', 'column_one', 'column_two', 'column_three']

    def test_three(self):
        assert ToDataFrameExampleOne().example_one()['column_one'].values == [1]
        assert ToDataFrameExampleOne().example_one()['column_two'].values == [2]
        assert ToDataFrameExampleOne().example_one()['column_three'].values == [3]
