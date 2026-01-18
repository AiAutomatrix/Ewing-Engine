'''
Validates the completeness of the box score data by comparing it against
the game finder data.
'''
import os
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(name)s:%(message)s')
logger = logging.getLogger(__name__)

def get_game_ids_from_parquet_files(path, prefix):
    '''Helper function to extract unique game IDs from a directory of parquet files.'''
    game_ids = set()
    if not os.path.exists(path):
        logger.warning(f"Directory not found: {path}")
        return game_ids

    files = [f for f in os.listdir(path) if f.startswith(prefix) and f.endswith('.parquet')]
    for file in files:
        df = pd.read_parquet(os.path.join(path, file))
        # Ensure the 'game_id' column (or 'gameid') exists
        if 'game_id' in df.columns:
            game_ids.update(df['game_id'].unique())
        elif 'gameid' in df.columns:
            game_ids.update(df['gameid'].unique())
    return game_ids

def validate_data_completeness():
    '''
    Compares the game IDs in the game_finder data (source of truth)
    with the game IDs in the downloaded boxscore data.
    '''
    processed_path = 'data/processed'

    # 1. Get all expected game IDs from game_finder files
    expected_game_ids = get_game_ids_from_parquet_files(processed_path, 'game_finder')
    if not expected_game_ids:
        logger.error("No game_finder data found. Cannot perform validation.")
        return

    # 2. Get all downloaded game IDs from boxscore files
    downloaded_game_ids = get_game_ids_from_parquet_files(processed_path, 'boxscore')

    # 3. Find the missing games
    missing_game_ids = expected_game_ids - downloaded_game_ids

    # 4. Generate and print the report
    logger.info("--- Data Completeness Report ---")
    logger.info(f"Total games expected: {len(expected_game_ids)}")
    logger.info(f"Games successfully downloaded: {len(downloaded_game_ids)}")
    logger.info(f"Games missing: {len(missing_game_ids)}")

    if missing_game_ids:
        logger.warning("The following game IDs are missing:")
        # Log missing IDs in a sorted, more readable format
        for game_id in sorted(list(missing_game_ids)):
            logger.warning(f"  - {game_id}")
    else:
        logger.info("Congratulations! The box score dataset is complete.")
    logger.info("--------------------------------")

if __name__ == "__main__":
    validate_data_completeness()
