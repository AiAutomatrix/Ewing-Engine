
import os
import pandas as pd
import logging
import time
from nba_api.stats.endpoints import BoxScoreTraditionalV3

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
PROCESSED_PATH = 'data/processed'
LOG_PATH = 'data/logs'
FAILED_LOG_FILE = os.path.join(LOG_PATH, "failed_boxscores.log")
BOXSCORES_FILE = os.path.join(PROCESSED_PATH, 'boxscores.parquet')
RETRIES = 3 # Keep retries for the repair script
DELAY = 5   # A more patient delay for the repair script

def fetch_and_append_boxscores(game_ids_to_fetch):
    """Fetches box scores for a list of game IDs and appends them to the main file."""
    if not game_ids_to_fetch:
        logging.info("No game IDs provided to fetch.")
        return

    logging.info(f"Starting repair fetch for {len(game_ids_to_fetch)} missing box scores.")
    newly_fetched_data = []

    for i, game_id in enumerate(sorted(list(game_ids_to_fetch))):
        logging.info(f"Attempting to fetch missing game {i + 1}/{len(game_ids_to_fetch)}: {game_id}")
        for attempt in range(RETRIES):
            try:
                box_score = BoxScoreTraditionalV3(game_id=game_id, timeout=60).get_data_frames()
                if box_score:
                    df = box_score[0]
                    df['game_id'] = game_id
                    newly_fetched_data.append(df)
                    logging.info(f"Successfully fetched box score for game {game_id}")
                    time.sleep(1) # Be respectful of the API
                    break  # Success
            except Exception as e:
                logging.warning(f"Error fetching game {game_id} on attempt {attempt + 1}: {e}")
                if attempt < RETRIES - 1:
                    logging.info(f"Retrying in {DELAY} seconds...")
                    time.sleep(DELAY)
                else:
                    logging.error(f"Failed to fetch game {game_id} after {RETRIES} attempts.")

    if newly_fetched_data:
        new_df = pd.concat(newly_fetched_data, ignore_index=True)
        if os.path.exists(BOXSCORES_FILE):
            existing_df = pd.read_parquet(BOXSCORES_FILE)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            # Drop duplicates in case a game was already present but logged as failed
            combined_df.drop_duplicates(subset=['game_id', 'player_id'], keep='last', inplace=True)
            combined_df.to_parquet(BOXSCORES_FILE)
            logging.info(f"Successfully appended {len(newly_fetched_data)} new box scores.")
        else:
            new_df.to_parquet(BOXSCORES_FILE)
            logging.info(f"Successfully created 'boxscores.parquet' with {len(newly_fetched_data)} box scores.")

if __name__ == "__main__":
    logging.info("--- Starting Data Reconciliation Process ---")
    if not os.path.exists(FAILED_LOG_FILE):
        logging.info("No failed log file found. Checking for missing games by comparing datasets.")
        # Fallback to the old method if the log file doesn't exist
        games_file = os.path.join(PROCESSED_PATH, 'games.parquet')
        if os.path.exists(games_file) and os.path.exists(BOXSCORES_FILE):
            expected_ids = set(pd.read_parquet(games_file)['game_id'].unique())
            downloaded_ids = set(pd.read_parquet(BOXSCORES_FILE)['game_id'].unique())
            missing_ids = expected_ids - downloaded_ids
            if missing_ids:
                logging.info(f"Found {len(missing_ids)} games missing via dataset comparison.")
                fetch_and_append_boxscores(missing_ids)
            else:
                logging.info("No missing games found via dataset comparison. Dataset is complete.")
        else:
            logging.info("No data files to compare. Exiting.")
    else:
        logging.info(f"Reading failed game IDs from {FAILED_LOG_FILE}")
        with open(FAILED_LOG_FILE, 'r') as f:
            failed_ids = {line.strip() for line in f if line.strip()}
        
        fetch_and_append_boxscores(failed_ids)
        # Optional: Clean up the log file after successful processing
        # os.remove(FAILED_LOG_FILE)

    logging.info("--- Data Reconciliation Process Complete ---")
