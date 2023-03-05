from c3d3.domain.c3.wrappers.binance.spot.wrapper import BinanceSpotExchange

import datetime
import requests as r


class BinanceSpotCexScreenerHandler(BinanceSpotExchange):

    @staticmethod
    def _formatting(json_: dict) -> dict:
        return {
            'price': float(json_['p']),
            'qty': float(json_['q']),
            'ts': datetime.datetime.fromtimestamp(json_['T'] / 10 ** 3),
            'side': 'BUY' if json_['m'] else 'SELL'
        }

    def get_overview(
            self,
            ticker: str,
            start: datetime.datetime, end: datetime.datetime,
            *args, **kwargs
    ):
        overviews: list = list()
        end = int(end.timestamp()) * 1000

        agg_trades = self.aggTrades(
            symbol=ticker,
            startTime=int(start.timestamp()) * 1000,
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
                symbol=ticker,
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
