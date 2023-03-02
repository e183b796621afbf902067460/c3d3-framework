from typing import Dict, Any, Optional, Generic, overload, final
from abc import ABC

from web3 import Web3
from web3.eth import Eth
from web3.exceptions import ValidationError, CannotHandleRequest
from web3.providers.base import BaseProvider

from c3d3.core.d3.typings.nodes.typings import NodeType


class iCBC(ABC):
    _ABI: str = None

    def __init__(self, address: str, node: Generic[NodeType]) -> None:
        self._address, self._node = address, node

        self._contract = self.contract = ...

    @property
    def contract(self) -> Eth.contract:
        return self._contract

    @contract.setter
    def contract(self, *args, **kwargs) -> None:
        self._contract = self.builder\
            .build(key='address', value=self._address)\
            .build(key='node', value=self._node)\
            .build(key='abi', value=self._ABI)\
            .preprocess()\
            .construct()

    @property
    def node(self) -> NodeType:
        return self._node

    @property
    def provider(self) -> BaseProvider:
        return self.node.provider

    class Builder:
        def __init__(self) -> None:
            self._options: Dict[str, Any] = dict()

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
                if k == 'address':
                    if not Web3.isAddress(value=v):
                        raise ValidationError("Invalid address.")
                elif k == 'node':
                    if not v.provider.isConnected():
                        raise CannotHandleRequest("Node is unhealthy.")
                elif k == 'abi':
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
            if self._options.get('address'):
                self._options['address'] = Web3.toChecksumAddress(value=self._options.get('address'))
            return self

        @final
        def construct(self) -> Eth.contract:
            return Web3(provider=self._options['node'].provider)\
                .eth\
                .contract(address=self._options['address'], abi=self._options['abi'])

    @property
    def builder(self) -> Builder:
        return self.Builder()
