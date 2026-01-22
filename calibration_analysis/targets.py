# calibration_analysis/targets.py

from dataclasses import dataclass
from typing import Dict

@dataclass
class CalibrationTarget:
    """Represents a historical target for a simulation metric."""
    name: str
    historical_value: float
    tolerance: float

# Define the historical targets based on real-world NBA data
CALIBRATION_TARGETS: Dict[str, CalibrationTarget] = {
    "average_total_points": CalibrationTarget(
        name="average_total_points",
        historical_value=224.0,  # Approximate league average total points
        tolerance=5.0
    ),
    "home_win_rate": CalibrationTarget(
        name="home_win_rate",
        historical_value=0.58,  # Approximate home win percentage
        tolerance=0.05
    ),
    "margin_of_victory_stddev": CalibrationTarget(
        name="margin_of_victory_stddev",
        historical_value=12.5,  # Approximate standard deviation of victory margins
        tolerance=1.5
    )
}
