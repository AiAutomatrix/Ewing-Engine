import sys
from engine.dependencies import get_simulation_instance
from engine.simulation import Simulation
from engine.config import SimulationConfig
import numpy as np

def test_home_court_advantage_effect():
    """
    Tests that increasing the home_court_advantage config param correctly
    increases the home team's score and decreases the away team's score.
    """
    print("\n--- Running Home Court Advantage Effect Test ---")
    game_id = '0022300061'  # A known good game_id

    try:
        global_simulation_instance = get_simulation_instance()

        target_game = next((g for g in global_simulation_instance.games if g.id == game_id), None)
        if not target_game:
            raise ValueError(f"Game ID {game_id} not found in loaded games.")

        home_team_abbr = global_simulation_instance.teams_by_id[target_game.home_team].abbreviation
        away_team_abbr = global_simulation_instance.teams_by_id[target_game.away_team].abbreviation
        print(f"Testing game: {home_team_abbr} vs {away_team_abbr}")

        # 1. Run a baseline simulation
        print("--- Running Baseline Simulation ---")
        baseline_config = SimulationConfig(seed=1, default_num_simulations=500)
        baseline_sim = Simulation(
            global_simulation_instance.players, global_simulation_instance.teams,
            global_simulation_instance.games, global_simulation_instance.boxscores, config=baseline_config
        )
        baseline_result = baseline_sim.run_simulation_with_config(home_team_id=home_team_abbr, away_team_id=away_team_abbr)
        baseline_home_avg = baseline_result.expected_scores['home']
        baseline_away_avg = baseline_result.expected_scores['away']
        print(f"Baseline Avg Score: {home_team_abbr} {baseline_home_avg:.2f} - {away_team_abbr} {baseline_away_avg:.2f}")

        # 2. Run a modified simulation with increased home court advantage
        print("--- Running Modified Simulation (Increased HCA) ---")
        modified_config = SimulationConfig(seed=1, home_court_advantage=10.0, default_num_simulations=500)
        modified_sim = Simulation(
            global_simulation_instance.players, global_simulation_instance.teams,
            global_simulation_instance.games, global_simulation_instance.boxscores, config=modified_config
        )
        modified_result = modified_sim.run_simulation_with_config(home_team_id=home_team_abbr, away_team_id=away_team_abbr)
        modified_home_avg = modified_result.expected_scores['home']
        modified_away_avg = modified_result.expected_scores['away']
        print(f"Modified Avg Score: {home_team_abbr} {modified_home_avg:.2f} - {away_team_abbr} {modified_away_avg:.2f}")

        # 3. Assert divergence
        assert modified_home_avg > baseline_home_avg
        assert modified_away_avg < baseline_away_avg
        print("--- Assertions PASSED ---")
        print("--- Home Court Advantage Effect Test: PASSED ---")

    except Exception as e:
        print(f"An unexpected error occurred during Home Court Advantage Effect Test: {e}")
        raise

def test_pace_modifier_effect():
    """
    Tests that increasing the pace_modifier config param correctly
    increases the total points scored in the game.
    """
    print("\n--- Running Pace Modifier Effect Test ---")
    game_id = '0022300061'

    try:
        global_simulation_instance = get_simulation_instance()

        target_game = next((g for g in global_simulation_instance.games if g.id == game_id), None)
        if not target_game:
            raise ValueError(f"Game ID {game_id} not found in loaded games.")

        home_team_abbr = global_simulation_instance.teams_by_id[target_game.home_team].abbreviation
        away_team_abbr = global_simulation_instance.teams_by_id[target_game.away_team].abbreviation
        print(f"Testing game: {home_team_abbr} vs {away_team_abbr}")

        # 1. Run a baseline simulation
        print("--- Running Baseline Simulation ---")
        baseline_config = SimulationConfig(seed=42, default_num_simulations=500)
        baseline_sim = Simulation(
            global_simulation_instance.players, global_simulation_instance.teams,
            global_simulation_instance.games, global_simulation_instance.boxscores, config=baseline_config
        )
        baseline_result = baseline_sim.run_simulation_with_config(home_team_id=home_team_abbr, away_team_id=away_team_abbr)
        baseline_total_score = baseline_result.expected_scores['home'] + baseline_result.expected_scores['away']
        print(f"Baseline Avg Total Score: {baseline_total_score:.2f}")

        # 2. Run a modified simulation with an increased pace modifier
        print("--- Running Modified Simulation (Increased Pace) ---")
        modified_config = SimulationConfig(seed=42, pace_modifier=1.2, default_num_simulations=500)

        modified_sim = Simulation(
            global_simulation_instance.players, global_simulation_instance.teams,
            global_simulation_instance.games, global_simulation_instance.boxscores, config=modified_config
        )
        modified_result = modified_sim.run_simulation_with_config(home_team_id=home_team_abbr, away_team_id=away_team_abbr)
        modified_total_score = modified_result.expected_scores['home'] + modified_result.expected_scores['away']
        print(f"Modified Avg Total Score: {modified_total_score:.2f}")

        # 3. Assert divergence
        assert modified_total_score > baseline_total_score
        print("--- Assertion PASSED ---")
        print("--- Pace Modifier Effect Test: PASSED ---")

    except Exception as e:
        print(f"An unexpected error occurred during Pace Modifier Effect Test: {e}")
        raise

if __name__ == "__main__":
    try:
        test_home_court_advantage_effect()
        test_pace_modifier_effect()
        print("\n--- All Simulation Config Effects Tests: PASSED ---")
    except Exception as e:
        print(f"\n--- A test failed ---")
        sys.exit(1)
