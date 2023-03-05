from abc import ABC, abstractmethod
from typing import Optional, final

from c3d3.core.decorators.camel2snake.decorator import camel2snake
from c3d3.core.decorators.classproperty.decorator import classproperty


class iTraderLeaf(ABC):

    _PEGS: dict = None

    @abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_price(self, a: str, b: str, *args, **kwargs) -> Optional[float]:
        raise NotImplementedError

    @final
    @classproperty
    @camel2snake
    def key(self) -> str:
        return self.__str__(self)

    @final
    def _peg(self, symbol: str) -> str:
        return self._PEGS[symbol] if symbol in self._PEGS else symbol
