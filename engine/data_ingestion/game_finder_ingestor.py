# engine/data_ingestion/game_finder_ingestor.py
from engine.data_ingestion.base_ingestor import BaseIngestor
import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder

class GameFinderIngestor(BaseIngestor):
    def __init__(self, season='2023-24'):
        super().__init__(df_list=[], name="GameFinder")
        self.season = season

    def ingest(self):
        """
        Fetches all game logs for the specified season.
        """
        print(f"Fetching game logs for season: {self.season}")
        game_finder = leaguegamefinder.LeagueGameFinder(
            season_nullable=self.season,
            league_id_nullable='00',
            season_type_nullable='Regular Season'
        )
        games_df = game_finder.get_data_frames()[0]

        # Standardize column names to lowercase
        games_df.columns = [col.lower() for col in games_df.columns]

        # Rename tricode column for consistency
        if 'team_abbreviation' in games_df.columns:
            games_df.rename(columns={'team_abbreviation': 'tricode'}, inplace=True)

        return [games_df]
