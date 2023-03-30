from c3d3.domain.c3.wrappers.binance.spot.wrapper import BinanceSpotExchange
from c3d3.infrastructure.c3.interfaces.cex_balance_screener.interface import iCexBalanceScreenerHandler
from c3d3.core.decorators.to_dataframe.decorator import to_dataframe
from c3d3.infrastructure.trad3r.root.root import TraderRoot

import datetime
import requests as r
import time


class BinanceSpotCexBalanceScreenerHandler(BinanceSpotExchange, iCexBalanceScreenerHandler):

    def __str__(self):
        return __class__.__name__

    def __init__(
            self,
            ticker: str, label: str,
            is_child: bool = False,
            *args, **kwargs
    ) -> None:
        if not is_child:
            BinanceSpotExchange.__init__(self, *args, **kwargs)
        iCexBalanceScreenerHandler.__init__(self, ticker=ticker, label=label, *args, **kwargs)

    def _formatting(self, json_: dict) -> dict:
        return {
            self._EXCHANGE_COLUMN: self.key,
            self._TICKER_COLUMN: self.ticker,
            self._LABEL_COLUMN: self.label,
            self._PRICE_COLUMN: TraderRoot.get_price(self.ticker),
            self._QTY_COLUMN: float(json_['free']) + float(json_['locked']),
            self._TS_COLUMN: datetime.datetime.utcnow()
        }

    @to_dataframe
    def do(self):
        overviews: list = list()
        account = self.account(timestamp=int(time.time() * 1000))
        if not self._validate_response(account):
            raise r.HTTPError(f'Invalid status code for aggTrades in {self.__class__.__name__}')
        account = account.json()
        for balance in account['assets']:
            if balance['asset'] == self.ticker:
                overviews.append(self._formatting(json_=balance))
                break
        return overviews
