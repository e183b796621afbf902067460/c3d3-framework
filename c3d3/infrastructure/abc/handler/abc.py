from abc import ABC, abstractmethod
from typing import overload, final

from c3d3.core.decorators.camel2snake.decorator import camel2snake
from c3d3.core.decorators.classproperty.decorator import classproperty


class iHandler(ABC):

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @overload
    def do(self):
        ...

    @abstractmethod
    def do(self):
        raise NotImplementedError

    @final
    @classproperty
    @camel2snake
    def key(self) -> str:
        return self.__str__(self)
