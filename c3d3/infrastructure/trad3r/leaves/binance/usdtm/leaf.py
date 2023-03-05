from typing import Optional

from c3d3.infrastructure.trad3r.interfaces.leaf.interface import iTraderLeaf
from c3d3.domain.c3.wrappers.binance.usdtm.wrapper import BinanceUSDTmExchange


class BinanceUSDTmTraderLeaf(iTraderLeaf, BinanceUSDTmExchange):

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
        return float(self.tickerPrice(symbol=a + b)['price'])
