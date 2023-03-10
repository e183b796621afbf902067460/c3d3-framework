from c3d3.infrastructure.abc.factory.abc import iFactory

from c3d3.infrastructure.d3.handlers.dex_screener.quickswap.v3.handler import QuickSwapV3DexScreenerHandler
from c3d3.infrastructure.d3.handlers.dex_screener.quickswap.v2.handler import QuickSwapV2DexScreenerHandler
from c3d3.infrastructure.d3.handlers.dex_screener.uniswap.v3.handler import UniSwapV3DexScreenerHandler
from c3d3.infrastructure.d3.handlers.dex_screener.uniswap.v2.handler import UniSwapV2DexScreenerHandler
from c3d3.infrastructure.d3.handlers.dex_screener.kyberswap.v3.handler import KyberSwapV3DexScreenerHandler
from c3d3.infrastructure.d3.handlers.dex_screener.velodrome.v2.handler import VelodromeV2DexScreenerHandler
from c3d3.infrastructure.d3.handlers.dex_screener.spookyswap.v2.handler import SpookySwapV2DexScreenerHandler


class DexScreenerFactory(iFactory):

    def __str__(self):
        return __class__.__name__


DexScreenerFactory.add_object(k=QuickSwapV2DexScreenerHandler.key, v=QuickSwapV2DexScreenerHandler)
DexScreenerFactory.add_object(k=QuickSwapV3DexScreenerHandler.key, v=QuickSwapV3DexScreenerHandler)
DexScreenerFactory.add_object(k=UniSwapV2DexScreenerHandler.key, v=UniSwapV2DexScreenerHandler)
DexScreenerFactory.add_object(k=UniSwapV3DexScreenerHandler.key, v=UniSwapV3DexScreenerHandler)
DexScreenerFactory.add_object(k=KyberSwapV3DexScreenerHandler.key, v=KyberSwapV3DexScreenerHandler)
DexScreenerFactory.add_object(k=VelodromeV2DexScreenerHandler.key, v=VelodromeV2DexScreenerHandler)
DexScreenerFactory.add_object(k=SpookySwapV2DexScreenerHandler.key, v=SpookySwapV2DexScreenerHandler)
