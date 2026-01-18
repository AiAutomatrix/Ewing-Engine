# engine/data_ingestion/player_stats_ingestor.py
from engine.data_ingestion.base_ingestor import BaseIngestor
import pandas as pd

class PlayerStatsIngestor(BaseIngestor):
    def __init__(self, df_list):
        super().__init__(df_list, name="PlayerStats")

    def ingest(self):
        if not self.df_list:
            return []

        processed_dfs = []
        for df in self.df_list:
            # Standardize column names to lowercase
            df.columns = [col.lower() for col in df.columns]

            # Rename columns for consistency
            if 'team_abbreviation' in df.columns:
                df.rename(columns={'team_abbreviation': 'tricode'}, inplace=True)
            if 'person_id' in df.columns:
                df.rename(columns={'person_id': 'player_id'}, inplace=True)
            
            processed_dfs.append(df)

        return processed_dfs
