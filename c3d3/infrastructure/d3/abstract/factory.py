from c3d3.infrastructure._abc.factory.abc import iFactory

from c3d3.infrastructure.d3.factories.dex_screener.factory import DexScreenerFactory
from c3d3.infrastructure.d3.factories.dex_supply_screener.factory import DexSupplyScreenerFactory
from c3d3.infrastructure.d3.factories.dex_borrow_screener.factory import DexBorrowScreenerFactory
from c3d3.infrastructure.d3.factories.dex_erc_screener.factory import DexERCScreenerFactory


class D3AbstractFactory(iFactory):

    def __str__(self):
        return __class__.__name__


D3AbstractFactory.add_object(k=DexScreenerFactory.key, v=DexScreenerFactory)
D3AbstractFactory.add_object(k=DexSupplyScreenerFactory.key, v=DexSupplyScreenerFactory)
D3AbstractFactory.add_object(k=DexBorrowScreenerFactory.key, v=DexBorrowScreenerFactory)
D3AbstractFactory.add_object(k=DexERCScreenerFactory.key, v=DexERCScreenerFactory)

