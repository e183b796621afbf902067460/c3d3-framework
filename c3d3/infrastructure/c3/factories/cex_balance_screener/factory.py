from c3d3.infrastructure._abc.factory.abc import iFactory

from c3d3.infrastructure.c3.handlers.cex_balance_screener.binance.spot.handler import BinanceSpotCexBalanceScreenerHandler
from c3d3.infrastructure.c3.handlers.cex_balance_screener.binance.usdtm.handler import BinanceUsdtmCexBalanceScreenerHandler


class CexBalanceScreenerFactory(iFactory):

    def __str__(self):
        return __class__.__name__


CexBalanceScreenerFactory.add_object(k=BinanceSpotCexBalanceScreenerHandler.key, v=BinanceSpotCexBalanceScreenerHandler)
CexBalanceScreenerFactory.add_object(k=BinanceUsdtmCexBalanceScreenerHandler.key, v=BinanceUsdtmCexBalanceScreenerHandler)
