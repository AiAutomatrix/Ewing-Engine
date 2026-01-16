from dataclasses import dataclass, field
from typing import Dict, Any
from engine.simulation import Simulation
from engine.assumptions import AssumptionRegistry
from engine.models import Team
from engine.data_ingestion.data_ingestion_runner import team_clean
from engine.adapters.team_adapter import TeamAdapter


@dataclass
class Scenario:
    """A named scenario with a set of assumption overrides."""
    name: str
    overrides: Dict[str, float]

    def run(self) -> Dict[str, Any]:
        """Run the simulation with the scenario's assumption overrides."""
        teams_df = team_clean[0]
        teams = TeamAdapter(teams_df).to_engine_objects()
        simulation = Simulation(players=[], teams=teams, games=[], boxscores=[])
        assumptions = AssumptionRegistry()
        for key, value in self.overrides.items():
            original_assumption = getattr(assumptions, key)
            setattr(assumptions, key, original_assumption.__class__(
                name=original_assumption.name,
                value=value,
                description=original_assumption.description
            ))
        return simulation.run_simulation_with_config(config=None, assumptions=assumptions)
