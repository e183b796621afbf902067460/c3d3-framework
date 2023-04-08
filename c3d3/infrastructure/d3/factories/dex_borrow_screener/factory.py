from c3d3.infrastructure._abc.factory.abc import iFactory

from c3d3.infrastructure.d3.handlers.dex_borrow_screener.aave.v3.handler import AAveV3DexBorrowScreenerHandler


class DexBorrowScreenerFactory(iFactory):

    def __str__(self):
        return __class__.__name__


DexBorrowScreenerFactory.add_object(k=AAveV3DexBorrowScreenerHandler.key, v=AAveV3DexBorrowScreenerHandler)
