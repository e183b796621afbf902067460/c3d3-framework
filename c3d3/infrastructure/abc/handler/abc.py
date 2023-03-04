from abc import ABC, abstractmethod
from typing import overload

from c3d3.core.decorators.camel2snake.decorators import camel2snake


class iHandler(ABC):

    @camel2snake
    def __str__(self) -> str:
        return self.__class__.__name__

    @overload
    def do(self, *args, **kwargs):
        ...

    @abstractmethod
    def do(self, *args, **kwargs):
        raise NotImplementedError
