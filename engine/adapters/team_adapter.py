from engine.models import Team

class TeamAdapter:
    def __init__(self, df):
        self.df = df

    def to_engine_objects(self):
        teams = []
        for _, row in self.df.iterrows():
            t = Team(
                id=row['team_id'],
                name=row.get('name', ''),
                abbreviation=row.get('abbreviation', ''),
                gp=row.get('gp', 0),
                w=row.get('w', 0),
                l=row.get('l', 0),
                pts=row.get('pts', 0),
                rebounds=row.get('reb', 0),
                assists=row.get('ast', 0),
                fg_pct=row.get('fg_pct', 0),
                turnovers=row.get('tov', 0),
                pace=row.get('pace', 0),
                off_rating=row.get('off_rating', 0),
                def_rating=row.get('def_rating', 0),
                efg_pct=row.get('efg_pct', 0),
                three_pt_rate=row.get('three_pt_rate', 0),
                ft_rate=row.get('ft_rate', 0),
            )
            teams.append(t)
        return teams