from c3d3.domain.d3.adhoc.chains.ethereum.chain import Ethereum


class Bsc(Ethereum):

    BLOCK_LIMIT = 3000
    NATIVE_TOKEN = 'BNB'
    API_ENDPOINT = 'https://api.bscscan.com/api'

    def __str__(self) -> str:
        return __class__.__name__
