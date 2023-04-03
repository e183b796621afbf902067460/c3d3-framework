from c3d3.infrastructure._abc.factory.abc import iFactory

from c3d3.infrastructure.d3.factories.dex_screener.factory import DexScreenerFactory


class D3AbstractFactory(iFactory):

    def __str__(self):
        return __class__.__name__


D3AbstractFactory.add_object(k=DexScreenerFactory.key, v=DexScreenerFactory)

