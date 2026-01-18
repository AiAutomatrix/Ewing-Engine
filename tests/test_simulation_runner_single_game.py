# tests/test_simulation_runner_single_game.py

import sys
from engine.dependencies import get_simulation_instance
from engine.config import SimulationConfig
from engine.simulation_runner import run_single_game_simulation

def test_simulation_runner_single_game():
    print("\n--- Running Simulation Runner Single Game Test ---")

    try:
        # 1. Initialize the global simulation instance to get all season data
        simulation_instance = get_simulation_instance()

        # 2. Define a test game_id, home_team_abbr, away_team_abbr
        # Find the first game in the simulation_instance
        if not simulation_instance.games:
            print("Error: No games found in simulation_instance. Cannot run test.")
            sys.exit(1)

        first_game = simulation_instance.games[0]
        test_game_id = first_game.id

        # Get abbreviations from the first game's teams
        home_team_obj = simulation_instance.teams_by_id.get(first_game.home_team)
        away_team_obj = simulation_instance.teams_by_id.get(first_game.away_team)

        if not home_team_obj or not away_team_obj:
            print(f"Error: Could not find team objects for game {test_game_id}")
            sys.exit(1)

        home_team_abbr = home_team_obj.abbreviation
        away_team_abbr = away_team_obj.abbreviation
        
        print(f"Testing game ID: {test_game_id}, Home: {home_team_abbr}, Away: {away_team_abbr}")

        # 3. Create a test SimulationConfig
        test_config = SimulationConfig(seed=42, default_num_simulations=10)
        print(f"Running simulation with config: seed={test_config.seed}, num_simulations={test_config.default_num_simulations}")

        # 4. Call run_single_game_simulation
        result = run_single_game_simulation(simulation_instance, home_team_abbr, away_team_abbr, config=test_config)

        # 5. Assertions
        assert result is not None, "Simulation result should not be None"
        print("Assertion Passed: Simulation result is not None.")

        assert result.win_probability, "Win probability should not be empty"
        print("Assertion Passed: Win probability is not empty.")
        
        # Check if score distributions are present (results will be arrays/lists due to Monte Carlo)
        # Note: 'home_score' and 'away_score' will be lists of scores from each simulation run
        assert 'home' in result.expected_scores, "Expected home score should be present in result.expected_scores"
        assert 'away' in result.expected_scores, "Expected away score should be present in result.expected_scores"
        print(f"Assertion Passed: Expected scores populated.")

        # 6. Print a summary of the result
        print("\n--- Simulation Result Summary ---")
        print(f"Game: {home_team_abbr} vs {away_team_abbr}")
        print(f"Home Win Probability: {result.win_probability.get('home'):.2f}")
        print(f"Away Win Probability: {result.win_probability.get('away'):.2f}")
        print(f"Avg Home Score: {result.expected_scores['home']:.2f}")
        print(f"Avg Away Score: {result.expected_scores['away']:.2f}")
        print(f"Expected Margin: {result.expected_margin:.2f}")

        # 7. Print a success message
        print("\n--- Simulation Runner Single Game Test: PASSED ---")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_simulation_runner_single_game()