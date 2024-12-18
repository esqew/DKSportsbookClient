from dataclasses import dataclass, field
from typing import Self
import requests

from .DKSportsbookClientBase import DKSportsbookClientBase
from .Event import Event

@dataclass
class League(DKSportsbookClientBase):
    """ Representation of a League (referred to internally as an "eventGroup") on DraftKings Sportsbook"""
    name: str
    id: int
    events: list = field(default_factory=list)

    @staticmethod
    def from_dict(league_dict: dict) -> Self:
        return League(league_dict.get('eventGroupName'), league_dict.get('eventGroupId'))
        
    @staticmethod
    def from_list(league_list: list[dict]) -> list[Self]:
        return [League.from_dict(league) for league in league_list]
        
    def get_events(self) -> list[Event] | None:
        endpoint = f'{DKSportsbookClientBase.sports_content_base_url}v1/leagues/{self.id}'
        self.events = Event.from_list(DKSportsbookClientBase._http_client.get(endpoint).json()['events'])
        return self.events