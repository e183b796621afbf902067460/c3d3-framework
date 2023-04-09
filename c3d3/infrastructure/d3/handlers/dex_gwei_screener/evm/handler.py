from c3d3.infrastructure.d3.interfaces.dex_gwei_screener.interface import iDexGweiScreenerHandler
from c3d3.infrastructure.trad3r.root.root import TraderRoot
from c3d3.core.decorators.to_dataframe.decorator import to_dataframe
from c3d3.domain.d3.adhoc.nodes.http.adhoc import HTTPNode

from web3 import Web3
import datetime


class EVMDexGweiScreenerHandler(iDexGweiScreenerHandler):

    def __str__(self):
        return __class__.__name__

    def __init__(self, chain: str, wallet_address: str, label: str, node: HTTPNode, *args, **kwargs):
        iDexGweiScreenerHandler.__init__(self, chain=chain, wallet_address=wallet_address, label=label)
        self._node = node

    @property
    def provider(self):
        return self._node.provider

    @to_dataframe
    def do(self):
        overview, now = list(), datetime.datetime.utcnow()
        wallet_address = Web3.to_checksum_address(value=self.wallet_address)

        balance = Web3(self.provider).eth.get_balance(self.wallet_address) / 10 ** 18
        overview.append(
            {
                self._CHAIN_NAME_COLUMN: self.chain.name,
                self._WALLET_ADDRESS_COLUMN: wallet_address,
                self._LABEL_COLUMN: self.label,
                self._SYMBOL_COLUMN: self.chain.NATIVE_TOKEN,
                self._CURRENT_PRICE_COLUMN: TraderRoot.get_price(a=self.chain.NATIVE_TOKEN),
                self._QTY_COLUMN: balance,
                self._TS_COLUMN: now
            }
        )
        return overview
