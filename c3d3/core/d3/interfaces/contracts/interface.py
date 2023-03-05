from typing import Dict, Any, Optional, Generic, overload, final
from abc import ABC

from web3 import Web3
from web3.eth import Eth
from web3.exceptions import ValidationError, CannotHandleRequest
from web3.providers.base import BaseProvider

from c3d3.core.d3.typings.nodes.typing import NodeType


class iCBC(ABC):
    _ABI: str = None

    __ADDRESS_KEY, __NODE_KEY, __ABI_KEY = 'address', 'node', 'abi'

    def __init__(self, address: str, node: Generic[NodeType]) -> None:
        self._address, self._node = address, node

        self._contract = self.contract = ...

    @property
    def contract(self) -> Eth.contract:
        return self._contract

    @property
    def address(self) -> str:
        return self.contract.address

    @contract.setter
    def contract(self, *args, **kwargs) -> None:
        self._contract = self.builder\
            .build(key=self.__ADDRESS_KEY, value=self._address)\
            .build(key=self.__NODE_KEY, value=self._node)\
            .build(key=self.__ABI_KEY, value=self._ABI)\
            .preprocess()\
            .construct()

    @property
    def node(self) -> NodeType:
        return self._node

    @property
    def provider(self) -> BaseProvider:
        return self.node.provider

    class Builder:
        def __init__(self, *args, **kwargs) -> None:
            self._options: Dict[str, Any] = dict()

            self.__ADDRESS_KEY, self.__NODE_KEY, self.__ABI_KEY = args

        @overload
        def build(self, params: Dict[str, Any]) -> "iCBC.Builder":
            ...

        @overload
        def build(self, key: str, value: Any) -> "iCBC.Builder":
            ...

        @final
        def build(
                self,
                key: Optional[str] = None,
                value: Optional[str] = None,
                params: Optional[Dict[str, Any]] = None
        ) -> "iCBC.Builder":

            def validate(k: str, v: Any) -> None:
                if k == self.__ADDRESS_KEY:
                    if not Web3.isAddress(value=v):
                        raise ValidationError("Invalid address.")
                elif k == self.__NODE_KEY:
                    if not v.provider.isConnected():
                        raise CannotHandleRequest("Node is unhealthy.")
                elif k == self.__ABI_KEY:
                    if not isinstance(v, str):
                        raise TypeError(f'Invalid ABI type: {type(v)}.')

            if isinstance(params, dict):
                for k, v in params.items():
                    validate(k=k, v=v)
                    self._options[k] = v
            elif isinstance(key, str):
                validate(k=key, v=value)
                self._options[key] = value
            return self

        @final
        def preprocess(self) -> "iCBC.Builder":
            if self._options.get(self.__ADDRESS_KEY):
                self._options[self.__ADDRESS_KEY] = Web3.toChecksumAddress(value=self._options.get(self.__ADDRESS_KEY))
            return self

        @final
        def construct(self) -> Eth.contract:
            return Web3(provider=self._options[self.__NODE_KEY].provider)\
                .eth\
                .contract(address=self._options[self.__ADDRESS_KEY], abi=self._options[self.__ABI_KEY])

    @property
    def builder(self) -> Builder:
        return self.Builder(self.__ADDRESS_KEY, self.__NODE_KEY, self.__ABI_KEY)
