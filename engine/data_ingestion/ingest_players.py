
import os
import pandas as pd
from nba_api.stats.endpoints import leaguedashplayerstats
from engine.data_ingestion.player_stats_ingestor import PlayerStatsIngestor

# --- Configuration ---
SEASON = "2023-24"
PROCESSED_DATA_PATH = "data/processed"

# --- Setup ---
os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

# --- Player Stats Ingestion ---
print("Starting player stats ingestion...")
player_stats_raw = leaguedashplayerstats.LeagueDashPlayerStats(
    season=SEASON,
    measure_type_detailed_all_star="Advanced"
).get_data_frames()[0]

player_stats_ingestor = PlayerStatsIngestor([player_stats_raw])
player_clean = player_stats_ingestor.ingest()

if player_clean:
    player_df = player_clean[0]
    # Save to a single, consolidated file
    player_df.to_parquet(f"{PROCESSED_DATA_PATH}/players.parquet")
    print(f"Player stats successfully ingested and saved to {PROCESSED_DATA_PATH}/players.parquet")
else:
    print("Warning: Player stats ingestion produced no data.")
