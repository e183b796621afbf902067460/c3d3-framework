from c3d3.infrastructure.c3.interfaces.cex_order_history_screener.interface import iCexOrderHistoryScreenerHandler
from c3d3.domain.c3.wrappers.binance.usdtm.wrapper import BinanceUsdtmExchange
from c3d3.core.decorators.to_dataframe.decorator import to_dataframe

import datetime
import time
import requests as r


class BinanceUsdtmCexOrderHistoryScreenerHandler(BinanceUsdtmExchange, iCexOrderHistoryScreenerHandler):

    def __str__(self):
        return __class__.__name__

    def __init__(
            self,
            ticker: str, label: str,
            start_time: datetime.datetime, end_time: datetime.datetime,
            is_child: bool = False,
            *args, **kwargs
    ) -> None:
        if not is_child:
            BinanceUsdtmExchange.__init__(self, *args, **kwargs)
        iCexOrderHistoryScreenerHandler.__init__(self, ticker=ticker, label=label, *args, **kwargs)
        self.start_time = start_time
        self.end_time = end_time

    @property
    def start(self):
        return self.start_time

    @property
    def end(self):
        return self.end_time

    def _formatting(self, json_: dict) -> dict:
        ts = datetime.datetime.fromtimestamp(json_['time'] / 10 ** 3)
        update_ts = datetime.datetime.fromtimestamp(json_['updateTime'] / 10 ** 3)
        return {
            self._EXCHANGE_COLUMN: self.key,
            self._LABEL_COLUMN: self.label,
            self._TICKER_COLUMN: self.ticker,
            self._MARKET_PRICE_COLUMN: float(json_['avgPrice']) if json_['type'] == 'MARKET' else None,
            self._LIMIT_PRICE_COLUMN: float(json_['price']) if json_['type'] == 'LIMIT' else None,
            self._QTY_COLUMN: float(json_['executedQty']),
            self._ORDER_ID_COLUMN: json_['orderId'],
            self._SIDE_COLUMN: json_['side'],
            self._STATUS_COLUMN: json_['status'],
            self._TYPE_COLUMN: json_['type'],
            self._TS_UPDATE_COLUMN: update_ts,
            self._TS_COLUMN: ts
        }

    def _handle(self, start: int, end: int):
        all_orders = self.allOrders(
            symbol=self.ticker,
            startTime=start,
            endTime=end,
            limit=1000,
            timestamp=int(time.time() * 1000)
        )
        if not self._validate_response(all_orders):
            raise r.HTTPError(f'Invalid status code for allOrders in  {self.__class__.__name__}')
        all_orders = all_orders.json()
        return all_orders

    @to_dataframe
    def do(self):
        overviews: list = list()
        end = int(self.end.timestamp()) * 1000
        all_orders = self._handle(start=int(self.start.timestamp()) * 1000, end=end)
        overviews.extend([self._formatting(json_=order) for order in all_orders])

        while True:
            start = all_orders[-1]['time'] + 1

            all_orders = self._handle(start=start, end=end)
            if not all_orders:
                break
            overviews.extend([self._formatting(json_=order) for order in all_orders])
        return overviews
