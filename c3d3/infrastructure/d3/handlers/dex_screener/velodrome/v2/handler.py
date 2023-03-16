from c3d3.domain.d3.wrappers.velodrome.v2.pool.wrapper import VelodromePairV2Contract
from c3d3.domain.d3.wrappers.velodrome.v2.factory.wrapper import VelodromePairFactoryV2Contract
from c3d3.domain.d3.adhoc.chains.optimism.chain import Optimism
from c3d3.infrastructure.d3.interfaces.dex_screener.interface import iDexScreenerHandler
from c3d3.infrastructure.trad3r.root.root import TraderRoot
from c3d3.core.decorators.to_dataframe.decorator import to_dataframe

import datetime
import requests

from web3.middleware import geth_poa_middleware
from web3._utils.events import get_event_data
from web3.logs import DISCARD
from web3 import Web3
from web3.exceptions import MismatchedABI, TransactionNotFound


class VelodromeV2DexScreenerHandler(VelodromePairV2Contract, iDexScreenerHandler):
    _FEE, _VERSION = None, 'v2'

    _factories = {
        Optimism.name: Web3.to_checksum_address('0x25CbdDb98b35ab1FF77413456B31EC81A6B6B746')
    }

    def __str__(self):
        return __class__.__name__

    def __init__(
            self,
            api_key: str, chain: str,
            start_time: datetime.datetime, end_time: datetime.datetime,
            is_reverse: bool, is_child: bool = False,
            *args, **kwargs
    ) -> None:
        if not is_child:
            VelodromePairV2Contract.__init__(self, *args, **kwargs)
        iDexScreenerHandler.__init__(self, api_key=api_key, chain=chain, start_time=start_time, end_time=end_time, is_reverse=is_reverse, *args, **kwargs)

    def _factory(self):
        return VelodromePairFactoryV2Contract(self._factories[self.chain.name], self.node)

    @to_dataframe
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

        factory = self._factory()
        self._FEE = factory.getFee(isStable=self.stable()) / 10 ** 4

        t0, t1 = self.token0(), self.token1()
        t0, t1 = t0 if not self.is_reverse else t1, t1 if not self.is_reverse else t0

        t0_decimals, t1_decimals = t0.decimals(), t1.decimals()
        pool_symbol = f'{t0.symbol()}/{t1.symbol()}'

        event_swap, event_codec, event_abi = self.contract.events.Sync, self.contract.events.Sync.web3.codec, self.contract.events.Sync._get_event_abi()
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
                r0, r1 = event_data['args']['reserve0'], event_data['args']['reserve1']
                r0, r1 = r0 if not self.is_reverse else r1, r1 if not self.is_reverse else r0

                try:
                    receipt = w3.eth.get_transaction_receipt(event_data['transactionHash'].hex())
                    tx = w3.eth.get_transaction(event_data['transactionHash'])
                except TransactionNotFound:
                    continue

                transfers = self.contract.events.Swap().processReceipt(receipt, errors=DISCARD)
                amount0, amount1 = None, None
                for transfer in transfers:
                    if transfer['address'] == self.contract.address:
                        amount0 = transfer['args']['amount0In'] if transfer['args']['amount0In'] else transfer['args']['amount0Out'] * -1
                        amount1 = transfer['args']['amount1In'] if transfer['args']['amount1In'] else transfer['args']['amount1Out'] * -1
                        break
                if not amount0 or not amount1:
                    continue
                amount0, amount1 = amount0 if not self.is_reverse else amount1, amount1 if not self.is_reverse else amount0
                try:
                    price = abs((amount1 / 10 ** t1_decimals) / (amount0 / 10 ** t0_decimals))
                    recipient = receipt['to']
                except (ZeroDivisionError, KeyError):
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
                        self._RESERVE0_COLUMN: r0,
                        self._RESERVE1_COLUMN: r1,
                        self._AMOUNT0_COLUMN: amount0,
                        self._AMOUNT1_COLUMN: amount1,
                        self._DECIMALS0_COLUMN: t0_decimals,
                        self._DECIMALS1_COLUMN: t1_decimals,
                        self._TRADE_FEE_COLUMN: self._FEE,
                        self._GAS_USED_COLUMN: receipt['gasUsed'] if self.chain.name != Optimism.name else int(receipt['l1GasUsed'], 16),
                        self._EFFECTIVE_GAS_PRICE_COLUMN: receipt['effectiveGasPrice'] if self.chain.name != Optimism.name else int(receipt['l1GasPrice'], 16),
                        self._GAS_SYMBOL_COLUMN: self.chain.NATIVE_TOKEN,
                        self._GAS_USD_PRICE_COLUMN: TraderRoot.get_price(self.chain.NATIVE_TOKEN),
                        self._INDEX_POSITION_IN_THE_BLOCK_COLUMN: receipt['transactionIndex'] if self.chain.name != Optimism.name else int(tx['index'], 16),
                        self._TX_HASH_COLUMN: event_data['transactionHash'].hex(),
                        self._TS_COLUMN: datetime.datetime.utcfromtimestamp(ts)
                    }
                )
        return overview
