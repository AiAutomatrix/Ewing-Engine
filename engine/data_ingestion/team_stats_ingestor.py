# engine/data_ingestion/team_stats_ingestor.py
import pandas as pd
from engine.data_ingestion.base_ingestor import BaseIngestor

class TeamStatsIngestor(BaseIngestor):
    def __init__(self, df_list):
        super().__init__(df_list, name="TeamStats")

    def ingest(self):
        """
        Combines and standardizes team statistics from multiple dataframes.
        This creates a canonical source of truth for team data.
        """
        if not self.df_list:
            return []

        # Concatenate all dataframes
        combined_df = pd.concat(self.df_list, ignore_index=True)

        # Standardize column names to lowercase for easier mapping
        combined_df.columns = [col.lower() for col in combined_df.columns]

        # Define all possible original column names and their standardized name
        rename_map = {
            'team_id': 'team_id',
            'team_name': 'name',
            'tricode': 'abbreviation',
            'team_abbreviation': 'abbreviation',
            'gp': 'gp',
            'w': 'w',
            'l': 'l',
            'pts': 'pts',
            'reb': 'reb',
            'ast': 'ast',
            'fg_pct': 'fg_pct',
            'tov': 'tov',
            'turnovers': 'tov',
            'pace': 'pace',
            'e_pace': 'pace',
            'offrtg': 'offrating',
            'off_rating': 'offrating',
            'e_off_rating': 'offrating',
            'defrtg': 'defrating',
            'def_rating': 'defrating',
            'e_def_rating': 'defrating',
            'efg_pct': 'efg_pct',
            'ar': 'ar',
            'ftr': 'ftr'
        }

        # Rename columns based on the map
        combined_df.rename(columns=rename_map, inplace=True)
        
        # Ensure only columns relevant to the adapter are kept, to avoid downstream conflicts
        expected_cols = [
            'team_id', 'name', 'abbreviation', 'gp', 'w', 'l', 'pts', 'reb', 'ast', 
            'fg_pct', 'tov', 'pace', 'offrating', 'defrating', 'efg_pct', 'ar', 'ftr'
        ]
        
        # Filter for existing columns to avoid KeyErrors
        existing_expected_cols = [col for col in expected_cols if col in combined_df.columns]
        
        # Drop duplicates based on team_id, keeping the first entry
        if 'team_id' in combined_df.columns:
            # Create a dataframe with only the expected columns before dropping duplicates
            result_df = combined_df[existing_expected_cols].copy()
            result_df.drop_duplicates(subset=['team_id'], keep='first', inplace=True)
            return [result_df]
        else:
            # If no team_id, we can't create a canonical source, something is wrong.
            return []
