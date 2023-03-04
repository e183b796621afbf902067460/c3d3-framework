from abc import ABC, abstractmethod
from typing import overload

from c3d3.core.decorators.camel2snake.decorators import camel2snake


class iHandler(ABC):

    @abstractmethod
    def __str__(cls) -> str:
        raise NotImplementedError

    @overload
    def do(self, *args, **kwargs):
        ...

    @abstractmethod
    def do(self, *args, **kwargs):
        raise NotImplementedError
