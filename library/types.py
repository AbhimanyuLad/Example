from typing import TypeAlias
from datetime import datetime


Order: TypeAlias = tuple[
    float,     # price
    datetime,   # timestamp
    int|None,       # id
    int,       # user_id
    int,       # resource_id
    int,       # quantity
    int,       # type: 0 = SELL, 1 = BUY
]


Trade: TypeAlias = tuple[
    int, # id
    int, # buy_order_id
    int, # sell_order_id
    int, # quantity
    float, # price
    datetime, # timestamp
]