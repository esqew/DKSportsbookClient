from dataclasses import dataclass

@dataclass
class Selection:
    id: str
    marketId: str
    label: str
    outcomeType: str
    odds: float
    points: float | None = None
    
    @property
    def american_odds(self) -> str:
        if (self.odds > 2.00):
            return f'+{(self.odds - 1) * 100}'
        else:
            return f'{-100 / (self.odds - 1)}'