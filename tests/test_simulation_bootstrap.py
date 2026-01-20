import sys
import numpy as np
import pytest
from engine.dependencies import get_simulation_instance
from engine.simulation import Simulation
from engine.config import SimulationConfig

def test_simulation_bootstrap():
    print("\n--- Running Simulation Bootstrap Test ---")

    try:
        initial_simulation_data = get_simulation_instance()

        custom_config = SimulationConfig(seed=42)

        sim = Simulation(
            initial_simulation_data.players,
            initial_simulation_data.teams,
            initial_simulation_data.games,
            initial_simulation_data.boxscores,
            config=custom_config
        )

        assert sim is not None, "Simulation instance should not be None."
        print("Assertion Passed: Simulation instance created.")

        assert sim.config is not None, "Simulation config should be set."
        assert sim.config.seed == 42, f"Simulation config seed expected 42, got {sim.config.seed}."
        print(f"Assertion Passed: Simulation config with seed {sim.config.seed} is correctly attached.")

        assert len(sim.teams_by_id) > 0, "teams_by_id should be populated."
        assert len(sim.teams_by_abbr) > 0, "teams_by_abbr should be populated."
        print(f"Assertion Passed: Teams lookup maps are populated (e.g., {len(sim.teams_by_id)} teams).")

        assert len(sim.games) > 0, "Games list should be populated."
        print(f"Assertion Passed: Games list is populated ({len(sim.games)} games).")

        # Correctly test for deterministic output by running the same simulation twice
        np.random.seed(sim.config.seed)
        first_run_result = sim.run_simulation_with_config(home_team_id="GSW", away_team_id="LAL", num_simulations=10)
        
        np.random.seed(sim.config.seed) # Re-seed
        second_run_result = sim.run_simulation_with_config(home_team_id="GSW", away_team_id="LAL", num_simulations=10)

        assert first_run_result.expected_margin == second_run_result.expected_margin, "Seeded simulations should be deterministic."
        print("Assertion Passed: RNG is deterministically seeded.")

        print("\n--- Simulation Bootstrap Test: PASSED ---")

    except AssertionError as ae:
        print(f"Assertion Error: {ae}")
        print("\n--- Simulation Bootstrap Test: FAILED ---")
        pytest.fail(f"Bootstrap test failed: {ae}")

