from c3d3.infrastructure.c3.interfaces.cex_balance_screener.interface import iCexBalanceScreenerHandler


class iCexOpenOrderScreenerHandler(iCexBalanceScreenerHandler):

    _ENTRY_PRICE_COLUMN = 'entry_price'
    _SIDE_COLUMN = 'side'
