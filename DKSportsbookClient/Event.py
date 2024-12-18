from dataclasses import dataclass
from typing import Self

from datetime import datetime

from .DKSportsbookClientBase import DKSportsbookClientBase
from .Category import Category

@dataclass
class Event(DKSportsbookClientBase):
    id: int
    name: str
    start_date: datetime
    subscription_key: str | None = None
    categories: list[Category] | None = None

    @staticmethod
    def from_dict(event_dict: dict) -> Self:
        return Event(event_dict.get('id'), event_dict.get('name'), datetime.fromisoformat(event_dict.get('startEventDate')), event_dict.get('subscriptionKey'))
    
    @staticmethod
    def from_list(event_list: list[dict]) -> list[Self]:
        return [Event.from_dict(event_dict) for event_dict in event_list]
    
    def get_categories(self) -> list[Category]:
        endpoint = f'{DKSportsbookClientBase.sports_content_base_url}v1/events/{self.id}/categories'
        self.categories = Category.from_list(DKSportsbookClientBase._http_client.get(endpoint).json()['events'][0]['categories'], self.id)
        return self.categories