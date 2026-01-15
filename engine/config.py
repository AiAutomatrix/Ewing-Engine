from dataclasses import dataclass, field
from engine.assumptions import AssumptionRegistry

@dataclass
class SimulationConfig:
    """
    Centralizes all simulation constants and tunable parameters.
    """
    # Possessions per game assumptions
    avg_pace: float = 100.0
    pace_std_dev: float = 3.0
    min_pace: int = 80
    max_pace: int = 140

    # Score variance controls
    score_variance_factor: float = 1.0

    # Home-court advantage factor
    home_court_advantage: float = 2.0  # Points per 100 possessions

    # Default Monte Carlo run count
    default_num_simulations: int = 1000

    # Phase 3: Assumption Registry
    assumptions: AssumptionRegistry = field(default_factory=AssumptionRegistry)

# Create a default config instance for easy import
default_config = SimulationConfig()
