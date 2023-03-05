from typing import TypeVar
from c3d3.infrastructure.trad3r.interfaces.leaf.interface import iTraderLeaf


TraderLeaf = TypeVar('TraderLeaf', bound=iTraderLeaf)
