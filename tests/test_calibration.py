
import numpy as np
from engine.simulation import Simulation
from engine.config import SimulationConfig, CalibrationParams
from engine.models import Team

def test_calibration_parameters_affect_simulation():
    # Create dummy data
    teams = [
        Team(id=1, name="Team A", abbreviation="A", pace=100, off_rating=110, def_rating=105, efg_pct=0.5, three_pt_rate=0.4, ft_rate=0.2),
        Team(id=2, name="Team B", abbreviation="B", pace=100, off_rating=105, def_rating=110, efg_pct=0.5, three_pt_rate=0.4, ft_rate=0.2),
    ]
    games = []
    boxscores = []
    players = []

    # --- Run with default config (no calibration) ---
    sim_no_calibration = Simulation(players, teams, games, boxscores, config=SimulationConfig(seed=42))
    analysis_no_calibration = sim_no_calibration.run_simulation_with_config(home_team_id="A", away_team_id="B", num_simulations=1)

    # --- Run with calibration that favors home team ---
    calibration_params = CalibrationParams(
        home_offense_scalar=1.2, 
        away_offense_scalar=0.8,
        global_score_multiplier=1.1
    )
    config_calibrated = SimulationConfig(seed=42, calibration=calibration_params)
    sim_calibrated = Simulation(players, teams, games, boxscores, config=config_calibrated)
    analysis_calibrated = sim_calibrated.run_simulation_with_config(home_team_id="A", away_team_id="B", num_simulations=1)

    # --- Assertions ---
    # Expect calibrated home score to be higher
    assert analysis_calibrated.expected_scores['home'] > analysis_no_calibration.expected_scores['home']
    # Expect calibrated away score to be lower
    assert analysis_calibrated.expected_scores['away'] < analysis_no_calibration.expected_scores['away']
