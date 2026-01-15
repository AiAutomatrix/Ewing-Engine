import unittest
from engine.calibration import calculate_calibration_metrics

class TestCalibration(unittest.TestCase):

    def test_calculate_calibration_metrics(self):
        """Test the calibration metrics calculation."""
        # Create some dummy historical replay data
        historical_replays = [
            {
                'simulation_results': {
                    'margin_distribution': list(range(-20, 20)),
                    'home_score_distribution': [100],
                    'away_score_distribution': [100]
                },
                'actual_margin': 5,
                'actual_score': {'home': 105, 'away': 100}
            }
        ]
        metrics = calculate_calibration_metrics(historical_replays)
        self.assertIsInstance(metrics.confidence_interval_coverage, float)

if __name__ == '__main__':
    unittest.main()
