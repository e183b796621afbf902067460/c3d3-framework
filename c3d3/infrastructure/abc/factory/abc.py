from abc import ABC
from typing import Union

from c3d3.infrastructure.abc.handler.abc import iHandler


class iFactory(ABC):

    __abc: dict = dict()

    @classmethod
    def add_object(cls, k: str, v: Union[iHandler, "iFactory"]) -> None:
        if not cls.__abc.get(k):
            cls.__abc[k] = v

    @classmethod
    def get_object(cls, k: str) -> Union[iHandler, "iFactory"]:
        obj = cls.__abc.get(k)
        if not obj:
            raise ValueError(f'Set value for {k} in {cls.__class__.__name__} factory')
        return obj
