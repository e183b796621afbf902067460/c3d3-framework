from abc import ABC, abstractmethod
from typing import overload, final

from c3d3.core.decorators.camel2snake.decorators import camel2snake
from c3d3.core.decorators.classproperty.decorators import classproperty


class iHandler(ABC):

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @overload
    def do(self, *args, **kwargs):
        ...

    @abstractmethod
    def do(self, *args, **kwargs):
        raise NotImplementedError

    @final
    @classproperty
    @camel2snake
    def key(self) -> str:
        return self.__str__(self)
