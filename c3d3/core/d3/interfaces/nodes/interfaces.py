from typing import Dict, Any, Optional, overload, final
from abc import ABC
from urllib import parse

from web3.providers.rpc import HTTPProvider
from web3.providers.base import BaseProvider
from web3.exceptions import ValidationError, CannotHandleRequest


class iCBN(ABC):

    __PROTOCOL_KEY, __URI_KEY, __PROVIDER_KEY = 'protocol', 'uri', 'provider'

    def __init__(self, protocol: str, uri: str) -> None:
        self._uri, self._protocol = uri, protocol

        self._provider = self.provider = ...

    @property
    def provider(self) -> BaseProvider:
        return self._provider

    @provider.setter
    def provider(self, *args, **kwargs) -> None:
        self._provider = self.builder\
            .build(key=self.__PROTOCOL_KEY, value=self._protocol)\
            .build(key=self.__URI_KEY, value=self._uri)\
            .connect()\
            .construct()

    class Builder:
        def __init__(self, *args, **kwargs) -> None:
            self._options: Dict[str, Any] = dict()

            self.__PROTOCOL_KEY, self.__URI_KEY, self.__PROVIDER_KEY = args

        @overload
        def build(self, params: Dict[str, Any]) -> "iCBN.Builder":
            ...

        @overload
        def build(self, key: str, value: str) -> "iCBN.Builder":
            ...

        @final
        def build(
                self,
                key: Optional[str] = None,
                value: Optional[str] = None,
                params: Optional[Dict[str, Any]] = None
        ) -> "iCBN.Builder":

            def validate(k: str, v: str) -> None:
                if k == self.__PROTOCOL_KEY:
                    if v.lower() not in ('http', 'https', 'websocket', 'wss'):
                        raise ValidationError("Invalid protocol.")
                elif k == self.__URI_KEY:
                    if parse.urlparse(v).scheme not in ('https', 'http', 'wss'):
                        raise ValidationError("Invalid uri.")

            if isinstance(params, dict):
                for k, v in params.items():
                    validate(k=k, v=v)
                    self._options[k] = v
            elif isinstance(key, str) and isinstance(value, str):
                validate(k=key, v=value)
                self._options[key] = value
            return self

        @final
        def connect(self) -> "iCBN.Builder":
            protocol = self._options.get(self.__PROTOCOL_KEY)
            if protocol in ('http', 'https'):
                http = HTTPProvider(endpoint_uri=self._options.get(self.__URI_KEY))
                if http.isConnected():
                    self._options[self.__PROVIDER_KEY] = http
                else:
                    raise CannotHandleRequest("HTTP provider is down.")
            if protocol in ('wss', 'websocket'):
                ...
            return self

        @final
        def construct(self) -> BaseProvider:
            return self._options[self.__PROVIDER_KEY]

    @property
    def builder(self) -> Builder:
        return self.Builder(self.__PROTOCOL_KEY, self.__URI_KEY, self.__PROVIDER_KEY)
