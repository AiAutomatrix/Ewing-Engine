import pandas as pd
from engine.data_ingestion.data_ingestion_runner import team_clean, game_clean
from engine.adapters.team_adapter import TeamAdapter
from engine.adapters.game_adapter import GameAdapter

def test_team_ids_align_between_games_and_teams():
    all_teams_data = pd.concat(team_clean)
    all_games_data = pd.concat(game_clean)

    teams = TeamAdapter(all_teams_data).to_engine_objects()
    team_map = {t.abbreviation: t.id for t in teams}
    games = GameAdapter(all_games_data, team_map=team_map).to_engine_objects()

    team_ids = {t.id for t in teams}

    for g in games:
        assert g.home_team in team_ids
        assert g.away_team in team_ids
