import sys
from engine.dependencies import get_simulation_instance
from engine.replay_engine import Engine

def test_single_game_engine_replay():
    game_id = '0022300061' # A known good game_id

    print(f"\n--- Running Single Game Engine Replay Activation Test for Game ID: {game_id} ---")

    try:
        # 1. Initialize simulation instance
        simulation_instance = get_simulation_instance()
        print("Simulation instance initialized.")

        # 2. Instantiate the Engine
        engine = Engine(simulation_instance)
        print("Engine instantiated.")

        # 3. Ingest game data and get ReplayState
        print(f"Ingesting game {game_id} into the Engine...")
        replay_state = engine.ingest_game(game_id)

        # 4. Assert engine state exists
        assert replay_state is not None, "ReplayState should not be None"
        assert replay_state.game is not None, "ReplayState.game should not be None"
        assert len(replay_state.teams) == 2, f"Expected 2 teams in ReplayState, got {len(replay_state.teams)}"
        assert len(replay_state.players) > 0, "ReplayState should contain players"
        print("ReplayState created and basic assertions passed.")

        # 5. Run feature extraction
        print(f"Extracting features for game {game_id}...")
        features = engine.extract_features(replay_state)

        # 6. Assert features are real
        assert features is not None, "Features object should not be None"
        assert features.game_features, "Game features should not be empty"
        assert features.team_features, "Team features should not be empty"
        assert features.player_features, "Player features should not be empty"
        print("Features extracted and basic assertions passed.")

        # 7. Print summary for human inspection
        print(features.summary())

        print("\n--- Engine Single Game Replay Activation Test: PASSED ---")

    except Exception as e:
        print(f"\n--- Engine Single Game Replay Activation Test: FAILED ---")
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_single_game_engine_replay()
