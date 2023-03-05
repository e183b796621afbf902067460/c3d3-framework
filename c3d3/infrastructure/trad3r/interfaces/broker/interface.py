from abc import ABC, abstractmethod
from typing import Optional


class iBroker(ABC):

    @abstractmethod
    def get_price(self, a: str, b: str, *args, **kwargs) -> Optional[float]:
        raise NotImplementedError
