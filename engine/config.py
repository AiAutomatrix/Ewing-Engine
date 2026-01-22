# engine/config.py

from dataclasses import dataclass, field
from typing import Optional
from .assumptions import Assumption, AssumptionRegistry
from .calibration import CalibrationParams

@dataclass
class SimulationConfig:
    """A configuration bundle for a simulation run."""
    seed: int = 42
    default_num_simulations: int = 500
    
    # Pace settings
    pace_std_dev: float = 3.0
    min_pace: int = 85
    max_pace: int = 115
    pace_modifier: Optional[float] = None
    
    # Assumptions
    assumptions: AssumptionRegistry = field(default_factory=AssumptionRegistry)
    
    # Calibration
    calibration: Optional[CalibrationParams] = None

    def __post_init__(self):
        """
        Post-initialization to handle conditional logic, particularly for
        updating the AssumptionRegistry based on direct config parameters.
        """
        if self.pace_modifier is not None:
            self.assumptions.pace_modifier = Assumption(
                name="pace_modifier",
                value=self.pace_modifier,
                description="Overridden pace modifier."
            )

default_config = SimulationConfig()
