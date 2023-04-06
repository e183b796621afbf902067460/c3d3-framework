from c3d3.infrastructure.d3.interfaces.dex_supply_screener.interface import iDexSupplyScreenerHandler
from c3d3.domain.d3.adhoc.chains.optimism.chain import Optimism
from c3d3.domain.d3.adhoc.chains.polygon.chain import Polygon
from c3d3.core.decorators.to_dataframe.decorator import to_dataframe
from c3d3.domain.d3.wrappers.aave.v3.pool.wrapper import AAveLendingPoolV3Contract
from c3d3.domain.d3.adhoc.erc20.adhoc import ERC20TokenContract
from c3d3.infrastructure.trad3r.root.root import TraderRoot

from web3 import Web3
from web3.exceptions import BadFunctionCallOutput
import datetime


class AAveV3DexSupplyScreenerHandler(ERC20TokenContract, iDexSupplyScreenerHandler):

    def __str__(self):
        return __class__.__name__

    def __init__(
            self,
            chain: str,
            wallet_address: str,
            label: str,
            *args, **kwargs
    ):
        ERC20TokenContract.__init__(self, *args, **kwargs)
        iDexSupplyScreenerHandler.__init__(self, chain=chain, wallet_address=wallet_address, label=label)

    _lending_pools = {
        Polygon.name: Web3.to_checksum_address('0x794a61358D6845594F94dc1DB02A252b5b4814aD'),
        Optimism.name: Web3.to_checksum_address('0x794a61358D6845594F94dc1DB02A252b5b4814aD')
    }

    def _lending_pool(self):
        return AAveLendingPoolV3Contract(address=self._lending_pools[self.chain.name], node=self.node)

    @to_dataframe
    def do(self):
        overview, address, now = list(), Web3.to_checksum_address(value=self.wallet_address), datetime.datetime.now()

        pool = self._lending_pool()

        reserve_token_symbol = self.symbol()
        reserve_token_price = TraderRoot.get_price(a=reserve_token_symbol)

        user_configuration: str = bin(pool.getUserConfiguration(address=address)[0])[2:]
        reserves_list: list = pool.getReservesList()
        for i, mask in enumerate(user_configuration[::-1]):
            reserve_token_address: str = reserves_list[i // 2]
            if reserve_token_address != self.contract.address:
                continue
            try:
                reserve_data: tuple = pool.getReserveData(asset=reserve_token_address)
            except BadFunctionCallOutput:
                continue
            if mask == '1' and i % 2:
                a_token_address: str = reserve_data[8]
                a_token: ERC20TokenContract = ERC20TokenContract(address=a_token_address, node=self.node)
                a_token_decimals: int = a_token.decimals()
                collateral: int = a_token.balanceOf(address=address) / 10 ** a_token_decimals

                a_overview = {
                    self._CHAIN_NAME_COLUMN: self.chain.name,
                    self._WALLET_ADDRESS_COLUMN: self.wallet_address,
                    self._PROTOCOL_NAME_COLUMN: self.key,
                    self._LABEL_COLUMN: self.label,
                    self._SYMBOL_COLUMN: reserve_token_symbol,
                    self._CURRENT_PRICE_COLUMN: reserve_token_price,
                    self._QTY_COLUMN: collateral,
                    self._TS_COLUMN: now
                }
                overview.append(a_overview)
        if not overview:
            overview.append(
                {
                    self._CHAIN_NAME_COLUMN: self.chain.name,
                    self._WALLET_ADDRESS_COLUMN: self.wallet_address,
                    self._PROTOCOL_NAME_COLUMN: self.key,
                    self._LABEL_COLUMN: self.label,
                    self._SYMBOL_COLUMN: reserve_token_symbol,
                    self._CURRENT_PRICE_COLUMN: reserve_token_price,
                    self._QTY_COLUMN: None,
                    self._TS_COLUMN: now
                }
            )
        return overview
