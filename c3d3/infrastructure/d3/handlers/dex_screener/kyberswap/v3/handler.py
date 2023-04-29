from c3d3.domain.d3.wrappers.kyberswap.v3.pool.wrapper import KyberSwapV3PoolContract
from c3d3.infrastructure.d3.interfaces.dex_screener.interface import iDexScreenerHandler
from c3d3.infrastructure.trad3r.root.root import TraderRoot
from c3d3.core.decorators.to_dataframe.decorator import to_dataframe

import datetime

from web3.middleware import geth_poa_middleware
from web3._utils.events import get_event_data
from web3.exceptions import TransactionNotFound
from web3 import Web3
from web3.exceptions import MismatchedABI


class KyberSwapV3DexScreenerHandler(KyberSwapV3PoolContract, iDexScreenerHandler):
    _FEE = None

    def __str__(self):
        return __class__.__name__

    def __init__(
            self,
            api_key: str, chain: str,
            start_time: datetime.datetime, end_time: datetime.datetime,
            is_reverse: bool,
            *args, **kwargs
    ) -> None:
        KyberSwapV3PoolContract.__init__(self, *args, **kwargs)
        iDexScreenerHandler.__init__(self, api_key=api_key, chain=chain, start_time=start_time, end_time=end_time, is_reverse=is_reverse, *args, **kwargs)

    @to_dataframe
    def do(self):
        start_ts, end_ts = self.start.timestamp(), self.end.timestamp()
        r_start = self.chain.get_block_by_ts(ts=int(self.start.timestamp()), api_key=self.api_key)
        r_end = self.chain.get_block_by_ts(ts=int(self.end.timestamp()), api_key=self.api_key)

        start_block = int(r_start)
        end_block = int(r_end)

        w3 = Web3(self.provider)
        w3.middleware_onion.inject(
            geth_poa_middleware,
            layer=0
        )
        self._FEE = self.swapFeeUnits() / 10 ** 5

        t0, t1 = self.token0(), self.token1()
        t0, t1 = t0 if not self.is_reverse else t1, t1 if not self.is_reverse else t0

        t0_decimals, t1_decimals = t0.decimals(), t1.decimals()
        pool_symbol = f'{t0.symbol()}/{t1.symbol()}'

        event_swap, event_codec, event_abi = self.contract.events.Swap, self.contract.events.Swap.w3.codec, self.contract.events.Swap._get_event_abi()

        overview = list()
        logs = self.chain.get_logs(
            address=self.contract.address,
            start_time=self.start,
            end_time=self.end,
            start_block=start_block,
            end_block=end_block,
            api_key=self.api_key
        )
        for log in logs:
            try:
                event_data = get_event_data(
                    abi_codec=event_codec,
                    event_abi=event_abi,
                    log_entry=log
                )
            except MismatchedABI:
                continue
            ts = self.chain.hex2int(log.timeStamp)
            if ts > end_ts:
                break

            sqrt_p, liquidity = event_data['args']['sqrtP'], event_data['args']['liquidity']

            a0, a1 = event_data['args']['deltaQty0'], event_data['args']['deltaQty1']
            a0, a1 = a0 if not self.is_reverse else a1, a1 if not self.is_reverse else a0

            try:
                price = abs((a1 / 10 ** t1_decimals) / (a0 / 10 ** t0_decimals))
            except (TransactionNotFound, ZeroDivisionError, KeyError):
                continue
            overview.append(
                {
                    self._CHAIN_NAME_COLUMN: self.chain.name,
                    self._POOL_ADDRESS_COLUMN: self.contract.address,
                    self._PROTOCOL_NAME_COLUMN: self.key,
                    self._POOL_SYMBOL_COLUMN: pool_symbol,
                    self._TRADE_PRICE_COLUMN: price,
                    self._SENDER_COLUMN: event_data.args.sender,
                    self._RECIPIENT_COLUMN: event_data.args.recipient,
                    self._AMOUNT0_COLUMN: a0,
                    self._AMOUNT1_COLUMN: a1,
                    self._DECIMALS0_COLUMN: t0_decimals,
                    self._DECIMALS1_COLUMN: t1_decimals,
                    self._SQRT_P_COLUMN: sqrt_p,
                    self._LIQUIDITY_COLUMN: liquidity,
                    self._TRADE_FEE_COLUMN: self._FEE,
                    self._GAS_USED_COLUMN: self.chain.hex2int(log['gasUsed']),
                    self._EFFECTIVE_GAS_PRICE_COLUMN: self.chain.hex2int(log['gasPrice']),
                    self._GAS_SYMBOL_COLUMN: self.chain.NATIVE_TOKEN,
                    self._GAS_USD_PRICE_COLUMN: TraderRoot.get_price(self.chain.NATIVE_TOKEN),
                    self._INDEX_POSITION_IN_THE_BLOCK_COLUMN: self.chain.hex2int(log['transactionIndex']),
                    self._TX_HASH_COLUMN: event_data['transactionHash'].hex(),
                    self._TS_COLUMN: datetime.datetime.utcfromtimestamp(ts)
                }
            )
        return overview
