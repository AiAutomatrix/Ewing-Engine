
import pandas as pd
import glob

game_files = glob.glob("data/processed/game_finder_*.parquet")
all_games_data = pd.concat([pd.read_parquet(f) for f in game_files])

print("Unique tricodes found in game_finder data:")
print(all_games_data['tricode'].unique())
