import pandas as pd
from engine.data_ingestion.data_ingestion_runner import player_clean, team_clean, game_clean, boxscore_clean
from engine.adapters.player_adapter import PlayerAdapter
from engine.adapters.team_adapter import TeamAdapter
from engine.adapters.game_adapter import GameAdapter
from engine.adapters.boxscore_adapter import BoxScoreAdapter
from engine.simulation import Simulation

def test_replay_output_structure():
    # Combine all ingested data
    all_players_data = player_clean[0]
    all_teams_data = team_clean[0]
    all_games_data = game_clean[0]
    all_boxscores_data = boxscore_clean[0]

    # Create engine objects from the combined data
    players = PlayerAdapter(all_players_data).to_engine_objects()
    teams = TeamAdapter(all_teams_data).to_engine_objects()
    team_map = {t.abbreviation: t.id for t in teams}
    games = GameAdapter(all_games_data, team_map=team_map).to_engine_objects()
    boxscores = BoxScoreAdapter(all_boxscores_data, team_map=team_map).to_engine_objects()

    sim = Simulation(players, teams, games, boxscores)
    results = sim.run_historical_replay()
    
    assert 'game_id' in results.columns
    assert 'win_probability_home' in results.columns
    assert len(results) > 0
