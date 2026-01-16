# engine/data_ingestion/boxscore_ingestor.py
from engine.data_ingestion.base_ingestor import BaseIngestor
import pandas as pd

class BoxScoreIngestor(BaseIngestor):
    def __init__(self, df_list):
        super().__init__(df_list, name="BoxScore")

    def ingest(self):
        if not self.df_list:
            return []

        # Concatenate all dataframes
        combined_df = pd.concat(self.df_list, ignore_index=True)

        # Standardize column names to lowercase
        combined_df.columns = [col.lower() for col in combined_df.columns]

        # Rename tricode column for consistency
        if 'teamtricode' in combined_df.columns:
            combined_df.rename(columns={'teamtricode': 'tricode'}, inplace=True)

        return [combined_df]
