from c3d3.domain.d3.wrappers.equalizer.v2.pool.wrapper import EqualizerPairV2Contract
from c3d3.infrastructure.d3.handlers.dex_screener.velodrome.v2.handler import VelodromeV2DexScreenerHandler

import datetime


class EqualizerV2DexScreenerHandler(EqualizerPairV2Contract, VelodromeV2DexScreenerHandler):
    _FEE = None

    def __str__(self):
        return __class__.__name__

    def __init__(
            self,
            api_key: str, chain: str,
            start_time: datetime.datetime, end_time: datetime.datetime,
            is_reverse: bool, is_child: bool = True,
            *args, **kwargs
    ) -> None:
        EqualizerPairV2Contract.__init__(self, *args, **kwargs)
        VelodromeV2DexScreenerHandler.__init__(self, api_key=api_key, chain=chain, start_time=start_time, end_time=end_time, is_reverse=is_reverse, is_child=is_child, *args, **kwargs)

    def _factory(self):
        return self.factory()
