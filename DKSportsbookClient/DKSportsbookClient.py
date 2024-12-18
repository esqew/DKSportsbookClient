from .DKSportsbookClientBase import DKSportsbookClientBase
from .Sport import Sport
from .League import League

class DKSportsbookClient(DKSportsbookClientBase):
    sports: list[Sport]

    def __init__(self, **kwargs) -> None:
        super().__init__()

        if not DKSportsbookClientBase._initialized:
            DKSportsbookClientBase._initialize()

        self.sports = Sport.from_list(DKSportsbookClientBase.sports)

    def sport(self, sport_name: str) -> Sport | None:
        """ Retrieves a Sport object by the name of the sport """
        results = [sport for sport in self.sports if sport.name == sport_name]
        if len(results) > 0:
            return next(results)
        else:
            return None
        
    def league(self, league_name: str) -> League | None:
        """ Retrieves the League object for the correspondingly-named league """
        results = [league for sport in self.sports for league in sport.leagues if league.name == league_name]
        if len(results) > 0:
            return results[0]
        else:
            return None
    