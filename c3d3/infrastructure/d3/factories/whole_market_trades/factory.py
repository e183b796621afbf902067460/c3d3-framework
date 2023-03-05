from typing import Generic

from c3d3.infrastructure.abc.factory.abc import iFactory
# from d3tl.typings.handlers.bids_and_asks.typing import BidsAndAsksHandler


class WholeMarketTradesFactory(iFactory):

    def __str__(self):
        return __class__.__name__
