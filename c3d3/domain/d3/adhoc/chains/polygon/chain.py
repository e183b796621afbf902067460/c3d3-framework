from typing import final
import requests
import time
import datetime

from c3d3.core.decorators.classproperty.decorator import classproperty
from c3d3.core.decorators.camel2snake.decorator import camel2snake

from web3.types import HexBytes
from web3.datastructures import AttributeDict


class Polygon:

    BLOCK_LIMIT = 3000
    NATIVE_TOKEN = 'MATIC'
    API_ENDPOINT = 'https://api.polygonscan.com/api'

    _LAST_REQ_INT = None
    _REQ_LIMIT = .2

    def __str__(self) -> str:
        return __class__.__name__

    @classmethod
    def _r(cls, q: str, api_key: str):
        if cls._LAST_REQ_INT:
            if time.time() - cls._REQ_LIMIT < cls._LAST_REQ_INT:
                time.sleep(cls._LAST_REQ_INT + cls._REQ_LIMIT - time.time() + .01)

        resp = requests.get(f"{cls.API_ENDPOINT}?{q}&apikey={api_key}").json()
        if resp['status'] == '1':
            return resp['result']
        else:
            ...
        cls._LAST_REQ_INT = time.time()

    @final
    @classproperty
    @camel2snake
    def name(self) -> str:
        return self.__str__(self)

    @classmethod
    def get_block_by_ts(cls, ts: int, api_key: str) -> str:
        return cls._r(
            q=f'?module=block&action=getblocknobytime&timestamp={ts}&closest=before',
            api_key=api_key
        )

    @classmethod
    def get_logs(
            cls,
            address: str,
            start_time: datetime.datetime, end_time: datetime.datetime,
            start_block: int, end_block: int,
            api_key: str
    ):
        logs, offset, timestamp = list(), 1000, end_time.timestamp() - start_time.timestamp()

        parts = int(((end_time - start_time).days * timestamp * 24 + (end_time - start_time).seconds) / timestamp)
        step = int((end_block - start_block) / parts)
        for i in range(parts):
            page = 1
            while True:
                page_logs = cls._r(
                    q=f'module=logs&action=getLogs&address={address}&fromBlock={start_block + i * step}&toBlock={start_block + (i + 1) * step}&page={page}&offset={offset}',
                    api_key=api_key
                )
                logs.extend(page_logs)
                page += 1
                if len(page_logs) < offset:
                    break
        attrs = list()
        for log in logs:
            log['topics'] = [HexBytes(topic) for topic in log['topics']]
            log['data'] = HexBytes(log['data'])
            log['blockHash'] = HexBytes(log['blockHash'])
            log['transactionHash'] = HexBytes(log['transactionHash'])
            attrs.append(AttributeDict(log))
        return attrs

    @classmethod
    def hex2int(cls, source):
        sign_bit_mask = 1 << (len(source) * 4 - 1)
        other_bits_mask = sign_bit_mask - 1
        value = int(source, 16)
        return - (value & sign_bit_mask) | (value & other_bits_mask)
