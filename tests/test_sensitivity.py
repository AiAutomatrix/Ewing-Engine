import unittest
from engine.sensitivity import SensitivityAnalysis

class TestSensitivity(unittest.TestCase):

    def test_sensitivity_analysis(self):
        """Test the sensitivity analysis engine."""
        sensitivity = SensitivityAnalysis()
        results = sensitivity.run_one_at_a_time('turnover_rate', [-0.1, 0.1])
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].assumption_name, 'turnover_rate')
        self.assertNotEqual(results[0].win_probability_delta, 0.0)

if __name__ == '__main__':
    unittest.main()
