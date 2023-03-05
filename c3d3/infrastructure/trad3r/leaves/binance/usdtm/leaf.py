from c3d3.infrastructure.trad3r.leaves.binance.spot.leaf import BinanceSpotTraderLeaf
from c3d3.domain.c3.wrappers.binance.usdtm.wrapper import BinanceUsdtmExchange


class BinanceUsdtmTraderLeaf(BinanceSpotTraderLeaf, BinanceUsdtmExchange):

    def __str__(self):
        return __class__.__name__
