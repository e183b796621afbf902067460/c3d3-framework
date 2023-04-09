from typing import final, overload, Dict, Any, Optional

from c3d3.domain.d3.adhoc.chains.map import ChainMap
from c3d3.infrastructure._abc.handler.abc import iHandler


class iDexGweiScreenerHandler(iHandler):

    __WALLET_ADDRESS_KEY, __CHAIN_KEY, __LABEL_KEY = 'wallet', 'chain', 'label'

    _CHAIN_NAME_COLUMN = 'chain_name'
    _WALLET_ADDRESS_COLUMN = 'wallet_address'
    _LABEL_COLUMN = 'label_name'
    _SYMBOL_COLUMN = 'symbol'
    _CURRENT_PRICE_COLUMN = 'current_price'
    _QTY_COLUMN = 'qty'
    _TS_COLUMN = 'ts'

    def __str__(self):
        raise NotImplementedError

    def __init__(self, chain: str, wallet_address: str, label: str, *args, **kwargs):
        self._chain, self._wallet_address, self._label = chain, wallet_address, label

        self.builder.build(
            key=self.__WALLET_ADDRESS_KEY, value=self._wallet_address
        ).build(
            key=self.__CHAIN_KEY, value=self._chain
        ).build(
            key=self.__LABEL_KEY, value=self._label
        )

    @property
    def chain(self):
        return ChainMap.get_chain(name=self._chain)

    @property
    def wallet_address(self):
        return self._wallet_address

    @property
    def label(self):
        return self._label

    class Builder:

        def __init__(self, *args, **kwargs) -> None:
            self._options: dict = dict()

            self.__WALLET_ADDRESS_KEY, self.__CHAIN_KEY, self.__LABEL_KEY = args

        @overload
        def build(self, params: Dict[str, Any]) -> "iDexGweiScreenerHandler.Builder":
            ...

        @overload
        def build(self, key: str, value: Any) -> "iDexGweiScreenerHandler.Builder":
            ...

        @final
        def build(
                self,
                key: Optional[str] = None,
                value: Optional[str] = None,
                params: Optional[Dict[str, Any]] = None
        ) -> "iDexGweiScreenerHandler.Builder":

            def validate(k: str, v: Any) -> None:
                if k == self.__WALLET_ADDRESS_KEY or self.__LABEL_KEY:
                    if not isinstance(v, str):
                        raise TypeError('Set valid API-key or Label-key type.')
                elif k == self.__CHAIN_KEY:
                    if not isinstance(v, str):
                        raise TypeError('Invalid Chain-key type.')

            if isinstance(params, dict):
                for k, v in params.items():
                    validate(k=k, v=v)
                    self._options[k] = v
            elif isinstance(key, str):
                validate(k=key, v=value)
                self._options[key] = value
            return self

    @property
    def builder(self):
        return self.Builder(self.__WALLET_ADDRESS_KEY, self.__CHAIN_KEY, self.__LABEL_KEY)

    def do(self):
        raise NotImplementedError
