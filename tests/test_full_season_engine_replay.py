import sys
import pandas as pd
from engine.dependencies import get_simulation_instance
from engine.replay_engine import Engine, ReplayState, Features
from typing import List, Dict, Any

def test_full_season_engine_replay():
    print("\n--- Running Full Season Feature Extraction Test Through Engine ---")

    try:
        simulation_instance = get_simulation_instance()
        engine = Engine(simulation_instance)

        total_games_attempted = len(simulation_instance.games)
        successful_extractions = 0
        failed_extractions = 0
        
        # Lists to store aggregated features for potential later use/auditing
        all_game_features: List[Dict[str, Any]] = []
        all_team_features: List[Dict[int, Dict[str, Any]]] = []
        all_player_features: List[Dict[int, Dict[str, Any]]] = []

        print(f"Total games to process: {total_games_attempted}")

        for i, game in enumerate(simulation_instance.games):
            if (i + 1) % 100 == 0 or (i + 1) == total_games_attempted:
                print(f"Processing game {i+1}/{total_games_attempted} (Game ID: {game.id})...")
            
            replay_state: ReplayState = engine.ingest_game(game.id)

            if replay_state is None:
                print(f"  Error: Ingesting game {game.id} failed. Skipping.")
                failed_extractions += 1
                continue
            
            # Additional check for empty lists within replay_state as a proxy for failed ingestion
            if not replay_state.game or not replay_state.teams or not replay_state.players or not replay_state.boxscores:
                print(f"  Warning: ReplayState for game {game.id} has empty components. Skipping.")
                failed_extractions += 1
                continue

            features: Features = engine.extract_features(replay_state)

            if features is None or not features.game_features or not features.team_features or not features.player_features:
                print(f"  Error: Feature extraction for game {game.id} resulted in empty features. Skipping.")
                failed_extractions += 1
                continue
            else:
                successful_extractions += 1
                all_game_features.append(features.game_features)
                all_team_features.append(features.team_features)
                all_player_features.append(features.player_features)

        print("\n--- Full Season Feature Extraction Summary ---\n")
        print(f"Total Games Attempted: {total_games_attempted}")
        print(f"Games with Successful Feature Extraction: {successful_extractions}")
        print(f"Games with Failed Feature Extraction: {failed_extractions}")
        
        if failed_extractions == 0:
            print("\nFULL SEASON FEATURE EXTRACTION: SUCCESS - All games processed for feature extraction.")
        else:
            print("\nFULL SEASON FEATURE EXTRACTION: FAILED - Some games failed feature extraction.")
            sys.exit(1) # Exit with a failure code if any game failed

    except Exception as e:
        print(f"\nAn unexpected error occurred during full season feature extraction: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_full_season_engine_replay()