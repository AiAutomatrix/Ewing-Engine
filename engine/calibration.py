
# engine/calibration.py

from dataclasses import dataclass

@dataclass
class CalibrationParams:
    """
    A structure to hold calibration parameters for the simulation.
    """
    global_score_multiplier: float = 1.0
    pace_modifier: float = 1.0
    pace_standard_deviation: float = 10.0
    home_offense_scalar: float = 1.0
    home_defense_scalar: float = 1.0
    away_offense_scalar: float = 1.0
    away_defense_scalar: float = 1.0
