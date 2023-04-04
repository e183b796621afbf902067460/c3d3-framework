from c3d3.infrastructure._abc.factory.abc import iFactory

from c3d3.infrastructure.c3.handlers.cex_open_order_screener.binance.usdtm.handler import BinanceUsdtmCexOpenOrderScreenerHandler


class CexOpenOrderScreenerFactory(iFactory):

    def __str__(self):
        return __class__.__name__


CexOpenOrderScreenerFactory.add_object(k=BinanceUsdtmCexOpenOrderScreenerHandler.key, v=BinanceUsdtmCexOpenOrderScreenerHandler)
