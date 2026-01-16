import pandas as pd
from engine.data_ingestion.data_ingestion_runner import player_clean, team_clean, game_clean, boxscore_clean
from engine.adapters.player_adapter import PlayerAdapter
from engine.adapters.team_adapter import TeamAdapter
from engine.adapters.game_adapter import GameAdapter
from engine.adapters.boxscore_adapter import BoxScoreAdapter
from engine.simulation import Simulation

def test_player_adapter():
    adapter = PlayerAdapter(player_clean[0])
    players = adapter.to_engine_objects()
    assert len(players) > 0
    assert hasattr(players[0], 'id')
    assert hasattr(players[0], 'points')

def test_simulation_runner():
    # Ensure engine can run on normalized ingested data
    all_players_data = player_clean[0]
    all_teams_data = team_clean[0]
    all_games_data = game_clean[0]
    all_boxscores_data = boxscore_clean[0]

    teams = TeamAdapter(all_teams_data).to_engine_objects()
    team_map = {t.abbreviation: t.id for t in teams}

    sim = Simulation(
        players=PlayerAdapter(all_players_data).to_engine_objects(),
        teams=teams,
        games=GameAdapter(all_games_data, team_map=team_map).to_engine_objects(),
        boxscores=BoxScoreAdapter(all_boxscores_data, team_map=team_map).to_engine_objects()
    )
    results = sim.run_historical_replay()
    assert results is not None
    assert 'win_probability_home' in results.columns
