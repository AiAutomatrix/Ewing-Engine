from engine.models import BoxScore

class BoxScoreAdapter:
    def __init__(self, df, team_map=None):
        self.df = df.copy()
        # Replace NaN with appropriate defaults
        self.df.fillna({
            'MIN': "",
            'PTS': 0,
            'REB': 0,
            'AST': 0,
            'FG_PCT': 0.0,
            'PLUS_MINUS': 0,
            'PLAYER_ID': 0,
        }, inplace=True)

    def to_engine_objects(self):
        box_scores = []
        for _, row in self.df.iterrows():
            bs = BoxScore(
                game_id=row['GAME_ID'],
                team_id=int(row['TEAM_ID']),
                player_id=int(row['PLAYER_ID']),
                minutes=str(row['MIN']),
                pts=int(row['PTS']),
                rebounds=int(row['REB']),
                assists=int(row['AST']),
                fg_pct=float(row['FG_PCT']),
                plus_minus=int(row['PLUS_MINUS'])
            )
            box_scores.append(bs)
        return box_scores
