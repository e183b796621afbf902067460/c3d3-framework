from typing import final
from abc import ABC, abstractmethod
import datetime

from c3d3.core.decorators.classproperty.decorator import classproperty
from c3d3.core.decorators.camel2snake.decorator import camel2snake


class iBBC(ABC):

    _NATIVE_TOKEN, _API_ENDPOINT = None, None
    _LAST_REQ_TIMESTAMP, _REQ_LIMIT_SECONDS = None, None

    @final
    @classproperty
    @camel2snake
    def name(self) -> str:
        return self.__str__(self)

    @abstractmethod
    def __str__(self) -> str:
        ...

    @abstractmethod
    def get_block_by_ts(self, ts: int, api_key: str) -> str:
        ...

    @abstractmethod
    def get_logs(
            self,
            address: str,
            start_time: datetime.datetime, end_time: datetime.datetime,
            start_block: int, end_block: int,
            api_key: str
    ):
        ...
