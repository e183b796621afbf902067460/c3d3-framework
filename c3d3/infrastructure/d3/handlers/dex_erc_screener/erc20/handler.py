from c3d3.domain.d3.adhoc.erc20.adhoc import ERC20TokenContract
from c3d3.infrastructure.d3.interfaces.dex_erc_screener.interface import iDexERCScreenerHandler
from c3d3.infrastructure.trad3r.root.root import TraderRoot
from c3d3.core.decorators.to_dataframe.decorator import to_dataframe

from web3 import Web3
import datetime


class ERC20DexERCScreenerHandler(ERC20TokenContract, iDexERCScreenerHandler):

    def __str__(self):
        return __class__.__name__

    def __init__(self, chain: str, wallet_address: str, label: str, *args, **kwargs):
        ERC20TokenContract.__init__(self, *args, **kwargs)
        iDexERCScreenerHandler.__init__(self, chain=chain, wallet_address=wallet_address, label=label)

    @to_dataframe
    def do(self):
        overview, now = list(), datetime.datetime.utcnow()
        wallet_address = Web3.to_checksum_address(value=self.wallet_address)

        symbol = self.symbol()
        decimals = self.decimals()

        balance = self.balanceOf(address=wallet_address) / 10 ** decimals
        overview.append(
            {
                self._CHAIN_NAME_COLUMN: self.chain.name,
                self._WALLET_ADDRESS_COLUMN: wallet_address,
                self._TOKEN_ADDRESS_COLUMN: self.address,
                self._LABEL_COLUMN: self.label,
                self._SYMBOL_COLUMN: symbol,
                self._CURRENT_PRICE_COLUMN: TraderRoot.get_price(a=symbol),
                self._QTY_COLUMN: balance,
                self._TS_COLUMN: now
            }
        )
        return overview
