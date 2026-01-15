import unittest
from engine.assumptions import AssumptionRegistry

class TestAssumptions(unittest.TestCase):

    def test_assumption_registry_defaults(self):
        """Test that the assumption registry has the correct default values."""
        assumptions = AssumptionRegistry()
        self.assertEqual(assumptions.possession_length_distribution.value, 10.0)
        self.assertEqual(assumptions.turnover_rate.value, 0.1)
        self.assertEqual(assumptions.shot_type_mix.value, 0.5)
        self.assertEqual(assumptions.free_throw_rate.value, 0.2)
        self.assertEqual(assumptions.offensive_rebound_rate.value, 0.2)
        self.assertEqual(assumptions.pace_modifier.value, 1.0)
        self.assertEqual(assumptions.home_court_advantage.value, 3.5)

if __name__ == '__main__':
    unittest.main()
