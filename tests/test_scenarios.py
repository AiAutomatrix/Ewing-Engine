import unittest
from engine.scenarios import Scenario

class TestScenarios(unittest.TestCase):

    def test_scenario_run(self):
        """Test running a scenario."""
        scenario = Scenario(
            name="High Pace",
            overrides={"pace_modifier": 1.2}
        )
        results = scenario.run()
        self.assertIsNotNone(results.win_probability)

if __name__ == '__main__':
    unittest.main()
