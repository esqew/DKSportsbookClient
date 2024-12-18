from dataclasses import dataclass
from typing import Self

from .DKSportsbookClientBase import DKSportsbookClientBase
from .Market import Market

@dataclass
class Category(DKSportsbookClientBase):
    id: int
    event_id: int
    name: str
    type: str | None = None
    markets: list[Market] | None = None

    @staticmethod
    def from_dict(category_dict: dict, event_id: int) -> Self:
        return Category(category_dict.get('id'), event_id, category_dict.get('name'), category_dict.get('categoryType'))
    
    @staticmethod
    def from_list(category_list: list[dict], event_id: int) -> list[Self]:
        return [Category.from_dict(category_dict, event_id) for category_dict in category_list]
    
    def load_markets(self) -> list[Market]:
        endpoint = f'{DKSportsbookClientBase.sports_content_base_url}v1/events/{self.event_id}/categories/{self.id}'
        response = DKSportsbookClientBase._http_client.get(endpoint).json()
        self.markets = Market.from_list(response['markets'], response['selections'])
        return self.markets