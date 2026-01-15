from dataclasses import dataclass
from typing import Dict
from engine.simulation import run_simulation_with_config

@dataclass
class HistoricalGame:
    """Represents a historical game with its actual outcome."""
    team_a: str
    team_b: str
    date: str
    actual_score: Dict[str, int]

    def replay(self) -> Dict:
        """Replay the game using the simulation engine and compare results."""
        sim_results = run_simulation_with_config(home_team_id=self.team_a, away_team_id=self.team_b, return_distributions=True)
        actual_margin = self.actual_score['home'] - self.actual_score['away']
        
        # Find the percentile of the actual outcome in the simulated distribution
        margin_distribution = sim_results.margin_distribution
        percentile = sum(1 for m in margin_distribution if m < actual_margin) / len(margin_distribution)

        return {
            "simulation_results": sim_results,
            "actual_score": self.actual_score,
            "actual_margin": actual_margin,
            "actual_outcome_percentile": percentile
        }
