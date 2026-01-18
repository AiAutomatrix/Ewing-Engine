import sys
import numpy as np
from engine.dependencies import get_simulation_instance
from engine.simulation import Simulation
from engine.config import SimulationConfig

def run_monte_carlo_simulation(seed, game_id, home_team_abbr, away_team_abbr):
    """Helper function to run a Monte Carlo simulation for a given seed and game."""
    config = SimulationConfig(seed=seed, default_num_simulations=500)
    sim_instance = get_simulation_instance()
    simulation = Simulation(
        sim_instance.players, sim_instance.teams, sim_instance.games, sim_instance.boxscores, config=config
    )
    results = simulation.run_simulation_with_config(
        home_team_id=home_team_abbr,
        away_team_id=away_team_abbr,
        return_distributions=True
    )
    
    home_scores = results.score_distributions['home']
    away_scores = results.score_distributions['away']
    
    return {
        "home_mean": np.mean(home_scores),
        "away_mean": np.mean(away_scores),
        "home_std_dev": np.std(home_scores),
        "away_std_dev": np.std(away_scores),
        "home_win_rate": results.win_probability['home']
    }

def test_monte_carlo_sanity():
    """
    Phase 11.1: Single-Game Monte Carlo Sanity Test.
    Validates that the simulation engine is stochastic, deterministic-when-seeded,
    and capable of generating distributions.
    """
    print("\n--- Phase 11.1: Single-Game Monte Carlo Sanity Test ---")
    game_id = '0022300061'  # DEN vs LAL
    simulations_per_run = 500

    try:
        global_simulation_instance = get_simulation_instance()
        target_game = next((g for g in global_simulation_instance.games if g.id == game_id), None)
        if not target_game:
            raise ValueError(f"Game ID {game_id} not found.")

        home_team_abbr = global_simulation_instance.teams_by_id[target_game.home_team].abbreviation
        away_team_abbr = global_simulation_instance.teams_by_id[target_game.away_team].abbreviation

        print(f"Game: {home_team_abbr} vs {away_team_abbr}")
        print(f"Simulations: {simulations_per_run}\n")

        # Run A (Seed = 42)
        run_a_results = run_monte_carlo_simulation(42, game_id, home_team_abbr, away_team_abbr)
        print("Run A (Seed = 42):")
        print(f"  Home Mean: {run_a_results['home_mean']:.2f}")
        print(f"  Away Mean: {run_a_results['away_mean']:.2f}")
        print(f"  Home Std Dev: {run_a_results['home_std_dev']:.2f}")
        print(f"  Away Std Dev: {run_a_results['away_std_dev']:.2f}")
        print(f"  Home Win Rate: {run_a_results['home_win_rate']:.2%}\n")

        # Run B (Seed = 42, Control)
        run_b_results = run_monte_carlo_simulation(42, game_id, home_team_abbr, away_team_abbr)
        print("Run B (Seed = 42, Control):")
        print(f"  Home Mean: {run_b_results['home_mean']:.2f}")
        print(f"  Away Mean: {run_b_results['away_mean']:.2f}")
        print(f"  Home Std Dev: {run_b_results['home_std_dev']:.2f}")
        print(f"  Away Std Dev: {run_b_results['away_std_dev']:.2f}")
        print(f"  Home Win Rate: {run_b_results['home_win_rate']:.2%}")
        
        # Determinism Check
        determinism_passed = all(np.isclose(run_a_results[k], run_b_results[k]) for k in run_a_results)
        print(f"  Determinism Check: {'PASSED' if determinism_passed else 'FAILED'}\n")

        # Run C (Seed = 99)
        run_c_results = run_monte_carlo_simulation(99, game_id, home_team_abbr, away_team_abbr)
        print("Run C (Seed = 99):")
        print(f"  Home Mean: {run_c_results['home_mean']:.2f}")
        print(f"  Away Mean: {run_c_results['away_mean']:.2f}")
        print(f"  Home Std Dev: {run_c_results['home_std_dev']:.2f}")
        print(f"  Away Std Dev: {run_c_results['away_std_dev']:.2f}")
        print(f"  Home Win Rate: {run_c_results['home_win_rate']:.2%}")

        # Variance Check
        variance_passed = not all(np.isclose(run_a_results[k], run_c_results[k]) for k in run_a_results)
        print(f"  Variance Check: {'PASSED' if variance_passed else 'FAILED'}\n")
        
        # Pass/Fail Criteria Evaluation
        std_dev_check = run_a_results['home_std_dev'] > 0 and run_a_results['away_std_dev'] > 0
        win_rate_check = 0 < run_a_results['home_win_rate'] < 1
        
        phase_11_passed = determinism_passed and variance_passed and std_dev_check and win_rate_check

        # Historical Result
        actual_scores = global_simulation_instance.game_scores.get(game_id, {'home': 'N/A', 'away': 'N/A'})
        actual_winner = "Home" if actual_scores['home'] > actual_scores['away'] else "Away"
        print("Historical Result:")
        print(f"  Actual Score: {actual_scores['home']} - {actual_scores['away']}")
        print(f"  Actual Winner: {actual_winner}\n")

        print(f"Phase 11.1 Status: {'PASSED' if phase_11_passed else 'FAILED'}")
        
        if not phase_11_passed:
             sys.exit(1)

    except Exception as e:
        print(f"An unexpected error occurred during Phase 11.1: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_monte_carlo_sanity()
