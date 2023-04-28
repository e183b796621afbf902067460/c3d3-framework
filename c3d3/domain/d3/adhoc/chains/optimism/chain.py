from c3d3.domain.d3.adhoc.chains.ethereum.chain import Ethereum


class Optimism(Ethereum):

    BLOCK_LIMIT = 3000
    NATIVE_TOKEN = 'ETH'
    API_ENDPOINT = 'https://api-optimistic.etherscan.io/api'

    def __str__(self) -> str:
        return __class__.__name__
