from c3d3.infrastructure.c3.handlers.cex_screener.binance.spot.handler import BinanceSpotCexScreenerHandler
from c3d3.domain.c3.wrappers.binance.usdtm.wrapper import BinanceUsdtmExchange


class BinanceUsdtmCexScreenerHandler(BinanceUsdtmExchange, BinanceSpotCexScreenerHandler):

    def __str__(self):
        return __class__.__name__
