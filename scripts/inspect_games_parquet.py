# scripts/inspect_games_parquet.py

import pandas as pd
import os

PROCESSED_DATA_PATH = "data/processed"
GAMES_FILE = os.path.join(PROCESSED_DATA_PATH, 'games.parquet')

if __name__ == "__main__":
    games_df = pd.read_parquet(GAMES_FILE)
    print(games_df.columns)
