from c3d3.infrastructure.c3.interfaces.cex_liquidation_screener.interface import iCexLiquidationScreenerHandler
from c3d3.domain.c3.wrappers.binance.usdtm.wrapper import BinanceUsdtmExchange
from c3d3.infrastructure.trad3r.root.root import TraderRoot
from c3d3.infrastructure.trad3r.leaves.binance.usdtm.leaf import BinanceUsdtmTraderLeaf
from c3d3.core.decorators.to_dataframe.decorator import to_dataframe

import datetime
import time
import requests as r


class BinanceUsdtmCexLiquidationScreenerHandler(BinanceUsdtmExchange, iCexLiquidationScreenerHandler):

    def __str__(self):
        return __class__.__name__

    def __init__(
            self,
            ticker: str, label: str,
            is_child: bool = False,
            *args, **kwargs
    ) -> None:
        if not is_child:
            BinanceUsdtmExchange.__init__(self, *args, **kwargs)
        iCexLiquidationScreenerHandler.__init__(self, ticker=ticker, label=label, *args, **kwargs)

    def _formatting(self, json_: dict) -> dict:
        return {
            self._EXCHANGE_COLUMN: self.key,
            self._LABEL_COLUMN: self.label,
            self._TICKER_COLUMN: self.ticker,
            self._CURRENT_PRICE_COLUMN: TraderRoot.get_price(self.ticker[:-4], source=BinanceUsdtmTraderLeaf.key),
            self._ENTRY_PRICE_COLUMN: float(json_['entryPrice']) if json_['entryPrice'] is not None else json_['entryPrice'],
            self._LIQUIDATION_PRICE_COLUMN: float(json_['liquidationPrice']) if json_['liquidationPrice'] is not None else json_['liquidationPrice'],
            self._QTY_COLUMN: float(json_['positionAmt']) if json_['positionAmt'] is not None else json_['positionAmt'],
            self._SIDE_COLUMN: json_['positionSide'],
            self._LEVERAGE_COLUMN: float(json_['leverage']) if json_['leverage'] is not None else json_['leverage'],
            self._UNREALIZED_PNL: float(json_['unRealizedProfit']) if json_['unRealizedProfit'] is not None else json_['unRealizedProfit'],
            self._TS_COLUMN: datetime.datetime.utcnow()
        }

    @to_dataframe
    def do(self):
        overviews: list = list()
        position_risk = self.positionRisk(symbol=self.ticker, timestamp=int(time.time() * 1000))
        if not self._validate_response(position_risk):
            raise r.HTTPError(f'Invalid status code for positionRisk in {self.__class__.__name__}')
        position_risk = position_risk.json()
        for position in position_risk:
            overviews.append(self._formatting(json_=position))
        if not overviews:
            overviews.append(
                self._formatting(
                    json_={
                        'entryPrice': None,
                        'liquidationPrice': None,
                        'positionAmt': None,
                        'positionSide': None,
                        'leverage': None,
                        'unRealizedProfit': None
                    }
                )
            )
        return overviews
