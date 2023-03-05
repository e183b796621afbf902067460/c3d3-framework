from c3d3.core.d3.interfaces.nodes.interface import iCBN


class HTTPNode(iCBN):

    __NODE_KEY = 'http'

    def __init__(self, uri: str) -> None:
        super().__init__(protocol=self.__NODE_KEY, uri=uri)
