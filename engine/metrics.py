import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from scipy.stats import skew, kurtosis
from engine.config import SimulationConfig # Import SimulationConfig

@dataclass
class SimulationMetrics:
    win_probability: Dict[str, float]
    expected_scores: Dict[str, float]
    expected_total_points: float
    total_points_std_dev: float
    expected_margin: float
    score_variance: Dict[str, float]
    margin_distribution: List[int]
    win_margin_distribution: Dict[int, int]
    score_skewness: Optional[Dict[str, float]] = None
    score_kurtosis: Optional[Dict[str, float]] = None
    score_distributions: Optional[Dict[str, List[int]]] = None

def analyze_results(results: List[Dict], return_distributions: bool = False, config: SimulationConfig = None) -> SimulationMetrics:
    """
    Analyzes raw simulation outputs and returns structured metrics.
    """
    num_simulations = len(results)

    home_wins = sum(1 for r in results if r["winner"] == "home")
    away_wins = sum(1 for r in results if r["winner"] == "away")
    draws = num_simulations - home_wins - away_wins

    home_scores = [r["home_score"] for r in results]
    away_scores = [r["away_score"] for r in results]
    total_points = [r["total_points"] for r in results]
    margins = [r["home_score"] - r["away_score"] for r in results]

    win_margin_distribution = {k: 0 for k in range(-50, 51)}
    for margin in margins:
        rounded_margin = int(round(margin))
        if rounded_margin in win_margin_distribution:
            win_margin_distribution[rounded_margin] += 1

    metrics = {
        "win_probability": {
            "home": home_wins / num_simulations,
            "away": away_wins / num_simulations,
            "draw": draws / num_simulations
        },
        "expected_scores": {
            "home": np.mean(home_scores),
            "away": np.mean(away_scores)
        },
        "expected_total_points": np.mean(total_points),
        "total_points_std_dev": np.std(total_points),
        "expected_margin": np.mean(margins),
        "score_variance": {
            "home": np.var(home_scores),
            "away": np.var(away_scores),
            "total": np.var(total_points)
        },
        "margin_distribution": [],
        "win_margin_distribution": win_margin_distribution
    }

    if return_distributions:
        metrics["margin_distribution"] = margins
        metrics["score_skewness"] = {
            "home": skew(home_scores),
            "away": skew(away_scores),
            "total": skew(total_points)
        }
        metrics["score_kurtosis"] = {
            "home": kurtosis(home_scores),
            "away": kurtosis(away_scores),
            "total": kurtosis(total_points)
        }
        metrics["score_distributions"] = {
            "home": home_scores,
            "away": away_scores
        }

    return SimulationMetrics(**metrics)