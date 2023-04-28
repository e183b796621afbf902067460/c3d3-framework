from c3d3.domain.d3.adhoc.chains.ethereum.chain import Ethereum


class Arbitrum(Ethereum):

    BLOCK_LIMIT = 12000
    NATIVE_TOKEN = 'ETH'
    API_ENDPOINT = 'https://api.arbiscan.io/api'

    def __str__(self) -> str:
        return __class__.__name__
