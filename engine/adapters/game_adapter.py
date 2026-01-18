import pandas as pd
from engine.models import Game

class GameAdapter:
    def __init__(self, df):
        self.df = df

    def to_engine_objects(self):
        games = []
        for _, row in self.df.iterrows():
            g = Game(
                id=row['game_id'],
                date=row.get('game_date', ''),
                home_team=int(row['home_team_id']),
                away_team=int(row['away_team_id']),
                scores='', # Placeholder
                plus_minus=0 # Placeholder
            )
            games.append(g)
        return games