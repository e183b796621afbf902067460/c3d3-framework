from c3d3.domain.d3.adhoc.chains.ethereum.chain import Ethereum


class Polygon(Ethereum):

    BLOCK_LIMIT = 3000
    NATIVE_TOKEN = 'MATIC'
    API_ENDPOINT = 'https://api.polygonscan.com/api'

    def __str__(self) -> str:
        return __class__.__name__
