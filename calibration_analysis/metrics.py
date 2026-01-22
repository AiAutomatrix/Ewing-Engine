# calibration_analysis/metrics.py

import numpy as np
from typing import List, Dict, Any

from .targets import CALIBRATION_TARGETS

def analyze_simulation_results(simulation_results: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Analyzes the raw results from a simulation run and computes key metrics.

    Args:
        simulation_results: A list of dictionaries, each representing a single game simulation.

    Returns:
        A dictionary of computed metrics.
    """
    total_points = [res["total_points"] for res in simulation_results]
    home_wins = [1 for res in simulation_results if res["winner"] == "home"]
    margins_of_victory = [abs(res["home_score"] - res["away_score"]) for res in simulation_results]

    return {
        "average_total_points": np.mean(total_points),
        "home_win_rate": len(home_wins) / len(simulation_results),
        "margin_of_victory_stddev": np.std(margins_of_victory)
    }

def compare_to_targets(analysis_metrics: Dict[str, float]) -> Dict[str, Dict[str, float]]:
    """
    Compares the computed simulation metrics against the defined historical targets.

    Args:
        analysis_metrics: A dictionary of computed metrics from a simulation run.

    Returns:
        A dictionary detailing the comparison, including the error from the target.
    """
    comparison = {}
    for metric_name, target in CALIBRATION_TARGETS.items():
        simulated_value = analysis_metrics.get(metric_name, 0.0)
        error = simulated_value - target.historical_value
        comparison[metric_name] = {
            "simulated": simulated_value,
            "target": target.historical_value,
            "error": error,
            "tolerance": target.tolerance
        }
    return comparison
