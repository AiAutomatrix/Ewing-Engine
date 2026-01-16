
import pandas as pd
from engine.data_ingestion.boxscore_ingestor import BoxScoreIngestor

def test_boxscore_ingestor_renames_tricode():
    # Create a dummy DataFrame with the problematic column name
    df = pd.DataFrame([{'teamtricode': 'ATL', 'player': 'Player A'}])
    ingestor = BoxScoreIngestor([df])
    processed_dfs = ingestor.ingest()
    
    # Ensure the column is correctly renamed to 'tricode'
    assert 'tricode' in processed_dfs[0].columns
    assert 'teamtricode' not in processed_dfs[0].columns
