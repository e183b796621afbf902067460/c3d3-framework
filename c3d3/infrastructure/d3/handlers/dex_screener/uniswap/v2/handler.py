from c3d3.infrastructure.d3.interfaces.dex_screener.interface import iDexScreenerHandler

from c3d3.domain.d3.wrappers.uniswap.v2.pool.wrapper import UniSwapV2PairContract
from c3d3.domain.d3.adhoc.erc20.adhoc import ERC20TokenContract

import datetime
import requests

from web3.middleware import geth_poa_middleware
from web3.logs import DISCARD
from web3._utils.events import get_event_data
from web3 import Web3
from web3.exceptions import MismatchedABI, TransactionNotFound


class UniSwapV2DexScreenerHandler(UniSwapV2PairContract, iDexScreenerHandler):
    _FEE = 0.003

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
            UniSwapV2PairContract.__init__(self, *args, **kwargs)
        iDexScreenerHandler.__init__(self, api_key=api_key, chain=chain, start_time=start_time, end_time=end_time, is_reverse=is_reverse, *args, **kwargs)

    def do(self):
        r_start = requests.get(self.api_uri.format(timestamp=int(self.start.timestamp()))).json()['result']
        r_end = requests.get(self.api_uri.format(timestamp=int(self.end.timestamp()))).json()['result']
        start_block = int(r_start)
        end_block = int(r_end)

        w3 = Web3(self.provider)
        w3.middleware_onion.inject(
            geth_poa_middleware,
            layer=0
        )

        t0_address, t1_address = self.token0(), self.token1()
        t0 = ERC20TokenContract(address=t0_address, node=self.node)
        t1 = ERC20TokenContract(address=t1_address, node=self.node)

        t0_decimals, t1_decimals = t0.decimals(), t1.decimals()
        t0_decimals, t1_decimals = t0_decimals if not self.is_reverse else t1_decimals, t1_decimals if not self.is_reverse else t0_decimals

        t0_symbol, t1_symbol = t0.symbol(), t1.symbol()
        pool_symbol = f'{t0_symbol}/{t1_symbol}' if not self.is_reverse else f'{t1_symbol}/{t0_symbol}'

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
                ts = w3.eth.getBlock(event_data['blockNumber']).timestamp
                if ts > self.end.timestamp():
                    break
                r0, r1 = event_data['args']['reserve0'], event_data['args']['reserve1']
                r0, r1 = r0 if not self.is_reverse else r1, r1 if not self.is_reverse else r0

                try:
                    receipt = w3.eth.get_transaction_receipt(event_data['transactionHash'].hex())
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
                        'symbol': pool_symbol,
                        'price': price,
                        'sender': receipt['from'],
                        'recipient': recipient,
                        'reserve0': r0,
                        'reserve1': r1,
                        'amount0': amount0,
                        'amount1': amount1,
                        'decimals0': t0_decimals,
                        'decimals1': t1_decimals,
                        'fee': self._FEE,
                        'gas_used': receipt['gasUsed'],
                        'effective_gas_price': receipt['effectiveGasPrice'] / 10 ** 18,
                        'gas_symbol': self.chain.NATIVE_TOKEN,
                        'index_position_in_the_block': receipt['transactionIndex'],
                        'tx_hash': event_data['transactionHash'].hex(),
                        'time': datetime.datetime.utcfromtimestamp(ts)
                    }
                )
        return overview
