from c3d3.infrastructure.d3.bridge.bridge import D3Bridge
from c3d3.infrastructure.c3.bridge.bridge import C3Bridge

from c3d3.infrastructure.d3.abstract.factory import D3AbstractFactory
from c3d3.infrastructure.c3.abstract.factory import C3AbstractFactory

from c3d3.infrastructure.d3.factories.dex_screener.factory import DexScreenerFactory
from c3d3.infrastructure.c3.factories.cex_screener.factory import CexScreenerFactory

from c3d3.infrastructure.d3.handlers.dex_screener.quickswap.v3.handler import QuickSwapV3DexScreenerHandler
from c3d3.infrastructure.d3.handlers.dex_screener.quickswap.v2.handler import QuickSwapV2DexScreenerHandler
from c3d3.infrastructure.d3.handlers.dex_screener.uniswap.v3.handler import UniSwapV3DexScreenerHandler
from c3d3.infrastructure.d3.handlers.dex_screener.uniswap.v2.handler import UniSwapV2DexScreenerHandler
from c3d3.infrastructure.d3.handlers.dex_screener.kyberswap.v3.handler import KyberSwapV3DexScreenerHandler
from c3d3.infrastructure.d3.handlers.dex_screener.velodrome.v2.handler import VelodromeV2DexScreenerHandler
from c3d3.infrastructure.d3.handlers.dex_screener.spookyswap.v2.handler import SpookySwapV2DexScreenerHandler
from c3d3.infrastructure.d3.handlers.dex_screener.equalizer.v2.handler import EqualizerV2DexScreenerHandler

from c3d3.infrastructure.c3.handlers.cex_screener.binance.usdtm.handler import BinanceUsdtmCexScreenerHandler

from c3d3.domain.d3.adhoc.chains.polygon.chain import Polygon
from c3d3.domain.d3.adhoc.chains.optimism.chain import Optimism
from c3d3.domain.d3.adhoc.chains.fantom.chain import Fantom

from c3d3.domain.d3.adhoc.nodes.http.adhoc import HTTPNode

import datetime
import pandas as pd


start_time = datetime.datetime(year=2023, month=3, day=8, hour=5, minute=33, second=0)
end_time = datetime.datetime(year=2023, month=3, day=8, hour=5, minute=34, second=0)


ticker = 'MATICUSDT'

matic_api_key = 'XTMZ21TVBX93CTGUZMJV6YCFYUMITQWX1Y'
optimism_api_key = 'KMIVA8ESRPTDJ3SIEI73NPX9P1EAPJV8CE'
fantom_api_key = 'PJFPWEZZU9THCYUX6IDSSND8YEBA13CJRP'

address = '0xAE81FAc689A1b4b1e06e7ef4a2ab4CD8aC0A087D'
is_reverse = False

node = HTTPNode(uri='https://rpc.ankr.com/polygon')


cex_screener = C3Bridge(
    abstract_factory=C3AbstractFactory,
    factory_key=CexScreenerFactory.key,
    object_key=BinanceUsdtmCexScreenerHandler.key
).init_object(
    ticker=ticker,
    start_time=start_time,
    end_time=end_time
)

dex_screener = D3Bridge(
    abstract_factory=D3AbstractFactory,
    factory_key=DexScreenerFactory.key,
    object_key=QuickSwapV3DexScreenerHandler.key
).init_object(
    start_time=start_time,
    end_time=end_time,
    api_key=matic_api_key,
    chain=Polygon.name,
    is_reverse=is_reverse,
    address=address,
    node=node
)


# cex_data = pd.DataFrame(cex_screener.do()).set_index('ts').price.resample('S').ohlc().reset_index()
dex_data = dex_screener.do()
print(dex_data)

# df = dex_data.merge(cex_data, how='outer', on='ts').sort_values('ts').fillna(method='ffill').dropna()
# df.to_csv('test.csv')
