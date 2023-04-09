from c3d3.infrastructure._abc.factory.abc import iFactory

from c3d3.infrastructure.d3.handlers.dex_erc_screener.erc20.handler import ERC20DexERCScreenerHandler


class DexERCScreenerFactory(iFactory):

    def __str__(self):
        return __class__.__name__


DexERCScreenerFactory.add_object(k=ERC20DexERCScreenerHandler.key, v=ERC20DexERCScreenerHandler)
