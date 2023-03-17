from typing import Optional

from c3d3.infrastructure.trad3r.interfaces.leaf.interface import iTraderLeaf
from c3d3.domain.c3.wrappers.binance.spot.wrapper import BinanceSpotExchange
from c3d3.core.decorators.singleton.decorator import singleton


@singleton
class BinanceSpotTraderLeaf(iTraderLeaf, BinanceSpotExchange):

    _PEGS = {
        'fUSDT': 'USDT',
        'WETH.e': 'ETH',
        'WBTC.e': 'BTC',
        'CRV.e': 'CRV',
        'WETH': 'ETH',
        'WBNB': 'BNB',
        'WBTC': 'BTC',
        'WFTM': 'FTM',
        'WMATIC': 'MATIC'
    }

    def __str__(self):
        return __class__.__name__

    def get_price(self, a: str, b: str, *args, **kwargs) -> Optional[float]:
        a, b = self._peg(symbol=a), 'USDT' if b == 'USD' else b
        try:
            return float(self.tickerPrice(symbol=a + b).json()['price'])
        except KeyError:
            return None


BinanceSpotTraderLeaf = BinanceSpotTraderLeaf()
