import pytest
from engine.data_ingestion.boxscore_ingestor import BoxScoreIngestor
from engine.data_ingestion.player_stats_ingestor import PlayerStatsIngestor
from engine.data_ingestion.team_stats_ingestor import TeamStatsIngestor
from engine.data_ingestion.game_finder_ingestor import GameFinderIngestor
import pandas as pd
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

def test_boxscore_ingestion():
    ingestor = BoxScoreIngestor(boxscore_dataframes)
    dfs = ingestor.ingest()
    assert len(dfs) > 0
    for df in dfs:
        assert 'gameid' in df.columns
        assert 'personid' in df.columns or 'teamid' in df.columns

def test_player_stats_ingestion():
    ingestor = PlayerStatsIngestor(player_stats_dataframes)
    dfs = ingestor.ingest()
    assert len(dfs) > 0
    for df in dfs:
        assert 'player_id' in df.columns

def test_team_stats_ingestion():
    ingestor = TeamStatsIngestor(team_stats_dataframes)
    dfs = ingestor.ingest()
    assert len(dfs) > 0
    for df in dfs:
        assert 'team_id' in df.columns

def test_game_finder_ingestion():
    ingestor = GameFinderIngestor(game_finder_dataframes)
    dfs = ingestor.ingest()
    assert len(dfs) > 0
    for df in dfs:
        assert 'game_id' in df.columns
