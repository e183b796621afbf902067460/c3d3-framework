from c3d3.infrastructure._abc.factory.abc import iFactory

from c3d3.infrastructure.c3.handlers.cex_order_history_screener.binance.usdtm.handler import BinanceUsdtmCexOrderHistoryScreenerHandler


class CexOrderHistoryScreenerFactory(iFactory):

    def __str__(self):
        return __class__.__name__


CexOrderHistoryScreenerFactory.add_object(k=BinanceUsdtmCexOrderHistoryScreenerHandler.key, v=BinanceUsdtmCexOrderHistoryScreenerHandler)
