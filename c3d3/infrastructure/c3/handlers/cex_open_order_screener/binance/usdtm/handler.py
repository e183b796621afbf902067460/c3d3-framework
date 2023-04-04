from c3d3.infrastructure.c3.interfaces.cex_open_order_screener.interface import iCexOpenOrderScreenerHandler
from c3d3.domain.c3.wrappers.binance.usdtm.wrapper import BinanceUsdtmExchange
from c3d3.infrastructure.trad3r.root.root import TraderRoot
from c3d3.infrastructure.trad3r.leaves.binance.usdtm.leaf import BinanceUsdtmTraderLeaf
from c3d3.core.decorators.to_dataframe.decorator import to_dataframe

import datetime
import time
import requests as r


class BinanceUsdtmCexOpenOrderScreenerHandler(BinanceUsdtmExchange, iCexOpenOrderScreenerHandler):

    def __str__(self):
        return __class__.__name__

    def __init__(
            self,
            ticker: str, label: str,
            is_child: bool = False,
            *args, **kwargs
    ) -> None:
        if not is_child:
            BinanceUsdtmExchange.__init__(self, *args, **kwargs)
        iCexOpenOrderScreenerHandler.__init__(self, ticker=ticker, label=label, *args, **kwargs)

    def _formatting(self, json_: dict) -> dict:
        return {
            self._EXCHANGE_COLUMN: self.key,
            self._LABEL_COLUMN: self.label,
            self._TICKER_COLUMN: self.ticker,
            self._PRICE_COLUMN: TraderRoot.get_price(self.ticker[:-4], source=BinanceUsdtmTraderLeaf.key),
            self._TRADE_PRICE_COLUMN: float(json_['price']) if json_['price'] is not None else json_['price'],
            self._QTY_COLUMN: float(json_['origQty']) if json_['origQty'] is not None else json_['origQty'],
            self._SIDE_COLUMN: json_['side'],
            self._TS_COLUMN: datetime.datetime.utcnow()
        }

    @to_dataframe
    def do(self):
        overviews: list = list()
        open_orders = self.openOrders(symbol=self.ticker, timestamp=int(time.time() * 1000))
        if not self._validate_response(open_orders):
            raise r.HTTPError(f'Invalid status code for openOrders in {self.__class__.__name__}')
        open_orders = open_orders.json()
        for open_order in open_orders:
            overviews.append(self._formatting(json_=open_order))
        if not overviews:
            overviews.append(
                self._formatting(
                    json_={
                        'price': None,
                        'origQty': None,
                        'side': None
                    }
                )
            )
        return overviews

