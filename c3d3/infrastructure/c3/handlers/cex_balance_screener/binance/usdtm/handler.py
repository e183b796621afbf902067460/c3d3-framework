from c3d3.infrastructure.c3.interfaces.cex_balance_screener.interface import iCexBalanceScreenerHandler
from c3d3.domain.c3.wrappers.binance.usdtm.wrapper import BinanceUsdtmExchange
from c3d3.infrastructure.trad3r.root.root import TraderRoot
from c3d3.core.decorators.to_dataframe.decorator import to_dataframe

import datetime
import time
import requests as r


class BinanceUsdtmCexBalanceScreenerHandler(BinanceUsdtmExchange, iCexBalanceScreenerHandler):

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
        iCexBalanceScreenerHandler.__init__(self, ticker=ticker, label=label, *args, **kwargs)

    def _formatting(self, json_: dict) -> dict:
        return {
            self._EXCHANGE_COLUMN: self.key,
            self._LABEL_COLUMN: self.label,
            self._TICKER_COLUMN: self.ticker,
            self._CURRENT_PRICE_COLUMN: TraderRoot.get_price(self.ticker),
            self._QTY_COLUMN: float(json_['marginBalance']),
            self._TS_COLUMN: datetime.datetime.utcnow()
        }

    @to_dataframe
    def do(self):
        overviews: list = list()
        account = self.account(timestamp=int(time.time() * 1000))
        if not self._validate_response(account):
            raise r.HTTPError(f'Invalid status code for account in {self.__class__.__name__}')
        account = account.json()

        for asset in account['assets']:
            if asset['asset'] == self.ticker:
                overviews.append(self._formatting(json_=asset))
                break
        return overviews

