from c3d3.domain.c3.wrappers.binance.spot.wrapper import BinanceSpotExchange
from c3d3.infrastructure.c3.interfaces.cex_screener.interface import iCexScreenerHandler
from c3d3.core.decorators.to_dataframe.decorator import to_dataframe

import datetime
import requests as r


class BinanceSpotCexScreenerHandler(BinanceSpotExchange, iCexScreenerHandler):

    _FEE = 0.001

    def __str__(self):
        return __class__.__name__

    def __init__(
            self,
            ticker: str, start_time: datetime.datetime, end_time: datetime.datetime,
            is_child: bool = False,
            *args, **kwargs
    ) -> None:
        if not is_child:
            BinanceSpotExchange.__init__(self, *args, **kwargs)
        iCexScreenerHandler.__init__(self, ticker=ticker, start_time=start_time, end_time=end_time, *args, **kwargs)

    def _formatting(self, json_: dict) -> dict:
        return {
            self._EXCHANGE_COLUMN: self.key,
            self._TICKER_COLUMN: self.ticker,
            self._PRICE_COLUMN: float(json_['p']),
            self._QTY_COLUMN: float(json_['q']),
            self._TS_COLUMN: datetime.datetime.fromtimestamp(json_['T'] / 10 ** 3),
            self._TRADE_FEE_COLUMN: self._FEE,
            self._SIDE_COLUMN: 'BUY' if json_['m'] else 'SELL'
        }

    def _handle(self, start: int, end: int):
        agg_trades = self.aggTrades(
            symbol=self.ticker,
            startTime=start,
            endTime=end,
            limit=1000
        )
        if not self._validate_response(agg_trades):
            raise r.HTTPError(f'Invalid status code for aggTrades in  {self.__class__.__name__}')
        agg_trades = agg_trades.json()
        return agg_trades

    @to_dataframe
    def do(self):
        overviews: list = list()
        end = int(self.end.timestamp()) * 1000
        agg_trades = self._handle(start=int(self.start.timestamp()) * 1000, end=end)
        overviews.extend([self._formatting(json_=agg_trade) for agg_trade in agg_trades])

        while True:
            start = agg_trades[-1]['T'] + 1

            agg_trades = self._handle(start=start, end=end)
            if not agg_trades:
                break
            overviews.extend([self._formatting(json_=agg_trade) for agg_trade in agg_trades])
        return overviews
