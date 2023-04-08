from c3d3.infrastructure.d3.interfaces.dex_supply_screener.interface import iDexSupplyScreenerHandler


class iDexBorrowScreenerHandler(iDexSupplyScreenerHandler):

    _HEALTH_FACTOR_COLUMN = 'health_factor'
