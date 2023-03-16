from c3d3.infrastructure.c3.handlers.cex_screener.binance.spot.handler import BinanceSpotCexScreenerHandler
from c3d3.domain.c3.wrappers.binance.usdtm.wrapper import BinanceUsdtmExchange

import datetime


class BinanceUsdtmCexScreenerHandler(BinanceUsdtmExchange, BinanceSpotCexScreenerHandler):

    def __str__(self):
        return __class__.__name__

    def __init__(
            self,
            ticker: str, start_time: datetime.datetime, end_time: datetime.datetime,
            is_child: bool = True,
            *args, **kwargs
    ) -> None:
        BinanceSpotCexScreenerHandler.__init__(self, ticker=ticker, start_time=start_time, end_time=end_time, is_child=is_child, *args, **kwargs)
        BinanceUsdtmExchange.__init__(self, *args, **kwargs)
