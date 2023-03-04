from abc import ABC

from c3d3.infrastructure.abc.factory.abc import iFactory
from c3d3.infrastructure.abc.handler.abc import iHandler


class iBridge(ABC):

    def __init__(self, abstract_factory: iFactory, factory_key: str, object_key: str) -> None:
        self._abstract_factory = abstract_factory

        self._factory_key, self._object_key = factory_key, object_key

    @property
    def abstract_factory(self) -> iFactory:
        return self._abstract_factory

    def _concrete_fabric(self) -> iFactory:
        return self.abstract_factory.get_object(self._factory_key)

    def concrete_object(self) -> iHandler:
        return self._concrete_fabric().get_object(self._object_key)
