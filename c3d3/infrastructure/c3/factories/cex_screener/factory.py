from c3d3.infrastructure._abc.factory.abc import iFactory

from c3d3.infrastructure.c3.handlers.cex_screener.binance.spot.handler import BinanceSpotCexScreenerHandler
from c3d3.infrastructure.c3.handlers.cex_screener.binance.usdtm.handler import BinanceUsdtmCexScreenerHandler


class CexScreenerFactory(iFactory):

    def __str__(self):
        return __class__.__name__


CexScreenerFactory.add_object(k=BinanceSpotCexScreenerHandler.key, v=BinanceSpotCexScreenerHandler)
CexScreenerFactory.add_object(k=BinanceUsdtmCexScreenerHandler.key, v=BinanceUsdtmCexScreenerHandler)
