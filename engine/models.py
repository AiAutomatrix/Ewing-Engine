# engine/models.py

import random
from abc import ABC, abstractmethod
from typing import Dict, Tuple
from engine.assumptions import AssumptionRegistry

class SimulationModel(ABC):
    """
    Abstract base class for simulation models. Defines the contract
    for how models can be swapped into the simulation engine.
    """
    @abstractmethod
    def get_possession_outcome(self, off_team: Dict, def_team: Dict, assumptions: AssumptionRegistry) -> Tuple[int, str]:
        """
        Simulates a single possession and returns the number of points scored and the outcome type.

        Args:
            off_team (Dict): The offensive team's data.
            def_team (Dict): The defensive team's data.
            assumptions (AssumptionRegistry): The assumptions to use for the simulation.

        Returns:
            Tuple[int, str]: A tuple containing the points scored (0, 1, 2, or 3) 
                             and a string describing the outcome (e.g., '2PT', 'MISS').
        """
        pass


class HeuristicModel(SimulationModel):
    """
    The default simulation model, using team-level stats and heuristics.
    """
    def __init__(self, league_avg_off_rating: float):
        self.league_avg_off_rating = league_avg_off_rating

    def get_possession_outcome(self, off_team: Dict, def_team: Dict, assumptions: AssumptionRegistry) -> Tuple[int, str]:
        """Simplified possession outcome model based on team-level heuristics."""
        adj_off_rating = off_team["off_rating"] * (def_team["def_rating"] / self.league_avg_off_rating)
        expected_pts_per_pos = adj_off_rating / 100.0

        rand = random.random()

        # Use assumptions from the registry
        three_prob = off_team["three_pt_rate"] * assumptions.shot_type_mix.value
        two_prob = (1 - off_team["three_pt_rate"]) * (1 - assumptions.shot_type_mix.value)
        ft_prob = off_team["ft_rate"] * assumptions.free_throw_rate.value

        current_ev = (3 * three_prob) + (2 * two_prob) + (1 * ft_prob)
        scale_factor = expected_pts_per_pos / current_ev if current_ev > 0 else 1.0

        p3 = three_prob * scale_factor
        p2 = two_prob * scale_factor
        pft = ft_prob * scale_factor
        p_turnover = assumptions.turnover_rate.value
        p0 = 1.0 - (p3 + p2 + pft + p_turnover)

        if p0 < 0:
            total = p3 + p2 + pft + p_turnover
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
