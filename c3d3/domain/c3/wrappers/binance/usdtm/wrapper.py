from typing import Optional, List

from c3d3.domain.c3.wrappers.binance.spot.wrapper import BinanceSpotExchange
from c3d3.core.decorators.permission.decorator import permission


class BinanceUsdtmExchange(BinanceSpotExchange):
    _ENDPOINT, _HEARTBEAT = 'https://fapi.binance.com', '/fapi/v1/ping'

    def tickerPrice(self, symbol: Optional[str] = None, symbols: Optional[List[str]] = None) -> dict:
        params: dict = {'symbol': symbol} if symbol else {'symbols': symbols}
        return self._r(method=self._GET, url='/fapi/v1/ticker/price', params=params).json()

    def aggTrades(
            self,
            symbol: str,
            fromId: Optional[int] = None,
            startTime: Optional[int] = None,
            endTime: Optional[int] = None,
            limit: Optional[int] = None
    ) -> dict:
        params: dict = {
            'symbol': symbol,
            'fromId': fromId,
            'startTime': startTime,
            'endTime': endTime,
            'limit': limit
        }
        return self._r(method=self._GET, url='/fapi/v1/aggTrades', params=params).json()

    @permission
    def account(
            self,
            timestamp: int,
            recvWindow: Optional[int] = None
    ) -> dict:
        params: dict = {'timestamp': timestamp} if recvWindow is None else {'timestamp': timestamp, 'recvWindow': recvWindow}
        params.update({'signature': self._signature(params)})

        return self._r(
            method=self._GET,
            url='/fapi/v2/account',
            params=params,
            headers=self._header()
        ).json()

    @permission
    def positionRisk(
            self,
            timestamp: int,
            symbol: Optional[str] = None,
            recvWindow: Optional[int] = None
    ) -> dict:
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
        ).json()

    @permission
    def openOrders(
            self,
            timestamp: int,
            symbol: Optional[str] = None,
            recvWindow: Optional[int] = None
    ) -> dict:
        params: dict = {
            'timestamp': timestamp
        }
        params.update({'signature': self._signature(params)})
        if symbol:
            params.update({'symbol': symbol})
        if recvWindow:
            params.update({'recvWindow': recvWindow})

        return self._r(
            method=self._GET,
            url='/fapi/v1/openOrders',
            params=params,
            headers=self._header()
        ).json()
