from typing import final
import requests

from c3d3.core.decorators.classproperty.decorator import classproperty
from c3d3.core.decorators.camel2snake.decorator import camel2snake


class Optimism:

    BLOCK_LIMIT = 3000
    NATIVE_TOKEN = 'ETH'
    API_ENDPOINT = 'https://api-optimistic.etherscan.io/api'

    def __str__(self) -> str:
        return __class__.__name__

    @final
    @classproperty
    @camel2snake
    def name(self) -> str:
        return self.__str__(self)

    @classmethod
    def get_block_by_ts(cls, ts: int, api_key: str) -> str:
        return requests.get(cls.API_ENDPOINT + f'?module=block&action=getblocknobytime&timestamp={ts}&closest=before&apikey=' + api_key).json()['result']

