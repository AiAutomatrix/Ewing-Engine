from dataclasses import dataclass, field
from typing import Dict, Any
from engine.simulation import run_simulation_with_config
from engine.assumptions import AssumptionRegistry

@dataclass
class Scenario:
    """A named scenario with a set of assumption overrides."""
    name: str
    overrides: Dict[str, float]

    def run(self) -> Dict[str, Any]:
        """Run the simulation with the scenario's assumption overrides."""
        assumptions = AssumptionRegistry()
        for key, value in self.overrides.items():
            original_assumption = getattr(assumptions, key)
            setattr(assumptions, key, original_assumption.__class__(
                name=original_assumption.name,
                value=value,
                description=original_assumption.description
            ))
        return run_simulation_with_config(config=None, assumptions=assumptions)
