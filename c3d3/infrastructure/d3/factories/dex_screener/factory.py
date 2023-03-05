from c3d3.infrastructure.abc.factory.abc import iFactory


class DexScreenerFactory(iFactory):

    def __str__(self):
        return __class__.__name__
