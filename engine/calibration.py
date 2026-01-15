from dataclasses import dataclass
from typing import List, Dict
import numpy as np

@dataclass
class CalibrationMetrics:
    """Metrics to evaluate the calibration of the simulation model."""
    confidence_interval_coverage: float
    spread_bias: float
    total_bias: float

def calculate_calibration_metrics(historical_replays: List[Dict]) -> CalibrationMetrics:
    """Calculate calibration metrics from a list of historical replays."""
    
    coverages = []
    spread_biases = []
    total_biases = []

    for replay in historical_replays:
        sim_margin_dist = replay['simulation_results']['margin_distribution']
        actual_margin = replay['actual_margin']
        
        # Confidence Interval Coverage
        lower_bound = np.percentile(sim_margin_dist, 2.5)
        upper_bound = np.percentile(sim_margin_dist, 97.5)
        coverages.append(1 if lower_bound <= actual_margin <= upper_bound else 0)

        # Spread Bias
        sim_spread = np.mean(sim_margin_dist)
        spread_biases.append(sim_spread - actual_margin)

        # Total Bias
        sim_total = replay['simulation_results']['home_score_distribution'][0] + replay['simulation_results']['away_score_distribution'][0]
        actual_total = replay['actual_score']['home'] + replay['actual_score']['away']
        total_biases.append(sim_total - actual_total)

    return CalibrationMetrics(
        confidence_interval_coverage=np.mean(coverages),
        spread_bias=np.mean(spread_biases),
        total_bias=np.mean(total_biases)
    )
