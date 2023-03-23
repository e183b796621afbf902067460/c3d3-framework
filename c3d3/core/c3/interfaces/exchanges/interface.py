from typing import Dict, Any, Optional, overload, final
from abc import ABC
import builtins

import requests as r


class iCBE(ABC):
    _ENDPOINT, _HEARTBEAT = None, None

    __ENDPOINT_KEY, __API_KEY, __SECRET_KEY, __HEARTBEAT_KEY, __PROXIES_KEY = 'endpoint', 'api_key', 'secret_key', 'heartbeat_endpoint', 'proxies'
    _GET, _POST, _DELETE, _PUT = 'get', 'post', 'delete', 'put'

    def __init__(self, api: Optional[str] = None, secret: Optional[str] = None, *args, **kwargs) -> None:
        self._api_key, self._secret_key = api, secret

        self._proxies = kwargs.get(self.__PROXIES_KEY) if kwargs.get(self.__PROXIES_KEY) else dict()

        self.builder.build(
            key=self.__ENDPOINT_KEY, value=self.endpoint
        ).build(
            key=self.__API_KEY, value=self.api_key
        ).build(
            key=self.__SECRET_KEY, value=self.secret_key
        ).build(
            key=self.__HEARTBEAT_KEY, value=self.heartbeat
        ).connect()

    @final
    def _r(
            self,
            method: str, url: str,
            params: Optional[dict] = None,
            headers: Optional[dict] = None
    ):
        if method == self._GET:
            return r.get(self.endpoint + url, params=params, headers=headers, proxies=self._proxies)
        elif method == self._POST:
            return r.post(self.endpoint + url, data=params, headers=headers, proxies=self._proxies)
        elif method == self._DELETE:
            return r.delete(self.endpoint + url, data=params, headers=headers, proxies=self._proxies)
        elif method == self._PUT:
            return r.put(self.endpoint + url, data=params, headers=headers, proxies=self._proxies)
        raise ConnectionError('Wrong method.')

    @property
    def endpoint(self) -> str:
        return self._ENDPOINT

    @property
    def heartbeat(self) -> str:
        return self._HEARTBEAT

    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def secret_key(self) -> str:
        return self._secret_key

    @final
    def _validate_response(self, r: r.Response) -> bool:
        return r.status_code == 200

    class Builder:

        __TIMEOUT: int = 16

        def __init__(self, *args, **kwargs) -> None:
            self._options: Dict[str, Any] = dict()

            self.cls, self.__ENDPOINT_KEY, self.__API_KEY, self.__SECRET_KEY, self.__HEARTBEAT_KEY = args

        @overload
        def build(self, params: Dict[str, Any]) -> "iCBE.Builder":
            ...

        @overload
        def build(self, key: str, value: Any) -> "iCBE.Builder":
            ...

        @final
        def build(
                self,
                key: Optional[str] = None,
                value: Optional[str] = None,
                params: Optional[Dict[str, Any]] = None
        ) -> "iCBE.Builder":

            def validate(k: str, v: Any) -> None:
                if k == self.__ENDPOINT_KEY:
                    if not isinstance(v, str):
                        raise TypeError('Endpoint is not string.')
                    if not v.startswith('https:') and not v.startswith('http:'):
                        raise r.HTTPError("Set valid endpoint.")
                if k == self.__HEARTBEAT_KEY:
                    if not isinstance(v, str):
                        raise TypeError('Heartbeat endpoint is not string.')
                elif k == self.__API_KEY:
                    if not isinstance(v, str):
                        if v is not None:
                            raise TypeError("Invalid API key.")
                elif k == self.__SECRET_KEY:
                    if not isinstance(v, str):
                        if v is not None:
                            raise TypeError("Invalid Secret key.")

            if isinstance(params, dict):
                for k, v in params.items():
                    validate(k=k, v=v)
                    self._options[k] = v
            elif isinstance(key, str):
                validate(k=key, v=value)
                self._options[key] = value
            return self

        def connect(self):
            try:
                status = r.get(self._options[self.__ENDPOINT_KEY] + self._options[self.__HEARTBEAT_KEY], timeout=self.__TIMEOUT).status_code
            except KeyError:
                raise TypeError('Set valid ping or endpoint parameter.')
            except r.ReadTimeout:
                builtins.print(f'Read timeout {self.__init__.__name__} in {self.cls.__class__.__name__}.')
            except r.ConnectionError:
                builtins.print(f'Broken {self.__init__.__name__} in {self.cls.__class__.__name__}.')
            return self

    @property
    def builder(self):
        return self.Builder(self, self.__ENDPOINT_KEY, self.__API_KEY, self.__SECRET_KEY, self.__HEARTBEAT_KEY)
