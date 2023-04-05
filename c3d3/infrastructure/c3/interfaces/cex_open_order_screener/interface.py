from c3d3.infrastructure.c3.interfaces.cex_balance_screener.interface import iCexBalanceScreenerHandler


class iCexOpenOrderScreenerHandler(iCexBalanceScreenerHandler):

    _ENTRY_PRICE_COLUMN = 'entry_price'
    _SIDE_COLUMN = 'side'

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
            self._TS_COLUMN
        ]
