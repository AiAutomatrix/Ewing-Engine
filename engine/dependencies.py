import pandas as pd
from engine.adapters.player_adapter import PlayerAdapter
from engine.adapters.team_adapter import TeamAdapter
from engine.adapters.game_adapter import GameAdapter
from engine.adapters.boxscore_adapter import BoxScoreAdapter
from engine.simulation import Simulation

def get_simulation_instance():
    """Initializes and returns a singleton Simulation instance."""
    games_df = pd.read_parquet("data/processed/games.parquet")
    boxscores_df = pd.read_parquet("data/processed/boxscores.parquet")

    # Calculate season averages for team stats from games_df
    # Note: 'min' here is game duration, not player minutes. 'pts' is team points for the game.
    team_stats_cols = ['team_id', 'tricode', 'team_name', 'min', 'pts', 'fg_pct', 'fg3_pct', 'ft_pct', 
                       'oreb', 'dreb', 'reb', 'ast', 'stl', 'blk', 'tov', 'pf', 'plus_minus']
    
    # We need to average these statistics per team across all their games
    # For simplicity, let's assume 'off_rating', 'def_rating', 'pace', 'efg_pct', 'three_pt_rate', 'ft_rate' 
    # are either directly available or can be derived/placeholder for now.
    # For a real system, these would likely come from external sources or more complex calculation.
    # For now, we will use some stats from games_df and add placeholders for others.

    # Group by team_id to calculate season averages for the relevant stats
    # Also include tricode and team_name which are consistent per team_id
    team_season_stats = games_df.groupby('team_id').agg(
        tricode=('tricode', 'first'),
        team_name=('team_name', 'first'),
        pace=('min', 'mean'),  # Using mean minutes as a proxy for pace, might need refinement
        off_rating=('pts', 'mean'), # Using mean points as a proxy for off_rating
        def_rating=('pts', 'mean'), # Placeholder: In a real system, this would be opponent points allowed
        efg_pct=('fg_pct', 'mean'),
        three_pt_rate=('fg3_pct', 'mean'), # Using 3pt_pct as proxy for three_pt_rate
        ft_rate=('ft_pct', 'mean'),
        gp=('game_id', 'nunique'), # Games played
        w=('wl', lambda x: (x == 'W').sum()), # Wins
        l=('wl', lambda x: (x == 'L').sum()) # Losses
    ).reset_index()

    # Rename columns to match Team dataclass expectations where necessary
    team_season_stats.rename(columns={
        'tricode': 'abbreviation',
        'team_name': 'name',
    }, inplace=True)
    
    # Fill any potential NaN from mean calculations if a team has no games or missing data
    team_season_stats.fillna(0, inplace=True)

    teams = TeamAdapter(team_season_stats).to_engine_objects()
    
    # Create a mapping from tricode to team_id for easier lookup
    # Use the newly created team_season_stats for this mapping
    tricode_to_team_id = dict(zip(team_season_stats['abbreviation'], team_season_stats['team_id']))

    # Create Players from boxscores_df
    players_df = boxscores_df[['PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID']].drop_duplicates().copy()
    players_df.rename(columns={'PLAYER_ID': 'player_id', 'PLAYER_NAME': 'name', 'TEAM_ID': 'team_id'}, inplace=True)
    players = PlayerAdapter(players_df).to_engine_objects()

    # Preprocess games_df (which now has one row per game) to create games_for_adapter_df
    games_for_adapter_data = []
    
    for _, row in games_df.iterrows():
        game_id = row['game_id']
        game_date = row['game_date']
        matchup = row['matchup']
        current_team_tricode = row['tricode']
        
        home_team_id = None
        away_team_id = None

        if 'vs.' in matchup: # Current team is home
            home_tricode = current_team_tricode
            opponent_part = matchup.split(' vs. ')[1].strip()
            # Find away_tricode, assuming it's the opponent part.
            # If opponent_part is not a tricode in our map, fall back to finding the other tricode in the game_id group
            if opponent_part in tricode_to_team_id:
                away_tricode = opponent_part
            else:
                # Fallback: Find the tricode of the other team in this game_id group
                other_team_row = games_df[(games_df['game_id'] == game_id) & (games_df['tricode'] != home_tricode)]
                if not other_team_row.empty:
                    away_tricode = other_team_row['tricode'].iloc[0]
                else:
                    # If still not found, skip or log error
                    continue # Skip this game if opponent cannot be identified

            home_team_id = tricode_to_team_id.get(home_tricode)
            away_team_id = tricode_to_team_id.get(away_tricode)

        elif '@' in matchup: # Current team is away
            away_tricode = current_team_tricode
            opponent_part = matchup.split(' @ ')[1].strip()
            # Find home_tricode, assuming it's the opponent part
            if opponent_part in tricode_to_team_id:
                home_tricode = opponent_part
            else:
                # Fallback: Find the tricode of the other team in this game_id group
                other_team_row = games_df[(games_df['game_id'] == game_id) & (games_df['tricode'] != away_tricode)]
                if not other_team_row.empty:
                    home_tricode = other_team_row['tricode'].iloc[0]
                else:
                    # If still not found, skip or log error
                    continue # Skip this game if opponent cannot be identified

            home_team_id = tricode_to_team_id.get(home_tricode)
            away_team_id = tricode_to_team_id.get(away_tricode)
        
        if home_team_id is not None and away_team_id is not None:
            # We need to make sure we're getting game-specific stats, not team-specific
            # The games_df already has one row per game. We need to ensure the TeamAdapter doesn't conflate these.
            # However, the GameAdapter only needs game_id, date, home_team_id, away_team_id.
            # The original row contains these, so we use it.
            game_data = {
                'game_id': game_id,
                'game_date': game_date,
                'home_team_id': home_team_id,
                'away_team_id': away_team_id,
                'season_id': row['season_id'],
                'min': row['min'], 
                'pts': row['pts'], # This is the current team's points for this game
                'fg_pct': row['fg_pct'],
                'fg3_pct': row['fg3_pct'],
                'ft_pct': row['ft_pct'],
                'oreb': row['oreb'],
                'dreb': row['dreb'],
                'reb': row['reb'],
                'ast': row['ast'],
                'stl': row['stl'],
                'blk': row['blk'],
                'tov': row['tov'],
                'pf': row['pf'],
                'plus_minus': row['plus_minus'],
                'wl': row['wl'],
            }
            games_for_adapter_data.append(game_data)


    games_for_adapter_df = pd.DataFrame(games_for_adapter_data)
    
    games = GameAdapter(games_for_adapter_df).to_engine_objects()
    boxscores = BoxScoreAdapter(boxscores_df).to_engine_objects()

    # The Simulation object is now initialized with the populated team stats
    return Simulation(players, teams, games, boxscores)

# Do not run simulation_instance = get_simulation_instance() at the top level
# as this script is imported by tests and would cause re-initialization.