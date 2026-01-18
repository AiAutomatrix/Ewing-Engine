# engine/config.py

from dataclasses import dataclass, field
from typing import Optional
from engine.assumptions import Assumption, AssumptionRegistry, default_assumptions
from engine.calibration import CalibrationParams

@dataclass
class SimulationConfig:
    """A configuration bundle for a simulation run."""
    seed: int = 42
    default_num_simulations: int = 500
    
    # Pace settings
    pace_std_dev: float = 3.0
    min_pace: int = 85
    max_pace: int = 115
    
    # Assumptions
    assumptions: AssumptionRegistry = field(default_factory=lambda: default_assumptions)
    
    # Calibration
    calibration: Optional[CalibrationParams] = None
