from abc import ABC, abstractmethod
from typing import final

from c3d3.core.decorators.classproperty.decorator import classproperty
from c3d3.core.decorators.camel2snake.decorator import camel2snake


class iFactory(ABC):

    __abc: dict = dict()

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @classmethod
    @final
    def add_object(cls, k, v) -> None:
        if not cls.__abc.get(k):
            cls.__abc[k] = v

    @classmethod
    @final
    def get_object(cls, k):
        obj = cls.__abc.get(k)
        if not obj:
            raise ValueError(f'Set value for {k} in {cls.__class__.__name__} factory')
        return obj

    @final
    @classproperty
    @camel2snake
    def key(self) -> str:
        return self.__str__(self)
