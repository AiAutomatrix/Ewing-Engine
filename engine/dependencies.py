# engine/dependencies.py

import pandas as pd
from engine.data_ingestion.data_ingestion_runner import (player_clean, team_clean, game_clean, boxscore_clean)
from engine.adapters.player_adapter import PlayerAdapter
from engine.adapters.team_adapter import TeamAdapter
from engine.adapters.game_adapter import GameAdapter
from engine.adapters.boxscore_adapter import BoxScoreAdapter
from engine.simulation import Simulation

def get_simulation_instance():
    """Initializes and returns a singleton Simulation instance."""
    all_players_data = player_clean[0]
    all_teams_data = team_clean[0]
    all_games_data = game_clean[0]
    all_boxscores_data = boxscore_clean[0]

    # Create a lookup for team abbreviations from the game data
    team_abbreviations = all_games_data[["team_id", "tricode"]].rename(
        columns={"tricode": "abbreviation"}
    ).drop_duplicates()

    # Use an inner merge to ensure only teams with abbreviations are included
    all_teams_data = pd.merge(
        all_teams_data,
        team_abbreviations,
        on="team_id",
        how="inner"  # Use 'inner' to filter out teams without game data
    )

    # Create engine objects from the combined data
    players = PlayerAdapter(all_players_data).to_engine_objects()
    teams = TeamAdapter(all_teams_data).to_engine_objects()
    
    # Create a map from team abbreviation to team ID for the adapters
    team_map_abbr_to_id = {t.abbreviation: t.id for t in teams}

    games = GameAdapter(all_games_data, team_map=team_map_abbr_to_id).to_engine_objects()
    boxscores = BoxScoreAdapter(all_boxscores_data, team_map=team_map_abbr_to_id).to_engine_objects()

    return Simulation(players, teams, games, boxscores)

simulation_instance = get_simulation_instance()
