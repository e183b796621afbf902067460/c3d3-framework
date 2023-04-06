from c3d3.infrastructure._abc.factory.abc import iFactory

from c3d3.infrastructure.d3.handlers.dex_supply_screener.aave.v3.handler import AAveV3DexSupplyScreenerHandler


class DexSupplyScreenerFactory(iFactory):

    def __str__(self):
        return __class__.__name__


DexSupplyScreenerFactory.add_object(k=AAveV3DexSupplyScreenerHandler.key, v=AAveV3DexSupplyScreenerHandler)
