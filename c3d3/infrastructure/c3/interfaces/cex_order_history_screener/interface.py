from c3d3.infrastructure.c3.interfaces.cex_open_order_screener.interface import iCexOpenOrderScreenerHandler


class iCexOrderHistoryScreenerHandler(iCexOpenOrderScreenerHandler):

    _MARKET_PRICE_COLUMN = 'market_price'
    _LIMIT_PRICE_COLUMN = 'limit_price'
    _ORDER_ID_COLUMN = 'order_id'
    _STATUS_COLUMN = 'status'
    _TS_UPDATE_COLUMN = 'ts_update'
    _TYPE_COLUMN = 'type'
