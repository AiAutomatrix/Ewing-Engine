# engine/data_ingestion/data_ingestion_runner.py
from engine.data_ingestion.boxscore_ingestor import BoxScoreIngestor
from engine.data_ingestion.player_stats_ingestor import PlayerStatsIngestor
from engine.data_ingestion.team_stats_ingestor import TeamStatsIngestor
from engine.data_ingestion.game_finder_ingestor import GameFinderIngestor
import pandas as pd

# Example: Load test data captured from Phase 4
from logs.phase4_data import (
    boxscore_dataframes_raw,
    player_stats_dataframes_raw,
    team_stats_dataframes_raw,
    game_finder_dataframes_raw
)

boxscore_dataframes = [pd.DataFrame(df) for df in boxscore_dataframes_raw]
player_stats_dataframes = [pd.DataFrame(df) for df in player_stats_dataframes_raw]
team_stats_dataframes = [pd.DataFrame(df) for df in team_stats_dataframes_raw]
game_finder_dataframes = [pd.DataFrame(df) for df in game_finder_dataframes_raw]

# Initialize ingestors
boxscore_ingestor = BoxScoreIngestor(boxscore_dataframes)
player_ingestor = PlayerStatsIngestor(player_stats_dataframes)
team_ingestor = TeamStatsIngestor(team_stats_dataframes)
game_ingestor = GameFinderIngestor(game_finder_dataframes)

# Run ingestion
boxscore_clean = boxscore_ingestor.ingest()
player_clean = player_ingestor.ingest()
team_clean = team_ingestor.ingest()
game_clean = game_ingestor.ingest()

print("Phase 5 ingestion complete. Data is normalized and ready for engine simulations.")
