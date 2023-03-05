from typing import Optional

from c3d3.core.c3.interfaces.exchanges.interface import iCBE


class CoinGeckoV3Exchange(iCBE):
    _ENDPOINT, _HEARTBEAT = "https://api.coingecko.com", '/ping'

    def simplePrice(
            self,
            ids: str,
            vs_currencies: str,
            include_market_cap: Optional[bool] = None,
            include_24hr_vol: Optional[bool] = None,
            include_24hr_change: Optional[bool] = None,
            include_last_updated_at: Optional[bool] = None,
            precision: Optional[int] = None
            ) -> dict:
        params: dict = {
            'ids': ids,
            'vs_currencies': vs_currencies
        }
        if include_market_cap:
            params.update({'include_market_cap': include_market_cap})
        if include_24hr_vol:
            params.update({'include_24hr_vol': include_24hr_vol})
        if include_24hr_change:
            params.update({'include_24hr_change': include_24hr_change})
        if include_last_updated_at:
            params.update({'include_last_updated_at': include_last_updated_at})
        if precision:
            params.update({'precision': precision})
        return self._r(
            method=self._GET,
            url='/simple/price',
            params=params
        ).json()
