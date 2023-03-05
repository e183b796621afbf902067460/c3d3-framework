from typing import final

from c3d3.core.decorators.classproperty.decorator import classproperty
from c3d3.core.decorators.camel2snake.decorator import camel2snake


class Polygon:

    BLOCK_LIMIT = 3000
    NATIVE_TOKEN = 'MATIC'

    def __str__(self) -> str:
        return __class__.__name__

    @final
    @classproperty
    @camel2snake
    def name(self) -> str:
        return self.__str__(self)
