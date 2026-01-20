# engine/dependencies.py

import pandas as pd
from engine.adapters.player_adapter import PlayerAdapter
from engine.adapters.team_adapter import TeamAdapter
from engine.adapters.game_adapter import GameAdapter
from engine.adapters.boxscore_adapter import BoxScoreAdapter
from engine.simulation import Simulation

_simulation_instance = None

def get_simulation_instance(force_reload=False):
    """Initializes and returns a singleton Simulation instance."""
    global _simulation_instance
    if _simulation_instance is None or force_reload:
        games_df = pd.read_parquet("data/processed/games.parquet")
        boxscores_df = pd.read_parquet("data/processed/boxscores.parquet")

        team_season_stats = games_df.groupby('team_id').agg(
            tricode=('tricode', 'first'),
            team_name=('team_name', 'first'),
            pace=('min', 'mean'),
            off_rating=('pts', 'mean'),
            def_rating=('pts', 'mean'),
            efg_pct=('fg_pct', 'mean'),
            three_pt_rate=('fg3_pct', 'mean'),
            ft_rate=('ft_pct', 'mean'),
            gp=('game_id', 'nunique'),
            w=('wl', lambda x: (x == 'W').sum()),
            l=('wl', lambda x: (x == 'L').sum())
        ).reset_index()

        team_season_stats.rename(columns={
            'tricode': 'abbreviation',
            'team_name': 'name',
        }, inplace=True)
        
        team_season_stats.fillna(0, inplace=True)

        teams = TeamAdapter(team_season_stats).to_engine_objects()
        
        tricode_to_team_id = dict(zip(team_season_stats['abbreviation'], team_season_stats['team_id']))

        players_df = boxscores_df[['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID']].drop_duplicates().copy()
        players_df.rename(columns={'PLAYER_ID': 'player_id', 'PLAYER_NAME': 'name', 'TEAM_ID': 'team_id'}, inplace=True)
        players = PlayerAdapter(players_df).to_engine_objects()

        # Reverted to the original, correct game processing logic.
        # This logic correctly identifies home/away teams and passes the
        # de-duplicated data to the adapter.
        distinct_games = games_df.drop_duplicates(subset=['game_id']).copy()
        games_for_adapter_data = []
        for _, row in distinct_games.iterrows():
            game_id = row['game_id']
            matchup = row['matchup']
            current_team_tricode = row['tricode']

            if 'vs.' in matchup:
                home_tricode = current_team_tricode
                away_tricode = matchup.split(' vs. ')[-1]
            elif '@' in matchup:
                away_tricode = current_team_tricode
                home_tricode = matchup.split(' @ ')[-1]
            else:
                continue

            home_team_id = tricode_to_team_id.get(home_tricode)
            away_team_id = tricode_to_team_id.get(away_tricode)

            if home_team_id and away_team_id:
                games_for_adapter_data.append({
                    'game_id': game_id,
                    'game_date': row['game_date'],
                    'home_team_id': home_team_id,
                    'away_team_id': away_team_id,
                    'season_id': row['season_id'],
                })

        games_for_adapter_df = pd.DataFrame(games_for_adapter_data)
        games = GameAdapter(games_for_adapter_df).to_engine_objects()
        boxscores = BoxScoreAdapter(boxscores_df).to_engine_objects()

        simulation = Simulation(players, teams, games, boxscores)

        if not force_reload:
            _simulation_instance = simulation
        
        return simulation

    return _simulation_instance