from typing import final, overload, Dict, Any, Optional
import requests as r

from c3d3.infrastructure.d3.consts.chains.map import ChainMap
from c3d3.infrastructure.abc.handler.abc import iHandler


class iDexScreenerHandler(iHandler):
    _FEE = None

    __URI_KEY, __API_KEY, __CHAIN_KEY = 'uri', 'api_key', 'chain'

    def __str__(self):
        raise NotImplementedError

    def __init__(
            self,
            uri: str, api_key: str, chain: str,
            *args, **kwargs
    ):
        self._uri = uri
        self._api_key = api_key
        self._chain = chain

        self.builder.build(
            key=self.__URI_KEY, value=self._uri
        ).build(
            key=self.__API_KEY, value=self._api_key
        ).build(
            key=self.__CHAIN_KEY, value=self._chain
        )

    @property
    def api_uri(self) -> str:
        return self._uri + 'api?module=block&action=getblocknobytime&timestamp={timestamp}&closest=before&apikey=' + self._api_key

    @property
    def chain(self):
        return ChainMap.get_chain(name=self._chain)

    class Builder:

        def __init__(self, *args, **kwargs) -> None:
            self._options: dict = dict()

            self.__URI_KEY, self.__API_KEY, self.__CHAIN_KEY = args

        @overload
        def build(self, params: Dict[str, Any]) -> "iDexScreenerHandler.Builder":
            ...

        @overload
        def build(self, key: str, value: Any) -> "iDexScreenerHandler.Builder":
            ...

        @final
        def build(
                self,
                key: Optional[str] = None,
                value: Optional[str] = None,
                params: Optional[Dict[str, Any]] = None
        ) -> "iDexScreenerHandler.Builder":

            def validate(k: str, v: Any) -> None:
                if k == self.__URI_KEY:
                    if not isinstance(v, str):
                        raise TypeError('Invalid URI type.')
                    if not v.startswith('https:') and not v.startswith('http:'):
                        raise r.HTTPError("Endpoint must startswith https or http, set valid endpoint.")
                elif k == self.__API_KEY:
                    if not isinstance(v, str):
                        raise TypeError('Set valid API key type.')
                elif k == self.__CHAIN_KEY:
                    if not isinstance(v, str):
                        raise TypeError('Invalid chain-key type.')

            if isinstance(params, dict):
                for k, v in params.items():
                    validate(k=k, v=v)
                    self._options[k] = v
            elif isinstance(key, str):
                validate(k=key, v=value)
                self._options[key] = value
            return self

    @property
    def builder(self):
        return self.Builder(self.__URI_KEY, self.__API_KEY, self.__CHAIN_KEY)

    def do(self):
        raise NotImplementedError
