from c3d3.infrastructure._abc.factory.abc import iFactory

from c3d3.infrastructure.d3.handlers.dex_gwei_screener.evm.handler import EVMDexGweiScreenerHandler


class DexGweiScreenerFactory(iFactory):

    def __str__(self):
        return __class__.__name__


DexGweiScreenerFactory.add_object(k=EVMDexGweiScreenerHandler.key, v=EVMDexGweiScreenerHandler)
