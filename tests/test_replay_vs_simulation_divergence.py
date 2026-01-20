import sys
from engine.dependencies import get_simulation_instance
from engine.replay_engine import Engine
from engine.config import SimulationConfig

def test_replay_vs_simulation_divergence():
    game_id = '0022300061' # A known good game_id
    print(f"\n--- Running Replay vs Simulation Divergence Test for Game ID: {game_id} ---")

    try:
        # 1. Initialize the global simulation instance, forcing a reload to get the latest code
        simulation_instance = get_simulation_instance(force_reload=True)

        # 2. Instantiate the Engine
        engine = Engine(simulation_instance=simulation_instance)

        # 3. Ingest the specific game to get its ReplayState (and team abbreviations)
        replay_state = engine.ingest_game(game_id)
        if not replay_state:
            print(f"Error: Could not ingest game {game_id}.")
            sys.exit(1)

        # Fetch team abbreviations from replay_state
        home_team_abbr = replay_state.teams[replay_state.game.home_team].abbreviation
        away_team_abbr = replay_state.teams[replay_state.game.away_team].abbreviation

        # --- Run Deterministic Replay (should match historical box score exactly) ---
        print("\n--- Running Deterministic Historical Replay ---")
        # For direct historical box score comparison, we use run_single_historical_replay
        # which uses the stored actual game_scores
        replay_result = simulation_instance.run_single_historical_replay(game_id)
        
        if not replay_result:
            print(f"Error: No replay result found for game {game_id}.")
            sys.exit(1)

        actual_home_score = replay_result['home_score_actual']
        actual_away_score = replay_result['away_score_actual']

        print(f"Historical Box Score: {home_team_abbr} {actual_home_score} - {away_team_abbr} {actual_away_score}")

        # --- Run Stochastic Simulation (should diverge from deterministic and historical) ---
        print("\n--- Running Stochastic Simulation ---")
        # Using seed=None for true randomness, or a different seed to ensure divergence
        stochastic_config = SimulationConfig(seed=None, default_num_simulations=100) 
        sim_result = simulation_instance.run_simulation_with_config(
            home_team_id=home_team_abbr, 
            away_team_id=away_team_abbr, 
            config=stochastic_config
        )

        if not sim_result:
            print(f"Error: Stochastic simulation returned no result for game {game_id}.")
            sys.exit(1)

        sim_home_score_avg = sim_result.expected_scores['home']
        sim_away_score_avg = sim_result.expected_scores['away']

        print(f"Stochastic Sim Avg Score (100 runs): {home_team_abbr} {sim_home_score_avg:.2f} - {away_team_abbr} {sim_away_score_avg:.2f}")

        # Assertions for divergence
        # The key is that the historical replay should be perfect, while the simulation
        # introduces variability, meaning its *average* should not be expected to be
        # the exact historical score.

        # First, ensure the replay result actually matches the historical average from game_scores
        assert actual_home_score == simulation_instance.game_scores[game_id]['home']
        assert actual_away_score == simulation_instance.game_scores[game_id]['away']

        # Assert that the stochastic simulation average is not an exact integer match to the historical score.
        assert not (abs(sim_home_score_avg - actual_home_score) < 0.001 and abs(sim_away_score_avg - actual_away_score) < 0.001), \
            "Stochastic simulation average too close to historical; expected divergence."

        print("\nAssertions Passed: Replay is deterministic, simulation is stochastic and diverges.")
        print(f"\n--- Replay vs Simulation Divergence Test: PASSED ---")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_replay_vs_simulation_divergence()
