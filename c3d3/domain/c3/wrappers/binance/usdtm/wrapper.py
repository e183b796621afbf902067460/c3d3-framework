from typing import Optional, List
import hmac
import hashlib
from urllib.parse import urlencode

from c3d3.core.c3.interfaces.exchanges.interface import iCBE
from c3d3.core.decorators.permission.decorator import permission


class BinanceUSDTmExchange(iCBE):
    _ENDPOINT, _HEARTBEAT = 'https://fapi.binance.com', '/fapi/v1/ping'

    __X_MBX_KEY = 'X-MBX-APIKEY'

    def __signature(self, params: dict):
        return hmac.new(self.secret_key.encode('utf-8'), urlencode(params).replace('%40', '@').encode('utf-8'), hashlib.sha256).hexdigest()

    def __header(self) -> dict:
        return {self.__X_MBX_KEY: self.api_key}

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
        params.update({'signature': self.__signature(params)})

        return self._r(
            method=self._GET,
            url='/fapi/v2/account',
            params=params,
            headers=self.__header()
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
        params.update({'signature': self.__signature(params)})

        return self._r(
            method=self._GET,
            url='/fapi/v2/positionRisk',
            params=params,
            headers=self.__header()
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
        params.update({'signature': self.__signature(params)})
        if symbol:
            params.update({'symbol': symbol})
        if recvWindow:
            params.update({'recvWindow': recvWindow})

        return self._r(
            method=self._GET,
            url='/fapi/v1/openOrders',
            params=params,
            headers=self.__header()
        ).json()
