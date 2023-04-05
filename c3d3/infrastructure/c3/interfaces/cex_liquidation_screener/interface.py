from c3d3.infrastructure.c3.interfaces.cex_open_order_screener.interface import iCexOpenOrderScreenerHandler


class iCexLiquidationScreenerHandler(iCexOpenOrderScreenerHandler):

    _LIQUIDATION_PRICE_COLUMN = 'liquidation_price'
    _LEVERAGE_COLUMN = 'leverage'
    _UNREALIZED_PNL = 'unrealized_pnl'

    @property
    def __columns(self):
        return [
            self._EXCHANGE_COLUMN,
            self._LABEL_COLUMN,
            self._TICKER_COLUMN,
            self._ENTRY_PRICE_COLUMN,
            self._CURRENT_PRICE_COLUMN,
            self._QTY_COLUMN,
            self._SIDE_COLUMN,
            self._LIQUIDATION_PRICE_COLUMN,
            self._LEVERAGE_COLUMN,
            self._UNREALIZED_PNL,
            self._TS_COLUMN
        ]
