from c3d3.infrastructure._abc.factory.abc import iFactory

from c3d3.infrastructure.c3.handlers.cex_liquidation_screener.binance.usdtm.handler import BinanceUsdtmCexLiquidationScreenerHandler


class CexLiquidationScreenerFactory(iFactory):

    def __str__(self):
        return __class__.__name__


CexLiquidationScreenerFactory.add_object(k=BinanceUsdtmCexLiquidationScreenerHandler.key, v=BinanceUsdtmCexLiquidationScreenerHandler)

