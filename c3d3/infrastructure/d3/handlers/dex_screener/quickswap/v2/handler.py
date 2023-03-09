import datetime

from c3d3.domain.d3.wrappers.quickswap.v2.pool.wrapper import QuickSwapV2PairContract
from c3d3.infrastructure.d3.handlers.dex_screener.uniswap.v2.handler import UniSwapV2DexScreenerHandler


class QuickSwapV2DexScreenerHandler(QuickSwapV2PairContract, UniSwapV2DexScreenerHandler):

    def __str__(self):
        return __class__.__name__

    def __init__(
            self,
            api_key: str, chain: str,
            start_time: datetime.datetime, end_time: datetime.datetime,
            is_reverse: bool, is_child: bool = True,
            *args, **kwargs
    ) -> None:
        QuickSwapV2PairContract.__init__(self, *args, **kwargs)
        UniSwapV2DexScreenerHandler.__init__(self, api_key=api_key, chain=chain, start_time=start_time, end_time=end_time, is_reverse=is_reverse, is_child=is_child, *args, **kwargs)
