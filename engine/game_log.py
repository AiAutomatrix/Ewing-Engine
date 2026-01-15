from typing import List, Dict, NamedTuple

class PossessionLog(NamedTuple):
    team: str
    outcome: str
    points: int

class GameLog:
    """
    Represents a single simulated game as a sequence of possessions.
    Disabled by default for performance.
    """
    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.log: List[PossessionLog] = []

    def record(self, team: str, outcome: str, points: int):
        if self.enabled:
            self.log.append(PossessionLog(team, outcome, points))

    def to_dict(self) -> List[Dict]:
        return [entry._asdict() for entry in self.log]
