# engine/data_ingestion/base_ingestor.py
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

class BaseIngestor:
    def __init__(self, df_list, name="Base"):
        self.df_list = df_list
        self.name = name
        self.cleaned_dfs = []

    def normalize_columns(self, df):
        df.columns = [c.lower() for c in df.columns]
        return df

    def ingest(self):
        logging.info(f"Ingesting {len(self.df_list)} DataFrames for {self.name}")
        for df in self.df_list:
            clean_df = self.normalize_columns(df)
            self.cleaned_dfs.append(clean_df)
        logging.info(f"Ingestion complete for {self.name}")
        return self.cleaned_dfs
