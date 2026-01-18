# scripts/select_calibration_games.py

import pandas as pd
import os

PROCESSED_DATA_PATH = "data/processed"
GAMES_FILE = os.path.join(PROCESSED_DATA_PATH, 'games.parquet')
CALIBRATION_IDS_FILE = os.path.join("data", 'calibration_game_ids.csv')

if __name__ == "__main__":
    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
    games_df = pd.read_parquet(GAMES_FILE)
    
    # Filter for regular season games and sort by date
    regular_season_games = games_df[games_df['series_description'] == 'Regular Season'].sort_values(by='game_date')
    
    # Select the first 200 games
    calibration_games = regular_season_games.head(200)
    
    # Save the game IDs to a CSV file
    calibration_games[['game_id']].to_csv(CALIBRATION_IDS_FILE, index=False)
    
    print(f"Selected {len(calibration_games)} games for calibration and saved their IDs to {CALIBRATION_IDS_FILE}")
