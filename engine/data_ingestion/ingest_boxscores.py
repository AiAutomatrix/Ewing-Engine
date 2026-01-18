
import os
import pandas as pd
from engine.data_ingestion.boxscore_ingestor import BoxScoreIngestor

# --- Configuration ---
PROCESSED_DATA_PATH = "data/processed"

# --- Setup ---
os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

# --- Box Score Ingestion ---
print("Starting box score ingestion...")
games_df = pd.read_parquet(f"{PROCESSED_DATA_PATH}/games.parquet")
game_ids = games_df['game_id'].unique()

boxscore_ingestor = BoxScoreIngestor()
boxscore_clean = boxscore_ingestor.ingest(game_ids=game_ids)

if boxscore_clean:
    boxscore_df = boxscore_clean[0]
    # Save to a single, consolidated file
    boxscore_df.to_parquet(f"{PROCESSED_DATA_PATH}/boxscores.parquet")
    print(f"Box score data for {len(game_ids)} games successfully ingested and saved to {PROCESSED_DATA_PATH}/boxscores.parquet")
else:
    print("Warning: Box score ingestion produced no data.")
