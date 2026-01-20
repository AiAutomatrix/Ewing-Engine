# engine/models.py

import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, Tuple
from dataclasses import dataclass, field
from engine.assumptions import AssumptionRegistry
from .config import CalibrationParams

@dataclass
class Player:
    id: int
    name: str
    team_id: int
    minutes: float
    points: float
    rebounds: float
    assists: float
    steals: float
    blocks: float
    fg_pct: float

@dataclass
class Team:
    id: int
    name: str
    abbreviation: str
    pace: float
    off_rating: float
    def_rating: float
    efg_pct: float
    three_pt_rate: float
    ft_rate: float
    gp: int = 0
    w: int = 0
    l: int = 0
    pts: float = 0.0
    rebounds: float = 0.0
    assists: float = 0.0
    fg_pct: float = 0.0
    turnovers: float = 0.0

@dataclass
class Game:
    id: int
    date: str
    home_team: int
    away_team: int
    scores: str
    plus_minus: float

@dataclass
class BoxScore:
    game_id: int
    team_id: int
    player_id: int
    minutes: str
    pts: int
    rebounds: int
    assists: int
    fg_pct: float
    plus_minus: int


class SimulationModel(ABC):
    @abstractmethod
    def get_possession_outcome(self, off_team: Dict, def_team: Dict, assumptions: AssumptionRegistry, is_home: bool, calibration: CalibrationParams = None, pace_modifier: float = 1.0) -> Tuple[int, str]:
        pass


class HeuristicModel(SimulationModel):
    def __init__(self, league_avg_off_rating: float, calibration: CalibrationParams = None):
        self.league_avg_off_rating = league_avg_off_rating
        self.calibration = calibration if calibration is not None else CalibrationParams()

    def get_possession_outcome(self, off_team: Dict, def_team: Dict, assumptions: AssumptionRegistry, is_home: bool, calibration: CalibrationParams = None, pace_modifier: float = 1.0) -> Tuple[int, str]:
        calc_calibration = calibration if calibration is not None else self.calibration

        adj_off_rating = off_team["off_rating"] * (def_team["def_rating"] / self.league_avg_off_rating)

        if is_home:
            adj_off_rating *= calc_calibration.home_offense_scalar
        else:
            adj_off_rating *= calc_calibration.away_offense_scalar

        # Apply pace modifier to the expected points calculation
        expected_pts_per_pos = (adj_off_rating / 100.0) * calc_calibration.global_score_multiplier * pace_modifier

        # The rest of the logic remains the same, ensuring probabilities are scaled correctly
        rand = np.random.rand()

        three_pt_rate = off_team.get("three_pt_rate", 0.35)
        ft_rate = off_team.get("ft_rate", 0.20)

        three_prob = three_pt_rate * assumptions.shot_type_mix.value
        two_prob = (1 - three_pt_rate) * (1 - assumptions.shot_type_mix.value)
        ft_prob = ft_rate * assumptions.free_throw_rate.value

        current_ev = (3 * three_prob) + (2 * two_prob) + (1 * ft_prob)
        scale_factor = expected_pts_per_pos / current_ev if current_ev > 0 else 1.0

        p3 = three_prob * scale_factor
        p2 = two_prob * scale_factor
        pft = ft_prob * scale_factor
        p_turnover = assumptions.turnover_rate.value
        p0 = 1.0 - (p3 + p2 + pft + p_turnover)

        if p0 < 0:
            total = p3 + p2 + pft + p_turnover
            if total > 0:
                p3 /= total
                p2 /= total
                pft /= total
                p_turnover /= total
        
        if rand < p3:
            return 3, "3PT"
        elif rand < p3 + p2:
            return 2, "2PT"
        elif rand < p3 + p2 + pft:
            return 1, "FT"
        elif rand < p3 + p2 + pft + p_turnover:
            return 0, "TO"
        else:
            return 0, "MISS"
