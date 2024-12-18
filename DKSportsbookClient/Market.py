from dataclasses import dataclass
from typing import Self

from .DKSportsbookClientBase import DKSportsbookClientBase
from .Selection import Selection

@dataclass
class Market(DKSportsbookClientBase):
    id: str
    event_id: int
    market_type: str
    name: str
    selections: list[Selection]

    @staticmethod
    def from_dict(market_dict: dict, selection_list: list[Selection]) -> Self:
        return Market(market_dict.get('id'), market_dict.get('event_id'), market_dict.get('marketType').get('name'), market_dict.get('name'), [selection for selection in selection_list if selection.get('marketId') == market_dict.get('id')])
    
    @staticmethod
    def from_list(market_list: list[dict], selection_list: list[Selection]) -> list[Self]:
        return [Market.from_dict(market_list_item, selection_list) for market_list_item in market_list]