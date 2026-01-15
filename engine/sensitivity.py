from dataclasses import dataclass, field
from typing import List
from engine.simulation import run_simulation_with_config
from engine.assumptions import AssumptionRegistry
from engine.metrics import SimulationMetrics

@dataclass
class SensitivityResult:
    """Result of a sensitivity analysis run."""
    assumption_name: str
    perturbation: float
    win_probability_delta: float
    expected_margin_delta: float

@dataclass
class SensitivityAnalysis:
    """Engine for running sensitivity analysis on simulation assumptions."""
    assumptions: AssumptionRegistry = field(default_factory=AssumptionRegistry)
    base_results: SimulationMetrics = field(init=False)

    def __post_init__(self):
        """Run baseline simulation."""
        self.base_results = run_simulation_with_config()

    def run_one_at_a_time(self, assumption_name: str, perturbations: List[float]) -> List[SensitivityResult]:
        """Run sensitivity analysis for a single assumption."""
        results = []
        for p in perturbations:
            # Create a copy of the assumptions to modify
            new_assumptions = self.assumptions
            original_value = getattr(new_assumptions, assumption_name).value
            setattr(new_assumptions, assumption_name, getattr(new_assumptions, assumption_name).__class__(
                name=assumption_name,
                value=original_value * (1 + p),
                description=getattr(new_assumptions, assumption_name).description
            ))

            # Run simulation with perturbed assumptions
            new_results = run_simulation_with_config(config=None, assumptions=new_assumptions)

            # Compare results
            win_prob_delta = new_results.win_probability['home'] - self.base_results.win_probability['home']
            margin_delta = new_results.expected_margin - self.base_results.expected_margin

            results.append(SensitivityResult(
                assumption_name=assumption_name,
                perturbation=p,
                win_probability_delta=win_prob_delta,
                expected_margin_delta=margin_delta
            ))
        return results
