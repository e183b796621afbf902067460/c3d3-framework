from typing import final

from c3d3.core.decorators.classproperty.decorators import classproperty
from c3d3.core.decorators.camel2snake.decorators import camel2snake


class Fantom:

    def __str__(self) -> str:
        return __class__.__name__

    @final
    @classproperty
    @camel2snake
    def name(self) -> str:
        return self.__str__(self)
