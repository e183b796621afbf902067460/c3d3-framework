from typing import final, overload, Dict, Any, Optional
from datetime import datetime

import requests as r
import pandas as pd

from c3d3.domain.d3.adhoc.chains.map import ChainMap
from c3d3.infrastructure._abc.handler.abc import iHandler


class iDexScreenerHandler(iHandler):
    _FEE = None

    __API_KEY, __CHAIN_KEY = 'api_key', 'chain'

    _CHAIN_NAME_COLUMN = 'chain_name'
    _POOL_ADDRESS_COLUMN = 'pool_address'
    _PROTOCOL_NAME_COLUMN = 'protocol_name'
    _POOL_SYMBOL_COLUMN = 'pool_symbol'
    _TRADE_PRICE_COLUMN = 'trade_price'
    _SENDER_COLUMN = 'sender'
    _RECIPIENT_COLUMN = 'recipient'
    _RESERVE0_COLUMN = 'reserve0'
    _RESERVE1_COLUMN = 'reserve1'
    _AMOUNT0_COLUMN = 'amount0'
    _AMOUNT1_COLUMN = 'amount1'
    _DECIMALS0_COLUMN = 'decimals0'
    _DECIMALS1_COLUMN = 'decimals1'
    _SQRT_P_COLUMN = 'sqrt_p'
    _LIQUIDITY_COLUMN = 'liquidity'
    _TRADE_FEE_COLUMN = 'trade_fee'
    _GAS_USED_COLUMN = 'gas_used'
    _EFFECTIVE_GAS_PRICE_COLUMN = 'effective_gas_price'
    _GAS_SYMBOL_COLUMN = 'gas_symbol'
    _GAS_USD_PRICE_COLUMN = 'gas_usd_price'
    _INDEX_POSITION_IN_THE_BLOCK_COLUMN = 'index_position_in_the_block'
    _TX_HASH_COLUMN = 'tx_hash'
    _TS_COLUMN = 'ts'

    def __str__(self):
        raise NotImplementedError

    def __init__(
            self,
            api_key: str, chain: str,
            start_time: datetime, end_time: datetime,
            is_reverse: bool,
            *args, **kwargs
    ):
        self._api_key = api_key
        self._chain = chain
        self._start_time, self._end_time = start_time, end_time
        self._is_reverse = is_reverse

        self.builder.build(
            key=self.__API_KEY, value=self._api_key
        ).build(
            key=self.__CHAIN_KEY, value=self._chain
        )

    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def chain(self):
        return ChainMap.get_chain(name=self._chain)

    @property
    def start(self):
        return self._start_time

    @property
    def end(self):
        return self._end_time

    @property
    def is_reverse(self):
        return self._is_reverse

    class Builder:

        def __init__(self, *args, **kwargs) -> None:
            self._options: dict = dict()

            self.__API_KEY, self.__CHAIN_KEY = args

        @overload
        def build(self, params: Dict[str, Any]) -> "iDexScreenerHandler.Builder":
            ...

        @overload
        def build(self, key: str, value: Any) -> "iDexScreenerHandler.Builder":
            ...

        @final
        def build(
                self,
                key: Optional[str] = None,
                value: Optional[str] = None,
                params: Optional[Dict[str, Any]] = None
        ) -> "iDexScreenerHandler.Builder":

            def validate(k: str, v: Any) -> None:
                if k == self.__API_KEY:
                    if not isinstance(v, str):
                        raise TypeError('Set valid API key type.')
                elif k == self.__CHAIN_KEY:
                    if not isinstance(v, str):
                        raise TypeError('Invalid chain-key type.')

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
        return self.Builder(self.__API_KEY, self.__CHAIN_KEY)

    def do(self):
        raise NotImplementedError
