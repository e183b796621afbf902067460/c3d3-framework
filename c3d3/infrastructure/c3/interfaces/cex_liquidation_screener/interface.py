from c3d3.infrastructure.c3.interfaces.cex_open_order_screener.interface import iCexOpenOrderScreenerHandler


class iCexLiquidationScreenerHandler(iCexOpenOrderScreenerHandler):

    _LIQUIDATION_PRICE_COLUMN = 'liquidation_price'
    _LEVERAGE_COLUMN = 'leverage'
    _UNREALIZED_PNL = 'unrealized_pnl'
