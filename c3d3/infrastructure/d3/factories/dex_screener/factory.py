from c3d3.infrastructure.abc.factory.abc import iFactory

from c3d3.infrastructure.d3.handlers.dex_screener.quickswap.v3.handler import QuickSwapV3DexScreenerHandler


class DexScreenerFactory(iFactory):

    def __str__(self):
        return __class__.__name__


DexScreenerFactory.add_object(k=QuickSwapV3DexScreenerHandler.key, v=QuickSwapV3DexScreenerHandler)
