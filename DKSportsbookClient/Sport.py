from dataclasses import dataclass, field
from .League import League
from typing import List, Self

@dataclass
class Sport:
    name: str
    id: int
    leagues: List[League] = field(default_factory=list)

    @staticmethod
    def from_dict(sport_dict: dict) -> Self:
        return Sport(sport_dict.get('displayName', sport_dict.get('nameIdentifier')), sport_dict.get('displayGroupId'), League.from_list(sport_dict.get('eventGroupInfos')))
    
    @staticmethod
    def from_list(sport_list: list[dict]) -> list[Self]:
        return [Sport.from_dict(sport) for sport in sport_list]