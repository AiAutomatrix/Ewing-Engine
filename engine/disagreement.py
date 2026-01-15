from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ModelDisagreement:
    """Framework for exposing structural uncertainty via competing models."""

    def compare_models(self, model_results: List[Dict]) -> Dict:
        """Compare the outputs of multiple models."""
        if not model_results or len(model_results) < 2:
            return {}

        # Example disagreement metric: Variance of win probabilities
        win_probabilities = [result['win_probability'] for result in model_results]
        win_probability_variance = self.variance(win_probabilities)

        return {
            "win_probability_variance": win_probability_variance
        }

    def variance(self, data: List[float]) -> float:
        """Calculate the variance of a list of numbers."""
        n = len(data)
        if n < 2:
            return 0.0
        mean = sum(data) / n
        return sum((x - mean) ** 2 for x in data) / n
