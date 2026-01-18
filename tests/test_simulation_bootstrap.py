import sys
import numpy as np
from engine.dependencies import get_simulation_instance
from engine.simulation import Simulation
from engine.config import SimulationConfig, default_config

def test_simulation_bootstrap():
    print("\n--- Running Simulation Bootstrap Test ---")

    try:
        # a. Initialize simulation_instance to get the initial data pools
        # This gives us access to the pre-processed players, teams, games, boxscores
        initial_simulation_data = get_simulation_instance()

        # b. Create a custom_config or use default_config and set seed
        custom_config = SimulationConfig(seed=42)

        # c. Instantiate sim = Simulation(...) with the custom_config
        sim = Simulation(
            initial_simulation_data.players,
            initial_simulation_data.teams,
            initial_simulation_data.games,
            initial_simulation_data.boxscores,
            config=custom_config
        )

        # d. Assert that sim is not None.
        assert sim is not None, "Simulation instance should not be None."
        print("Assertion Passed: Simulation instance created.")

        # e. Assert that sim.config is not None and that sim.config.seed is 42.
        assert sim.config is not None, "Simulation config should be set."
        assert sim.config.seed == 42, f"Simulation config seed expected 42, got {sim.config.seed}."
        print(f"Assertion Passed: Simulation config with seed {sim.config.seed} is correctly attached.")

        # f. Assert that sim.teams_by_id and sim.teams_by_abbr are populated.
        assert len(sim.teams_by_id) > 0, "teams_by_id should be populated."
        assert len(sim.teams_by_abbr) > 0, "teams_by_abbr should be populated."
        print(f"Assertion Passed: Teams lookup maps are populated (e.g., {len(sim.teams_by_id)} teams).")

        # g. Assert that sim.games is populated.
        assert len(sim.games) > 0, "Games list should be populated."
        print(f"Assertion Passed: Games list is populated ({len(sim.games)} games).")

        # Verify RNG is seeded correctly (by running a simple random operation)
        # Note: numpy.random.rand() should produce the same sequence after seeding
        # but directly checking its output after this global seed might be tricky
        # if other modules call np.random. Let's just trust np.random.seed works.
        test_random_val = np.random.rand()
        np.random.seed(42) # Re-seed to check if this specific value is produced
        assert np.isclose(test_random_val, np.random.rand()), "RNG might not be deterministically seeded or another call interfered."
        print("Assertion Passed: RNG appears to be deterministically seeded.")


        # h. Print a success message.
        print("\n--- Simulation Bootstrap Test: PASSED ---")

    except AssertionError as ae:
        print(f"Assertion Error: {ae}")
        print("\n--- Simulation Bootstrap Test: FAILED ---")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("\n--- Simulation Bootstrap Test: FAILED ---")
        sys.exit(1)

if __name__ == "__main__":
    test_simulation_bootstrap()
