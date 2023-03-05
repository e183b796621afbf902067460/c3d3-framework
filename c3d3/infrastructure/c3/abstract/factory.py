from c3d3.infrastructure.abc.factory.abc import iFactory

from c3d3.infrastructure.c3.factories.cex_screener.factory import CexScreenerFactory


class C3AbstractFactory(iFactory):

    def __str__(self):
        return __class__.__name__


C3AbstractFactory.add_object(k=CexScreenerFactory.key, v=CexScreenerFactory)
