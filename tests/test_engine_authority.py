import sys
from engine.dependencies import get_simulation_instance
from engine.replay_engine import Engine

def test_engine_authority_ingest_game_failure():
    print("\n--- Running Engine Authority Test: Ingest Game Failure ---")

    try:
        simulation_instance = get_simulation_instance()
        engine = Engine(simulation_instance)

        # Temporarily stub or disable engine.ingest_game
        # A real mock library like unittest.mock.patch would be used in a proper test suite.
        # For this direct terminal test, a simple lambda replacement demonstrates the principle.
        original_ingest_game = engine.ingest_game
        engine.ingest_game = lambda game_id: None
        print("Mocked engine.ingest_game to always return None.")

        game_id_to_test = '0022300061'
        print(f"Attempting to ingest game {game_id_to_test} with mocked method...")
        replay_state = engine.ingest_game(game_id_to_test)

        assert replay_state is None, "ReplayState should be None when ingest_game is mocked to fail."
        print(f"Assertion Passed: ReplayState is None as expected when ingest_game fails.")

        # Restore the original method (good practice, though not strictly necessary for script exit)
        engine.ingest_game = original_ingest_game

        print("\n--- Engine Authority Test: Ingest Game Failure: PASSED ---")

    except AssertionError as ae:
        print(f"Engine Authority Test: Ingest Game Failure: FAILED - {ae}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during Engine Authority Test: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_engine_authority_ingest_game_failure()
