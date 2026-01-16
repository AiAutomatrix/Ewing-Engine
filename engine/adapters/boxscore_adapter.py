from engine.models import BoxScore

class BoxScoreAdapter:
    def __init__(self, df, team_map=None):
        self.df = df
        self.team_map = team_map if team_map is not None else {}

    def to_engine_objects(self):
        box_scores = []
        for _, row in self.df.iterrows():
            team_id = self.team_map.get(row['tricode'])
            if not team_id:
                continue
            print(f"Creating BoxScore for game_id: {row['gameid']}")
            bs = BoxScore(
                game_id=row['gameid'],
                team_id=team_id,
                player_id=row.get('personid', 0),
                minutes=row.get('min', ''),
                pts=row.get('points', 0),
                rebounds=row.get('reb', 0),
                assists=row.get('assists', 0),
                fg_pct=row.get('fg_pct', 0),
                plus_minus=row.get('plusminuspoints', 0)
            )
            box_scores.append(bs)
        return box_scores
