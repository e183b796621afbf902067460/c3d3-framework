from typing import TypeVar
from c3d3.core.c3.interfaces.exchanges.interfaces import iCBE


ExchangeType = TypeVar('ExchangeType', bound=iCBE)
