
import os
import pandas as pd
from nba_api.stats.endpoints import leaguedashteamstats
from engine.data_ingestion.team_stats_ingestor import TeamStatsIngestor

# --- Configuration ---
SEASON = "2023-24"
PROCESSED_DATA_PATH = "data/processed"

# --- Setup ---
os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

# --- Team Stats Ingestion ---
print("Starting team stats ingestion...")
team_stats_raw = leaguedashteamstats.LeagueDashTeamStats(
    season=SEASON,
    measure_type_detailed_all_star="Advanced"
).get_data_frames()[0]

team_stats_ingestor = TeamStatsIngestor([team_stats_raw])
team_clean = team_stats_ingestor.ingest()

if team_clean:
    team_df = team_clean[0]
    assert len(team_df) >= 30, "Expected at least 30 teams"
    # Save to a single, consolidated file
    team_df.to_parquet(f"{PROCESSED_DATA_PATH}/teams.parquet")
    print(f"Team stats successfully ingested and saved to {PROCESSED_DATA_PATH}/teams.parquet")
else:
    print("Warning: Team stats ingestion produced no data.")
