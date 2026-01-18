import pandas as pd

def inspect_parquet_files():
    """
    Loads 'games.parquet' and 'boxscores.parquet', prints their schema,
    row count, and the first 5 rows.
    """
    
    # Inspect games.parquet
    print('--- Inspecting data/processed/games.parquet ---')
    try:
        games_df = pd.read_parquet('data/processed/games.parquet')
        print('\nSchema (games_df):')
        games_df.info()
        print(f'\nRow Count (games_df): {len(games_df)}')
        print('\nHead (games_df):')
        print(games_df.head())
    except FileNotFoundError:
        print("Error: 'data/processed/games.parquet' not found.")
    except Exception as e:
        print(f"Error processing 'games.parquet': {e}")

    print('\n' + '='*50 + '\n')

    # Inspect boxscores.parquet
    print('--- Inspecting data/processed/boxscores.parquet ---')
    try:
        boxscores_df = pd.read_parquet('data/processed/boxscores.parquet')
        print('\nSchema (boxscores_df):')
        boxscores_df.info()
        print(f'\nRow Count (boxscores_df): {len(boxscores_df)}')
        print('\nHead (boxscores_df):')
        print(boxscores_df.head())
    except FileNotFoundError:
        print("Error: 'data/processed/boxscores.parquet' not found.")
    except Exception as e:
        print(f"Error processing 'boxscores.parquet': {e}")

if __name__ == "__main__":
    inspect_parquet_files()