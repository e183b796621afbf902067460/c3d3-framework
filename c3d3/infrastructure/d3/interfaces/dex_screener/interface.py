from typing import final, overload, Dict, Any, Optional
from datetime import datetime

import requests as r
import pandas as pd

from c3d3.domain.d3.adhoc.chains.map import ChainMap
from c3d3.infrastructure.abc.handler.abc import iHandler


class iDexScreenerHandler(iHandler):
    _FEE, _VERSION = None, None

    __API_KEY, __CHAIN_KEY = 'api_key', 'chain'

    __V2, __V3 = 'v2', 'v3'

    __CHAIN_NAME_COLUMN = 'chain_name'
    __POOL_ADDRESS_COLUMN = 'pool_address'
    __PROTOCOL_NAME_COLUMN = 'protocol_name'
    __POOL_SYMBOL_COLUMN = 'pool_symbol'
    __TRADE_PRICE_COLUMN = 'trade_price'
    __SENDER_COLUMN = 'sender',
    __RECIPIENT_COLUMN = 'recipient'
    __RESERVE0_COLUMN = 'reserve0'
    __RESERVE1_COLUMN = 'reserve1'
    __AMOUNT0_COLUMN = 'amount0'
    __AMOUNT1_COLUMN = 'amount1'
    __DECIMALS0_COLUMN = 'decimals0'
    __DECIMALS1_COLUMN = 'decimals1'
    __SQRT_P_COLUMN = 'sqrt_p'
    __LIQUIDITY_COLUMN = 'liquidity'
    __TRADE_FEE_COLUMN = 'trade_fee'
    __GAS_USED_COLUMN = 'gas_used'
    __EFFECTIVE_GAS_PRICE_COLUMN = 'effective_gas_price'
    __GAS_SYMBOL_COLUMN = 'gas_symbol'
    __GAS_USD_PRICE_COLUMN = 'gas_usd_price'
    __INDEX_POSITION_IN_THE_BLOCK_COLUMN = 'index_position_in_the_block'
    __TX_HASH_COLUMN = 'tx_hash'
    __TS_COLUMN = 'ts'

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

        self._df = self.__init_df()

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

    @property
    def df(self) -> pd.DataFrame:
        return self._df

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

    @property
    def __v2_columns(self):
        return [
            self.__CHAIN_NAME_COLUMN,
            self.__POOL_ADDRESS_COLUMN,
            self.__PROTOCOL_NAME_COLUMN,
            self.__POOL_SYMBOL_COLUMN,
            self.__TRADE_PRICE_COLUMN,
            self.__SENDER_COLUMN,
            self.__RECIPIENT_COLUMN,
            self.__RESERVE0_COLUMN,
            self.__RESERVE1_COLUMN,
            self.__AMOUNT0_COLUMN,
            self.__AMOUNT1_COLUMN,
            self.__DECIMALS0_COLUMN,
            self.__DECIMALS1_COLUMN,
            self.__TRADE_FEE_COLUMN,
            self.__GAS_USED_COLUMN,
            self.__EFFECTIVE_GAS_PRICE_COLUMN,
            self.__GAS_SYMBOL_COLUMN,
            self.__GAS_USD_PRICE_COLUMN,
            self.__INDEX_POSITION_IN_THE_BLOCK_COLUMN,
            self.__TX_HASH_COLUMN,
            self.__TS_COLUMN
        ]

    @property
    def __v3_columns(self):
        return [
            self.__CHAIN_NAME_COLUMN,
            self.__POOL_ADDRESS_COLUMN,
            self.__PROTOCOL_NAME_COLUMN,
            self.__POOL_SYMBOL_COLUMN,
            self.__TRADE_PRICE_COLUMN,
            self.__SENDER_COLUMN,
            self.__RECIPIENT_COLUMN,
            self.__AMOUNT0_COLUMN,
            self.__AMOUNT1_COLUMN,
            self.__DECIMALS0_COLUMN,
            self.__DECIMALS1_COLUMN,
            self.__SQRT_P_COLUMN,
            self.__LIQUIDITY_COLUMN,
            self.__TRADE_FEE_COLUMN,
            self.__GAS_USED_COLUMN,
            self.__EFFECTIVE_GAS_PRICE_COLUMN,
            self.__GAS_SYMBOL_COLUMN,
            self.__GAS_USD_PRICE_COLUMN,
            self.__INDEX_POSITION_IN_THE_BLOCK_COLUMN,
            self.__TX_HASH_COLUMN,
            self.__TS_COLUMN
        ]

    def __init_df(self) -> pd.DataFrame:
        if self._VERSION == self.__V2:
            return pd.DataFrame(columns=self.__v2_columns)
        elif self._VERSION == self.__V3:
            return pd.DataFrame(columns=self.__v3_columns)
