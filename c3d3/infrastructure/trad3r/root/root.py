from typing import Dict, Optional
from functools import lru_cache

from c3d3.infrastructure.trad3r.typings.leaf.typing import TraderLeaf
from c3d3.core.decorators.yieldmethod.decorator import yieldmethod

from c3d3.infrastructure.trad3r.leaves.coingecko.v3.leaf import CoinGeckoV3TraderLeaf
from c3d3.infrastructure.trad3r.leaves.binance.spot.leaf import BinanceSpotTraderLeaf
from c3d3.infrastructure.trad3r.leaves.binance.usdtm.leaf import BinanceUsdtmTraderLeaf


class TraderRoot:

    _TRADERS: Dict[str, TraderLeaf] = dict()

    @classmethod
    def add_trader(cls, name, trader: TraderLeaf) -> None:
        if not cls._TRADERS.get(name):
            cls._TRADERS[name] = trader

    @classmethod
    @lru_cache
    @yieldmethod
    def get_price(
            cls,
            a: str, b: str = 'USD', source=None,
            *args, **kwargs) -> Optional[float]:
        if source:
            trader = cls._TRADERS.get(source)
            if not trader:
                raise KeyError(f"No such Trader {source}.")
            yield trader.get_price(a=a, b=b)
        else:
            for _, trader in cls._TRADERS.items():
                yield trader.get_price(a=a, b=b, *args, **kwargs)


TraderRoot.add_trader(name=BinanceSpotTraderLeaf.key, trader=BinanceSpotTraderLeaf)
TraderRoot.add_trader(name=CoinGeckoV3TraderLeaf.key, trader=CoinGeckoV3TraderLeaf)
TraderRoot.add_trader(name=BinanceUsdtmTraderLeaf.key, trader=BinanceUsdtmTraderLeaf)
