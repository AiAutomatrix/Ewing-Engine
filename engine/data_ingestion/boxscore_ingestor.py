
import time
import logging
import random
from nba_api.stats.endpoints import boxscoretraditionalv2, boxscoretraditionalv3
from engine.data_ingestion.base_ingestor import BaseIngestor

class BoxScoreIngestor(BaseIngestor):
    def __init__(self):
        super().__init__(df_list=None, name="BoxScore")

    def ingest(self, game_ids, api_version, timeout, delay):
        """
        Executes a single, flexible ingestion pass on a chunk of game_ids.
        The behavior of this function is controlled entirely by its parameters.
        """
        total_games_in_chunk = len(game_ids)
        logging.info(f"Executing pass for {total_games_in_chunk} games using API_VERSION='{api_version}', TIMEOUT={timeout}s, DELAY={delay}")
        
        successful_box_scores = []
        failed_game_ids = []
        
        endpoint_class = boxscoretraditionalv2.BoxScoreTraditionalV2 if api_version == 'v2' else boxscoretraditionalv3.BoxScoreTraditionalV3

        for i, game_id in enumerate(game_ids):
            try:
                if i > 0 and i % 5 == 0:
                    logging.info(f"  -> Chunk progress: {i}/{total_games_in_chunk}...")
                
                api_call = endpoint_class(game_id=game_id, timeout=timeout)
                boxscore_df = api_call.get_data_frames()[0]

                # CORRECTED: Use uppercase column name to match API standard
                boxscore_df['GAME_ID'] = game_id

                successful_box_scores.append(boxscore_df)

            except Exception as e:
                logging.warning(f"  -> Request failed for game {game_id} (API: {api_version}, Timeout: {timeout}s): {e}")
                failed_game_ids.append(game_id)
            
            time.sleep(delay() if callable(delay) else delay)

        return successful_box_scores, failed_game_ids
