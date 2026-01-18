
import os
import pandas as pd
from engine.data_ingestion.game_finder_ingestor import GameFinderIngestor

# --- Configuration ---
SEASON = "2023-24"
PROCESSED_DATA_PATH = "data/processed"

# --- Setup ---
os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

# --- Game Finder Ingestion ---
print(f"Starting game finder ingestion for season: {SEASON}")
# Pass the season to the ingestor
game_finder_ingestor = GameFinderIngestor(season=SEASON)
game_clean = game_finder_ingestor.ingest()

if game_clean:
    game_df = game_clean[0]
    # Save to a single, consolidated file
    game_df.to_parquet(f"{PROCESSED_DATA_PATH}/games.parquet")
    print(f"Game finder data successfully ingested and saved to {PROCESSED_DATA_PATH}/games.parquet")
else:
    print("Warning: Game finder ingestion produced no data.")
