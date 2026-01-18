
import os
import pandas as pd
import logging
import time
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from engine.data_ingestion.game_finder_ingestor import GameFinderIngestor
from engine.data_ingestion.boxscore_ingestor import BoxScoreIngestor

PROCESSED_DATA_PATH = "data/processed"
SEASON = "2023-24"

GAMES_FILE = os.path.join(PROCESSED_DATA_PATH, 'games.parquet')
BOXSCORES_FILE = os.path.join(PROCESSED_DATA_PATH, 'boxscores.parquet')

# --- Hard limit for this specific test ---
INGESTION_LIMIT = 600

def get_missing_game_ids():
    """Checks for existing games and returns only the IDs that are missing."""
    if not os.path.exists(GAMES_FILE):
        logging.error("Games file not found. Cannot determine missing IDs.")
        return set()
    
    expected_ids = set(pd.read_parquet(GAMES_FILE)['game_id'].unique())
    
    if not os.path.exists(BOXSCORES_FILE):
        logging.info("No boxscores file found. All games are considered missing.")
        return expected_ids
        
    # Use a try-except block for robustness against empty/malformed files
    try:
        downloaded_ids = set(pd.read_parquet(BOXSCORES_FILE)['GAME_ID'].unique())
        missing_ids = expected_ids - downloaded_ids
        logging.info(f"Found {len(downloaded_ids)} existing boxscores. Resuming for {len(missing_ids)} missing games.")
    except Exception as e:
        logging.warning(f"Could not read existing boxscores file (error: {e}). Assuming all games are missing.")
        missing_ids = expected_ids
        
    return missing_ids

def append_to_parquet(df_list, path):
    """Appends a list of dataframes to a parquet file, creating it if it doesn't exist."""
    if not df_list:
        return
    
    new_data = pd.concat(df_list, ignore_index=True)
    
    if os.path.exists(path):
        existing_data = pd.read_parquet(path)
        combined = pd.concat([existing_data, new_data], ignore_index=True)
        # Using uppercase to match the API's DataFrame columns
        combined.drop_duplicates(subset=['GAME_ID', 'PLAYER_ID'], keep='last', inplace=True)
        combined.to_parquet(path)
    else:
        new_data.to_parquet(path)
        
    logging.info(f"Saved {len(new_data)} new records to {path}.")

if __name__ == "__main__":
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    logging.info("--- STARTING RUN --- ")

    # Step 1: Ensure games list is available
    if not os.path.exists(GAMES_FILE):
        logging.info(f"Game list not found. Fetching for season {SEASON}.")
        game_finder = GameFinderIngestor(season=SEASON).ingest()[0]
        game_finder.drop_duplicates(subset=['game_id'], keep='first').to_parquet(GAMES_FILE)
        logging.info(f"Saved {len(game_finder)} total games to {GAMES_FILE}")

    # Step 2: Determine what work needs to be done
    missing_ids = list(get_missing_game_ids())
    if not missing_ids:
        logging.info("No missing box scores found. Nothing to do. Pipeline finished.")
    else:
        boxscore_ingestor = BoxScoreIngestor()
        total_ingested_this_run = 0
        
        # Use simple, reliable parameters
        params = {'api_version': 'v2', 'chunk_size': 25, 'timeout': 20, 'delay': 1}
        chunks = [missing_ids[i:i + params['chunk_size']] for i in range(0, len(missing_ids), params['chunk_size'])]

        logging.info(f"Starting ingestion for {len(missing_ids)} games, with a hard limit of ~{INGESTION_LIMIT} games for this run.")

        # Step 3: Process chunks until the limit is reached
        for i, chunk in enumerate(chunks):
            logging.info(f"Processing chunk {i+1}/{len(chunks)}...")
            successes, failures = boxscore_ingestor.ingest(
                chunk,
                params['api_version'],
                params['timeout'],
                params['delay']
            )
            
            if successes:
                append_to_parquet(successes, BOXSCORES_FILE)
                total_ingested_this_run += len(successes)
            
            if total_ingested_this_run >= INGESTION_LIMIT:
                logging.info(f"Reached ingestion limit ({total_ingested_this_run}/{INGESTION_LIMIT}). Halting run as requested.")
                break

    logging.info("--- RUN CONCLUDED --- ")
