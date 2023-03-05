from c3d3.domain.c3.wrappers.binance.spot.wrapper import BinanceSpotExchange
from c3d3.infrastructure.c3.interfaces.cex_screener.interface import iCexScreenerHandler

import datetime
import requests as r


class BinanceSpotCexScreenerHandler(BinanceSpotExchange, iCexScreenerHandler):

    def __str__(self):
        return __class__.__name__

    def __init__(
            self,
            ticker: str, start_time: datetime.datetime, end_time: datetime.datetime,
            *args, **kwargs
    ) -> None:
        BinanceSpotExchange.__init__(self, *args, **kwargs)
        iCexScreenerHandler.__init__(self, ticker=ticker, start_time=start_time, end_time=end_time, *args, **kwargs)

    @staticmethod
    def _formatting(json_: dict) -> dict:
        return {
            'price': float(json_['p']),
            'qty': float(json_['q']),
            'ts': datetime.datetime.fromtimestamp(json_['T'] / 10 ** 3),
            'side': 'BUY' if json_['m'] else 'SELL'
        }

    def do(self):
        overviews: list = list()
        end = int(self.end.timestamp()) * 1000

        agg_trades = self.aggTrades(
            symbol=self.ticker,
            startTime=int(self.start.timestamp()) * 1000,
            endTime=end,
            limit=1000
        )
        if not self._validate_response(agg_trades):
            raise r.HTTPError(f'Invalid status code for aggTrades in  {self.__class__.__name__}')
        agg_trades = agg_trades.json()
        overviews.extend([self._formatting(json_=agg_trade) for agg_trade in agg_trades])

        while True:
            start = agg_trades[-1]['T'] + 1

            agg_trades = self.aggTrades(
                symbol=self.ticker,
                startTime=start,
                endTime=end,
                limit=1000
            )
            if not self._validate_response(agg_trades):
                raise r.HTTPError(f'Invalid status code for aggTrades in  {self.__class__.__name__}')
            agg_trades = agg_trades.json()
            if not agg_trades:
                break
            overviews.extend([self._formatting(json_=agg_trade) for agg_trade in agg_trades])
        return overviews
