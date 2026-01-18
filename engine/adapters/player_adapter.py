from engine.models import Player

class PlayerAdapter:
    def __init__(self, df):
        self.df = df

    def to_engine_objects(self):
        players = []
        for _, row in self.df.iterrows():
            p = Player(
                id=row['player_id'],
                name=row['name'],
                team_id=row['team_id'],
                minutes=row.get('minutes', 0),
                points=row.get('pts', 0),
                rebounds=row.get('rebounds', 0),
                assists=row.get('assists', 0),
                steals=row.get('steals', 0),
                blocks=row.get('blocks', 0),
                fg_pct=row.get('fg_pct', 0)
            )
            players.append(p)
        return players