import datetime
import requests

from c3d3.domain.d3.adhoc.erc20.adhoc import ERC20TokenContract
from c3d3.domain.d3.wrappers.quickswap.v3.pool.wrapper import QuickSwapV3AlgebraPoolContract
from c3d3.infrastructure.d3.interfaces.dex_screener.interface import iDexScreenerHandler

from web3.middleware import geth_poa_middleware
from web3._utils.events import get_event_data
from web3 import Web3
from web3.exceptions import MismatchedABI, TransactionNotFound


class QuickSwapV3DexScreenerHandler(QuickSwapV3AlgebraPoolContract, iDexScreenerHandler):
    _FEE = None

    def __str__(self):
        return __class__.__name__

    def __init__(
            self,
            uri: str, api_key: str, chain: str,
            start_time: datetime.datetime, end_time: datetime.datetime,
            is_reverse: bool,
            *args, **kwargs
    ) -> None:
        QuickSwapV3AlgebraPoolContract.__init__(self, *args, **kwargs)
        iDexScreenerHandler.__init__(self, uri=uri, api_key=api_key, chain=chain, start_time=start_time, end_time=end_time, is_reverse=is_reverse, *args, **kwargs)

    def do(self):
        r_start = requests.get(self.api_uri.format(timestamp=int(self.start.timestamp()))).json()['result']
        r_end = requests.get(self.api_uri.format(timestamp=int(self.end.timestamp()))).json()['result']
        start_block = int(r_start)
        end_block = int(r_end)

        w3 = Web3(self.node)
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

        event_swap, event_codec, event_abi = self.contract.events.Swap, self.contract.events.Swap.web3.codec, self.contract.events.Swap._get_event_abi()

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
                sqrt_p, liquidity = event_data['args']['price'], event_data['args']['liquidity']

                a0, a1 = event_data['args']['amount0'], event_data['args']['amount1']
                try:
                    receipt = w3.eth.get_transaction_receipt(event_data['transactionHash'].hex())
                except TransactionNotFound:
                    continue

                for log in receipt['logs']:
                    if log['topics'][0].hex() == '0x598b9f043c813aa6be3426ca60d1c65d17256312890be5118dab55b0775ebe2a':
                        self._FEE = int(log['data'], 16) / 10 ** 6
                        break
                else:
                    continue
                a0, a1 = a0 if not self.is_reverse else a1, a1 if not self.is_reverse else a0
                try:
                    price = abs((a1 / 10 ** t1_decimals) / (a0 / 10 ** t0_decimals))
                    recipient = receipt['to']
                except (ZeroDivisionError, KeyError):
                    continue

                overview.append(
                    {
                        'symbol': pool_symbol,
                        'price': price,
                        'sender': receipt['from'],
                        'recipient': recipient,
                        'amount0': a0,
                        'amount1': a1,
                        'decimals0': t0_decimals,
                        'decimals1': t1_decimals,
                        'sqrt_p': sqrt_p,
                        'liquidity': liquidity,
                        'fee': self._FEE,
                        'gas_used': receipt['gasUsed'],
                        'gas_symbol': self.chain.NATIVE_TOKEN,
                        'effective_gas_price': receipt['effectiveGasPrice'] / 10 ** 18,
                        'index_position_in_the_block': receipt['transactionIndex'],
                        'tx_hash': event_data['transactionHash'].hex(),
                        'time': datetime.datetime.utcfromtimestamp(ts)
                    }
                )
        return overview