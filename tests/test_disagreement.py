import unittest
from engine.disagreement import ModelDisagreement

class TestDisagreement(unittest.TestCase):

    def test_model_disagreement(self):
        """Test the model disagreement framework."""
        disagreement = ModelDisagreement()
        model_results = [
            {'win_probability': 0.6},
            {'win_probability': 0.65}
        ]
        comparison = disagreement.compare_models(model_results)
        self.assertIn('win_probability_variance', comparison)

if __name__ == '__main__':
    unittest.main()
