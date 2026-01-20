import sys
from engine.dependencies import get_simulation_instance
from engine.config import SimulationConfig
from engine.assumptions import Assumption, AssumptionRegistry
import numpy as np

def test_home_court_advantage_effect():
    """
    Tests that increasing the home_court_advantage config param correctly
    increases the home team's score and decreases the away team's score.
    """
    print("\n--- Running Home Court Advantage Effect Test ---")
    game_id = '0022300061'  # A known good game_id
    simulation_instance = get_simulation_instance(force_reload=True)
    target_game = next((g for g in simulation_instance.games if g.id == game_id), None)
    if not target_game:
        raise ValueError(f"Game ID {game_id} not found in loaded games.")

    home_team_abbr = simulation_instance.teams_by_id[target_game.home_team].abbreviation
    away_team_abbr = simulation_instance.teams_by_id[target_game.away_team].abbreviation
    print(f"Testing game: {home_team_abbr} vs {away_team_abbr}")

    # 1. Run a baseline simulation
    print("--- Running Baseline Simulation ---")
    baseline_config = SimulationConfig(seed=1, default_num_simulations=500)
    baseline_result = simulation_instance.run_simulation_with_config(
        home_team_id=home_team_abbr, away_team_id=away_team_abbr, config=baseline_config
    )
    baseline_home_avg = baseline_result.expected_scores['home']
    baseline_away_avg = baseline_result.expected_scores['away']
    print(f"Baseline Avg Score: {home_team_abbr} {baseline_home_avg:.2f} - {away_team_abbr} {baseline_away_avg:.2f}")

    # 2. Run a modified simulation with increased home court advantage
    print("--- Running Modified Simulation (Increased HCA) ---")
    modified_config = SimulationConfig(seed=1, default_num_simulations=500)
    new_assumptions_hca = AssumptionRegistry()
    new_assumptions_hca.home_court_advantage = Assumption(name="home_court_advantage", value=10.0, description="Increased HCA for testing")
    modified_config.assumptions = new_assumptions_hca
    modified_result = simulation_instance.run_simulation_with_config(
        home_team_id=home_team_abbr, away_team_id=away_team_abbr, config=modified_config
    )
    modified_home_avg = modified_result.expected_scores['home']
    modified_away_avg = modified_result.expected_scores['away']
    print(f"Modified Avg Score: {home_team_abbr} {modified_home_avg:.2f} - {away_team_abbr} {modified_away_avg:.2f}")

    # 3. Assert divergence
    assert modified_home_avg > baseline_home_avg
    assert modified_away_avg < baseline_away_avg
    print("--- Assertions PASSED ---")
    print("--- Home Court Advantage Effect Test: PASSED ---")

def test_pace_modifier_effect():
    """
    Tests that increasing the pace_modifier config param correctly
    increases the total points scored in the game.
    """
    print("\n--- Running Pace Modifier Effect Test ---")
    game_id = '0022300061'
    simulation_instance = get_simulation_instance(force_reload=True)
    target_game = next((g for g in simulation_instance.games if g.id == game_id), None)
    if not target_game:
        raise ValueError(f"Game ID {game_id} not found in loaded games.")

    home_team_abbr = simulation_instance.teams_by_id[target_game.home_team].abbreviation
    away_team_abbr = simulation_instance.teams_by_id[target_game.away_team].abbreviation
    print(f"Testing game: {home_team_abbr} vs {away_team_abbr}")

    # 1. Run a baseline simulation
    print("--- Running Baseline Simulation ---")
    baseline_config = SimulationConfig(seed=42, default_num_simulations=500)
    baseline_result = simulation_instance.run_simulation_with_config(
        home_team_id=home_team_abbr, away_team_id=away_team_abbr, config=baseline_config
    )
    baseline_total_score = baseline_result.expected_scores['home'] + baseline_result.expected_scores['away']
    print(f"Baseline Avg Total Score: {baseline_total_score:.2f}")

    # 2. Run a modified simulation with an increased pace modifier
    print("--- Running Modified Simulation (Increased Pace) ---")
    modified_config = SimulationConfig(seed=42, default_num_simulations=500, pace_modifier=1.2)
    modified_result = simulation_instance.run_simulation_with_config(
        home_team_id=home_team_abbr, away_team_id=away_team_abbr, config=modified_config
    )
    modified_total_score = modified_result.expected_scores['home'] + modified_result.expected_scores['away']
    print(f"Modified Avg Total Score: {modified_total_score:.2f}")

    # 3. Assert divergence
    assert modified_total_score > baseline_total_score
    print("--- Assertion PASSED ---")
    print("--- Pace Modifier Effect Test: PASSED ---")

if __name__ == "__main__":
    try:
        test_home_court_advantage_effect()
        test_pace_modifier_effect()
        print("\n--- All Simulation Config Effects Tests: PASSED ---")
    except Exception as e:
        print(f"\n--- A test failed ---")
        sys.exit(1)
