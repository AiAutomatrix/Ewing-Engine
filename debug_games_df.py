import pandas as pd

def debug_games_data():
    """
    Loads games.parquet, prints the head of relevant columns, and then
    selects and prints rows for a specific game_id that appears more than once,
    to help understand the home/away team structure.
    """
    try:
        games_df = pd.read_parquet('data/processed/games.parquet')
    except FileNotFoundError:
        print("Error: 'data/processed/games.parquet' not found. Please ensure the file exists.")
        return

    print('--- Head of games_df (relevant columns) ---')
    print(games_df[['game_id', 'team_id', 'tricode', 'matchup', 'game_date']].head(10))
    print('\n' + '='*50 + '\n')

    # Find a game_id that appears more than once
    game_id_counts = games_df['game_id'].value_counts()
    complete_games = game_id_counts[game_id_counts == 2]

    if not complete_games.empty:
        sample_game_id = complete_games.index[0]
        print(f'--- Rows for a sample complete game_id ({sample_game_id}) ---')
        print(games_df[games_df['game_id'] == sample_game_id][['game_id', 'team_id', 'tricode', 'matchup', 'game_date']])
    else:
        print('No game_id found with exactly two entries (complete game).')
        # Fallback: if no game has exactly two entries, show any game_id with multiple entries
        incomplete_games = game_id_counts[game_id_counts > 1]
        if not incomplete_games.empty:
            sample_game_id = incomplete_games.index[0]
            print(f'--- Rows for a sample game_id with multiple entries ({sample_game_id}) ---')
            print(games_df[games_df['game_id'] == sample_game_id][['game_id', 'team_id', 'tricode', 'matchup', 'game_date']])

if __name__ == "__main__":
    debug_games_data()