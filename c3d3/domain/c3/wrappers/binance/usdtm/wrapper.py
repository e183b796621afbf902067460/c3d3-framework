from typing import Optional, List
from requests import Response

from c3d3.domain.c3.wrappers.binance.spot.wrapper import BinanceSpotExchange
from c3d3.core.decorators.permission.decorator import permission


class BinanceUsdtmExchange(BinanceSpotExchange):
    _ENDPOINT, _HEARTBEAT = 'https://fapi.binance.com', '/fapi/v1/ping'

    def tickerPrice(self, symbol: Optional[str] = None, symbols: Optional[List[str]] = None) -> Response:
        params: dict = {'symbol': symbol} if symbol else {'symbols': symbols}
        return self._r(method=self._GET, url='/fapi/v1/ticker/price', params=params)

    def aggTrades(
            self,
            symbol: str,
            fromId: Optional[int] = None,
            startTime: Optional[int] = None,
            endTime: Optional[int] = None,
            limit: Optional[int] = None
    ) -> Response:
        params: dict = {
            'symbol': symbol,
            'fromId': fromId,
            'startTime': startTime,
            'endTime': endTime,
            'limit': limit
        }
        return self._r(method=self._GET, url='/fapi/v1/aggTrades', params=params)

    @permission
    def account(
            self,
            timestamp: int,
            recvWindow: Optional[int] = None
    ) -> Response:
        params: dict = {'timestamp': timestamp} if recvWindow is None else {'timestamp': timestamp, 'recvWindow': recvWindow}
        params.update({'signature': self._signature(params)})
        return self._r(
            method=self._GET,
            url='/fapi/v2/account',
            params=params,
            headers=self._header()
        )

    @permission
    def positionRisk(
            self,
            timestamp: int,
            symbol: Optional[str] = None,
            recvWindow: Optional[int] = None
    ) -> Response:
        params: dict = {'timestamp': timestamp}
        if symbol:
            params.update({'symbol': symbol})
        if recvWindow:
            params.update({'recvWindow': recvWindow})
        params.update({'signature': self._signature(params)})
        return self._r(
            method=self._GET,
            url='/fapi/v2/positionRisk',
            params=params,
            headers=self._header()
        )

    @permission
    def openOrders(
            self,
            timestamp: int,
            symbol: Optional[str] = None,
            recvWindow: Optional[int] = None
    ) -> Response:
        params: dict = {
            'timestamp': timestamp
        }
        if symbol:
            params.update({'symbol': symbol})
        if recvWindow:
            params.update({'recvWindow': recvWindow})
        params.update({'signature': self._signature(params)})
        return self._r(
            method=self._GET,
            url='/fapi/v1/openOrders',
            params=params,
            headers=self._header()
        )

    @permission
    def historicalTrades(
            self,
            symbol: str,
            limit: Optional[int] = None,
            from_id: Optional[int] = None
    ) -> Response:
        params = dict()
        params.update({'symbol': symbol})
        if limit:
            params.update({'limit': limit})
        if from_id:
            params.update({'fromId': from_id})
        params.update({'signature': self._signature(params)})
        return self._r(
            method=self._GET,
            url='/fapi/v1/historicalTrades',
            params=params,
            headers=self._header()
        )

    @permission
    def allOrders(
            self,
            symbol: str,
            timestamp: int,
            orderId: Optional[int] = None,
            startTime: Optional[int] = None,
            endTime: Optional[int] = None,
            limit: Optional[int] = None,
            recvWindow: Optional[int] = None
    ) -> Response:
        params = dict()
        params.update(
            {
                'symbol': symbol,
                'timestamp': timestamp
            }
        )
        if orderId:
            params.update({'orderId': orderId})
        if startTime:
            params.update({'startTime': startTime})
        if endTime:
            params.update({'endTime': endTime})
        if limit:
            params.update({'limit': limit})
        if recvWindow:
            params.update({'recvWindow': recvWindow})
        params.update({'signature': self._signature(params)})
        return self._r(
            method=self._GET,
            url='/fapi/v1/allOrders',
            params=params,
            headers=self._header()
        )

    @permission
    def userTrades(
            self,
            symbol: str,
            timestamp: int,
            orderId: Optional[int] = None,
            fromId: Optional[int] = None,
            startTime: Optional[int] = None,
            endTime: Optional[int] = None,
            limit: Optional[int] = None,
            recvWindow: Optional[int] = None
    ) -> Response:
        params = dict()
        params.update(
            {
                'symbol': symbol,
                'timestamp': timestamp
            }
        )
        if orderId:
            params.update({'orderId': orderId})
        if fromId:
            params.update({'fromId': fromId})
        if startTime:
            params.update({'startTime': startTime})
        if endTime:
            params.update({'endTime': endTime})
        if limit:
            params.update({'limit': limit})
        if recvWindow:
            params.update({'recvWindow': recvWindow})
        params.update({'signature': self._signature(params)})
        return self._r(
            method=self._GET,
            url='/fapi/v1/userTrades',
            params=params,
            headers=self._header()
        )
