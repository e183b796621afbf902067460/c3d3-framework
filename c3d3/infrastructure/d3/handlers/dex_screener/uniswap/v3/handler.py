from c3d3.infrastructure.d3.interfaces.dex_screener.interface import iDexScreenerHandler
from c3d3.domain.d3.adhoc.chains.optimism.chain import Optimism
from c3d3.domain.d3.wrappers.uniswap.v3.pool.wrapper import UniSwapV3PoolContract
from c3d3.infrastructure.trad3r.root.root import TraderRoot

import datetime
import requests

from web3.middleware import geth_poa_middleware
from web3._utils.events import get_event_data
from web3 import Web3
from web3.exceptions import MismatchedABI, TransactionNotFound


class UniSwapV3DexScreenerHandler(UniSwapV3PoolContract, iDexScreenerHandler):
    _FEE, _VERSION = None, 'v3'

    def __str__(self):
        return __class__.__name__

    def __init__(
            self,
            api_key: str, chain: str,
            start_time: datetime.datetime, end_time: datetime.datetime,
            is_reverse: bool,
            *args, **kwargs
    ) -> None:
        UniSwapV3PoolContract.__init__(self, *args, **kwargs)
        iDexScreenerHandler.__init__(self, api_key=api_key, chain=chain, start_time=start_time, end_time=end_time, is_reverse=is_reverse, *args, **kwargs)

    def do(self):
        r_start = self.chain.get_block_by_ts(ts=int(self.start.timestamp()), api_key=self.api_key)
        r_end = self.chain.get_block_by_ts(ts=int(self.end.timestamp()), api_key=self.api_key)

        start_block = int(r_start)
        end_block = int(r_end)

        w3 = Web3(self.provider)
        w3.middleware_onion.inject(
            geth_poa_middleware,
            layer=0
        )
        self._FEE = self.fee() / 10 ** 6

        t0, t1 = self.token0(), self.token1()
        t0, t1 = t0 if not self.is_reverse else t1, t1 if not self.is_reverse else t0

        t0_decimals, t1_decimals = t0.decimals(), t1.decimals()
        pool_symbol = f'{t0.symbol()}/{t1.symbol()}'

        event_swap, event_codec, event_abi = self.contract.events.Swap, self.contract.events.Swap.w3.codec, self.contract.events.Swap._get_event_abi()

        overview = list()
        while start_block < end_block:
            events = w3.eth.get_logs(
                {
                    'fromBlock': start_block,
                    'toBlock': start_block + self.chain.BLOCK_LIMIT,
                    'address': self.contract.address
                }
            )
            start_block += self.chain.BLOCK_LIMIT
            for event in events:
                try:
                    event_data = get_event_data(
                        abi_codec=event_codec,
                        event_abi=event_abi,
                        log_entry=event
                    )
                except MismatchedABI:
                    continue
                ts = w3.eth.get_block(event_data['blockNumber']).timestamp
                if ts > self.end.timestamp():
                    break
                sqrt_p, liquidity = event_data['args']['sqrtPriceX96'], event_data['args']['liquidity']

                a0 = event_data['args']['amount0'] if not self.is_reverse else event_data['args']['amount1']
                a1 = event_data['args']['amount1'] if not self.is_reverse else event_data['args']['amount0']

                try:
                    price = abs((a1 / 10 ** t1_decimals) / (a0 / 10 ** t0_decimals))
                    receipt = w3.eth.get_transaction_receipt(event_data['transactionHash'].hex())
                    tx = w3.eth.get_transaction(event_data['transactionHash'])
                    recipient = receipt['to']
                except (TransactionNotFound, ZeroDivisionError, KeyError):
                    continue
                overview.append(
                    {
                        self._CHAIN_NAME_COLUMN: self.chain.name,
                        self._POOL_ADDRESS_COLUMN: self.contract.address,
                        self._PROTOCOL_NAME_COLUMN: self.key,
                        self._POOL_SYMBOL_COLUMN: pool_symbol,
                        self._TRADE_PRICE_COLUMN: price,
                        self._SENDER_COLUMN: receipt['from'],
                        self._RECIPIENT_COLUMN: recipient,
                        self._AMOUNT0_COLUMN: a0,
                        self._AMOUNT1_COLUMN: a1,
                        self._DECIMALS0_COLUMN: t0_decimals,
                        self._DECIMALS1_COLUMN: t1_decimals,
                        self._SQRT_P_COLUMN: sqrt_p,
                        self._LIQUIDITY_COLUMN: liquidity,
                        self._TRADE_FEE_COLUMN: self._FEE,
                        self._GAS_USED_COLUMN: receipt['gasUsed'] if self.chain.name not in Optimism.name else int(receipt['l1GasUsed'], 16),
                        self._EFFECTIVE_GAS_PRICE_COLUMN: receipt['effectiveGasPrice'] if self.chain.name not in Optimism.name else int(receipt['l1GasPrice'], 16),
                        self._GAS_SYMBOL_COLUMN: self.chain.NATIVE_TOKEN,
                        self._GAS_USD_PRICE_COLUMN: TraderRoot.get_price(self.chain.NATIVE_TOKEN),
                        self._INDEX_POSITION_IN_THE_BLOCK_COLUMN: receipt['transactionIndex'] if self.chain.name not in Optimism.name else int(tx['index'], 16),
                        self._TX_HASH_COLUMN: event_data['transactionHash'].hex(),
                        self._TS_COLUMN: datetime.datetime.utcfromtimestamp(ts)
                    }
                )
        return overview
