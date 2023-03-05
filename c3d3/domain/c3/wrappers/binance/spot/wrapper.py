from typing import Optional, List
import hmac
import hashlib
from urllib.parse import urlencode
from requests import Response

from c3d3.core.c3.interfaces.exchanges.interface import iCBE
from c3d3.core.decorators.permission.decorator import permission


class BinanceSpotExchange(iCBE):
    _ENDPOINT, _HEARTBEAT = 'https://api.binance.com', '/api/v3/ping'

    _X_MBX_KEY = 'X-MBX-APIKEY'

    def _signature(self, params: dict):
        return hmac.new(self.secret_key.encode('utf-8'), urlencode(params).replace('%40', '@').encode('utf-8'), hashlib.sha256).hexdigest()

    def _header(self) -> dict:
        return {self._X_MBX_KEY: self.api_key}

    def tickerPrice(self, symbol: Optional[str] = None, symbols: Optional[List[str]] = None) -> Response:
        params: dict = {'symbol': symbol} if symbol else {'symbols': symbols}
        return self._r(method=self._GET, url='/api/v3/ticker/price', params=params)

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
        return self._r(method=self._GET, url='/api/v3/aggTrades', params=params)

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
            url='/api/v3/account',
            params=params,
            headers=self._header()
        )
