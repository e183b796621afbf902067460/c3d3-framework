import datetime
from typing import final, overload, Dict, Any, Optional
import pandas as pd

from c3d3.infrastructure._abc.handler.abc import iHandler


class iCexBalanceScreenerHandler(iHandler):

    __TICKER_KEY, __LABEL_KEY = 'ticker', 'label'

    _EXCHANGE_COLUMN = 'exchange'
    _LABEL_COLUMN = 'label'
    _TICKER_COLUMN = 'ticker'
    _PRICE_COLUMN = 'price'
    _QTY_COLUMN = 'qty'
    _TS_COLUMN = 'ts'

    def __str__(self):
        raise NotImplementedError

    def __init__(self, ticker: str,  label: str, *args, **kwargs) -> None:
        self._ticker, self._label = ticker, label

        self.builder.build(
            key=self.__TICKER_KEY, value=self._ticker
        ).build(
            key=self.__LABEL_KEY, value=self._label
        )

        self._df = self.__init_df()

    @property
    def ticker(self):
        return self._ticker

    @property
    def label(self):
        return self._label

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    class Builder:

        def __init__(self, *args, **kwargs) -> None:
            self._options: dict = dict()

            self.__TICKER_KEY, self.__LABEL_KEY = args

        @overload
        def build(self, params: Dict[str, Any]) -> "iCexBalanceScreenerHandler.Builder":
            ...

        @overload
        def build(self, key: str, value: Any) -> "iCexBalanceScreenerHandler.Builder":
            ...

        @final
        def build(
                self,
                key: Optional[str] = None,
                value: Optional[str] = None,
                params: Optional[Dict[str, Any]] = None
        ) -> "iCexBalanceScreenerHandler.Builder":

            def validate(k: str, v: Any) -> None:
                if k == self.__TICKER_KEY or k == self.__LABEL_KEY:
                    if not isinstance(v, str):
                        raise TypeError('Invalid Ticker type.')

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
        return self.Builder(self.__TICKER_KEY, self.__LABEL_KEY)

    def do(self):
        raise NotImplementedError

    @property
    def __columns(self):
        return [
            self._EXCHANGE_COLUMN,
            self._LABEL_COLUMN,
            self._TICKER_COLUMN,
            self._PRICE_COLUMN,
            self._QTY_COLUMN,
            self._TS_COLUMN
        ]

    def __init_df(self) -> pd.DataFrame:
        return pd.DataFrame(columns=self.__columns)
