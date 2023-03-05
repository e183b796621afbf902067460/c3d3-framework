from typing import Optional

from c3d3.core.c3.interfaces.exchanges.interface import iCBE


class GateIOSpotExchange(iCBE):
    _ENDPOINT, _HEARTBEAT = "https://api.gateio.ws", ''

    def tickers(
            self,
            currency_pair: Optional[str] = None,
            timezone: Optional[str] = None
    ) -> list:
        params = dict()
        if currency_pair:
            params.update({'currency_pair': currency_pair})
        if timezone:
            params.update({'timezone': timezone})
        return self._r(
            method=self._GET,
            url='/api/v4/spot/tickers',
            params=params
        ).json()
