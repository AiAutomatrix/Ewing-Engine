# engine/data_ingestion/player_stats_ingestor.py
from engine.data_ingestion.base_ingestor import BaseIngestor
import pandas as pd

class PlayerStatsIngestor(BaseIngestor):
    def __init__(self, df_list):
        super().__init__(df_list, name="PlayerStats")

    def ingest(self):
        if not self.df_list:
            return []

        # Concatenate all dataframes
        combined_df = pd.concat(self.df_list, ignore_index=True)

        # Standardize column names to lowercase
        combined_df.columns = [col.lower() for col in combined_df.columns]

        # Rename columns for consistency
        if 'team_abbreviation' in combined_df.columns:
            combined_df.rename(columns={'team_abbreviation': 'tricode'}, inplace=True)
        if 'person_id' in combined_df.columns:
            combined_df.rename(columns={'person_id': 'player_id'}, inplace=True)

        return [combined_df]
