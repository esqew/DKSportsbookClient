from dataclasses import dataclass
from typing import Self

@dataclass
class Selection:
    id: str
    market_id: str
    label: str
    outcome_type: str
    odds: float
    points: float | None = None
    
    @property
    def american_odds(self) -> str:
        if (self.odds > 2.00):
            return f'+{(self.odds - 1) * 100}'
        else:
            return f'{-100 / (self.odds - 1)}'
        
    @staticmethod
    def from_dict(selection_dict: dict) -> Self:
        return Selection(selection_dict.get('id'), selection_dict.get('marketId'), selection_dict.get('label'), selection_dict.get('outcome_type'), selection_dict.get('trueOdds'), selection_dict.get('points'))
    
    @staticmethod
    def from_list(selection_list: list[dict]) -> list[Self]:
        return [Selection.from_dict(selection_dict) for selection_dict in selection_list]