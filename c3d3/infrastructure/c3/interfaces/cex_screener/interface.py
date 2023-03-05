import datetime
from typing import final, overload, Dict, Any, Optional

from c3d3.infrastructure.abc.handler.abc import iHandler


class iCexScreenerHandler(iHandler):

    __TICKER_KEY, __START_TIME_KEY, __END_TIME_KEY = 'ticker', 'start_time', 'end_time'

    def __str__(self):
        raise NotImplementedError

    def __init__(self, ticker: str, start_time: datetime.datetime, end_time: datetime.datetime, *args, **kwargs) -> None:
        self._ticker = ticker
        self._start_time, self._end_time = start_time, end_time

        self.builder.build(
            key=self.__TICKER_KEY, value=self._ticker
        ).build(
            key=self.__START_TIME_KEY, value=self._start_time
        ).build(
            key=self.__END_TIME_KEY, value=self._end_time
        )

    @property
    def start(self):
        return self._start_time

    @property
    def end(self):
        return self._end_time

    @property
    def ticker(self):
        return self._ticker

    class Builder:

        def __init__(self, *args, **kwargs) -> None:
            self._options: dict = dict()

            self.__TICKER_KEY, self.__START_TIME_KEY, self.__END_TIME_KEY = args

        @overload
        def build(self, params: Dict[str, Any]) -> "iCexScreenerHandler.Builder":
            ...

        @overload
        def build(self, key: str, value: Any) -> "iCexScreenerHandler.Builder":
            ...

        @final
        def build(
                self,
                key: Optional[str] = None,
                value: Optional[str] = None,
                params: Optional[Dict[str, Any]] = None
        ) -> "iCexScreenerHandler.Builder":

            def validate(k: str, v: Any) -> None:
                if k == self.__TICKER_KEY:
                    if not isinstance(v, str):
                        raise TypeError('Invalid Ticker type.')
                elif k == self.__START_TIME_KEY or k == self.__END_TIME_KEY:
                    if not isinstance(v, datetime.datetime):
                        raise TypeError('Set valid start_time and end_time type.')

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
        return self.Builder(self.__TICKER_KEY, self.__START_TIME_KEY, self.__END_TIME_KEY)

    def do(self):
        raise NotImplementedError
