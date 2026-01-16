from engine.models import Game

class GameAdapter:
    def __init__(self, df, team_map=None):
        self.df = df
        self.team_map = team_map if team_map is not None else {}

    def to_engine_objects(self):
        games = []
        for _, row in self.df.drop_duplicates(subset=['game_id']).iterrows():
            home_team_abbr, away_team_abbr = self._parse_matchup(row.get('matchup', ''))

            if not home_team_abbr or not away_team_abbr:
                continue

            home_team_id = self.team_map.get(home_team_abbr)
            away_team_id = self.team_map.get(away_team_abbr)

            if not home_team_id or not away_team_id:
                continue

            g = Game(
                id=row['game_id'],
                date=row.get('game_date', ''),
                home_team=home_team_id,
                away_team=away_team_id,
                scores=row.get('matchup', ''), # Placeholder, actual scores are in boxscore
                plus_minus=row.get('plus_minus', 0)
            )
            games.append(g)
        return games

    def _parse_matchup(self, matchup_str):
        parts = matchup_str.replace(' vs. ', '@').split('@')
        if len(parts) != 2:
            return None, None
        
        team_abbr_1 = parts[0].strip()
        team_abbr_2 = parts[1].strip()
        
        if ' vs. ' in matchup_str:
            return team_abbr_1, team_abbr_2
        else:
            return team_abbr_2, team_abbr_1
