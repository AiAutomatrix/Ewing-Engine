from dataclasses import dataclass, field

@dataclass
class Assumption:
    name: str
    value: float
    description: str

@dataclass
class AssumptionRegistry:
    """
    Centralized registry for all simulation assumptions.
    Defaults are set to reproduce Phase 2 results exactly.
    """
    possession_length_distribution: Assumption = field(default_factory=lambda: Assumption(
        name="possession_length_distribution",
        value=10.0,
        description="Distribution of time per possession."
    ))
    turnover_rate: Assumption = field(default_factory=lambda: Assumption(
        name="turnover_rate",
        value=0.1,
        description="Probability of a turnover on a given possession."
    ))
    shot_type_mix: Assumption = field(default_factory=lambda: Assumption(
        name="shot_type_mix",
        value=0.5,
        description="Mix of 2-point vs 3-point shots."
    ))
    free_throw_rate: Assumption = field(default_factory=lambda: Assumption(
        name="free_throw_rate",
        value=0.2,
        description="Rate at which free throws are awarded."
    ))
    offensive_rebound_rate: Assumption = field(default_factory=lambda: Assumption(
        name="offensive_rebound_rate",
        value=0.2,
        description="Probability of securing an offensive rebound."
    ))
    pace_modifier: Assumption = field(default_factory=lambda: Assumption(
        name="pace_modifier",
        value=1.0,
        description="Multiplier to adjust the pace of the game."
    ))
    home_court_advantage: Assumption = field(default_factory=lambda: Assumption(
        name="home_court_advantage",
        value=3.5,
        description="Points awarded to the home team."
    ))
