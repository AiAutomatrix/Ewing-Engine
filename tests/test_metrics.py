# tests/test_metrics.py

import numpy as np
from engine.metrics import analyze_results


def test_analyze_results_deterministic():
    """Tests that the metrics analysis is deterministic given the same inputs."""
    # A simple, fixed set of simulation results
    results = [
        {"winner": "home", "home_score": 110, "away_score": 100, "total_points": 210},
        {"winner": "away", "home_score": 95, "away_score": 105, "total_points": 200},
        {"winner": "home", "home_score": 120, "away_score": 115, "total_points": 235},
        {"winner": "home", "home_score": 100, "away_score": 90, "total_points": 190},
        {"winner": "away", "home_score": 102, "away_score": 108, "total_points": 210},
    ]

    metrics1 = analyze_results(results)
    metrics2 = analyze_results(results)

    assert metrics1.win_probability["home"] == metrics2.win_probability["home"]
    assert metrics1.expected_scores["away"] == metrics2.expected_scores["away"]
    assert np.isclose(metrics1.expected_spread, metrics2.expected_spread)


def test_win_probability():
    """Tests the win probability calculation."""
    results = [
        {"winner": "home", "home_score": 1, "away_score": 0, "total_points": 1},
        {"winner": "home", "home_score": 1, "away_score": 0, "total_points": 1},
        {"winner": "away", "home_score": 0, "away_score": 1, "total_points": 1},
        {"winner": "draw", "home_score": 1, "away_score": 1, "total_points": 2},
    ]
    metrics = analyze_results(results)
    assert metrics.win_probability["home"] == 0.5
    assert metrics.win_probability["away"] == 0.25
    assert metrics.win_probability["draw"] == 0.25
