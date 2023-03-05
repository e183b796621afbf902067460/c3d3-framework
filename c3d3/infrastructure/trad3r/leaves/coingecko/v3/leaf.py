from typing import Optional
import time

from c3d3.infrastructure.trad3r.interfaces.leaf.interface import iTraderLeaf
from c3d3.domain.c3.wrappers.coingecko.v3.wrapper import CoinGeckoV3Exchange


class CoinGeckoV3TraderLeaf(iTraderLeaf, CoinGeckoV3Exchange):

    _PEGS = {
        'USDT': 'tether',
        'ETH': 'ethereum',
        'BTC': 'bitcoin',
        'WETH': 'weth',
        'WBNB': 'wbnb',
        'WBTC': 'wrapped-bitcoin',
        'amWETH': 'aave-polygon-weth',
        'amWBTC': 'aave-polygon-wbtc',
        'stETH': 'staked-ether',
        'WFTM': 'wrapped-fantom',
        'WAVAX': 'wrapped-avax',
    }

    __SLEEP = 12

    def __str__(self):
        return __class__.__name__

    def get_price(self, a: str, b: str, *args, **kwargs) -> Optional[float]:
        a, b = self._peg(symbol=a), 'usd' if b == 'USD' else b
        response = self.simplePrice(ids=a, vs_currencies=b)
        while response.status_code == 429:
            time.sleep(self.__SLEEP)
            response = self.simplePrice(ids=a, vs_currencies=b)
        return response.json()[a][b]
