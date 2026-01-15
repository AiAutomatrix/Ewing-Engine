import unittest
from engine.historical import HistoricalGame

class TestHistorical(unittest.TestCase):

    def test_historical_replay(self):
        """Test replaying a historical game."""
        game = HistoricalGame(
            team_a="GSW",
            team_b="LAL",
            date="2023-01-01",
            actual_score={"home": 100, "away": 95}
        )
        replay_results = game.replay()
        self.assertIn('actual_outcome_percentile', replay_results)

if __name__ == '__main__':
    unittest.main()
