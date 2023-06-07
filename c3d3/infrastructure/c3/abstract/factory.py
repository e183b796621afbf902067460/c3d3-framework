from c3d3.infrastructure._abc.factory.abc import iFactory

from c3d3.infrastructure.c3.factories.cex_screener.factory import CexScreenerFactory
from c3d3.infrastructure.c3.factories.cex_balance_screener.factory import CexBalanceScreenerFactory
from c3d3.infrastructure.c3.factories.cex_open_order_screener.factory import CexOpenOrderScreenerFactory
from c3d3.infrastructure.c3.factories.cex_liquidation_screener.factory import CexLiquidationScreenerFactory
from c3d3.infrastructure.c3.factories.cex_order_history_screener.factory import CexOrderHistoryScreenerFactory


class C3AbstractFactory(iFactory):

    def __str__(self):
        return __class__.__name__


C3AbstractFactory.add_object(k=CexScreenerFactory.key, v=CexScreenerFactory)
C3AbstractFactory.add_object(k=CexBalanceScreenerFactory.key, v=CexBalanceScreenerFactory)
C3AbstractFactory.add_object(k=CexOpenOrderScreenerFactory.key, v=CexOpenOrderScreenerFactory)
C3AbstractFactory.add_object(k=CexLiquidationScreenerFactory.key, v=CexLiquidationScreenerFactory)
C3AbstractFactory.add_object(k=CexOrderHistoryScreenerFactory.key, v=CexOrderHistoryScreenerFactory)
